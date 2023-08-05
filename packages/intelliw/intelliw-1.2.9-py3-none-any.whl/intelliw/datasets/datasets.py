'''
Author: hexu
Date: 2021-10-14 14:54:05
LastEditTime: 2023-03-30 20:20:36
LastEditors: Hexu
Description: 数据集
FilePath: /iw-algo-fx/intelliw/datasets/datasets.py
'''
import json
from typing import List, Tuple, overload
from intelliw.datasets.spliter import get_set_spliter
from intelliw.datasets.datasource_base import AbstractDataSource, DataSourceEmpty, AbstractDataSourceWriter, \
    EmptyDataSourceWriter, DataSourceType as DST, DatasetType, AlgorithmsType, DataSourceReaderException
from intelliw.utils.logger import _get_framework_logger
from intelliw.config import config
from intelliw.utils.global_val import gl

logger = _get_framework_logger()


def get_datasource(stype, **kwargs) -> AbstractDataSource:
    """获取数据集

    Args:
        stype      SOURCE_TYPE
        dsaddr     DATA_SOURCE_ADDRESS
        addr       INPUT_ADDR
        raddr      INPUT_GETROW_ADDR
        mid        INPUT_MODEL_ID
        dsid       INPUT_DATA_SOURCE_ID
        dstt       INPUT_DATA_SOURCE_TRAIN_TYPE
        nlpctypt   NLP_CORPORA_INPUT_TYPE
        tmaddr    INPUT_DATA_META_ADDR

        if SOURCE_TYPE = 1
            NEED: DATA_SOURCE_ADDRESS
        if SOURCE_TYPE = 2
            NEED: INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_MODEL_ID
        if SOURCE_TYPE = 4
            NEED: INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_DATA_SOURCE_ID, INPUT_DATA_SOURCE_TRAIN_TYPE
        if SOURCE_TYPE = 5
            NEED: INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_DATA_SOURCE_ID, INPUT_DATA_META_ADDR
        if SOURCE_TYPE = 21
            NEED: INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_DATA_SOURCE_ID, INPUT_DATA_SOURCE_TRAIN_TYPE, NLP_CORPORA_INPUT_TYPE

    Returns:
        AbstractDataSource: 数据集class
    """
    if stype == DST.EMPTY:
        return DataSourceEmpty()
    elif stype == DST.REMOTE_CSV:
        from intelliw.datasets.datasource_remote_csv import DataSourceRemoteCsv
        return DataSourceRemoteCsv(kwargs['dsaddr'])
    elif stype == DST.LOCAL_CSV:
        from intelliw.datasets.datasource_local_csv import DataSourceLocalCsv
        return DataSourceLocalCsv(kwargs['csvpath'])
    elif stype == DST.INTELLIV:
        from intelliw.datasets.datasource_intelliv import DataSourceIntelliv
        return DataSourceIntelliv(kwargs['addr'], kwargs['raddr'], kwargs['mid'])
    elif stype == DST.IW_IMAGE_DATA:
        from intelliw.datasets.datasource_iwimgdata import DataSourceIwImgData
        return DataSourceIwImgData(kwargs['addr'], kwargs['raddr'], kwargs['dsid'], kwargs['dstt'])
    elif stype == DST.IW_FACTORY_DATA:
        from intelliw.datasets.datasource_iwfactorydata import DataSourceIwFactoryData
        return DataSourceIwFactoryData(kwargs['addr'], kwargs['raddr'], kwargs['tmaddr'], kwargs['dsid'])
    elif stype == DST.NLP_CORPORA:
        from intelliw.datasets.datasource_nlp_corpora import DataSourceNLPCorpora
        return DataSourceNLPCorpora(kwargs['addr'], kwargs['dsid'], kwargs['dstt'], kwargs['nlpctypt'])
    else:
        err_msg = "数据读取失败，无效的数据源类型: {}".format(stype)
        raise ValueError(err_msg)


def get_datasource_writer(cfg: str = None) -> AbstractDataSourceWriter:
    output_datasource_type = 0
    cfg = cfg or config.OUTPUT_DATASET_INFO
    if cfg:
        if isinstance(cfg, str):
            cfg = json.loads(cfg)
        output_datasource_type = cfg['sourceType']

    if output_datasource_type == DST.EMPTY:
        return EmptyDataSourceWriter()
    elif output_datasource_type in (DST.INTELLIV, DST.IW_FACTORY_DATA):
        from intelliw.datasets.dataset_writer import DataSourceWriter
        return DataSourceWriter(output_config=cfg, writer_type=output_datasource_type)
    else:
        err_msg = f"输出数据源设置失败，无效的数据源类型: {output_datasource_type}"
        raise ValueError(err_msg)


