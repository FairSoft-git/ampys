from collections import Counter
import glob
import os

class Reporter(object):

    def __init__(self):
        self.msg = []
        self.compiled = True
        self.functions = []
        self.function_cases = Counter()
        self.passed_cases = Counter()


    def onCompilationError(self, lineno, offset, msg):
        self.msg.append('{} (Line {}, Column {})'.format(msg, lineno, offset))


    def onCompilationCheckFinish(self, passed):
        self.compiled = passed
        if passed:
            self.msg.append('Compliation and format checking passed')
        else:
            self.msg.append('Compliation and format checking failed')


    def onCannotFindFunctionError(self, func_name):
        self.msg.append('Cannot find function: {}'.format(func_name))


    def onFunctionTestCasePassed(self, func_name):
        if func_name not in self.function_cases:
            self.functions.append(func_name)

        self.function_cases[func_name] += 1
        self.passed_cases[func_name] += 1


    def onFunctionTestCaseFail(self, func_name, args, return_value, excepted_value):
        if func_name not in self.function_cases:
            self.functions.append(func_name)
            
        argStrs = []
        for a in args:
            if type(a) == str:
                argStrs.append("'" + a + "'")
            else:
                argStrs.append(str(a))

        self.msg.append('Case Failed: {}({}) returns {}, excepted: {}'.format(func_name, 
            ', '.join(argStrs), return_value, excepted_value))
        self.function_cases[func_name] += 1


    def onFunctionTestCaseTimeout(self, func_name, args):
        if func_name not in self.function_cases:
            self.functions.append(func_name)
            
        argStrs = []
        for a in args:
            if type(a) == str:
                argStrs.append("'" + a + "'")
            else:
                argStrs.append(str(a))

        self.msg.append('Case Failed: {}({}) timeout'.format(func_name, ', '.join(argStrs)))
        self.function_cases[func_name] += 1


    def onFunctionTypeCheckingFail(self, func_name, return_type, excepted_value):
        self.msg.append('Type Checking Failed: {} returns {}, excepted: {}'.format(func_name, return_type, excepted_value))
        self.function_cases[func_name] += 1


    def report(self, verbose):
        if verbose == 0:
            msg = []
            if self.compiled:
                msg.append('Compliation and format checking passed')

                total = sum([v for k, v in self.function_cases.most_common()])
                passed = sum([v for k, v in self.passed_cases.most_common()])
                msg.append('Result: {}/{}'.format(passed, total))

                for func_name in self.functions:
                    msg.append('\t{}: {}/{} passed'.format(func_name, 
                        self.passed_cases[func_name], self.function_cases[func_name]))
            else:
                msg.append('Compliation and format checking failed')

        elif verbose == 1:
            msg = list(self.msg)
            if self.compiled:
                total = sum([v for k, v in self.function_cases.most_common()])
                passed = sum([v for k, v in self.passed_cases.most_common()])
                msg.append('Result: {}/{}'.format(passed, total))

                for func_name in self.functions:
                    msg.append('\t{}: {}/{} passed'.format(func_name, 
                        self.passed_cases[func_name], self.function_cases[func_name]))


        return '\n'.join(msg)


class Assignment(object):

    def __init__(self, source_code, reporter = None):
        '''
        Create a new marker based on source code.

        Parameters
        ----------
        source_code : string
            source code
        reporter : Reporter or subclass of Reporter
            the reporter used for generating the report of mark
        '''

        self.source_code = source_code

        if reporter:
            self.reporter = reporter
        else:
            self.reporter = Reporter()


    def generateReport(self, verbose = 0):
        '''
        Generate assignment report.

        Parameters
        ----------
        verbose : int
            the verbose level. 
            when verbose = 0, only show the result.
            when verbose = 1, show the details.
        '''
        return self.reporter.report(verbose)

