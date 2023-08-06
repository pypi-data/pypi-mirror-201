import re
import time

from ats_base.common import func
from ats_base.log.logger import logger
from ats_base.service import app, pro, em, udm, mm

from ats_case.case.context import Context
from ats_case.common.enum import ProClazz, OperationClazz
from ats_case.common.error import APIError

"""
    常用操作命令
"""


def send(context: Context, todo: dict, types=2, retry_times: int = 3):
    """
    发送操作命令 - 向测试端app
    :param context:         上下文
    :param todo:            任务
    :param types:
    :param retry_times:     失败重试次数（默认：3次）
    :return:
    """
    result = None

    try:
        data = {
            'type': types,
            'exec_time': func.sys_current_time(),
            'test_sn': context.test_sn,
            'case_id': context.case.id,
            'meter_pos': context.meter.pos,
            'step_id': context.runtime.step,
            'todo': todo
        }

        logger.info('~ @TCC-SEND-> client:{} data:{}'.format(context.tester.api, data))
        result = app.send(context.tester.api, data)
        logger.info('~ @TCC-SEND<- result:{}'.format(result))
    # except requests.exceptions.MissingSchema as me:
    #     logger.error(str(me))
    #     raise AssertionError(str(me))
    except Exception as ae:
        logger.error(str(ae))

        retry_times -= 1
        if retry_times <= 0:
            raise APIError(context.tester.api)
        else:
            sleep(5)
            send(context, todo, types, retry_times)

    return result


def sleep(seconds: float):
    """
    休眠
    :param seconds:     秒
    :return:
    """
    logger.info('~ @TCC-SLEEP-> {}secs'.format(seconds))
    time.sleep(seconds)


def offbench(context: Context, disabled=1):
    """
    脱表台
    :param context:
    :param disabled:     秒
    :return:
    """
    clazz = OperationClazz(context.case.steps[str(context.runtime.step)].get('type'))

    if disabled == 1:
        if clazz == OperationClazz.BENCH:
            return True

    return False


def cache(context: Context, data):
    """
    缓存
    :param context:
    :param data:
    :return:
    """
    pass


"""
    内部方法
"""


def _replace(context: Context, data: dict):
    sd = str(data)
    sd = sd.replace('$', '"')

    re_list = re.findall(r"#(.+?)\'", sd)
    for r in re_list:
        v = eval(r)
        if type(v) is str:
            sd = sd.replace('#{}'.format(r), v)
        else:
            sd = sd.replace('\'#{}\''.format(r), str(v))

    re_list = re.findall(r"&(.+?)\'", sd)
    for r in re_list:
        sd = sd.replace(r, '{}:{}:{}:{}'.format(context.test_sn, context.case.id, context.meter.pos, r))

    return eval(sd)


def _replace_bench0(context: Context, data: dict):
    sd = str(data)

    re_list = re.findall(r"#(.+?)\'", sd)
    for r in re_list:
        v = eval(r)
        if type(v) is str:
            sd = sd.replace('#{}'.format(r), v)
        else:
            sd = sd.replace('\'#{}\''.format(r), str(v))

    return eval(sd)


def _replace_bench1(data: dict, v_data: dict):
    sd = str(data)

    re_list = re.findall(r"&(.+?)\'", sd)
    for r in re_list:
        v = v_data[r]
        if type(v) is str:
            sd = sd.replace('&{}'.format(r), v)
        else:
            sd = sd.replace('\'&{}\''.format(r), str(v))

    return eval(sd)


"""
    通讯协议篇
"""


def meter(protocol: str):
    return Meter(protocol)


