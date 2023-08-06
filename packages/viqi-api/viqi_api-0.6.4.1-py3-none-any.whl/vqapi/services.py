# pylint: disable=wrong-import-order,wrong-import-position
# import functools
import hashlib
import io
import json
import logging
import os
import pickle
import posixpath
import random
import shutil
import string
import tarfile
import tempfile
import time
import urllib.parse

# from pickle import dumps, loads
from typing import BinaryIO, Callable, Dict, Optional
from urllib.parse import parse_qsl, urlparse

import boto3
import botocore
import requests
import tenacity
import tifffile
from bq.metadoc.formats import Metadoc
from requests_toolbelt import MultipartEncoder

from vqapi.exception import http_code_future_not_ready

from .exception import BQApiError, FutureNotFoundError, code_to_exception
from .util import is_uniq_code, normalize_unicode

# from botocore.credentials import RefreshableCredentials
# from botocore.session import get_session


log = logging.getLogger("vqapi.services")

try:
    import tables
except ImportError:
    log.warning("pytables services not available")

try:
    import pandas as pd
except ImportError:
    log.warning("pandas services not available")

try:
    import numpy as np
except ImportError:
    log.warning("numpy services not available")

# DEFAULT_TIMEOUT=None
DEFAULT_TIMEOUT = 60 * 60  # 1 hour


################### Helpers ######################


def _prepare_mountpath(path: str) -> str:
    if path.startswith("store:"):
        path = path[len("store:") :]
    return path.strip("/")


def _prepare_uniq(id: str) -> str:
    if not is_uniq_code(id):
        raise BQApiError(f'"{id}" is not a valid resource id')
    return id


def _prepare_uniq_or_alias_or_path(id: str) -> str:
    if id.startswith("store:"):
        id = id[len("store:") :]
    return id.strip("/")


class ResponseFile(io.IOBase):
    """
    IO byte stream to return single file responses. Can be used as context manager.
    """

    def __init__(self, response):
        if isinstance(response, str):
            # file path
            self.stream = open(response, "rb")
            self.fpath = response
        else:
            response.raw.decode_content = True  # in case of compression
            self.stream = response.raw
            self.fpath = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.close()

    def read(self, size=-1):
        return self.stream.read(size)

    def readall(self):
        return self.stream.read()

    def readinto(self, b):
        raise io.UnsupportedOperation("no readinto in reponse stream")

    def close(self):
        self.stream.close()

    def write(self, b):
        raise io.UnsupportedOperation("no write in reponse stream")

    def copy_into(self, localpath):
        "copy this file into localpath/ and return its path"
        if self.fpath is not None:
            outname = os.path.join(localpath, os.path.basename(self.fpath))
            shutil.copyfile(self.fpath, outname)
        else:
            outname = os.path.join(localpath, "responsefile")
            with open(outname, "wb") as fout:
                shutil.copyfileobj(self.stream, fout)
        return outname

    def force_to_filepath(self):
        "force this file into a locally accessible file and return its path"
        if self.fpath is not None:
            return self.fpath
        else:
            with tempfile.NamedTemporaryFile(mode="w+b", prefix="viqicomm", delete=False) as fout:  # who deletes this?
                shutil.copyfileobj(self.stream, fout)
                return fout.name


class ResponseFolder:
    """
    Class to return folder structure. Can be used as context manager.
    """

    def __init__(self, response):
        if isinstance(response, str):
            # folder path
            self.stream = response
        else:
            # http response => interpret as tarfile
            # self.stream = tarfile.open(fileobj=response.raw, mode='r|')  # this does not work because tarfile needs seeks
            self.stream = tarfile.open(
                fileobj=io.BytesIO(response.content), mode="r|"
            )  # TODO: may lead to out of memory

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not isinstance(self.stream, str):
            self.stream.close()

    def copy_into(self, localpath):
        "copy this folder structure into localpath/ and return its path"
        if isinstance(self.stream, str):
            outname = os.path.join(localpath, os.path.basename(self.stream))
            shutil.copytree(self.stream, outname)
        else:
            self.stream.extractall(localpath)
            # localpath should now contain a single folder with subfolders/files
            outname = next(
                os.path.abspath(os.path.join(localpath, name))
                for name in os.listdir(localpath)
                if os.path.isdir(os.path.join(localpath, name))
            )
        return outname

    def force_to_filepath(self):
        "force this folder structure into a locally accessible (tar) file and return its path"
        with tempfile.NamedTemporaryFile(
            mode="w+b", prefix="viqicomm", suffix=".tar", delete=False
        ) as fout:  # who deletes this?
            if isinstance(self.stream, str):
                # folder path => package it as single tar file
                with tarfile.open(fileobj=fout, mode="w") as tout:  # TODO: could compress here
                    tout.add(self.stream, os.path.basename(self.stream), recursive=True)
            else:
                # is alread tarfile obj => copy to actual file
                shutil.copyfileobj(self.stream.fileobj, fout)
        return fout.name


class FutureResponse:
    def __init__(self, status_code: int, doc: Metadoc):
        self.status_code = status_code
        self._doc = doc

    def doc(self):
        return self._doc

    @property
    def text(self):
        # TODO: hack... return json directly from future service instead one day
        return json.dumps(self._doc.to_json())


####
#### KGK
#### Still working on filling this out
#### would be cool to have service definition language to make these.
#### TODO more service, renders etc.


