import os
import pytest

from datetime import datetime

from ats_base.common import func
from ats_base.service import mm

from ats_case.common.enum import WorkMode


def run(**kwargs):
    try:
        mode = WorkMode(kwargs.get('mode'))
        if mode == WorkMode.FORMAL:
            pt = FormalMode(kwargs)
        else:
            pt = DebugMode(kwargs)
        pt.run()
    except:
        pass


class ExecMode(object):
    def __init__(self, data: dict):
        self._data = data
        self._username = self._data.get('tester').get('username', '')
        self._sn = self.gen_sn()

    def run(self):
        pass

    def gen_sn(self):
        return self._now() + self._username.upper()

    def _now(self):
        return datetime.now().strftime('%y%m%d%H%M%S%f')

    def _save(self):
        pass

    def _build(self, work_mode: WorkMode, code: str = None):
        if code is None:
            code = 'case'

        user_dir = func.makeDir(os.environ.get('PROJECT_DIR'), 'testcase', work_mode.value.lower(), self._username)
        template_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'template', 'testcase_v1.tmp')
        script_file = os.path.join(user_dir, 'test_{}.py'.format(code))

        with open(template_file, 'r', encoding='UTF-8') as file:
            content = file.read()
            content = content.replace('{script}', code.upper())
        with open(script_file, 'w', encoding='UTF-8') as file:
            file.write(content)

        return script_file


class FormalMode(ExecMode):
    def run(self):
        self._save()

        cases = self._data.get('cases')
        meters = self._data.get('meters')

        for cid, case in cases.items():
            for i in range(len(meters)):
                # 客户端出来的参数需要缓存case, meter，context从数据库里去原始数据
                # i = 0 执行操作表台 传入参数index
                # pytest.main(
                #     ["-sv", self._build(WorkMode.FORMAL), '--sn={}'.format(self._sn), '--cid={}'.format(cid),
                #      '--rerun={}'.format(rerun)])
                pass

    def _save(self):
        mm.Dict.put('debug:log', self._sn, self._data)


class DebugMode(ExecMode):
    def __init__(self, data: dict):
        super().__init__(data)

    def run(self):
        self._save()
        pytest.main(["-sv", self._build(WorkMode.DEBUG), '--sn={}'.format(self._sn)])

    def _save(self):
        mm.Dict.put('debug:log', self._sn, self._data)