class Meter(object):
    def __init__(self, protocol):
        self._protocol = ProClazz(protocol)
        self._comm_addr = None
        self._operation = None
        self._element = None
        self._parameter = None
        self._addition = None
        self._security = None
        self._frame = None
        self._parse = None
        self._func = None
        self._func_module = None
        self._func_parameter = {}

    def comm_addr(self, addr: str):
        self._comm_addr = addr
        return self

    def operation(self, op: str):
        self._operation = op
        return self

    def element(self, di):
        self._element = di
        return self

    def parameter(self, param=None):
        self._parameter = param
        return self

    def addition(self, addi=None):
        self._addition = addi
        return self

    def security(self, se=None):
        self._security = se
        return self

    def function(self, data):
        self._func = data.get('code')
        self._func_module = data.get('module')
        self._func_parameter = data.get('parameter', {})

        return self

    def frame(self, hexStr: str):
        self._frame = hexStr
        return self

    def encode(self, context: Context):
        logger.info(
            '~ @PRO-ENCODE-> protocol:{} comm_addr:{} operation:{} element:{}'.format(self._protocol,
                                                                                      self._comm_addr,
                                                                                      self._operation,
                                                                                      self._element))
        if type(self._parameter) is dict:
            self._parameter = _replace(context, self._parameter)

        parse = pro.encode(func.to_dict(protocol=self._protocol.name, comm_addr=self._comm_addr,
                                        operation=self._operation, element=self._element, parameter=self._parameter,
                                        addition=self._addition, security=self._security))
        logger.info('~ @PRO-ENCODE<- protocol:{} frame:{}'.format(self._protocol, parse.get('frame')))

        self._frame = parse.get('frame')
        return self._frame

    def decode(self, context: Context):
        logger.info('~ @PRO-DECODE-> protocol:{} frame:{}'.format(self._protocol, self._frame))
        data = pro.decode(func.to_dict(protocol=self._protocol.name, frame=self._frame))
        logger.info('~ @PRO-DECODE<- protocol:{} parse:{}'.format(self._protocol, data))

        self._handle_framing(context, data)

        self._parse = data.get('parse').get('link_data').get('mission').get('result')
        return self._parse

    def _handle_framing(self, context: Context, data: dict, index=0):
        try:
            next_frame = data['parse']['next_frame']
        except:
            next_frame = None

        if next_frame is not None:
            part_frame = data['parse']['session']['part_frame']
            pfs = context.session.set('part_frame', str(index), part_frame)

            result = send(context,
                          todo={
                              'meter:comm': {'channel': {'type': 'RS485', 'baudrate': 9600}, 'frame': next_frame}})
            self._frame = result.get('result')
            data = pro.decode(func.to_dict(protocol=self._protocol.name, frame=self._frame))

            self.handle_framing(context, data, index + 1)

    def _flush(self, context: Context):
        context.runtime.steps.update({context.runtime.step: func.to_dict(obj='meter', op=self._operation
                                                                         , element=self._element
                                                                         , parameter=self._parameter,
                                                                         result=self._parse)})

    def acv(self, context: Context):
        result = str(self._parse)
        if self._func is not None:
            if type(self._func_parameter) is not dict:
                self._func_parameter = {}
            self._func_parameter['result'] = self._parse
            self._func_parameter = _replace(context, self._func_parameter)
            try:
                self._func_parameter['expect_result'] = context.runtime.steps[context.runtime.step - 1]
            except:
                pass

            logger.info('~ @ACD-> module:{} function:{} parameter:{}'.format(
                self._func_module, self._func, self._func_parameter))
            result = udm.acv(module='meter.{}'.format(self._func_module), function=self._func
                             , data=self._func_parameter, url=context.acd_url)
            logger.info('~ @ACD<- module:{} function:{} result:{}'.format(self._func_module, self._func, result))

        return result

    def exec(self, context: Context):
        self.encode(context)
        result = send(context,
                      todo={'meter:comm': {'channel': {'type': 'RS485', 'baudrate': 9600}, 'frame': self._frame}})
        self._frame = result.get('result')
        self.decode(context)

        self._flush(context)

        send(context, todo={'app:show': {'msg': self.acv(context)}})


"""
    加密机篇
"""


def encrypt(protocol: str):
    return Encryptor(protocol)


class Encryptor(object):
    def __init__(self, protocol):
        self._protocol = ProClazz(protocol)
        self._operation = None
        self._parameter = None
        self._func_parameter = {}
        self._result = None

    def operation(self, op: str):
        self._operation = op
        return self

    def parameter(self, param=None):
        self._parameter = param
        return self

    def handle(self, context: Context):
        try:
            if self._parameter is None:
                self._parameter = {}
            self._parameter = context.runtime.steps[context.runtime.step - 1]['result']
            self._parameter['basename'] = context.session.basename
        except:
            pass

        logger.info(
            '~ @EM-> protocol:{} operation:{} parameter:{}'.format(self._protocol, self._operation, self._parameter))
        self._result = em.handle(self._protocol.name, self._operation, self._parameter)
        logger.info('~ @EM<- protocol:{} operation:{} result:{}'.format(self._protocol, self._operation, self._result))
        self._flush(context)

    def _flush(self, context: Context):
        context.runtime.steps.update({context.runtime.step: func.to_dict(obj='em', op=self._operation
                                                                         , parameter=self._parameter,
                                                                         result=self._result)})

    def acv(self, context: Context):
        # self._func_parameter['basename'] = context.session.basename
        # self._func_parameter['parameter'] = self._parameter
        self._func_parameter['result'] = self._result

        logger.info('~ @ACD-> module:{} function:{} parameter:{}'.format(
            self._protocol.name, self._operation, self._parameter))
        result = udm.acv(module='em.{}'.format(self._protocol.name), function=self._operation
                         , data=self._func_parameter, url=context.acd_url)
        logger.info('~ @ACD<- module:{} function:{} result:{}'.format(self._protocol.name, self._operation, result))

        return result

    def exec(self, context: Context):
        self.handle(context)
        send(context, todo={'app:show': {'msg': self.acv(context)}})


