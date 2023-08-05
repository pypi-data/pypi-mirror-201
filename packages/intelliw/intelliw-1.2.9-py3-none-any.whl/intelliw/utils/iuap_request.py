"""
iUAP HTTP auth protocol implementation
"""
import time
import math
import ssl
import hashlib
import base64
import urllib.request
import urllib.parse
import urllib.error
from intelliw.config import config

try:
    import jwt

    has_jwt_package = True
except ImportError:
    print("[Framework Log] \033[33mIf want use authsdk, you need: pip install pyjwt\033[0m")
    has_jwt_package = False

DEFAULT_TIMEOUT: float = 10.0

# 全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context


class Response:
    def __init__(self, status: int, body: str, error: Exception = None):
        self.status = status
        self.body = body
        self.error = error
        self.json = self._try_json()

    def raise_for_status(self):
        """
        raise :class:`IuapRequestException <IuapRequestException>` if status is not 200
        """
        if self.status != 200:
            msg = 'http request error, status: [{}], body: [{}] '.format(
                self.status, self.body)
            if self.error is not None:
                raise IuapRequestException(
                    msg + str(self.error)) from self.error
            raise IuapRequestException(msg)

    def _try_json(self):
        import json
        try:
            return json.loads(self.body)
        except:
            return None

    def __str__(self):
        return 'status: {}, body: {}, error: {}'.format(self.status, self.body, self.error)


class IuapRequestException(Exception):
    pass


def download(url, output_path=None, method="GET", params=None, body=None, json=None, headers=None):
    # 加签
    token = ""
    if has_jwt_package:
        token = ""
    if has_jwt_package:
        token = sign(url, params)

    if headers is None:
        headers = {}
    headers['YYCtoken'] = token

    resp = __do_request(method=method, url=url,
                        data=body, params=params, json=json)
    if output_path is None:
        return resp
    else:
        resp.raise_for_status()
        mode = "w" if isinstance(resp.body, str) else "wb"
        with open(output_path, mode) as code:
            code.write(resp.body)


# stream_download 流式下载文件
def stream_download(url, output_path, method="get", params=None, body=None, json=None, headers=None):
    def report_hook(count, block_size, total_size):
        chunk_size = 1024
        speed = ((count * block_size) / (time.time() - start_time)) / \
            (chunk_size ** 2)
        plan = 100.0 * count * block_size / total_size
        print("\r[Framework Log] dataset downloading: {:.3f}, speed: {:.3f}MB/s".format(
            plan, speed), flush=True)
    # 加签
    token = ""
    if has_jwt_package:
        token = ""
    if has_jwt_package:
        token = sign(url, params)

    if headers is None:
        headers = {}
    headers['YYCtoken'] = token
    start_time = time.time()
    urllib.request.urlretrieve(url, output_path, report_hook)


def get(url: str, headers: dict = None, params: dict = None, timeout: float = DEFAULT_TIMEOUT) -> Response:
    """
    get request

    :param url: request url
    :param headers: request headers
    :param params: request url params
    :return: Response
    """
    return sign_and_request(url, 'GET', headers, params, timeout=timeout)


def post_json(url: str, headers: dict = None, params: dict = None, json: object = None,
              timeout: float = DEFAULT_TIMEOUT) -> Response:
    """
    post request, send data as json

    :param url: request url
    :param headers: request headers
    :param params: request url parameters
    :param json: request body. if data is not `str`, it will be serialized as json.
    :return: Response
    """

    if headers is None:
        headers = {}
    headers['Content-type'] = 'application/json; charset=UTF-8'
    return sign_and_request(url, 'POST', headers, params, json=json, timeout=timeout)


def put_file(url: str, headers: dict = None, params: dict = None, data: object = None,
             timeout: float = DEFAULT_TIMEOUT, need_auth=False) -> Response:
    if headers is None:
        headers = {'Content-Type': 'application/octet-stream'}
    return sign_and_request(url, 'PUT', headers, params, data=data, timeout=timeout, need_auth=need_auth)


