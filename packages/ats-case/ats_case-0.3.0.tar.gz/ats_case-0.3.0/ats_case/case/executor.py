from importlib import import_module

from ats_base.log.logger import logger

from ats_case.case import translator, command
from ats_case.case.context import Context
from ats_case.common.enum import *


def execute(context: Context):
    if context.mode == WorkMode.FORMAL:
        FormalExecutor(context).exec()
    else:
        DebugExecutor(context).exec()


class Executor(object):
    def __init__(self, context: Context):
        self._context = context
        self._model = None

    def exec(self):
        pass

    def is_exec(self):
        ifs = self._context.case.control.get('ifs')
        if ifs is not None and type(ifs) is dict and len(ifs) > 0:
            for func, values in ifs.items():
                if command.ats().operation(func).parameter(values).exec(self._context):
                    return False
        return True

    def step_exec(self):
        try:
            logger.info('~ @TCC-STEP-> steps[#{}] execute'.format(self._context.runtime.step))

            if self.is_exec():
                getattr(self._model, 'step_{}'.format(self._context.runtime.step))(self._context)
        except Exception as e:
            logger.error(str(e))

    def loop_meet(self):
        try:
            loops = self._context.case.control.get('loops')

            if loops is None or type(loops) is not list or len(loops) <= 0:
                return False

            if self._context.runtime.loop_sn >= len(loops):
                return False
            loop = loops[self._context.runtime.loop_sn]
            ranges = loop.get('range')
            count = loop.get('count')

            step_start = int(ranges.split(':')[0])
            step_end = int(ranges.split(':')[1])

            if step_start <= self._context.runtime.step <= step_end:
                self._context.runtime.loop_start_step = step_start
                self._context.runtime.loop_end_step = step_end
                self._context.runtime.loop_count = int(count)
                self._context.runtime.loop_index = 0
                return True
        except Exception as e:
            logger.error(str(e))

        return False

    def loop_exec(self):
        logger.info('~ @TCC-LOOP-> loops[#{}] start. -range {}:{}  -count {}'.format(
            self._context.runtime.loop_sn, self._context.runtime.loop_start_step,
            self._context.runtime.loop_end_step, self._context.runtime.loop_count))

        command.client().operation('show').message('循环[#{}]开始, 步骤范围[{}-{}], 共{}次'.format(
            self._context.runtime.loop_sn, self._context.runtime.loop_start_step,
            self._context.runtime.loop_end_step, self._context.runtime.loop_count)).exec(self._context)

        # while self._context.runtime.loop_index < self._context.runtime.loop_count:
        for i in range(1, self._context.runtime.loop_count + 1):
            self._context.runtime.loop_index = i

            logger.info('~ @TCC-LOOP-> loops[#{}], -count {}, -index {}'.format(
                self._context.runtime.loop_sn, self._context.runtime.loop_count,
                self._context.runtime.loop_index))
            command.client().operation('show').message('循环[#{}], 共{}次, 当前第{}次'.format(
                self._context.runtime.loop_sn, self._context.runtime.loop_count,
                self._context.runtime.loop_index)).exec(self._context)

            for j in range(self._context.runtime.loop_start_step, self._context.runtime.loop_end_step + 1):
                self._context.runtime.step = j
                self.step_exec()

        command.client().operation('show').message("循环结束...").exec(self._context)
        logger.info('~ @TCC-LOOP-> loops[#{}] end.'.format(self._context.runtime.loop_sn))
        self._context.runtime.loop_sn += 1


class FormalExecutor(Executor):
    def exec(self):
        # 分为两种情况: 1. 手动编写脚本 2.自动编写脚本
        pass


class DebugExecutor(Executor):
    def exec(self):
        steps = translator.translate(self._context)
        self._model = import_module('script.debug.{}.steps'.format(self._context.tester.username.lower()))

        index = 0
        while index < len(steps):
            self._context.runtime.step = steps[index]
            if self.loop_meet():
                self.loop_exec()
            else:
                self.step_exec()

            if self._context.runtime.step > (index + 1):
                index = self._context.runtime.step
            else:
                index += 1
