import sys
import imp

class FunctionTestCase(object):

    def __init__(self, checker, description):
        self.checker = checker
        self.description = description
        self.args = []


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

        r = self.checker.target(*self.args)
        if type(r) != return_type:
            self.checker.reporter.onFunctionTypeCheckingFail(
                self.checker.func_name,
                type(r), return_type)
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

        r = self.checker.target(*self.args)
        if r != value:
            self.checker.reporter.onFunctionTestCaseFail(
                self.checker.func_name,
                self.args,
                r, value)
        else:
            self.checker.reporter.onFunctionTestCasePassed(self.checker.func_name)

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
        self.target = self.loadFunc(assignment.source, func_name)


    def loadFunc(self, filename, func_name):
        with open(filename) as fin:
            content = fin.read()
            module = imp.new_module('assignment')
            exec(content, module.__dict__)

        if hasattr(module, func_name):
            return getattr(module, func_name)
        else:
            self.reporter.onCannotFindFunctionError(func_name)
            return None


    def newCase(self, description = ''):
        return FunctionTestCase(self, description)
