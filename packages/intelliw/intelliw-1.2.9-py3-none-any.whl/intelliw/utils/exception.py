'''
Author: Hexu
Date: 2022-03-30 11:47:31
LastEditors: Hexu
LastEditTime: 2023-03-27 14:17:57
FilePath: /iw-algo-fx/intelliw/utils/exception.py
Description: 错误类定义
'''
####### error class #######


import os


class ExceptionNoStack(Exception):
    def ignore_stack(self):
        return True


class PipelineException(Exception):
    pass


class ModelLoadException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return '''模型加载异常\n
        报错信息: {}\n
        可能原因:\n
        1 内存分配过小, 模型加载时服务崩溃\n
        2 模型文件是否存在,加载模型的路径是否正确\n
        3 是否补全load函数,load函数是否存在问题\n
        4 如果使用checkpoint,检查代码是否正确加载checkpoint\n
        '''.format(self.msg)

    def ignore_stack(self):
        return True


class DatasetException(Exception):
    def ignore_stack(self):
        return True


class InferException(Exception):
    pass


class FeatureProcessException(Exception):
    def ignore_stack(self):
        return True


class DataSourceDownloadException(Exception):
    def ignore_stack(self):
        return True


class LinkServerException(Exception):
    pass


class HttpServerException(Exception):
    pass


class CheckpointException(Exception):
    def __str__(self) -> str:
        return '''
        checkpoint保存模型异常，发生错误的可能：
            1. save()方法在save_checkpoint()方法之前调用,请在训练结束后调用save()方法保存模型
            2. save_checkpoint()方法多次调用
        '''

    def ignore_stack(self):
        return True


class FileTransferDevice(Exception):
    def __init__(self, file, transfer_type) -> None:
        self.curkey = None
        self.err_msg = None
        self.transfer_type = transfer_type
        self.__put_file__(file)

    def __put_file__(self, file) -> None:
        from intelliw.utils.storage_service import StorageService
        from intelliw.config import config
        import intelliw.utils.message as message
        from intelliw.utils.global_val import gl

        try:
            if config.is_server_mode():
                self.curkey = os.path.join(config.STORAGE_SERVICE_PATH,
                                           config.SERVICE_ID, "data_check.json")
                StorageService(
                    self.curkey, config.FILE_UP_TYPE, "upload"
                ).upload(file)
                gl.recorder.report(message.CommonResponse(
                    200, 'file_transfer', 'success',
                    {'filepath': self.curkey},
                    businessType=self.transfer_type))
        except Exception as e:
            import logging
            self.err_msg = e
            logging.error(f"上传文件错误: {e}")

    def __str__(self) -> str:
        msg = ""
        if self.err_msg is None:
            msg = f'''文件传输成功：
            文件传输类型：{self.transfer_type}
            文件详情请查看：{self.curkey}
            '''
        else:
            msg = f'''文件传输错误:
            文件传输类型：{self.transfer_type}
            错误详情: {self.err_msg}
        '''
        return msg

    def ignore_stack(self):
        return True