class BaseServiceProxy:
    def __init__(self, session, service_url, timeout=DEFAULT_TIMEOUT):
        self.session = session
        self.service_url = service_url
        self.timeout = timeout

    def construct(self, path, params=None):
        url = self.service_url
        if params:
            path = f"{path}?{urllib.parse.urlencode(params)}"
        if path:
            url = urllib.parse.urljoin(str(url), str(path))
        return url

    # =================== TODO: get rid of render param ============
    # =================== TODO: move parts of formats.py into api section =========================

    def request(self, path=None, params=None, method="get", render=None, **kw):
        """
        @param path: a path relative to service (maybe a string or list)
        @param params: a diction of value to encode as params
        @param method: request type (get, put, post, etc)
        @param render: 'doc'/'etree'/'xml' to request doc response, 'json' for JSON response
        @return a request.response (INDEPENDENT OF render!)
        """
        if isinstance(path, list):
            path = "/".join(path)

        if path and path[0] == "/":
            path = path[1:]
        if path:
            path = urllib.parse.urljoin(str(self.service_url), str(path))
        else:
            path = self.service_url

        # no longer in session https://github.com/requests/requests/issues/3341
        timeout = kw.pop("timeout", self.timeout)
        headers = kw.pop("headers", self.session.c.headers)
        data = kw.get("data")
        if isinstance(data, str):  # hacky way to guess content type
            data = data.lstrip()
            if data[0] == "<":
                headers["Content-Type"] = "text/xml"  # TODO: -------------- use formatters on kw['data']!!!!
            elif data[0] in ("{", "["):
                headers["Content-Type"] = "application/json"  # TODO: -------------- use formatters on kw['data']!!!!
        #         if render in ("xml", "etree", "doc"):
        #             headers["Accept"] = "text/xml"
        if render in ("json",):
            headers["Accept"] = "application/json"
        else:
            headers["Accept"] = "text/xml"  # default xml transmission
        # ignore any format request because it is handled via render and headers
        # not all params are dics, they may be a list of tuples for ordered params
        if params is not None and isinstance(params, dict):
            params.pop("format", None)

        response = self.session.c.request(
            url=path,
            params=params,
            method=method,
            timeout=timeout,
            headers=headers,
            **kw,
        )
        return response

    def fetch(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, **kw)

    def get(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, **kw)

    def post(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, method="post", **kw)

    def put(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, method="put", **kw)

    def patch(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, method="patch", **kw)

    def delete(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, method="delete", **kw)

    def fetch_file(self, path=None, params=None, render=None, localpath=None, **kw):
        with self.fetch(path=path, params=params, render=render, stream=True, **kw) as response:
            if response.status_code != requests.codes.ok:  # pylint: disable=no-member
                raise BQApiError(response)

            # OK response download
            original_length = content_left = response.headers.get("content-length")
            # log.debug('content-length: %s', original_length)
            content_md5 = response.headers.get("x-content-md5")
            content_left = content_left is not None and int(content_left)
            if content_md5 is not None:
                content_hasher = hashlib.md5()
                log.debug("x-content-md5: %s", content_md5)

            with open(localpath, "wb") as fb:
                # for block in response.iter_content(chunk_size = 16 * 1024 * 1024): #16MB
                while True:
                    block = response.raw.read(16 * 1024 * 1024, decode_content=True)
                    if block:
                        if content_left is not None:
                            content_left -= 16 * 1024 * 1024
                        if content_md5:
                            content_hasher.update(block)
                        fb.write(block)
                    else:
                        break
                fb.flush()
        # content-left can be < 0 when accept-encoding is a compressed type: gzip, deflate
        if original_length is not None and content_left > 0:
            raise BQApiError(response)
        if content_md5 is not None and content_md5 != content_hasher.hexdigest():
            raise BQApiError(response)

        return response


class FuturizedServiceProxy(BaseServiceProxy):
    def _wait_for_future(self, future_id: str, retry_time: int = 5) -> Metadoc:
        future_service = self.session.service("futures")
        try:
            future_state = "PENDING"
            while future_state in ("PENDING", "PROCESSING"):
                time.sleep(retry_time)
                future_state = future_service.get_state(future_id)
            return future_service.get_result(future_id)
        finally:  # because get_result could throw an exception!
            try:
                future_service.delete(future_id)
            except FutureNotFoundError:
                # already deleted
                pass

    def _reraise_exception(self, response):
        exc = response.headers.get("x-viqi-exception")
        if exc is not None:
            # exception was returned... re-raise it
            code_to_exception(response)

    def _ensure_future_result(self, response, method="get", render=None, **kw):
        fut = response.headers.get("x-viqi-future")
        if fut is not None:
            # future was returned => wait for result
            retry_time = int(response.headers.get("Retry-After", 5))
            res = self._wait_for_future(fut, retry_time)
            # replace the original future response with a new response with OK code and result doc
            # TODO: how to do this properly?
            response = FutureResponse(200, res)

        else:
            while response.status_code == http_code_future_not_ready:  # could also be one of the retry-futures (321)
                retry_time = int(response.headers.get("Retry-After", 5))
                retry_url_toks = urlparse(response.headers.get("Location"))
                time.sleep(retry_time)
                path_without_service = "/".join(retry_url_toks.path.strip("/").split("/")[1:])  # assume same service
                response = self.request(
                    path=path_without_service,
                    params=dict(parse_qsl(retry_url_toks.query)),
                    method=method,
                    render=render,
                    future_wait=False,
                    **kw,
                )

        return response

    def _prep_result(self, res, render=None):
        if res is None:
            return res
        if render == "doc":
            return res.doc()
        elif render == "etree":
            log.warn("use of render=etree deprecated")
            return Metadoc.convert_back(res.doc())
        elif render == "json":
            return json.loads(res.text) if res.text else res.text
        else:
            return res

    def request(self, path=None, params=None, method="get", render=None, future_wait=True, **kw):
        """
        @param path: a path relative to service (maybe a string or list)
        @param params: a diction of value to encode as params
        @param method: request type (get, put, post, etc)
        @param render: 'doc'/'etree'/'xml' to request doc response, 'json' for JSON response
        @param future_wait: if true, wait for result in case future came back; if false, return even if future doc
        @return a request.response (INDEPENDENT OF render!)
        """
        # enable redirects again; futures use code 321 which is not affected by requests redirect handling
        #         kw["allow_redirects"] = kw.get(
        #             "allow_redirects", False
        #         )  # turn off redirects by default as it will interfere with future handling
        response = super().request(path=path, params=params, method=method, render=render, **kw)

        # handle two special cases: (1) exception came back, (2) future came back
        self._reraise_exception(response)
        if future_wait:
            response = self._ensure_future_result(response, method=method, render=render, **kw)

        return response


class AdminProxy(FuturizedServiceProxy):
    def login_as(self, user_name):
        data = self.session.service("meta")
        userxml = data.fetch("user", params={"name": user_name, "wpublic": 1}, render="doc")
        user_uniq = userxml.find(f"user[@name='{user_name}']")
        if user_uniq is not None:
            user_uniq = user_uniq.get("resource_uniq")
            response = self.fetch(f"user/{user_uniq}/login")
            response.raise_for_status()

            # check the login succeded
            user_session = self.session.service("auth_service").get("session", render="doc")
            user_id = user_session.find("user").get("value")
            # user_id is /<user_uniq"
            if user_id[1:] == user_uniq:
                return user_uniq

        # login failed
        return None

    def login_create(self, login_id: str) -> requests.Response:
        """Login as LOGIN_ID , create user if not already create

        Args:
          login_id should be a valid login id (email)
        Returns:
         a Response
        """
        return self.post(f"user/{login_id}/login?create=true")


