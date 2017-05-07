# -*- coding: utf-8 -*-

from .context import detest

import unittest


class Test1(unittest.TestCase):

    def test_testsuite_as_root(self):
        result = detest.Detest().parse("tests/test1.xml")
        self.assertEqual(len(result.test_suites), 1)
        test_suite = result.test_suites[0]
        self.assertEqual(test_suite.name, "nosetests")
        self.assertEqual(test_suite.errors, 2)
        self.assertEqual(test_suite.tests, 104)
        self.assertEqual(test_suite.skipped, 63)
        self.assertEqual(test_suite.failures, 1)


class Test2(unittest.TestCase):
    def test_no_errors_failure(self):
        result = detest.Detest().parse("tests/test2.xml")
        self.assertEqual(len(result.test_suites), 1)
        test_suite = result.test_suites[0]
        self.assertEqual(test_suite.name, "")
        self.assertEqual(test_suite.errors, 0)
        self.assertEqual(test_suite.tests, 66)
        self.assertEqual(test_suite.skipped, 0)
        self.assertEqual(test_suite.failures, 1)


class Test3(unittest.TestCase):
    def test_failure_tag(self):
        result = detest.Detest().parse("tests/test3.xml")
        self.assertEqual(len(result.test_suites), 1)
        test_suite = result.test_suites[0]
        self.assertEqual(test_suite.name, "bla")
        self.assertEqual(test_suite.errors, 0)
        self.assertEqual(test_suite.tests, 3)
        (test_case1, test_case2, test_case3) = test_suite.test_cases
        self.assertEqual(test_case1.name, "test_CheckType")
        self.assertEqual(test_case1.class_name, None)
        self.assertEqual(test_case1.failure, None)
        self.assertEqual(test_case2.name, "test_CheckOther")
        self.assertEqual(test_case2.class_name, "aaa.cc")
        self.assertIsNotNone(test_case2.failure)
        self.assertIsNone(test_case2.failure.type)
        self.assertIsNone(test_case2.failure.content)
        self.assertEqual(test_case3.name, "test_Data")
        self.assertEqual(test_case3.class_name, "aaa.bbb.ccc")
        self.assertIsNotNone(test_case3.failure)
        self.assertEqual(test_case3.failure.type, "AssertionError")


class Test4(unittest.TestCase):
    def test_testsuites_as_root(self):
        result = detest.Detest().parse("tests/test4.xml")
        self.assertEqual(len(result.test_suites), 1)
        self.assertEqual(result.time.seconds, 45)
        test_suite = result.test_suites[0]
        self.assertEqual(test_suite.name, "base_test_1")
        self.assertEqual(test_suite.errors, 1)
        self.assertEqual(test_suite.tests, 4)
        self.assertEqual(test_suite.failures, 1)


class Test5(unittest.TestCase):
    def test_timestamp(self):
        result = detest.Detest().parse("tests/test5.xml")
        self.assertEqual(len(result.test_suites), 1)
        test_suite = result.test_suites[0]
        self.assertEqual(test_suite.name, "Toplevel Test Suite")
        self.assertEqual(test_suite.errors, 1)
        self.assertEqual(test_suite.tests, 2)


class Test6(unittest.TestCase):
    def test_empty_test_cases(self):
        result = detest.Detest().parse("tests/test6.xml")
        self.assertEqual(len(result.test_suites), 1)
        test_suite = result.test_suites[0]
        self.assertEqual(test_suite.name, "com.github.review.CommentSourceTest")
        self.assertEqual(test_suite.errors, 0)
        self.assertEqual(test_suite.failures, 0)
        self.assertEqual(test_suite.time.total_seconds(), 0)
        self.assertEqual(test_suite.time.total_seconds(), 0)


class Test7(unittest.TestCase):
    def test_phantom(self):
        result = detest.Detest().parse("tests/test7.xml")
        self.assertEqual(len(result.test_suites), 1)
        test_suite = result.test_suites[0]
        self.assertEqual(test_suite.name, "PhantomJS 1.9.7 (Linux)")
        self.assertEqual(test_suite.errors, 0)
        self.assertEqual(test_suite.failures, 0)
        self.assertEqual(test_suite.tests, 269)


class Test8(unittest.TestCase):
    def test_bad_time(self):
        result = detest.Detest().parse("tests/test8.xml")
        self.assertEqual(len(result.test_suites), 1)
        test_suite = result.test_suites[0]
        self.assertEqual(test_suite.name, "test.suite.bad.time")
        self.assertEqual(test_suite.errors, 0)
        self.assertEqual(test_suite.tests, 1)
        self.assertEqual(test_suite.time, None)


class Test9(unittest.TestCase):
    def test_weird_time(self):
        result = detest.Detest().parse("tests/test9.xml")
        self.assertEqual(len(result.test_suites), 1)
        test_suite = result.test_suites[0]
        self.assertEqual(test_suite.name, "test.suite.bad.time2")
        self.assertEqual(test_suite.errors, 0)
        self.assertEqual(test_suite.tests, 1)
        self.assertEqual(test_suite.time.total_seconds(), 13323.232)
        test_case = test_suite.test_cases[0]
        self.assertEqual(test_case.time.total_seconds(), 29.34)


if __name__ == '__main__':
    unittest.main()
