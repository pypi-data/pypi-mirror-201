'''
Author: Hexu
Date: 2022-04-25 15:16:48
LastEditors: Hexu
LastEditTime: 2023-03-24 11:11:04
FilePath: /iw-algo-fx/intelliw/datasets/datasource_iwimgdata.py
Description: 图片数据集
'''
import ssl
import json
import math
import os
import shutil
import urllib.request as requests
import urllib.error
import socket

from intelliw.config import config
from intelliw.datasets.datasource_base import AbstractDataSource, DataSourceReaderException
from intelliw.utils.exception import DataSourceDownloadException
from intelliw.utils import iuap_request
from intelliw.utils.logger import _get_framework_logger
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = _get_framework_logger()


def err_handler(request, exception):
    print("请求出错,{}".format(exception))


class CocoProcess:
    coco_type = 3
    coco_config = None
    licenses = None
    info = None
    categories = None
    set_config = None

    @classmethod
    def set_coco_info(cls, instance):
        cls.info = instance['info']
        cls.licenses = instance['licenses']
        cls.categories = instance['categories']
        cls.coco_config = cls.__gen_config(
            instance['images'], instance['annotations'])
        cls.reset_config()

    @classmethod
    def reset_config(cls):
        cls.set_config = {'licenses': cls.licenses, 'info': cls.info,
                          'categories': cls.categories, 'images': [], 'annotations': []}

    @classmethod
    def __gen_config(cls, images, annotations):
        a_map = {}
        for a in annotations:
            image_id = a['image_id']
            a_map[image_id] = a_map.get(image_id, [])
            a_map[image_id].append(a)
        return {i['file_name']: {'image': i, 'annotation': a_map[i['id']]} for i in images}

    @classmethod
    def gen_config(cls, filename):
        meta = cls.coco_config.get(filename)
        if meta is None:
            return f"image:{filename} annotation not exist"
        cls.set_config['images'].append(meta['image'])
        cls.set_config['annotations'].extend(meta['annotation'])
        return None

    @classmethod
    def flush(cls, path):
        with open(path, 'w+') as fp:
            json.dump(cls.set_config, fp, ensure_ascii=False)