class AuthProxy(FuturizedServiceProxy):
    def login_providers(self, **kw):
        return self.request("login_providers", **kw)

    def credentials(self, **kw):
        return self.request("credentials", **kw)

    def get_session(self, **kw):  # hides session
        return self.request("session", **kw)

    def get(self, path=None, params=None, render=None, **kw):
        res = super().get(path=path, params=params, render=render, **kw)
        return self._prep_result(res, render)


class BlobProxy(FuturizedServiceProxy):
    def create_blob(self, path: str, blob: object):
        """Create binary resource at given path from the given object/file.

        Args:
            path (str): mountpath for new blob
            blob (object): object to store (if str, is assumed to be local filename)

        Raises:
            DuplicateFile: path already exists
            ResourceNotFoundError: path not valid
            IllegalOperation: blob creation not allowed at given path
            BQApiError: any other error

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> blob_service.create_blob('store://mymount/my/path/name.jpg', '/tmp/image.jpg')
        """
        # prep inputs
        path = _prepare_mountpath(path)

        if isinstance(blob, str):
            with open(blob, "rb") as fh:
                filedata = fh.read()
        else:
            filedata = pickle.dumps(blob)

        res = self.post(path, headers={"Content-Type": "application/octet-stream"}, data=filedata)

        # prep outputs
        code_to_exception(res)

    def delete_blob(self, path: str):
        """Delete binary resource at given path.

        Args:
            path (str): mountpath for blob to delete

        Raises:
            ResourceNotFoundError: path not valid
            IllegalOperation: blob deletion not allowed (e.g., resource is registered or path is container)
            BQApiError: any other error

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> blob_service.delete_blob('store://mymount/my/path/name.jpg')
        """
        # prep inputs
        path = _prepare_mountpath(path)

        res = self.delete(path)

        # prep outputs
        code_to_exception(res)

    def register(self, path: str = None, resource: Metadoc = None) -> Metadoc:
        """Register blob at a given mount path.

        Args:
            path (str, optional): mountpath to blob
            resource (Metadoc, optional): assign suggested type, permissions and metadata at registration time

        Returns:
            Metadoc: resource document

        Raises:
            AlreadyRegisteredError: blob already registered
            ResourceNotFoundError: path not valid
            IllegalOperation: blob registration not allowed at given path
            BQApiError: any other error

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> blob_service.register(path='store://mymount/my/path/name.jpg')
            <Metadoc at 0x...>
        """
        # prep inputs
        log.debug(f"register {path}")
        path = _prepare_mountpath(path)

        res = self.post(posixpath.join("register", path), data=resource)

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def unregister(self, path: str = None, resource: Metadoc = None):
        """Unregister blob with given id.

        Args:
            path (str, optional): mount-path of blob
            resource (Metadoc, optional): resource to unregister

        Returns:
            bool: True, if successfully unregistered

        Raises:
            ResourceNotFoundError: invalid mount-path or id
            NotRegisteredError: blob not registered

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> blob_service.unregister(path='store://mymount/my/path/name.jpg')
            True
        """
        # prep inputs
        log.debug(f"unregister {path}")
        if path is None and resource is not None:
            path = resource.text.split(",", 1)[0]
        log.debug(f"unregister {path}")
        path = _prepare_mountpath(path)

        res = self.post(posixpath.join("unregister", path))

        # prep outputs
        code_to_exception(res)

        return True

    def read_chunk(
        self,
        blob_id: str,
        content_selector: str = None,
        vts: str = None,
        as_stream: bool = False,
    ):
        """Read chunk of resource specified by id.

        Args:
            blob_id (uuid): mount-path or uuid or alias of blob
            content_selector (str): blob-specific selector of subset to return (or all if None)
            vts (str): version timestamp to return (or latest if None)
            as_stream (bool): return chunk as bytes stream (ResponseFile/ResponseFolder), otherwise return as localpath

        Returns:
            ResponseFile or ResponseFolder or bytes: file obj or folder obj or blob byte array

        Raises:
            NoAuthorizationError: no access permission for blob
            ResourceNotFoundError: no blob with given id
            BQApiError: any other error

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> with blob_service.read_chunk('00-123456789', as_stream=True) as fp:
            >>>    fo.read(1024)
        """
        # prep inputs
        blob_id = _prepare_uniq_or_alias_or_path(blob_id)

        headers = {}
        if content_selector is not None:
            headers["x-content-selector"] = content_selector
        if vts is not None:
            headers["x-vts"] = vts
        res = self.get(f"/{blob_id}", headers=headers, stream=as_stream)

        # prep outputs
        code_to_exception(res)

        if res.headers["content-type"] == "application/x-tar":
            # this is a tarfile of a folder structure
            res = ResponseFolder(res)
        else:
            # this is a single file
            res = ResponseFile(res)

        if as_stream:
            return res
        else:
            # caller wants local copy... this may be never used/needed...
            localpath = tempfile.mkdtemp()  # who deletes this?
            return res.copy_into(localpath)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


