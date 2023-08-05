#!/usr/bin/env python
# coding: utf-8

import os
import json
import time
import datetime
import threading
import numpy as np
from intelliw.utils import message
from intelliw.config import config
from intelliw.core.infer import Infer
from intelliw.utils.logger import _get_framework_logger
from intelliw.interface import apihandler
from intelliw.utils.util import get_json_encoder

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder


class FlaskJSONEncoder(_JSONEncoder):
    """重载flask的json encoder, 确保jsonfy()能解析numpy的json"""

    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (datetime.datetime, datetime.timedelta)):
            return obj.__str__()
        else:
            return super(FlaskJSONEncoder, self).default(obj)


class Flask(_Flask):
    """重载flask的jsonencoder, 确保能解析numpy的json"""
    json_encoder = FlaskJSONEncoder


logger = _get_framework_logger()


class Application():
    """推理服务路由类
    example:
        @Application.route("/infer-api", method='get', need_feature=True)
        def infer(self, test_data):
            pass
    args:
        path           访问路由   /infer-api
        method         访问方式，支持 get post push delete head patch options
        need_feature   是否需要使用特征工程, 如果是自定义与推理无关的函数, 请设置False
    """

    # Set URL handlers
    HANDLERS = []

    def __init__(self, custom_router):
        self.app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"),
                         static_folder=os.path.join(os.path.dirname(__file__), "static"))
        self.__handler_process(custom_router)

    def __call__(self):
        return self.app

    @classmethod
    def route(cls, path, **options):
        def decorator(f):
            func = f.__name__
            cls.HANDLERS.append((path, apihandler.MainHandler, {'func': func, 'method': options.pop(
                'method', 'post'), 'need_feature': options.pop('need_feature', True)}))
            return f
        return decorator

    def __handler_process(self, router):
        # 加载自定义api, 配置在algorithm.yaml中
        for r in router:
            path, func, method, need_feature = r["path"], r["func"], r.get(
                "method", "post").lower(), r.get("need_feature", True)
            Application.HANDLERS.append((path, apihandler.MainHandler, {
                'func': func, 'method': method, 'need_feature': need_feature}))

        # 检查用户是否完全没有配置路由
        if len(Application.HANDLERS) == 0:
            Application.HANDLERS.append((r'/predict', apihandler.MainHandler,
                                         {'func': 'infer', 'method': 'post', 'need_feature': True}))  # 默认值

        # 集中绑定路由
        _route_cache = dict()
        for r, _, info in Application.HANDLERS:
            f, m, nf = info.get('func'), info.pop(
                'method'), info.get('need_feature')
            if _route_cache.get(r+f, None):
                continue
            _route_cache[r+f] = True
            self.app.add_url_rule(r, view_func=apihandler.MainHandler.as_view(
                r), methods=[m], defaults=info)
            logger.info(f"方法: {f} 加载成功, 访问路径：{r}, 访问方法:{m}, 是否需要特征处理:{nf}")

        # healthcheck
        # gateway
        self.app.add_url_rule(
            '/healthcheck', view_func=apihandler.HealthCheckHandler.as_view("healthcheck"))
        # eureka
        self.app.add_url_rule(
            '/CloudRemoteCall/', view_func=apihandler.EurekaHealthCheckHandler.as_view("eurekahealthcheck"))


class ApiService:
    def __init__(self, port, path, response_addr):
        self.port = port        # 8888
        self.PERODIC_INTERVAL = config.PERODIC_INTERVAL if config.PERODIC_INTERVAL == 0 else 10
        infer = Infer(path, response_addr, self.PERODIC_INTERVAL)
        self.reporter = infer.pipeline.recorder
        self.custom_router = infer.pipeline.custom_router
        self.app = Application(self.custom_router)()
        self.app.config.update({"infer": infer, "reporter": self.reporter})

        self._report_start()

    def _report_start(self):
        msg = [{'status': 'start', 'inferid': config.INFER_ID,
                'instanceid': config.INSTANCE_ID, 'inferTaskStatus': []}]
        self.reporter.report(
            message.CommonResponse(200, "inferstatus", '', json.dumps(msg, cls=get_json_encoder(), ensure_ascii=False)))

    def _eureka_server(self):
        if len(config.EUREKA_SERVER) > 0:
            from intelliw.core.linkserver import linkserver
            try:
                should_register = config.EUREKA_APP_NAME != ''
                iports = json.loads(config.REGISTER_CLUSTER_ADDRESS)
                profile = config.EUREKA_ZONE or 'test'
                linkserver.client(
                    config.EUREKA_SERVER, config.EUREKA_PROVIDER_ID,
                    should_register, config.EUREKA_APP_NAME, iports, profile)
                logger.info(
                    f"eureka server client init success, register:{should_register}, server name: {config.EUREKA_APP_NAME}")
            except Exception as e:
                logger.error(
                    f"eureka server client init failed, error massage: {e}")

    def _flask_server(self):
        if self.PERODIC_INTERVAL > 0:
            timer = threading.Timer(
                self.PERODIC_INTERVAL, self.perodic_callback)
            timer.daemon = True
            timer.start()
        try:
            from gevent.pywsgi import WSGIServer
            if config.USEMULTIPROCESS:
                # 多进程
                from multiprocessing import cpu_count, Process
                server = WSGIServer(('0.0.0.0', self.port), self.app)
                server.start()

                def serve_forever():
                    server.start_accepting()
                    server._stop_event.wait()

                for _ in range(cpu_count()):
                    p = Process(target=serve_forever)
                    p.start()
                    logger.info(f"multiprocessing server start, pid: {p.pid}")
            else:
                # 携程io
                WSGIServer(('0.0.0.0', self.port), self.app).serve_forever()
        except ImportError:
            logger.warn(
                "\033[33mIf want use a production WSGI server, you need: pip install gevent\033[0m")
            self.app.run('0.0.0.0', self.port)

    def perodic_callback(self):
        infer = self.app.config["infer"]
        while True:
            infer.perodic_callback()
            time.sleep(self.PERODIC_INTERVAL)

    def run(self):
        self._eureka_server()
        self._flask_server()
