import sys
import imp
import multiprocessing as mp
import time
import queue
import unittest
import inspect
import re

class FunctionTestCase(object):

    def __init__(self, checker, description, max_running_time = 1):
        self.checker = checker
        self.description = description
        self.args = []
        self.max_running_time = max_running_time


    def when(self, *args):
        '''
        Set the parameters of this test case.

        Parameters
        ----------
        *args: any types
            the input paremeters
        '''
        self.args = args
        return self


    def run(self):
        '''
        Run this test case. This will return two values:
        first return value is whether this function returns successfully;
        second return value is the original return from this function.
        '''
        q = mp.Queue()

        def workerFunc():
            try:
                r = self.checker.target(*self.args)
                q.put((True, self.args, r))
            except Exception:
                q.put((False, self.args, None))

        worker = mp.Process(target = workerFunc)
        worker.start()

        try:
            return q.get(timeout = self.max_running_time)
        except queue.Empty:
            while worker.is_alive():
                worker.terminate()

            return False, self.args, None


    def shouldReturnType(self, return_type):
        '''
        Set the return type of this test case.

        Parameters
        ----------
        return_type: any type
            the return type
        '''
        if not self.checker.target:
            self.checker.reporter.onFunctionTypeCheckingFail(
                self.checker.func_name, None, return_type)
            return self.checker

        success, post_args, r = self.run()

        if success and type(r) == return_type:
            self.checker.reporter.onFunctionTestCasePassed(self.checker.func_name)
        else:
            self.checker.reporter.onFunctionTypeCheckingFail(
                self.checker.func_name,
                type(r), return_type)
        
        return self.checker


    def shouldNotReturn(self):
        '''
        Set this test case will not return anything.
        '''
        if not self.checker.target:
            self.checker.reporter.onFunctionTypeCheckingFail(
                self.checker.func_name, None, return_type)
            return self.checker

        success, post_args, r = self.run()
        if not success or r:
            self.checker.reporter.onFunctionTestCaseFail(
                self.checker.func_name,
                self.args,
                r, None)
        else:
            self.checker.reporter.onFunctionTestCasePassed(self.checker.func_name)

        return self.checker


    def shouldReturn(self, value):
        '''
        Set the expected return value of this test case.

        Parameters
        ----------
        value: any type
            the expected return value
        '''
        if not self.checker.target:
            self.checker.reporter.onFunctionTestCaseFail(
                self.checker.func_name,
                self.args,
                None, value)
            return self.checker

        success, post_args, r = self.run()
        if success and r == value:
            self.checker.reporter.onFunctionTestCasePassed(self.checker.func_name)
        else:
            self.checker.reporter.onFunctionTestCaseFail(
                self.checker.func_name,
                self.args,
                r, value)
            
        return self.checker


    def shouldModifyParams(self, *args):
        '''
        Set the expected modified parameter values.

        Parameters
        ----------
        args: any type
            the expected modified paremeters
        '''
        if not self.checker.target:
            self.checker.reporter.onFunctionTestCaseFail(
                self.checker.func_name,
                self.args,
                None, value)
            return self.checker

        success, post_args, r = self.run()
        
        passed = True
        for post_arg, expected_arg in zip(post_args, args):
            if post_arg != expected_arg:
                passed = False
                break

        if success and passed:
            self.checker.reporter.onFunctionTestCasePassed(self.checker.func_name)
        else:
            self.checker.reporter.onFunctionTestCaseFail(
                self.checker.func_name,
                self.args,
                r, args)
            
        return self.checker


def loadFunc(assignment, func_name):
    module = imp.new_module('assignment')
    for dependency in assignment.dependencies:
        module.__dict__[dependency.__name__] = dependency

    exec(assignment.source_code, module.__dict__)

    if hasattr(module, func_name):
        return getattr(module, func_name)
    else:
        return None


class FunctionChecker(object):

    def __init__(self, assignment, func_name):
        '''
        Create a new function checker.

        Parameters
        ----------
        assignment : Assignment
            the assignment to be checked
        func_name : str
            the name of function to be checked
        '''
        self.func_name = func_name
        self.reporter = assignment.reporter
        self.target = loadFunc(assignment, func_name)


    def newCase(self, description = ''):
        return FunctionTestCase(self, description)


FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')

def parseFuncName(test):
    if test.find('.') > 0:
        _, func_name, _ = test.split('.')
    else:
        func_name = test

    if 'Test' == func_name[:4]:
        func_name = func_name[4:]

    func_name = FIRST_CAP_RE.sub(r'\1_\2', func_name)
    return ALL_CAP_RE.sub(r'\1_\2', func_name).lower()


class UnittestResult(unittest.TestResult):

    def __init__(self, reporter):
        unittest.TestResult.__init__(self)
        self.reporter = reporter
    
    
    def addFailure(self, test, err):
        func_name = parseFuncName(test.id())
        self.reporter.onUnittestFail(func_name, 
             'Test case failed on {}.{}(): \n{}'.format(
                test.id().split('.')[1],
                test.id().split('.')[-1], 
                self._exc_info_to_string(err, test)))


    def addSuccess(self, test):
        func_name = parseFuncName(test.id())
        self.reporter.functionPass(func_name)



class UnittestChecker(object):

    def __init__(self, assignment, unittest_path, module_name, max_running_time = 2):
        '''
        Create a new function checker based on unittest.

        Parameters
        ----------
        assignment : Assignment
            the assignment to be checked

        unittest_path: str
            path of unittest module

        module_name: str
            the name of target module using in unittest file
        '''
        self.assignment = assignment
        self.unittest_path = unittest_path
        self.module_name = module_name
        self.max_running_time = max_running_time

        self.load()


    def load(self):
        module = imp.new_module(self.module_name)
        for dependency in self.assignment.dependencies:
            module.__dict__[dependency.__name__] = dependency

        exec(self.assignment.source_code, module.__dict__)

        ut = imp.new_module('assignment_unittest_module')
        ut.__dict__[self.module_name] = module
        with open(self.unittest_path) as fin:
            exec(fin.read(), ut.__dict__)

        self.cases = []
        for name, obj in inspect.getmembers(ut, inspect.isclass):
            if issubclass(obj, unittest.TestCase):
                self.cases.append(obj)


    def check(self):
        ENDLESS_LOOP = -1
        SUCCESS = 0
        FAIL = -2

        q = mp.Queue()

        for case in self.cases:
            func_name = parseFuncName(case.__name__)

            def workerFunc(case, reporter):
                suite = unittest.defaultTestLoader.loadTestsFromTestCase(case)
                result = UnittestResult(reporter)
                suite.run(result)
                q.put(reporter)

            worker = mp.Process(target = workerFunc, args = (case, self.assignment.reporter))
            worker.start()

            try:
                self.assignment.reporter = q.get(timeout = self.max_running_time)
            except queue.Empty:
                while worker.is_alive():
                    worker.terminate()

                self.assignment.reporter.onFunctionTimeout(func_name)
                