class ImportProxy(FuturizedServiceProxy):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.upload_prefix = "/home/uploads"  # TODO fetch from user prefences
        self.upload_default_mount = "/home"  # TODO fetch from user
        self.protocol_info_map = {"/home": None}  # Map of store to best protocol

    def destination_path(self, srcpath, dstpath):
        """Create a valid destination path from src and dst

        Examples:
          Source known, destination None
          destination_path("filename.tif", None) -> upload_prefix/filename.tif
          destination_path("path2/to/file/filename.tif", None) -> upload_prefix/path/to/file/filename.tif
          destination_path("/home/user/path2/to/file/filename.tif", None) -> upload_pefix/filename.tif

          Source None, destination
          destination_path(None, "filename.tif") -> upload_mount/filename.tif
          destination_path(None, "relatitive_path/filename.tif") -> upload_mount/relative_path/filename.tif
          destination_path(None, "/home/project/to/path/filename.tif") -> "/home/project/to/path/filename.tif"

          Source and Destination -> use dest
          destination_path("filename.tif", "filename.tif") -> upload_mount/filename.tif
          destination_path("path2/to/file/filename.tif", "filename.tif") -> $upload_mount/filename.tif
          destination_path("path2/to/file/filename.tif", "relative_path/filename.tif") -> $upload_mount/path/to/file/filename.tif
          destination_path("/home/user/path2/to/file/filename.tif", "/home/poject/path2/filename.tif") -> /home/project/path2/filename.tif

          Source and Destination Dir (marked by trailing "/" -> use src + dest
          destination_path("filename.tif", "apath/") -> $upload_mount/apath/tfilename.tif
          destination_path("path2/to/file/filename.tif", "apath/") -> $upload_mount/apath/filename.tif
          destination_path("/home/user/path2/to/file/filename.tif", "/home/mount/apath/") -> /home/mount/apath/filename.tif

        """
        if dstpath is None:
            dstpath = self.upload_prefix
            if srcpath == "/":
                return posixpath.join(dstpath, srcpath[1:])
            return posixpath.join(dstpath, srcpath)

        if dstpath[-1] == "/":  # DIR destination
            dstpath = posixpath.join(dstpath, os.path.basename(srcpath))

        if dstpath[0] != "/":  # NOT absolute upload, join with def
            return posixpath.join(self.upload_default_mount, dstpath)

        return dstpath

    # @functools.lru_cache(maxsize=None)
    def transfer_protocol_info(self, path: str = None, protocol: str = None) -> Optional[Metadoc]:
        """Return proto info for best transfer_protocol

        Args:
            path : the destination storepath
        Returns:
           A proto_info dict: with protocol specific information
        """
        if path is None:
            path = self.upload_prefix
        if path[0] == "/":
            path = path[1:]

        dirpath = os.path.dirname(path)
        mount = dirpath.split("/")[0]  # 'home/hello/aaa.jpg' -> ['home', 'hello', 'aaa.jpg']
        if (mount, protocol) in self.protocol_info_map:
            return self.protocol_info_map[(mount, protocol)]

        if protocol is not None:
            available_protocols = [Metadoc.create_doc("prototcol", type=protocol)]
        else:
            protocols = self.fetch(posixpath.join("/transfer_protocol", dirpath))
            # Choose the preferred one by order
            code_to_exception(protocols)
            proto_doc = protocols.doc()
            # log.info("PROTO %s", str(proto_doc))
            available_protocols = proto_doc.path_query("protocol")

        for proto in available_protocols:
            # check if we know one
            if hasattr(self, "transfer_" + proto.attrib["type"]):
                # we know how to transfer, grab info
                proto_info = self.fetch(
                    posixpath.join("/transfer_protocol", dirpath),
                    params={"protocol": proto.attrib["type"]},
                )
                code_to_exception(proto_info)
                proto_info = proto_info.doc()
                self.protocol_info_map[(mount, None)] = proto_info
                self.protocol_info_map[(mount, proto)] = proto_info
                return proto_info
        return None

    def transfer_file(
        self,
        srcpath: str,
        dstpath: str = None,
        xml: Metadoc = None,
        callback: Callable = None,
        protocol: str = None,
    ):
        """Transfer a file to the system
        Args:
          srcpath : the path to the local file or filename to give to the file object
          xml     :
        """
        with open(srcpath, "rb") as src:
            return self.transfer_fileobj(
                src,
                xml=xml,
                callback=callback,
                srcpath=srcpath,
                dstpath=dstpath,
                protocol=protocol,
            )

    def transfer_fileobj(
        self,
        fileobj: BinaryIO,
        srcpath: str = None,
        dstpath: str = None,
        xml: Metadoc = None,
        callback: Callable = None,
        protocol: str = None,
    ):
        if srcpath is None and hasattr(fileobj, "name"):
            srcpath = fileobj.name
        dstpath = self.destination_path(srcpath, dstpath)
        transfer_info = self.transfer_protocol_info(path=dstpath, protocol=protocol)
        # log.info("TRANS %s", str(transfer_info))
        # Use the protocol to  find a method to transfer the file
        if transfer_info is not None:
            protocol = transfer_info.path_query("protocol")[0]
            transfer_fct = getattr(self, "transfer_" + protocol.attrib["type"])
            if transfer_fct is not None:
                return transfer_fct(
                    fileobj=fileobj,
                    dstpath=dstpath,
                    xml=xml,
                    callback=callback,
                    transfer_info=transfer_info,
                )
        raise BQApiError("No transfer protocol supported for file transfer")

    def transfer_multipart(
        self,
        fileobj: BinaryIO,
        dstpath: str,
        xml=None,
        callback=None,
        transfer_info=None,
    ):
        fields = {}
        filename = normalize_unicode(fileobj.__name__)
        fields["file"] = (
            os.path.basename(filename),
            fileobj,
            "application/octet-stream",
        )
        if xml is not None:
            fields["file_resource"] = (None, xml, "application/xml")
        if fields:
            # https://github.com/requests/toolbelt/issues/75
            m = MultipartEncoder(fields=fields)
            m._read = m.read  # pylint: disable=protected-access
            # filesize = os.fstat (fileobj).st_size
            # haveread = 0

            def reader(size):
                buff = m._read(8192 * 1024)  # 8MB
                # haveread += 8192
                if callable(callback):
                    callback(len(buff))
                return buff

            m.read = reader
            # ID generator is used to force load balancing operations
            response = self.post(
                "transfer_" + id_generator(),
                data=m,
                headers={"Accept": "text/xml", "Content-Type": m.content_type},
            )
            code_to_exception(response)
            return response.doc()

    def transfer_binary(self, fileobj, dstpath, xml=None, callback=None, transfer_info=None):
        response = self.post(
            posixpath.join("transfer_direct", dstpath[1:]),
            data=fileobj,
            headers={"Content-Type": "application/octet-stream"},
        )
        code_to_exception(response)

        if xml is None:
            return None

        blobs = self.session.service("blobs")
        blob = blobs.register(path=dstpath[1:], resource=xml)

        # blob = blobs.register(posixpath.join(path, filename))
        # if xml:
        #     meta = self.session.service('meta')
        #     # Find the uploaded blob and register with XML
        #     for kid in Metadoc.from_tagxml(xml):
        #         blob.append(kid)
        #     meta.put(blob.get("resource_uniq"), data=blob)
        return blob

    def transfer_s3(
        self,
        fileobj: BinaryIO,
        dstpath,
        xml=None,
        callback=None,
        transfer_info=None,
        **kw,
    ):
        """Transfer a file to s3
        Args :
            fileob  : the options open file object
            dstpath : a store path i.e. /storename/d1/d2
            xml     : xml to registered
            info    : metadoc
                       <transfer>
                         <protocol type="fsxlustre">
                         <info>
                           <Credentials>
                            <AccessKeyId></AccessKeyId>
                            <SessionToken></SessionToken>
                            <SecretAccessKey>TMWnEWRxPak+Pebk8ngp28fp5tvoVlg3yrbxfQ5x</SecretAccessKey>
                            <Expiration>2022-06-28 19:32:58+00:00</Expiration>
                           </Credentials>
                           <Destination>
                             <S3>
                              <Region>us-west-2</Region>
                              <Bucket>viqi-lustre-staging</Bucket>
                              <Folder>users/admin/testdir</Folder>
                              <Uid>1000</Uid>
                              <Gid>1000</Gid>
                            </S3>
                          </Destination>
                     </protocol>
                   </transfer>
        Returns:
         the list of files transferred
        """
        # Get cliend creds from info

        filename = os.path.basename(dstpath)
        partial_path = "/".join(dstpath.split("/")[2:-1])
        try:
            upload_ok = False
            s3client = None
            for _ in range(3):  # Attempt upload 3 times with expired token handling
                info = transfer_info.path_query("//info")[0].to_json()
                s3_info = info["info"]
                log.debug(
                    "INFO %s destpath:%s filename:%s fileobj:%s",
                    s3_info,
                    dstpath,
                    filename,
                    fileobj,
                )
                if s3client is None:
                    s3client = self._s3_session(s3_info["Credentials"])

                try:
                    if not self._s3_dir_exists(s3client, s3_info, partial_path):
                        self._s3_create_dirs(s3client, s3_info, partial_path)
                    s3client.upload_fileobj(
                        fileobj,
                        Bucket=s3_info["Destination"]["S3"]["Bucket"],
                        Key=posixpath.join(
                            s3_info["Destination"]["S3"]["Folder"],
                            partial_path,
                            filename,
                        ),
                        Callback=callback,
                        ExtraArgs={
                            "Metadata": {
                                "user-agent": "aws-fsx-lustre",
                                "file-permissions": "0100660",
                                "file-owner": s3_info["Destination"]["S3"]["Uid"],
                                "file-group": s3_info["Destination"]["S3"]["Gid"],
                            }
                        },
                    )
                    fileobj.close()
                    upload_ok = True
                    break
                except botocore.exceptions.ClientError as error:
                    code = error.response["Error"]["Code"]
                    log.warn("AWS Client error %s -> code %s", error, code)
                    if code in ("ExpiredToken", "AccessDenied"):
                        transfer_info = self._s3_refresh(transfer_info)
                        s3client = None
                        fileobj = open(fileobj.name, "rb")  # Potential File Obj Leak
                        continue

            if not upload_ok:
                raise BQApiError(f"Failed upload of {filename}. S3 token invalid")

            if xml is None:
                return None

            # register the uploaded file with xml if available
            blobs = self.session.service("blobs")
            if isinstance(xml, str):
                xml = Metadoc.from_naturalxml(xml)

            try:
                time.sleep(2)
                for attempt in tenacity.Retrying(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(2)):
                    log.info(f"REGISTER {dstpath}")
                    blobdoc = blobs.register(path=dstpath, resource=xml)
                    return blobdoc
            except tenacity.RetryError:
                log.error("Regsitration failed after upload")

        except boto3.exceptions.S3UploadFailedError:
            log.exception("During upload of %s", filename)
        return None

    def _s3_create_dirs(self, s3client, s3_info: dict, path: str):
        """Ensure directory exists and has proper metadata (permissions)"""
        head, tail = posixpath.split(path)
        if not tail:  # special case for trailing '/'
            head, tail = posixpath.split(head)
        if head and tail:
            # check if head exists
            if not self._s3_dir_exists(s3client, s3_info, head):
                # log.debug("recurse %s", head)
                self._s3_create_dirs(s3client, s3_info, head)
        #
        self._s3_mkdir(s3client, s3_info, path)

    def _s3_dir_exists(self, s3client, s3_info, dirpath):
        """Check if user rooted directory exists"""
        try:
            # log.debug("s3_direxists %s", dirpath)
            s3client.head_object(
                Bucket=s3_info["Destination"]["S3"]["Bucket"],
                Key=posixpath.join(s3_info["Destination"]["S3"]["Folder"], dirpath, ""),
            )
            return True
        except botocore.exceptions.ClientError as error:
            code = error.response["Error"]["Code"]
            log.debug("s3direxists error %s", code)
        return False

    def _s3_mkdir(self, s3client, s3_info, dirpath):
        try:
            # log.debug("s3_mkdir %s ", dirpath)
            s3client.put_object(
                Bucket=s3_info["Destination"]["S3"]["Bucket"],
                Key=posixpath.join(s3_info["Destination"]["S3"]["Folder"], dirpath, ""),
                Metadata={
                    "file-owner": s3_info["Destination"]["S3"]["Uid"],
                    "file-group": s3_info["Destination"]["S3"]["Gid"],
                },
            )
        except botocore.exceptions.ClientError as error:
            code = error.response["Error"]["Code"]
            log.debug("ended on %s", code)

    def _s3_session(self, s3_info: Dict):
        """Create a long-lasting s3 Session suitable for caching
        Args:
           s3_info : {"AccessKeyId": "ID",
                       "SessionToken": "Token", "SecretAccessKey":
                       "Secret", "Expiration": "Expires"}

        Returns:
          a S3 boto client
        TODO :  Utilize a refreshable credential provider
                https://stackoverflow.com/questions/61899028/where-can-i-find-the-documentation-for-writing-custom-aws-credential-provider-us
        """
        session = boto3.session.Session()  # see https://github.com/boto/boto3/issues/801
        s3client = session.client(
            "s3",
            aws_access_key_id=s3_info["AccessKeyId"],
            aws_secret_access_key=s3_info["SecretAccessKey"],
            aws_session_token=s3_info["SessionToken"],
        )
        return s3client

        raise BQApiError("transfer_s3 not implemented")

    def _s3_refresh(self, transfer_info: Metadoc) -> Metadoc:
        """Fetch new credential when expired
            info    : metadoc
                       <transfer>
                         <protocol type="fsxlustre">
                         <info>
                           <Credentials>
                            <AccessKeyId></AccessKeyId>
                            <SessionToken></SessionToken>
                            <SecretAccessKey>TMWnEWRxPak+Pebk8ngp28fp5tvoVlg3yrbxfQ5x</SecretAccessKey>
                            <Expiration>2022-06-28 19:32:58+00:00</Expiration>
                           </Credentials>
                           <Destination>
                             <S3>
                              <Region>us-west-2</Region>
                              <Bucket>viqi-lustre-staging</Bucket>
                              <Folder>users/admin/testdir</Folder>
                            </3>
                          </Destination>
                     </protocol>
                   </transfer>
        Returns:
         the list of files transferred
        """
        transfer_info = self.post("transfer_protocol", data=transfer_info)
        return transfer_info

    def transfer_fsxlustre(self, *args, **kw) -> Metadoc:
        return self.transfer_s3(*args, **kw)

    def register_list(self, script_name) -> Metadoc:
        """List available scripts"""
        scripts = self.fetch("register")
        code_to_exception(scripts)
        return scripts.doc()

    def register_run(self, script_name, storepath) -> Metadoc:
        """Run a registration script"""
        run = Metadoc(tag="resource")
        run.add_tag("script", value=script_name)
        run.add_tag("path", value=storepath)
        resp = self.post("register", data=run)
        code_to_exception(resp)
        return resp.doc()

    def import_register_run(self, script_name, storepath, params):
        """Run an importer script
            echo "<request><script>avia-plate</script> <path>store://local/2022-12-12/experiment1</path> </request>"|  http -a admin:admin POST http://hq.viqi.org:8180/import/register  content-type:application/xml
        Args:
          <resource>
            <script>avia-plate</script>
            <path>store://local/2022-12-12/experiment1</path>
            <params>
              <blah></blah>
              <blah></blah>
            </params>
          </resource>

        { "resource" : {  "script": "avia-plate", "path": "store://local/2022-12-12/experiment1" } }

        """
        # Retrieve scsript and params from request
        # prep inputs
        path = "register"

        body = Metadoc(tag="resource")
        body.add_tag("script", value=script_name)
        body.add_tag("path", value=storepath)
        body.add_child(params)
        res = self.post(path, data=body)

        # prep outputs
        code_to_exception(res)

        return res.doc()


