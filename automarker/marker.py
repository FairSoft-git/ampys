from collections import Counter
import glob
import os
import imp
import os.path

SUCCESS = 0
WARNING = 1
ERROR   = 2

SPLITTER = '-' * 50

class Reporter(object):

    def __init__(self):
        self.msg = []
        self.compiled = True
        self.breakSandbox = False
        self.functions = []
        self.function_cases = Counter()
        self.passed_cases = Counter()
        self.timeout_funcs = set()
        self.fail_cases = []
        self.runtimeError = False


    def onCompilationError(self, lineno, offset, msg):
        self.msg.append((WARNING, '{} (Line {}, Column {})'.format(msg, lineno, offset)))


    def onCompilationCheckFinish(self, compiled):
        self.compiled = not self.breakSandbox and compiled
        if self.compiled:
            self.msg.append((SUCCESS, 'Compliation passed'))
        else:
            self.msg.append((ERROR, 'Compliation failed'))


    def onBreakSandbox(self, lineno, offset, msg):
        self.breakSandbox = True
        self.msg.append((ERROR, '{} (Line {}, Column {})'.format(msg, lineno, offset)))


    def onRuntimeError(self, err):
        self.compiled = False
        self.msg.append((ERROR, '{}'.format(err)))


    def functionFail(self, func_name):
        if func_name not in self.function_cases:
            self.functions.append(func_name)

        self.function_cases[func_name] += 1


    def functionPass(self, func_name):
        if func_name not in self.function_cases:
            self.functions.append(func_name)

        self.function_cases[func_name] += 1
        self.passed_cases[func_name] += 1


    def onCannotFindFunctionError(self, func_name):
        self.functionFail(func_name)


    def onFunctionTestCasePassed(self, func_name):
        self.functionPass(func_name)


    def onUnittestFail(self, func_name, description):
        self.functionFail(func_name)
        self.fail_cases.append(description)


    def onFunctionTestCaseFail(self, func_name, args, return_value, excepted_value):
        self.functionFail(func_name)


    def onFunctionTypeCheckingFail(self, func_name, return_type, excepted_value):
        self.functionFail(func_name)


    def onFunctionTimeout(self, func_name):
        self.functionFail(func_name)
        self.timeout_funcs.add(func_name)
        self.fail_cases.append('{}() timeout'.format(func_name))


    def simpleReport(self):
        msg = list(self.msg)
        for func_name in self.function_cases.keys():
            passed = self.passed_cases[func_name]
            total  = self.function_cases[func_name]

            if passed == total:
                code = SUCCESS
            else:
                code = ERROR

            msg.append((code, 'Testing {}() : {}/{}'.format(func_name, passed, total)))
            if func_name in self.timeout_funcs:
                msg.append((ERROR, '{}(): Time Limit Exceeded'.format(func_name)))

        return [{'err':c, 'msg':m} for c, m in msg]


    def report(self, verbose = 0):
        if verbose == 0:
            return self.simpleReport()
        elif verbose == 1:
            msg = ['DEBUG INFO:', SPLITTER]
            if not self.compiled:
                msg.append('Compliation failed')

            msg += self.fail_cases
            msg.append(SPLITTER)
            msg.append('OUTPUT MSG:')
            msg += [l['msg'] for l in self.simpleReport()]

            return msg


class Assignment(object):

    def __init__(self, source_code, dependencies = [], reporter = None):
        '''
        Create a new marker based on source code.

        Parameters
        ----------
        source_code : string
            source code
        dependencies : list of modules
            assignment dependency modules
        reporter : Reporter or subclass of Reporter
            the reporter used for generating the report of mark
        '''

        self.source_code = source_code
        self.dependencies = dependencies

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


def mark(code, script_filepath):
    base_dir = os.path.dirname(script_filepath)
    with open(script_filepath) as fin:
        # load testing script
        script_content = fin.read()
        module = imp.new_module('test_script')
        exec(script_content, module.__dict__)

        # get mark function from script file
        mark_script = getattr(module, 'mark')

        # mark code
        return mark_script(base_dir, code)