import ast
import re

class CompilationChecker(object):
    '''
    Check is there something wrong when compiling.
    Formating check can also be performed in this stage
    '''

    def __init__(self, assignment):
        self.assignment = assignment
        self.checkers = []


    def should(self, func, description):
        '''
        Add checker function and requirment description

        Parameters
        ---------
        func : function
            Checking function. This function should accept 4 parameters:
                source_code (string): the source code of assignment
                node (ast.Node): abstract syntax root node of parsed source code
                description (string): the description of this checker
                reporter (marker.reporter): report generator
            and it should return whether the assignment can pass this checker
        description : string
            the description of this checker

        Returns
        -------
        bool
            whether the assignemt can pass this checker
        '''
        self.checkers.append((func, description))
        return self


    def check(self):
        '''
        Check the assignment

        Returns
        -------
        bool
            whether the assignemt can pass this checker        
        '''
        passed = True
        source = self.assignment.source
        reporter = self.assignment.reporter

        with open(source) as fin:
            content = fin.read()

            try:
                node = ast.parse(content, source)
            except Exception as e:
                # compile error
                reporter.onCompilationError(e.lineno, e.offset, e.msg)
                passed = False

            if passed:
                # check all the requirements
                for checker, description in self.checkers:
                    if not checker(content, node, description, reporter):
                        passed = False

        reporter.onCompliationCheckFinish(passed)
        return passed



def NotUseImports(exceptions = []):
    '''
    Requirement of that the source code shouldn't use any imports 
    (except those on exceptions list).

    Parameters
    ----------
    exceptions : list of string
        the names of imports which can be used

    Returns
    -------
    function:
        checker function
    '''
    exceptions = set(exceptions)

    def _useImports(source_code, node, description, reporter):
        passed = True

        for n in ast.walk(node):
            if isinstance(n, ast.Import):
                if n.names[0].name not in exceptions:
                    reporter.onCompilationError(n.lineno, n.col_offset, description)
                    passed = False

            elif isinstance(n, ast.ImportFrom):
                if n.module not in exceptions:
                    reporter.onCompilationError(n.lineno, n.col_offset, description)
                    passed = False

        return passed

    return _useImports


def NotUseFuncs(names):
    '''
    Requirement of that the source code shouldn't use function, 
    such as print() or input().

    Parameters
    ----------
    names: list of string
        the names of forbidden function

    Returns
    -------
    function:
        checker function
    '''
    names = set(names)

    def _notUseFuncs(source_code, node, description, reporter):
        passed = True

        for n in ast.walk(node):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                if n.func.id in names:
                    reporter.onCompilationError(n.lineno, n.col_offset, description)
                    passed = False

        return passed

    return _notUseFuncs



def NotUsePrint():
    '''
    Requirement of that the source code shouldn't use print().

    Returns
    -------
    function:
        checker function
    '''
    return NotUseFuncs(['print'])


def NotUseInput():
    '''
    Requirement of that the source code shouldn't use input() or raw_input().
    
    Returns
    -------
    function:
        checker function
    '''
    return NotUseFuncs(['input', 'raw_input'])


def HaveDocstrings():
    '''
    Requirement of that the source code should have docstring for each function.
    
    Returns
    -------
    function:
        checker function
    '''

    def _haveDocstrings(source_code, node, description, reporter):
        passed = True

        for n in ast.walk(node):
            if isinstance(n, ast.FunctionDef):
                doc = ast.get_docstring(n)
                if not doc:
                    reporter.onCompilationError(n.lineno, n.col_offset, description)
                    passed = False

        return passed

    return _haveDocstrings


def FollowFormattingStyle():
    '''
    Requirement of that the source code should follow the provided formatting style.
    
    Returns
    -------
    function:
        checker function
    '''
    VARIABLE_NAME_MATCHER = re.compile(r'^[a-z0-9_]+$')
    CONSTANT_NAME_MATCHER = re.compile(r'^[A-Z0-9_]+$')
    TAB_MATCHER = re.compile(r'^\t+')

    OP_MAP = {
        # binary operators
        ast.Add     : '\+',
        ast.Sub     : '-',
        ast.Mult    : '\*',
        ast.Div     : '/',
        ast.FloorDiv: '//',
        ast.Mod     : '%',
        ast.Pow     : '\*\*',
        ast.LShift  : '<<',
        ast.RShift  : '>>',
        ast.BitOr   : '\|',
        ast.BitXor  : '\^',
        ast.BitAnd  : '&',
        # compare operators
        ast.Eq      : '==',
        ast.NotEq   : '!=',
        ast.Lt      : '<',
        ast.LtE     : '<=',
        ast.Gt      : '>',
        ast.GtE     : '>='
    }

    def _follorFormattingStyle(source_code, node, description, reporter):
        passed = True
        # check variable names and parameter names
        def checkName(n, name):
            if  not VARIABLE_NAME_MATCHER.match(name) \
            and not CONSTANT_NAME_MATCHER.match(name):
                reporter.onCompilationError(n.lineno, n.col_offset, 
                    'Variable name doesn\'t follow formatting style: ' + name)
                return False
            return True

        for n in ast.walk(node):
            if isinstance(n, ast.Assign):
                for name in [t.id for t in n.targets if isinstance(t, ast.Name)]:
                    if not checkName(n, name):
                        passed = False

            elif isinstance(n, ast.FunctionDef):
                if not checkName(n, n.name):
                    passed = False

                for arg in n.args.args:
                    if not checkName(n, arg.arg):
                        passed = False

        # check tabs
        lines = source_code.split('\n')
        for i, l in enumerate(lines):
            if TAB_MATCHER.match(l):
                reporter.onCompilationError(i+1, 0, 'Do not use tab to indent. Use 4 spaces instead.')
                passed = False

        # check line length < 80
        for i, l in enumerate(lines):
            if len(l) > 80:
                reporter.onCompilationError(i+1, 0, 'Each line must be less than 80 characters long including spaces.')
                passed = False

        # check space between op
        errLines = set()
        def checkOp(n, op, l):
            m = re.search('\\S' + op, l) or re.search(op + '\\S+', l)
            if m:
                errLines.add((n.lineno, m.start() + 1))

        for n in ast.walk(node):
            if hasattr(n, 'lineno'):
                l = lines[n.lineno - 1]

            if isinstance(n, ast.BinOp):
                if type(op) in OP_MAP:
                    checkOp(n, OP_MAP[type(n.op)], l)

            elif isinstance(n, ast.Compare):
                for op in n.ops:
                    if type(op) in OP_MAP:
                        checkOp(n, OP_MAP[type(op)], l)

            elif isinstance(n, ast.Assign):
                checkOp(n, '=', l)

        for lineno, col_offset in errLines:
            reporter.onCompilationError(lineno, col_offset, 
                'There should be a blank space before and after every operator')

        if len(errLines) > 0:
            passed = False

        return passed

    return _follorFormattingStyle   