class DatasetProxy(FuturizedServiceProxy):
    def create(self, dataset_name, member_list, **kw):
        """Create a dataset from a list of resource_uniq elements"""
        data = self.session.service("data_service")
        dataset = Metadoc(tag="dataset", name=dataset_name)
        for member_uniq in member_list:
            member = dataset.add_tag("value", type="object")
            member.text = member_uniq

        return data.post(data=dataset, render="doc")

    def delete(self, dataset_uniq, members=False, **kw):
        if members:
            params = kw.pop("params", {})
            params["duri"] = dataset_uniq
            return self.fetch("delete", params=params, **kw)
        data = self.session.service("data_service")
        return data.delete(dataset_uniq)

    def append_member(self, dataset_uniq, resource_uniq, **kw):
        """Append an element"""
        data = self.session.service("data_service")
        member = Metadoc(tag="value", type="object")
        member.text = data.construct(resource_uniq)
        self.post(dataset_uniq, data=member, render="doc")

    def delete_member(self, dataset_uniq, resource_uniq, **kw):
        """Delete a member..
        @return new dataset if success or None
        """
        data = self.session.service("data_service")
        dataset = data.fetch(dataset_uniq, params={"view": "full"}, render="doc")
        members = dataset.path_query('value[text()="%s"]' % data.construct(resource_uniq))
        for member in members:
            member.delete()
        if len(members):
            return data.put(dataset_uniq, data=dataset, render="doc")
        return None


