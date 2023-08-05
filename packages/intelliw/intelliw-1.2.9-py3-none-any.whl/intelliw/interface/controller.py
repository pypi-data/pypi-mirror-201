#!/usr/bin/env python
# coding: utf-8
'''
Author: hexu
Date: 2021-10-25 15:20:34
LastEditTime: 2023-03-27 14:17:42
LastEditors: Hexu
Description: 线上调用的入口文件
FilePath: /iw-algo-fx/intelliw/interface/controller.py
'''
import traceback
from intelliw.core.pipeline import Pipeline
from intelliw.config import config
from intelliw.utils.logger import _get_framework_logger
from absl.flags import argparse_flags as argparse


logger = _get_framework_logger()


class FrameworkArgs:
    def __init__(self, args=None):
        self.path = "" if args is None else args.path
        self.method = "importalg" if args is None else args.method
        self.name = "predict" if args is None else args.name
        self.format = "" if args is None else args.format
        self.task = "infer" if args is None else args.task
        self.port = 8888 if args is None else args.port
        self.response = None if args is None else args.response
        self.output = "" if args is None else args.output


def __parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-p", "--path", default="",
                        type=str, help="package path")
    parser.add_argument("-m", "--method", default="importalg",
                        type=str, help="method")
    parser.add_argument("-n", "--name", default="predict",
                        type=str, help="name")
    parser.add_argument("-o", "--output", default="", type=str, help="output")
    parser.add_argument("-f", "--format", default="",
                        type=str, help="batch format")
    parser.add_argument("-t", "--task", default="infer",
                        type=str, help="task type: infer/train")
    parser.add_argument("--port", default=8888, type=int, help="port")
    parser.add_argument("-r", "--response",
                        default=None, type=str, help="response addr, which can be used to report status")

    return parser.parse_args()


def main(args):
    try:
        if args.method == "importalg":
            config.FRAMEWORK_MODE = config.FrameworkMode.Import
            pl = Pipeline(args.response)
            pl.importalg(args.path, False)
        elif args.method == "importmodel":
            config.FRAMEWORK_MODE = config.FrameworkMode.Import
            pl = Pipeline(args.response)
            pl.importmodel(args.path, False)
        elif args.method == "train":
            from intelliw.interface.trainjob import TrainServer
            config.FRAMEWORK_MODE = config.FRAMEWORK_MODE or config.FrameworkMode.Train
            train = TrainServer(args.path, config.DATASET_INFO, args.response)
            train.run()
        elif args.method == "apiservice":
            from intelliw.interface.apijob import ApiService
            config.FRAMEWORK_MODE = config.FrameworkMode.Infer
            apiservice = ApiService(args.port, args.path, args.response)
            apiservice.run()
        elif args.method == "batchservice":
            from intelliw.interface.batchjob import BatchService
            config.FRAMEWORK_MODE = config.FrameworkMode.Batch
            batchservice = BatchService(
                args.format, args.path, config.DATASET_INFO, config.OUTPUT_DATASET_INFO, args.response, args.task)
            batchservice.run()
        elif args.method == "validateservice":
            from intelliw.interface.validatejob import ValidateService
            validateservice = ValidateService(
                args.name, args.port, args.path, args.response)
            validateservice.run()
        exit(0)
    except Exception as e:
        stack_info = traceback.format_exc()
        logger.error("fail to execute and stack:\n{}".format(str(stack_info)))
        exit(1)


def run():
    framework_args = FrameworkArgs(__parse_args())
    config.update_by_env()
    main(framework_args)


if __name__ == '__main__':
    framework_args = FrameworkArgs(__parse_args())
    config.update_by_env()
    main(framework_args)