def sign_and_request(url: str,
                     method: str = 'GET',
                     headers: dict = None,
                     params: dict = None,
                     data: bytes = None,
                     json: dict = None,
                     timeout: float = DEFAULT_TIMEOUT, need_auth=True) -> Response:
    """
    sign and do request

    :param url: request url, without query
    :param method: Http request method, GET, POST...
    :param headers: request headers
    :param params: parameters will be sent as url parameters. Also used to generate signature if sign_params is None.
    :param data: request body
    :param json: Request body in Json format
    :param sign_params: params used to generate signature, if sign_params is None, signature will be generated base on params.
    :param timeout: url access timeout
    :return: response body
    """
    token = ""
    if has_jwt_package and need_auth:
        if params is None:
            params = {}
        params['AuthSdkServer'] = "true"
        token = sign(url, params)

    if headers is None:
        headers = {}
    headers['YYCtoken'] = token
    headers['instanceID'] = config.INSTANCE_ID

    return __do_request(url, method, headers, params, data, json, timeout=timeout)


def sign(url: str, params: dict) -> str:
    """
    generate iuap signature

    :param url: request url, without parameters
    :param headers: request headers
    :param params:  request parameters, x-www-form-urlencoded request's body parameters should also be included.
    :return: iuap signature
    """
    issue_at = __issue_at()
    sign_key = __build_sign_key(
        config.ACCESS_KEY, config.ACCESS_SECRET, issue_at, url)
    jwt_payload = {
        "sub": url,
        "iss": config.ACCESS_KEY,
        "iat": issue_at
    }
    if params is not None and len(params) > 0:
        sorted_params = sorted(params.items())
        for item in sorted_params:
            if item[1] is None:
                val = ''
            elif len(str(item[1])) >= 1024:
                val = str(__java_string_hashcode(str(item[1])))
            else:
                val = str(item[1])
            jwt_payload[item[0]] = val

    jwt_token = jwt.encode(jwt_payload, key=sign_key, algorithm='HS256')
    return str(jwt_token, encoding='UTF-8')


def __issue_at():
    issue_at = int(time.time())
    issue_at = math.floor(issue_at / 600) * 600
    return issue_at


def __build_sign_key(access_key, access_secret, access_ts, url):
    str_key = access_key + access_secret + str(access_ts * 1000) + url
    sign_key_bytes = hashlib.sha256(str_key.encode('UTF-8')).digest()
    return base64.standard_b64encode(sign_key_bytes).decode('UTF-8')


def __java_string_hashcode(s: str):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000


def __do_request(url: str,
                 method: str = 'GET',
                 headers: dict = {},
                 params: dict = {},
                 data: bytes = None,
                 json: object = None,
                 timeout: float = DEFAULT_TIMEOUT) -> Response:
    # data format
    if json is not None:
        import json as json_m
        try:
            data = json_m.dumps(json).encode('utf-8')
        except:
            data = bytes(str(json), encoding="utf-8")

    # params format
    if params is not None and len(params) > 0:
        url = url + '?' + urllib.parse.urlencode(params)

    # header format
    if headers is None:
        headers = {}
    headers = {
        **headers,
        **{'X-tenantId': config.TENANT_ID,
           'tenant_id': config.TENANT_ID,
           'tenantId': config.TENANT_ID}
    }

    # do request
    req = urllib.request.Request(
        url=url, data=data, headers=headers, method=method)
    for i in range(1, 5):
        body = None
        try:
            # 创建未验证的上下文
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(
                req, timeout=timeout, context=context)
            body = response.read()
            try:
                body = body.decode('UTF-8')
            except UnicodeDecodeError:
                body = body
            return Response(response.status, body)
        except urllib.error.HTTPError as e:
            if i == 4:
                raise e
            time.sleep(i * 2)
            print(f"[request] request retry time: {i}, url: {url}, body: {body}, error: {e}")