class MexProxy(FuturizedServiceProxy):
    def get_all_mexes(self) -> Metadoc:
        """Get module execution (mex) documents for all running modules.

        Returns:
            Metadoc: mex document

        Raises:
            BQApiError: any other error

        Examples:
            >>> mex_service = bqsession.service('mexes')
            >>> mex_service.get_all_mexes()
            <Metadoc at 0x...>
        """
        res = self.get("")

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def get_mex(self, mex_id: str) -> Metadoc:
        """Get module execution (mex) document for the execution specified.

        Args:
            mex_id (uuid): mex uniq

        Returns:
            Metadoc: mex document

        Raises:
            MexNotFoundError: if no mex with given id was found
            BQApiError: any other error

        Examples:
            >>> mex_service = bqsession.service('mexes')
            >>> mex_service.get_mex('00-123456789')
            <Metadoc at 0x...>
        """
        # prep inputs
        mex_id = _prepare_uniq(mex_id)

        res = self.get(f"/{mex_id}")

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def get_mex_log(self, mex_id: str) -> Metadoc:
        """Get module execution (mex) log for the execution specified.

        Args:
            mex_id (uuid): execution identifier

        Returns:
            Metadoc: <log>logtext</log>

        Raises:
            MexNotFoundError: if no mex with given id was found

        Examples:
            >>> mex_service = bqsession.service('mexes')
            >>> mex_service.get_mex_log('00-123456789')
            2021-07-02 03:00:56,848 DEBUG [urllib3.connectionpool] (_new_conn) - Starting ne...
        """
        # prep inputs
        mex_id = _prepare_uniq(mex_id)

        res = self.get(f"/{mex_id}/log")

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def request(self, path=None, params=None, method="get", render=None, **kw):
        # TODO: add real api fct
        res = super().request(path=path, params=params, method=method, render=render, **kw)
        return self._prep_result(res, render)