class DataSourceIwImgData(AbstractDataSource):
    """
    非结构化存储数据源
    图片数据源
    """

    def __init__(self, input_address, get_row_address, ds_id, ds_type):
        """
        智能分析数据源
        :param input_address:   获取数据 url
        :param get_row_address: 获取数据总条数 url
        :param ds_id:   数据集Id
        """
        self.input_address = input_address
        self.get_row_address = get_row_address
        self.ds_id = ds_id
        self.ds_type = ds_type
        self.__total = None
        self.__gen_img_dir()

    def __gen_img_dir(self):
        logger = _get_framework_logger()
        filepath = os.path.join('./', config.CV_IMG_FILEPATH)
        if os.path.exists(filepath):
            logger.warn(f"图片数据保存路径存在:{filepath}, 正在删除路径内容")
            shutil.rmtree(filepath, ignore_errors=True)
        os.makedirs(config.CV_IMG_ANNOTATION_FILEPATH, 0o755, True)
        os.makedirs(config.CV_IMG_TRAIN_FILEPATH, 0o755, True)
        os.makedirs(config.CV_IMG_VAL_FILEPATH, 0o755, True)
        os.makedirs(config.CV_IMG_TEST_FILEPATH, 0o755, True)

    def total(self):
        if self.__total is not None:
            return self.__total
        logger = _get_framework_logger()
        params = {'dsId': self.ds_id, 'yTenantId': config.TENANT_ID}
        response = iuap_request.get(self.get_row_address, params=params)
        if 200 != response.status:
            msg = "获取行数失败，url: {}, response: {}".format(
                self.get_row_address, response)
            raise DataSourceReaderException(msg)

        row_data = response.json
        self.__total = row_data['data']

        if not isinstance(self.__total, int):
            msg = "获取行数返回结果错误, response: {}, request_url: {}".format(
                row_data, self.get_row_address)
            raise DataSourceReaderException(msg)
        return self.__total

    def reader(self, page_size=10000, offset=0, limit=0, transform_function=None, dataset_type='train_set'):
        return self.__Reader(self.input_address, self.ds_id, self.ds_type, self.total(), dataset_type, page_size, offset, limit, transform_function)

    def download_images(self, images, transform_function=None, dataset_type='train_set'):
        r = self.reader(page_size=1, offset=0, limit=0,
                        transform_function=transform_function, dataset_type=dataset_type)
        r.set_download(images)
        return r()

    class __Reader:
        def __init__(self, input_address, ds_id, ds_type, total, process_type, page_size=100, offset=0, limit=0, transform_function=None):
            """
            eg. 91 elements, page_size = 20, 5 pages as below:
            [0,19][20,39][40,59][60,79][80,90]
            offset 15, limit 30:
            [15,19][20,39][40,44]
            offset 10 limit 5:
            [10,14]
            """
            logger = _get_framework_logger()
            if offset > total:
                msg = "偏移量大于总条数:偏移 {}, 总条数: {}".format(offset, total)
                raise DataSourceReaderException(msg)
            self.input_address = input_address
            self.ds_id = ds_id
            self.ds_type = ds_type
            self.limit = limit
            self.offset = offset
            self.total = total
            if limit <= 0:
                self.limit = total - offset
            elif offset + limit > total:
                self.limit = total - offset
            self.page_size = page_size
            self.total_page = math.ceil(total / self.page_size)
            self.start_page = math.floor(offset / self.page_size)
            self.end_page = math.ceil((offset + self.limit) / page_size) - 1
            self.start_index_in_start_page = offset - self.start_page * page_size
            self.end_index_in_end_page = offset + self.limit - 1 - self.end_page * page_size
            self.current_page = self.start_page
            self.total_read = 0
            self.process_type = process_type
            self.transform_function = transform_function
            """
            print("total_page={},start_page={},end_page={},start_index={},end_index={},current_page={}"
                  .format(self.total_page,
                          self.start_page,
                          self.end_page,
                          self.start_index_in_start_page,
                          self.end_index_in_end_page,
                          self.current_page))
            """

        def get_data_bar(self):
            """数据拉取进度条"""
            if self.current_page % 5 == 1:
                try:
                    proportion = round((self.total_read/self.total)*100, 2)
                    logger.info(
                        f"数据获取中: 共{self.total}条数据, 已获取{self.total_read}条, 进度{proportion}%")
                except:
                    pass

        @property
        def iterable(self):
            return True

        def __iter__(self):
            return self

        def __next__(self):
            logger = _get_framework_logger()
            if self.current_page > self.end_page:
                logger.info('共读取原始数据 {} 条'.format(self.total_read))
                raise StopIteration

            self.get_data_bar()

            try:
                page = self._read_page(self.current_page, self.page_size)
                if self.current_page == self.start_page or self.current_page == self.end_page:
                    # 首尾页需截取有效内容
                    start_index = 0
                    end_index = len(page['data']['content']) - 1
                    if self.current_page == self.start_page:
                        start_index = self.start_index_in_start_page
                    if self.current_page == self.end_page:
                        end_index = self.end_index_in_end_page
                    page['data']['content'] = page['data']['content'][start_index: end_index + 1]

                data = page['data']['content']
                self.current_page += 1
                self.total_read += len(data)
                return data
            except Exception as e:
                logger.exception(
                    "图片数据源读取失败, input_address: [{}]".format(self.ds_id))
                raise DataSourceReaderException(f'智能分析数据源读取失败:{e}') from e

        def _read_page(self, page_index, page_size):
            """
            图片数据接口，分页读取数据
            :param page_index: 页码，从 0 开始
            :param page_size:  每页大小
            :return:
            """
            request_data = {'dsId': self.ds_id, 'pageNumber': page_index,
                            'pageSize': page_size, 'yTenantId': config.TENANT_ID,
                            'type': self.ds_type}
            response = iuap_request.get(
                url=self.input_address, params=request_data)
            response.raise_for_status()
            return response.json

        def set_download(self, page):
            logger = _get_framework_logger()
            if self.ds_type == CocoProcess.coco_type:
                CocoProcess.reset_config()
                if CocoProcess.coco_config is None:
                    annotation_urls = page[0]['annotationUrl']
                    annotation = save_file(
                        annotation_urls, timeout=90, is_img=False)
                    if annotation is None:
                        raise DataSourceReaderException(
                            f'图片数据级标注信息有误，标注文件地址：{annotation_urls}')
                    annotation = json.loads(annotation)
                    CocoProcess.set_coco_info(annotation)

            err_count, success_count, err_msg = 0, 0, ""
            with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
                futures = [executor.submit(self.__download, p) for p in page]
                for f in as_completed(futures):
                    try:
                        filename = f.result()
                        success_count += 1
                        if success_count % 10 == 0:
                            logger.info(f"dataset downloading: {success_count}/{self.total}")
                    except Exception as e:
                        err_count += 1
                        err_msg = e
                        logger.error(
                            f'dataset download error: {e}, total {err_count}')

            if err_count > 5 and success_count / err_count < 1000:
                raise DataSourceDownloadException(
                    f"下载失败的图片过多,  successed: {success_count},  failed: {err_count}, msg: {err_msg}")

            if self.ds_type == CocoProcess.coco_type:
                filename = self.process_type + ".json"
                CocoProcess.flush(os.path.join(
                    '.', config.CV_IMG_ANNOTATION_FILEPATH, filename))

            logger.info(
                f"数据集 {self.process_type} 下载完成， 成功{success_count}, 失败{err_count}")

        def __download(self, page):
            url = page['url']
            annotation_url = page['annotationUrl']
            filename = page['rowFileName']
            annotationname = filename.replace(
                page['fileNameType'], page['annotationType'])

            # 图片下载， 图片可能伴随特征工程
            if self.process_type == 'train_set':
                process_file = config.CV_IMG_TRAIN_FILEPATH
            elif self.process_type == 'validation_set':
                process_file = config.CV_IMG_VAL_FILEPATH
            else:
                process_file = config.CV_IMG_TEST_FILEPATH

            filepath = os.path.join('.', process_file, filename)
            if save_file(url, filepath, self.transform_function, timeout=90, is_img=True) is None:
                raise Exception(f"image:{filename} download error")

            # 标注下载或写入内存
            if self.ds_type == CocoProcess.coco_type:
                err = CocoProcess.gen_config(filename)
                if err is not None:
                    raise KeyError(f"CocoProcess.gen_config error: {err}")
            else:
                filepath = os.path.join(
                    '.', config.CV_IMG_ANNOTATION_FILEPATH, annotationname)
                if save_file(annotation_url, filepath, is_img=False) is None:
                    raise Exception(
                        f"annotation:{annotationname} download error")

            return filename

        def __call__(self):
            abspath = os.path.abspath('.')
            return {'path': os.path.join(abspath, config.CV_IMG_FILEPATH),
                    'train_set': os.path.join(abspath, config.CV_IMG_TRAIN_FILEPATH),
                    'val_set': os.path.join(abspath, config.CV_IMG_VAL_FILEPATH),
                    'test_set': os.path.join(abspath, config.CV_IMG_TEST_FILEPATH),
                    'annotations': os.path.join(abspath, config.CV_IMG_ANNOTATION_FILEPATH)}


def save_file(url, filepath=None, transform_function=None, timeout=None, is_img=True):
    logger = _get_framework_logger()
    try:
        # 创建未验证的上下文
        context = ssl._create_unverified_context()
        request = requests.Request(url=url, method='GET')
        response = requests.urlopen(request, timeout=timeout, context=context)
        status = response.status
        if status == 200:
            if is_img:
                data = response.read()
                if transform_function:
                    data = transform_function(data)
                if filepath:
                    with open(filepath, 'wb') as fp:
                        fp.write(data)
                    return filepath
            else:
                data = response.read().decode('UTF-8')
                if filepath:
                    with open(filepath, 'w', encoding="utf8") as fp:
                        fp.write(data)
                    return filepath
            return data
        else:
            logger.error(
                "http get url {} failed, status is {}".format(url, status))
            return None
    except urllib.error.HTTPError as e:
        logger.error("http get url {} failed, error is {}".format(url, e))
        return None
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            logger.error("http get url {} failed, read timeout: 90s".format(url))
        return None
