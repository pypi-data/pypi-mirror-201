import os
import sys
import inspect
import json
from typing import Tuple


class FrameworkMode:
    Import = "import"
    Train = "train"
    Infer = "infer"
    Batch = "batch"
    DistTrain = "distributedtrain"
    Analysis = "analysis"


FLAME_PROF_MODE = False
FRAMEWORK_MODE = ''  # import/train/infer/batch

# 运行模式 SCAFFOLDING 脚手架，SERVER 服务端
RUNNING_MODE = 'SERVER'
DOMIAN_IUAP_AIP_CONSOLE = ''    # 接口环境
REGISTER_CLUSTER_ADDRESS = ''   # 服务的ip➕端口  json: ['','']

# basic
TENANT_ID = ''
# 实例 id，代表当前运行实例
INSTANCE_ID = ''
# 推理任务 id
INFER_ID = ''
# 任务 id，推理任务时与 INFER_ID 相同
SERVICE_ID = ''
# 是否专属化
IS_SPECIALIZATION = 0

# 数据集相关
DATASET_BY_ID_ADDRESS = ""  # 通过url可以获取数据集所需的所有环境信息
SOURCE_TYPE = 0  # 0/6/7/8  # 0-空数据  6-表格数据 7-图像数据 8-文本数据
DATASET_INFO = ''
# cv: 0-自有 1-labelme 2-voc 3-coco  nlp: 20-txt 21-csv 22-json
INPUT_DATA_SOURCE_TRAIN_TYPE = 22
""" 数据集信息, json list
空 0:
表格 6:
    远程csv  1
    智能分析  2
    本地csv  3
    数据工场  5
图像 7:
    图片数据源 4
文本 8:
    nlp语料 21

CSV_PATH = ''
DATA_SOURCE_ADDRESS = ''
INPUT_ADDR = ''
INPUT_GETROW_ADDR = ''
INPUT_MODEL_ID = ''
INPUT_DATA_SOURCE_ID = ''
INPUT_DATA_SOURCE_TRAIN_TYPE = 2 cv: 0-自有 1-labelme 2-voc 3-coco  nlp: 20-txt 21-csv 22-json
"""

# 数据输出 输出数据源类型，0 空，2 智能分析, 5 数据工场
OUTPUT_DATASET_INFO = '{"sourceType":0}'

# 数据读取
DATA_SOURCE_READ_SIZE = 10000
DATA_SOURCE_READ_LIMIT = sys.maxsize
TRAIN_DATASET_RATIO = 0.8   # 训练集比例
VALID_DATASET_RATIO = 0.2   # 验证集比例
TEST_DATASET_RATIO = 0.0    # 测试集比例
DATA_SPLIT_MODE = 1         # 数据集划分模式, -1 不分割, 0 顺序划分，1 全局随机划分，2 根据目标列随机划分


# cv数据存储文件名
CV_IMG_FILEPATH = "tmp_local_cv_image_data/"
CV_IMG_TRAIN_FILEPATH = os.path.join(CV_IMG_FILEPATH, "train/")
CV_IMG_VAL_FILEPATH = os.path.join(CV_IMG_FILEPATH, "val/")
CV_IMG_TEST_FILEPATH = os.path.join(CV_IMG_FILEPATH, "test/")
CV_IMG_ANNOTATION_FILEPATH = os.path.join(CV_IMG_FILEPATH, "annotations/")


# nlp语料存储文件名
# nlp数据格式，接口获取数据为：文件、行 或 为 本地数据（file/row/local）
NLP_CORPORA_INPUT_TYPE = 'local'
NLP_CORPORA_FILEPATH = "tmp_local_nlp_corpora_data/"
NLP_CORPORA_TRAIN_FILEPATH = os.path.join(NLP_CORPORA_FILEPATH, "train/")
NLP_CORPORA_VAL_FILEPATH = os.path.join(NLP_CORPORA_FILEPATH, "val/")
NLP_CORPORA_TEST_FILEPATH = os.path.join(NLP_CORPORA_FILEPATH, "test/")


# 推理服务
TOKEN = ''             # API 响应 token
API_EXTRAINFO = True   # API 响应包含 extra info
PERODIC_INTERVAL = -1  # Infer上报间隔，单位秒，-1 永不上报

# 云存储相关
STORAGE_SERVICE_PATH = ''
STORAGE_SERVICE_URL = ''
FILE_UP_TYPE = ""   # 对应的类型 AliOss/Minio

# AuthSDK
ACCESS_KEY = ''
ACCESS_SECRET = ''

# eureka
START_EUREKA = False
EUREKA_ZONE = 'test'      # online/pre/test/daily
EUREKA_SERVER = ''        # eureka服务地址
EUREKA_APP_NAME = ''      # 注册服务名称
EUREKA_PROVIDER_ID = ''   # 注册服务租户

# multiprocessing
USEMULTIPROCESS = False

# 分布式
DIST_IS_MASTER = False

# Spark
SPARK_MODE = False

# checkpoint
CHECKPOINT_MODE = False
CHECKPOINT_SAVE_MAX = 100


def is_server_mode():
    return 'SERVER' == RUNNING_MODE


def str2bool(str):
    return True if str.lower() == 'true' else False


def update_by_env():
    module = sys.modules[__name__]
    for k, v in module.__dict__.items():
        if k.startswith('__') or inspect.isfunction(v) or inspect.ismodule(v):
            continue
        env_val = os.environ.get(k)
        if env_val is None:
            env_val = os.environ.get(k.upper())

        if env_val is not None:
            if env_val != '':
                if isinstance(getattr(module, k), bool):
                    setattr(module, k, str2bool(env_val))
                else:
                    setattr(module, k, type(getattr(module, k))(env_val))
            elif env_val == '' and isinstance(getattr(module, k), str):
                setattr(module, k, env_val)