class TableProxy(FuturizedServiceProxy):
    def load_array(self, table_uniq, path, slices=None, want_info=False):
        """
        Load array from BisQue.
        """
        slices = slices or []
        if table_uniq.startswith("http"):
            table_uniq = table_uniq.split("/")[-1]
        slice_list = []
        for single_slice in slices:
            if isinstance(single_slice, slice):
                slice_list.append(
                    "{};{}".format(
                        single_slice.start or "",
                        "" if single_slice.stop is None else single_slice.stop - 1,
                    )
                )
            elif isinstance(single_slice, int):
                slice_list.append(f"{single_slice};{single_slice}")
            else:
                raise BQApiError("malformed slice parameter")
        path = "/".join([table_uniq.strip("/"), path.strip("/")])
        info_url = "/".join([path, "info", "format:json"])
        info_response = self.get(info_url)
        try:
            num_dims = len(json.loads(info_response.text).get("sizes"))
        except ValueError:
            raise BQApiError("array could not be read")
        # fill slices with missing dims
        for _ in range(num_dims - len(slice_list)):
            slice_list.append(";")
        data_url = "/".join([path, ",".join(slice_list), "format:hdf"])
        response = self.get(data_url)
        # convert HDF5 to Numpy array (preserve indices??)
        with tables.open_file(
            "array.h5",
            driver="H5FD_CORE",
            driver_core_image=response.content,
            driver_core_backing_store=0,
        ) as h5file:
            res = h5file.root.array.read()
        if want_info:
            return res, json.loads(info_response.text)
        else:
            return res

    def store_array(self, array, storepath, name) -> Metadoc:
        """
        Store numpy array or record array in BisQue and return resource doc.
        """
        try:
            dirpath = tempfile.mkdtemp()
            # (1) store array as HDF5 file
            out_name = name + ".h5" if not name.endswith((".h5", ".hdf5")) else name  # importer needs extension .h5
            out_file = os.path.join(dirpath, out_name)
            with tables.open_file(out_file, "w", filters=tables.Filters(complevel=5)) as h5file:  # compression level 5
                if array.__class__.__name__ == "recarray":
                    h5file.create_table(h5file.root, name, array)
                elif array.__class__.__name__ == "ndarray":
                    h5file.create_array(h5file.root, name, array)
                else:
                    raise BQApiError("unknown array type")  # TODO: more specific error
            # (2) call bisque blob service with file
            mountpath = posixpath.join(storepath, out_name)
            blobs = self.session.service("blobs")
            blobs.create_blob(path=mountpath, localfile=out_file)
            # (3) register resource
            return blobs.register(path=mountpath)

        finally:
            shutil.rmtree(dirpath)

    def load_table(self, table_uniq, path, slices=None, as_dataframe=True):
        """
        Load table as a numpy recarray or pandas dataframe.
        """
        ndarr, info = self.load_array(table_uniq, path, slices, want_info=True)
        res = np.core.records.fromarrays(ndarr.transpose(), names=info["headers"], formats=info["types"])
        if as_dataframe is True:
            res = pd.DataFrame.from_records(res)
        return res

    def store_table(self, table, storepath, name) -> Metadoc:
        """
        Store numpy recarray or pandas dataframe in BisQue and return resource doc.
        """
        if isinstance(table, pd.DataFrame):
            table = table.to_records()
        if table.__class__.__name__ != "recarray":
            raise BQApiError("unknown table type")  # TODO: more specific error
        return self.store_array(table, storepath, name)


class ImageProxy(FuturizedServiceProxy):
    class ImagePixels:
        """manage requests to the image pixels"""

        def __init__(self, image_service, image_uniq):
            self.image_service = image_service
            self.image_uniq = image_uniq
            self.ops = []

        def _construct_url(self):
            """build the final url based on the operation"""
            return self.image_service.construct(
                path="{}?{}".format(self.image.get_docid(), "&".join("%s=%s" % tp for tp in self.ops))
            )

        # TODO: image_fetch instead of want_str, need better way to infer return type (binary or str)
        def fetch(self, path=None, stream=False, want_str=False):
            """resolve the current and fetch the pixel"""
            # url = self._construct_url()
            if path is not None:
                response = self.image_service.fetch_file(path=self.image_uniq, params=self.ops, localpath=path)
            else:
                response = self.image_service.fetch(self.image_uniq, params=self.ops, stream=stream)
                return response.text if want_str else response.content

        def command(self, operation, arguments=""):
            arguments = "" if arguments is None else arguments
            self.ops.append((operation, arguments))  # In case None is passed .. requests library removes
            return self

        def slice(self, x="", y="", z="", t=""):
            """Slice the current image"""
            return self.command("slice", f"{x},{y},{z},{t}")

        def format(self, fmt):
            return self.command("format", fmt)

        def resize(self, w="", h="", interpolation=""):
            """interpoaltion may be,[ NN|,BL|,BC][,AR]"""
            return self.command("resize", f"{w},{h},{interpolation}")

        def localpath(self):
            return self.command("localpath")

        def meta(self):
            return self.command("meta")

        def info(self):
            return self.command("info")

        def asarray(self):
            # Force format to be tiff by removing any format and append format tiff
            self.ops = [tp for tp in self.ops if tp[0] != "format"]
            self.format("tiff")
            with self.image_service.fetch(path=self.image_uniq, params=self.ops, stream=True) as response:
                # response.raw.decode_content = True
                return tifffile.imread(io.BytesIO(response.content))

        def savearray(self, fname, imdata=None, imshape=None, dtype=None, **kwargs):
            import_service = self.image_service.session.service("import_service")
            imfile = tempfile.mkstemp(suffix=".tiff")
            tifffile.imsave(imfile, imdata, imshape, dtype, **kwargs)
            import_service.transfer_fileobj(fname, fileobj=open(imfile, "rb"))
            os.remove(imfile)

        ## End ImagePixels

    def get_thumbnail(self, image_uniq, **kw):
        # url = urllib.parse.urljoin( self.session.service_map['image_service'], image_uniq, 'thumbnail' )
        r = self.get("%s/thumbnail" % image_uniq)
        return r

    def get_metadata(self, image_uniq, **kw):
        r = self.get("%s/meta" % image_uniq, render="doc").doc()
        return r

    def pixels(self, image_uniq):
        return ImageProxy.ImagePixels(self, image_uniq)


class ExportProxy(FuturizedServiceProxy):
    valid_param = {"files", "datasets", "dirs", "urls", "users", "compression"}

    def fetch_export(self, **kw):
        params = {key: val for key, val in list(kw.items()) if key in self.valid_param and val is not None}
        response = self.fetch("stream", params=params, stream=kw.pop("stream", True))
        return response

    def fetch_export_local(self, localpath, stream=True, **kw):
        response = self.fetch_export(stream=stream, **kw)
        if response.status_code == requests.codes.ok:
            with open(localpath, "wb") as f:
                shutil.copyfileobj(response.raw, f)
        return response