class DataSets:
    def __init__(self, datasource: AbstractDataSource):
        self.datasource = datasource
        self.alldata = list()
        self.column_meta = list()
        self.model_type = gl.get("model_type")  # 分类/回归/ocr/时间序列/文本分类。。。。。

    def empty_reader(self, dataset_type=DatasetType.TRAIN):
        return self.datasource.reader(page_size=1, offset=0, limit=0, transform_function=None, dataset_type=dataset_type)

    def reader(self, page_size=10000, offset=0, limit=0, split_transform_function=None):
        return self.datasource.reader(page_size, offset, limit, split_transform_function)

    @overload
    def data_pipeline(self, split_transform_function,
                      alldata_transform_function, feature_process): pass

    def data_pipeline(self, *args):
        if config.SOURCE_TYPE == DST.NLP_TYPE:
            return self._nlp_data(config.DATA_SPLIT_MODE)
        elif config.SOURCE_TYPE == DST.CV_TYPE:
            return self._images_data(*self._data_pipeline(*args))
        else:
            if self.model_type == AlgorithmsType.TIME_SERIES:
                args = list(args)
                args.extend([True, True])
            train, validation, test = self._data_pipeline(*args)
            return [train], [validation], [test]

    def read_all_data(self, split_transform_function=None):
        reader = self.reader(config.DATA_SOURCE_READ_SIZE, 0,
                             self.datasource.total(), split_transform_function)
        for idx, r in enumerate(reader):
            if config.SOURCE_TYPE != DST.CV_TYPE:
                if idx == 0:
                    self.column_meta = reader.meta
                    self.alldata = r
                elif 'result' in r and 'result' in self.alldata:
                    self.alldata['result'].extend(r['result'])
            else:
                self.alldata.extend(r)
        return self.alldata

    def _data_pipeline(self, stf, atf, fp, ignore_dp=False, ignore_split=False):
        # 获取全部数据(切片数据处理， 列选择和数据筛选)
        alldata = self.read_all_data(stf)

        _data_process_args = [
            alldata, atf, fp
        ]
        _get_set_spliter_args = [
            alldata
        ]

        if ignore_dp:
            _data_process_args.append(True)
        if ignore_split:
            _get_set_spliter_args.append(True)

        # 数据处理（时间序列，全局函数和特征工程）
        alldata = self._data_process(*_data_process_args)

        # 数据集切分
        spliter = get_set_spliter(*_get_set_spliter_args)

        # 数据集处理 图片下载/语料下载/数据返回
        return spliter.train_reader(), spliter.validation_reader(), spliter.test_reader()

    def _data_process(self, alldata, atf, fp, do_nothing=False):
        if do_nothing is True:
            pass
        elif config.SOURCE_TYPE == DST.CV_TYPE:
            pass
        elif atf or fp:
            alldata = atf(alldata) if atf else alldata
            alldata = fp(alldata) if fp else alldata
        return alldata

    def _images_data(self, train, val, test):
        tr = self.datasource.download_images(
            train, dataset_type=DatasetType.TRAIN)
        v = self.datasource.download_images(
            val, dataset_type=DatasetType.VALID)
        te = self.datasource.download_images(
            test, dataset_type=DatasetType.TEST)
        return tr, v, te

    def _nlp_data(self, split_mode: int):
        self.datasource.corpora_process(split_mode)
        return [self.datasource()]*3


class MultipleDataSets:
    def __init__(self) -> None:
        self._total = 0
        self.datasets: List[DataSets] = list()
        self.join_type = "no"
        self.model_type = gl.get("model_type")  # 分类/回归/ocr/时间序列/文本分类。。。。。
        self.column_meta = list()

    @property
    def total(self):
        return self._total

    @property
    def onlyone(self):
        return self._total == 1

    def add(self, dataset: DataSets):
        self.datasets.append(dataset)
        self._total += 1

    def pop(self, idx=None):
        if idx is not None and isinstance(idx, int):
            return self.datasets.pop(idx)
        else:
            return self.datasets.pop()

    @overload
    def data_pipeline(self, split_transform_function,
                      alldata_transform_function, feature_process): pass

    def data_pipeline(self, *args):
        # train_set_list, validation_set_list, test_set_list
        trl, vl, tel = [[None]*self._total for _ in range(3)]
        args = list(args)
        args.append(True)  # TODO 多数据集暂时不支持特征工程
        if self.model_type == AlgorithmsType.TIME_SERIES:
            args.append(True)
        for idx in range(self._total):
            gl.set("dataset_idx", idx)
            dataset = self.pop(0)
            trl[idx], vl[idx], tel[idx] = dataset._data_pipeline(*args)
            self.column_meta.extend(dataset.column_meta)
        return trl, vl, tel

    def read_all_data(self, split_transform_function=None):
        all_set_data = []
        for _ in range(self._total):
            dataset = self.pop(0)
            all_set_data.append(
                dataset.read_all_data(split_transform_function))
            self.column_meta.extend(dataset.column_meta)
        # TODO join process
        return all_set_data


