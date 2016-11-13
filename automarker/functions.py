import sys
import imp
import multiprocessing as mp
import time


class FunctionTestCase(object):

    def __init__(self, checker, description, max_running_time = 5):
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
        q = mp.Queue()

        def workerFunc():
            q.put(self.checker.target(*self.args))

        worker = mp.Process(target = workerFunc)
        worker.start()

        try:
            return q.get(timeout = self.max_running_time)
        except mp.Queue.empty:
            while worker.is_alive():
                worker.terminate()

            raise TimeoutError()


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

        try:
            r = self.run()
            if type(r) != return_type:
                self.checker.reporter.onFunctionTypeCheckingFail(
                    self.checker.func_name,
                    type(r), return_type)
            else:
                self.checker.reporter.onFunctionTestCasePassed(self.checker.func_name)

        except TimeoutError:
                self.checker.reporter.onFunctionTestCaseTimeout(
                    self.checker.func_name,
                    self.args)

        return self.checker


    def shouldNotReturn(self):
        '''
        Set this test case will not return anything.
        '''
        if not self.checker.target:
            self.checker.reporter.onFunctionTypeCheckingFail(
                self.checker.func_name, None, return_type)
            return self.checker

        try:
            r = self.run()
            if r:
                self.checker.reporter.onFunctionTestCaseFail(
                    self.checker.func_name,
                    self.args,
                    r, None)
            else:
                self.checker.reporter.onFunctionTestCasePassed(self.checker.func_name)

        except TimeoutError:
                self.checker.reporter.onFunctionTestCaseTimeout(
                    self.checker.func_name,
                    self.args)

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

        try:
            r = self.run()
            if r != value:
                self.checker.reporter.onFunctionTestCaseFail(
                    self.checker.func_name,
                    self.args,
                    r, value)
            else:
                self.checker.reporter.onFunctionTestCasePassed(self.checker.func_name)

        except Exception:
                self.checker.reporter.onFunctionTestCaseTimeout(
                    self.checker.func_name,
                    self.args)
            
        return self.checker



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
        self.target = self.loadFunc(assignment, func_name)


    def loadFunc(self, assignment, func_name):
        module = imp.new_module('assignment')
        exec(assignment.source_code, module.__dict__)

        if hasattr(module, func_name):
            return getattr(module, func_name)
        else:
            self.reporter.onCannotFindFunctionError(func_name)
            return None


    def newCase(self, description = ''):
        return FunctionTestCase(self, description)