"""
    表台篇
"""


def bench(manufacture: str):
    return Bench(manufacture)


class Bench(object):
    def __init__(self, manufacture):
        self._manufacture = manufacture
        self._operation = None
        self._parameter = None
        self._function = None
        self._interval = None
        self._result = None
        self._exec_times = 0
        self._sleep = 0

    def operation(self, command: str):
        self._operation = command
        return self

    def parameter(self, param=None):
        self._parameter = param
        return self

    def function(self, f=None):
        self._function = f
        return self

    def sleep(self, sec=0):
        self._sleep = sec
        return self

    def interval(self, times=0):
        self._interval = times
        return self

    def encode(self, context: Context):
        logger.info(
            '~ @BENCH-> manufacture:{} operation:{} parameter:{}'.format(self._manufacture, self._operation,
                                                                         self._parameter))

        if type(self._parameter) is dict:
            self._parameter = _replace_bench0(context, self._parameter)
        if self._function is not None and len(self._function) > 0:
            self._built_in(context)

    def decode(self, context: Context):
        logger.info('~ @BENCH<- manufacture:{} operation:{} result:{}'.format(self._manufacture,
                                                                              self._operation, self._result))

        self._result = {'result': self._result.get('result')}
        self._flush(context)

    def _built_in(self, context: Context):
        logger.info('~ @BUILTIN-> module:{} parameter:{}'.format('bench', self._parameter))
        for op, d in self._function.items():
            v_data = udm.built_in(module='bench', function=op, data=func.to_dict(
                param=d, iabc=context.meter.iabc, voltage=context.meter.rated_voltage,
                current=context.meter.rated_current, index=self._exec_times), url=context.acd_url)
            self._parameter = _replace_bench1(self._parameter, v_data)

        logger.info('~ @BUILTIN<- module:{} parameter:{}'.format('bench', self._parameter))

    def acv(self, context: Context):
        logger.info('~ @ACD-> module:{} function:{} parameter:{}'.format(
            'bench', self._operation, self._result))
        result = udm.acv(module='bench.{}'.format(self._manufacture), function=self._operation
                         , data=self._result, url=context.acd_url)
        logger.info('~ @ACD<- module:{} function:{} result:{}'.format('bench', self._operation, result))

        return result

    def _flush(self, context: Context):
        context.runtime.steps.update({context.runtime.step: func.to_dict(obj='bench', op=self._operation
                                                                         , parameter=self._parameter,
                                                                         result=self._result)})

    def rest(self, context: Context):
        if self._sleep > 0:
            send(context, todo={'app:show': {'msg': '系统休眠{}秒, 等待表台调整完毕...'.format(self._sleep)}})
            sleep(self._sleep)

    def _times(self, context: Context):
        if self._interval > 0:
            if context.runtime.loop_index == 0 or (context.runtime.loop_index + 1) % self._interval != 0:
                return

        self._exec_times += 1

    def exec(self, context: Context):
        self._times(context)

        self.encode(context)
        self._result = send(context, todo={'bench:{}'.format(self._operation): self._parameter})
        self.decode(context)

        send(context, todo={'app:show': {'msg': self.acv(context)}})

        self.rest(context)


"""
    测试终端篇
"""


def client():
    return App()


class App(object):
    def __init__(self):
        self._name = 'app'
        self._operation = None
        self._message = None
        self._parameter = None
        self._command = None

    def operation(self, command: str):
        self._operation = command
        return self

    def message(self, msg: str):
        self._message = msg
        return self

    def parameter(self, param=None):
        self._parameter = param
        return self

    def encode(self):
        logger.info('~ @APP-> operation:{} message:{}'.format(self._operation, self._message))
        self._command = {'{}:{}'.format(self._name, self._operation): self._message}

        return self._command

    def decode(self):
        pass

    def exec(self, context: Context):
        self.encode()
        send(context, todo=self._command)


"""
    平台篇
"""


def ats():
    return ATS()


class ATS(object):
    def __init__(self):
        self._name = 'ats'
        self._operation = None
        self._parameter = None

    def operation(self, command: str):
        self._operation = command
        return self

    def parameter(self, param=None):
        self._parameter = param
        return self

    def exec(self, context: Context):
        logger.info('~ @ATS-> operation:{} parameter:{}'.format(self._operation, self._parameter))
        return eval('{}(context, {})'.format(self._operation, self._parameter))