def get_dataset(cfg) -> Tuple[DataSets, MultipleDataSets]:
    if cfg and isinstance(cfg, str):
        dataset_conf = json.loads(cfg)
    else:
        dataset_conf = cfg
    # 空数据
    if config.SOURCE_TYPE == 0:
        datasource = get_datasource(0)
        return DataSets(datasource)
    # table, cv, nlp
    elif config.SOURCE_TYPE in [6, 7, 8]:
        mds = MultipleDataSets()
        for cfg in dataset_conf:
            stype, kwargs = _get_dataset_args(cfg)
            datasource = get_datasource(stype, **kwargs)
            mds.add(DataSets(datasource))
        if mds.onlyone:
            return mds.pop()
        return mds
    else:
        raise DataSourceReaderException(
            f"Error Source Type: {config.SOURCE_TYPE}")


_dependent_param = {
    1: "DATA_SOURCE_ADDRESS",
    2: "INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_MODEL_ID",
    4: "INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_DATA_SOURCE_ID, INPUT_DATA_SOURCE_TRAIN_TYPE",
    5: "INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_DATA_SOURCE_ID, INPUT_DATA_META_ADDR",
    21: "INPUT_ADDR, INPUT_GETROW_ADDR, INPUT_DATA_SOURCE_ID, INPUT_DATA_SOURCE_TRAIN_TYPE, NLP_CORPORA_INPUT_TYPE"
}


def _get_dataset_args(cfg: dict) -> dict:
    stype = cfg["SOURCE_TYPE"]
    kwargs = {}
    errmsg = f"Source Type: {stype}, Need Parameters: [{_dependent_param.get(stype)}]"
    try:
        if stype == DST.REMOTE_CSV:
            kwargs = {"dsaddr": cfg["DATA_SOURCE_ADDRESS"]}
        elif stype == DST.LOCAL_CSV:
            kwargs = {"csvpath": cfg["CSV_PATH"]}
        elif stype == DST.INTELLIV:
            mid = cfg["INPUT_MODEL_ID"]
            raddr = cfg["INPUT_GETROW_ADDR"]
            kwargs = {"addr": cfg["INPUT_ADDR"],
                      "raddr": f"{raddr}/{mid}/null",
                      "mid": mid}
        elif stype == DST.IW_IMAGE_DATA:
            kwargs = {"addr": cfg["INPUT_ADDR"],
                      "raddr": cfg["INPUT_GETROW_ADDR"],
                      "dsid": cfg["INPUT_DATA_SOURCE_ID"],
                      "dstt": cfg.get("INPUT_DATA_SOURCE_TRAIN_TYPE", 3)}
        elif stype == DST.IW_FACTORY_DATA:
            kwargs = {"addr": cfg["INPUT_ADDR"],
                      "raddr": cfg["INPUT_GETROW_ADDR"],
                      "dsid": cfg["INPUT_DATA_SOURCE_ID"],
                      "tmaddr": cfg["INPUT_DATA_META_ADDR"]}
        elif stype == DST.NLP_CORPORA:
            cpath = cfg.get("NLP_CORPORA_PATH", "")
            if len(cpath) > 0:
                kwargs = {"addr": cpath, "dsid": "", "nlpctypt": "local",
                          "dstt": cfg.get("INPUT_DATA_SOURCE_TRAIN_TYPE", 22)}
            else:
                kwargs = {"addr": cfg["INPUT_ADDR"],
                          "dsid": cfg["INPUT_DATA_SOURCE_ID"],
                          "dstt": cfg.get("INPUT_DATA_SOURCE_TRAIN_TYPE", 22),
                          "nlpctypt": cfg["NLP_CORPORA_INPUT_TYPE"]}
    except KeyError:
        raise DataSourceReaderException(errmsg)
    return stype, kwargs
