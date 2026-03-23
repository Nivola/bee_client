# SPDX-License-Identifier: EUPL-1.2
#
# (C) Copyright 2018-2026 CSI-Piemonte

from os import listdir
from sys import path
import unittest

from beecell.simple import dynamic_import
from .platform import CmpPlatformAbstractService
from .client import CmpBaseService


class CmpPlatformTestService(CmpPlatformAbstractService):
    """Cmp business div"""

    def __init__(self, manager):
        CmpBaseService.__init__(self, manager)

    def get(self, local_package_path, package, plan):
        res = None
        if package is not None and plan is not None:
            prj = package.replace("_", "-")
            path.append(f"{local_package_path}/{prj}")
            test_run = dynamic_import(f"{package}.regression.{plan}")
            test_groups = filter(lambda x: x.find("tests_") == 0, dir(test_run))
            res = [{"package": package, "test-plan": plan, "test-group": i} for i in test_groups]

        self.logger.debug("res: %s", res)
        return res

    def run(
        self,
        local_package_path,
        package,
        plan,
        group=None,
        test=None,
        tests=None,
        config=None,
        extra_config=None,
        validate=False,
        user="test1",
        max=2,
        endpoints_forced=None,
        report_file=None,
    ) -> unittest.result.TestResult:
        if config is None:
            config = f"{local_package_path}/beehive-tests/beehive_tests/configs/test/beehive.yml"

        args = {
            "conf": config,
            "exconf": extra_config,
            "validate": validate,
            "user": user,
            "max": int(max),
            "endpointsForced": endpoints_forced,
            "stream": "custom",
            "report_file": report_file,
            "skip_log_config": True,
        }

        prj = package.replace("_", "-")
        test_file = f"{local_package_path}/{prj}/{package}/regression"
        file_list = [f.replace(".py", "") for f in listdir(test_file)]
        if plan not in file_list:
            raise Exception(f"Test {plan} is not available")
        path.append(f"{local_package_path}/{prj}")
        test_run = dynamic_import(f"{package}.regression.{plan}")
        self.logger.debug("run - test_run: %s", test_run)

        if group is not None:
            if tests is not None:
                idxs = tests.split(",")
                all_tests = getattr(test_run, group)
                tests = []
                for idx in idxs:
                    tests.append(all_tests[int(idx)])
                test_run.tests = tests
            else:
                test_run.tests = getattr(test_run, group)
        elif test is not None:
            test_run.tests = [test]
        print("run tests:")
        for item in test_run.tests:
            self.logger.debug("run - item: %s", item)
            print(f"- {item}")

        self.logger.debug("run - args: %s", args)
        return test_run.run(args)