class DataProxy(FuturizedServiceProxy):
    # TODO: add real API fcts
    def request(self, path=None, params=None, method="get", render="doc", view=None, **kw):
        if view is not None:
            if isinstance(view, list):
                view = ",".join(view)
            params = params or {}
            params["view"] = view

        res = super().request(path=path, params=params, method=method, render=render, **kw)

        # prep outputs
        code_to_exception(res)

        return self._prep_result(res, render)

    def fetch(self, path=None, params=None, render="doc", **kw):
        return super().fetch(path=path, params=params, render=render, **kw)

    def get(self, path=None, params=None, render="doc", **kw):
        return super().get(path=path, params=params, render=render, **kw)

    def patch(self, path=None, params=None, render="doc", **kw):
        return super().patch(path=path, params=params, render=render, **kw)

    def post(self, path=None, params=None, render="doc", **kw):
        return super().post(path=path, params=params, render=render, **kw)

    def put(self, path=None, params=None, render="doc", **kw):
        return super().put(path=path, params=params, render=render, **kw)

    def delete(self, path=None, params=None, render=None, **kw):
        return super().delete(path=path, params=params, render=render, **kw)


class DirProxy(FuturizedServiceProxy):
    def create_container(self, path: str, name: str, container_type: str = "folder"):
        """Create new container with name at given path.

        Args:
            path (str): mountpath holding new container
            name (str): name of new container
            container_type (str): 'folder' or 'tablecontainer'

        Raises:
            IllegalOperation: path already exists
            ResourceNotFoundError: path not valid

        Examples:
            >>> dir_service = bqsession.service('dirs')
            >>> dir_service.create_container('store://mymount/my/path', 'new_container', container_type='tablecontainer')
        """
        # prep inputs
        path = _prepare_mountpath(path)

        res = self.post(
            path,
            data=Metadoc.from_naturalxml(f'<dir name="{name}" type="{container_type}" />'),
        )

        # prep outputs
        code_to_exception(res)

    def list_files(
        self,
        path,
        want_meta=False,
        want_types=False,
        patterns=None,
        limit=100,
        offset=0,
    ):
        """List all entries (registered and unregistered, resources and containers) at the given path.

        Args:
            path (str): mount-path to list
            want_meta (bool): if True, include metadata per entry
            want_types (bool): if True, include type guesses per entry (slow!)
            patterns (list of str): one or more wildcard patterns for filtering of entries (these are ORed)
            limit (int): max number of entries to return
            offset (int): starting entry number (for paging)

        Returns:
            Metadoc: doc describing path and all selected entries as children

        Raises:
            NoSuchFileError: file at mount-path does not exist
            NoSuchPathError: mount-path does not exist
            IllegalOperation: mount does not exist

        Examples:
            >>> dir_service = bqsession.service('dirs')
            >>> str(dir_service.list_files('/mymount/dir1', limit=10))
            '<dir name="mymount" ...> <dir ... /> ... <image ... /> <resource ... /> </dir>'
        """
        # prep inputs
        params = {}
        view_options = []
        if want_meta:
            view_options.append("meta")
        if want_types:
            view_options.append("types")
        if view_options:
            params["view"] = ",".join(view_options)
        if patterns:
            params["patterns"] = ",".join(patterns)
        params["limit"] = limit
        params["offset"] = offset

        res = self.get(path, params=params)

        # prep outputs
        code_to_exception(res)

        return res.doc()


class FutureProxy(FuturizedServiceProxy):
    def get_state(self, future_id):
        """Get state of the future with the given id.

        Args:
            future_id: future id

        Returns:
            str: state of future (e.g., PENDING or FINISHED)

        Raises:
            FutureNotFoundError: if no future with given id was found
            BQApiError: any other error

        Examples:
            >>> future_service = bqsession.service('futures')
            >>> future_service.get_state('8196770f-ea2e-4bc6-b569-9e29fc031d46')
            'PENDING'
        """
        res = self.get(f"/{future_id}")

        # prep outputs
        code_to_exception(res)

        return res.doc().get("state")

    def get_result(self, future_id):
        """Get result of the future with the given id.

        Args:
            future_id: future id

        Returns:
            Metadoc: result of the future or None, if no result

        Raises:
            ValueError: result can not be rendered as doc
            FutureNotFoundError: if no future with given id was found
            FutureNotReadyError: if future result is not ready yet
            BQApiError: any other error
            Exception: any exception raised by the async task

        Examples:
            >>> future_service = bqsession.service('futures')
            >>> future_service.get_result('8196770f-ea2e-4bc6-b569-9e29fc031d46')
            <Metadoc at 0x...>
        """
        res = self.get(f"/{future_id}/result")

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def delete(self, future_id):
        """Delete future with the given id.

        Args:
            future_id: future id

        Raises:
            FutureNotFoundError: if no future with given id was found
            BQApiError: any other error

        Examples:
            >>> future_service = bqsession.service('futures')
            >>> future_service.delete('8196770f-ea2e-4bc6-b569-9e29fc031d46')
        """
        res = super().delete(f"/{future_id}")

        # prep outputs
        code_to_exception(res)


SERVICE_PROXIES = {
    "admin": AdminProxy,
    "auths": AuthProxy,
    "blobs": BlobProxy,
    "meta": DataProxy,
    "mexes": MexProxy,
    "datasets": DatasetProxy,
    "import": ImportProxy,
    "tables": TableProxy,
    "pixels": ImageProxy,
    "dirs": DirProxy,
    "services": BaseServiceProxy,
    "futures": FutureProxy,
}


class ServiceFactory:
    @classmethod
    def make(cls, session, service_name):
        # translate to new service name
        service_name = session._RENAMED_SERVICES.get(service_name, service_name)
        svc = SERVICE_PROXIES.get(service_name, FuturizedServiceProxy)
        if session.service_map and service_name not in session.service_map:
            return None
        service_url = session.service_map[service_name]
        return svc(session, service_url)


def test_module():
    from vqapi import VQSession

    session = VQSession().init_local("admin", "admin", "http://localhost:8080")
    admin = session.service("admin")
    data = session.service("data_service")
    # admin.user(uniq).login().fetch ()
    xml = data.get("user", params={"resource_name": "admin"}, render="doc")
    user_uniq = xml.find("user").get("resource_uniq")
    admin.fetch(f"/user/{user_uniq}/login")


if __name__ == "__main__":
    test_module()
