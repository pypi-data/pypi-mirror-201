'''
Author: hexu
Date: 2021-11-19 10:29:02
LastEditTime: 2023-03-21 10:20:41
LastEditors: Hexu
Description: 文件存储服务
FilePath: /iw-algo-fx/intelliw/utils/storage_service.py
'''
import os
import io
import mimetypes
from intelliw.utils import iuap_request
from intelliw.config.config import STORAGE_SERVICE_URL, INSTANCE_ID


class StorageService:
    """
        文件传输，通过服务端获取的临时url进行文件在多个云存储（AliOss/Minio/HWObs）上的操作
        所有的请求需要进行加签
    """

    def __init__(self, key, client_type, process_type):
        """
        初始化下载/上传链接
            Args:
                key :
                    upload ： 文件存储于桶的位置（包含文件名） OSS_PATH + filename
                    download : AI工作坊存储在环境变量的值     DATA_SOURCE_ADDRESS
                client_type ： AliOss/Minio/HWObs
                process_type : download/upload
            Returns:
                self.service_url 为服务端根据client_type，process_type生成的链接， download和upload操作需要此链接
        """
        self.key = key
        self.client_type = self._get_client_type(client_type)
        self.service_url = self.__client_init(
            key, self.client_type, process_type)
        self.content_type = mimetypes.guess_type(key)[0] or 'application/octet-stream'
    
    def __client_init(self, key, client_type, process_type):
        """
        从服务端获取云存储操作链接

        下载链接一般可以直接下载的
        """
        if not STORAGE_SERVICE_URL and process_type == "download" and key.startswith("http"):
            return self.key

        resp = iuap_request.get(url=STORAGE_SERVICE_URL, params={
                                "key": key, "UrlType": process_type, "clientType": client_type, 'instanceid': INSTANCE_ID})
        resp.raise_for_status
        result = resp.json
        assert result.get("status") == 1, result
        return result.get("data")

    def upload(self, file):
        """
        通过操作链接进行上传操作
            Args:
                filepath ： 上传文件本地路径
        """
        def _put_file(f):
            headers = {'Content-Type': self.content_type}
            resp = iuap_request.put_file(
                url=self.service_url, headers=headers, data=f, need_auth=False)
            resp.raise_for_status()

        if isinstance(file, str) and os.path.exists(file) and os.path.isfile(file):
            try:
                with open(file, 'rb') as f:
                    _put_file(f)
            except Exception as e:
                raise Exception(f'{e}')
        elif isinstance(file, (bytes, bytearray, io.BufferedIOBase)):
            _put_file(file)
        else:
            raise FileNotFoundError('上传的文件文件不存在')

    def download(self, output_path, stream=False):
        """
        通过操作链接进行下载操作
            Args:
                output_path ： 下载文件保存路径
        """
        if os.path.exists(output_path):
            raise FileExistsError(f'文件 {output_path} 已存在')
        if stream:
            iuap_request.stream_download(
                method="get", url=self.service_url, output_path=output_path)
        else:
            iuap_request.download(url=self.service_url,
                                  output_path=output_path)

    def _get_client_type(self, _type):
        env_val = _type.upper()
        if env_val == "MINIO":
            return "Minio"
        elif env_val == "ALIOSS":
            return "AliOss"
        elif env_val == "HWOBS":
            return "HWObs"
        else:
            return "AliOss"