def set_dataset_config(dataset_id: str = None, dataset_ratio: list = [0.7, 0.3, 0], local_csv: Tuple[str, list] = None, local_corpus: str = None):
    """通过ai工作坊接口设置数据集所需的环境变量

    Args:
        dataset_id (str): 数据集id, 从ai工作坊页面上获取

    所需环境变量:
        SOURCE_TYPE = 3
        INPUT_MODEL_ID = ''
        INPUT_DATA_SOURCE_ID = ''
        INPUT_DATA_SOURCE_TRAIN_TYPE = 2
        DATA_SOURCE_ADDRESS = ''

        if SOURCE_TYPE = 1
            NEED: DATA_SOURCE_ADDRESS
        if SOURCE_TYPE = 2
            NEED: INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_MODEL_ID
        if SOURCE_TYPE = 4
            NEED: INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_DATA_SOURCE_ID, INPUT_DATA_SOURCE_TRAIN_TYPE
        if SOURCE_TYPE = 5
            NEED: INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_DATA_SOURCE_ID
        if SOURCE_TYPE = 21
            NEED: INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_DATA_SOURCE_ID, INPUT_DATA_SOURCE_TRAIN_TYPE, NLP_CORPORA_INPUT_TYPE
    """
    module = sys.modules[__name__]

    if not local_csv and not local_corpus and not dataset_id:
        setattr(module, "SOURCE_TYPE", 0)
        return

    if dataset_id is not None:
        update_by_env()

    _csv_file_check = False
    _nlp_corpus_check = False
    if isinstance(local_csv, list):
        for c in local_csv:
            if c and not os.path.exists(c):
                break
        else:
            _csv_file_check = True
    elif isinstance(local_csv, str):
        _csv_file_check = local_csv and os.path.exists(local_csv)

    if local_corpus:
        _nlp_corpus_check = os.path.exists(local_corpus)

    if not dataset_id and not _csv_file_check and not _nlp_corpus_check:
        raise Exception(
            "数据集错误,请通过--csv设置本地csv文件 或 -C设置本地nlp语料文件夹, 或者--dataset设置在线数据集")

    setattr(module, "TRAIN_DATASET_RATIO", dataset_ratio[0])
    setattr(module, "VALID_DATASET_RATIO", dataset_ratio[1])
    setattr(module, "TEST_DATASET_RATIO", dataset_ratio[2])

    dataset_list = []
    if not dataset_id:
        if local_csv:
            setattr(module, "SOURCE_TYPE", 6)
            if isinstance(local_csv, str):
                dataset_list = [{"SOURCE_TYPE": 3, "CSV_PATH": local_csv}]
            elif isinstance(local_csv, list):
                dataset_list = [{"SOURCE_TYPE": 3, "CSV_PATH": c}
                                for c in local_csv]
        elif local_corpus:
            setattr(module, "SOURCE_TYPE", 8)
            dataset_info = {"SOURCE_TYPE": 21}
            dataset_info["NLP_CORPORA_PATH"] = local_corpus
            dataset_info["INPUT_DATA_SOURCE_TRAIN_TYPE"] = INPUT_DATA_SOURCE_TRAIN_TYPE
            dataset_list.append(dataset_info)
    else:
        from intelliw.utils import iuap_request
        DATASET_URL = os.environ.get('DATASET_BY_ID_ADDRESS')
        for i in dataset_id.split(","):
            dataset_info = {}
            resp = iuap_request.get(DATASET_URL, params={"dataSetId": dataset_id})
            resp.raise_for_status()
            body = resp.json
            if body['status'] == 0:
                raise Exception(f"get dataset info response: {body}")
            result = body['data']
            source = result["SOURCE_TYPE"]
            if result.get("TENANT_ID"):
                setattr(module, "TENANT_ID", result.get("TENANT_ID"))
            if source == 1:
                setattr(module, "SOURCE_TYPE", 6)
                dataset_info["DATA_SOURCE_ADDRESS"] = result["DATA_SOURCE_ADDRESS"]
            else:
                dataset_info["INPUT_ADDR"] = result["INPUT_ADDR"]
                dataset_info["INPUT_GETROW_ADDR"] = result["INPUT_GETROW_ADDR"]
                if source == 2:
                    setattr(module, "SOURCE_TYPE", 6)
                    mid = result["INPUT_MODEL_ID"]
                    dataset_info["INPUT_GETROW_ADDR"] = result["INPUT_GETROW_ADDR"]
                    dataset_info["INPUT_MODEL_ID"] = mid
                elif source == 4:
                    setattr(module, "SOURCE_TYPE", 7)
                    dataset_info["INPUT_DATA_SOURCE_ID"] = result["INPUT_DATA_SOURCE_ID"]
                elif source == 5:
                    setattr(module, "SOURCE_TYPE", 6)
                    dataset_info["INPUT_DATA_SOURCE_ID"] = result["INPUT_DATA_SOURCE_ID"]
                    dataset_info["INPUT_DATA_META_ADDR"] = result["INPUT_DATA_META_ADDR"]
                elif source == 21:
                    setattr(module, "SOURCE_TYPE", 8)
                    dataset_info["INPUT_DATA_SOURCE_ID"] = result["INPUT_DATA_SOURCE_ID"]
                    dataset_info["NLP_CORPORA_INPUT_TYPE"] = result["NLP_CORPORA_INPUT_TYPE"]
            dataset_info["SOURCE_TYPE"] = source
            dataset_list.append(dataset_info)
    setattr(module, "DATASET_INFO", json.dumps(
        dataset_list, ensure_ascii=False))
