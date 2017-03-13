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
        compiled = True
        content = self.assignment.source_code
        reporter = self.assignment.reporter

        try:
            node = ast.parse(content, 'assignment.py')
        except Exception as e:
            # compile error
            reporter.onCompilationError(e.lineno, e.offset, e.msg)
            compiled = False

        if compiled:
            # check all the requirements
            for checker, description in self.checkers:
                if not checker(content, node, description, reporter):
                    passed = False

        reporter.onCompilationCheckFinish(compiled)
        return not reporter.breakSandbox and compiled



############################################
# Rules
############################################



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
                    reporter.onBreakSandbox(n.lineno, n.col_offset, description)
                    passed = False

            elif isinstance(n, ast.ImportFrom):
                if n.module not in exceptions:
                    reporter.onBreakSandbox(n.lineno, n.col_offset, description)
                    passed = False
                    
            elif isinstance(n, ast.Name):
                if n.id == '__import__':
                    reporter.onBreakSandbox(n.lineno, n.col_offset, description)
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
            if isinstance(n, ast.Name):
                if n.id in names:
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


def NotUseEval():
    '''
    Requirement of that the source code shouldn't use eval(), exec() or compile().
    
    Returns
    -------
    function:
        checker function
    '''
    names = set(['eval', 'exec', 'compile'])

    def _notUseFuncs(source_code, node, description, reporter):
        passed = True

        for n in ast.walk(node):
            if isinstance(n, ast.Name):
                if n.id in names:
                    reporter.onBreakSandbox(n.lineno, n.col_offset, description)
                    passed = False

        return passed

    return _notUseFuncs


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
        ast.Add     : '+',
        ast.Sub     : '-',
        ast.Mult    : '\*',
        ast.Div     : '/',
        ast.FloorDiv: '//',
        ast.Mod     : '%',
        ast.Pow     : '**',
        ast.LShift  : '<<',
        ast.RShift  : '>>',
        ast.BitOr   : '|',
        ast.BitXor  : '^',
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

        lines = source_code.split('\n')
        
        # check tabs
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
        op_lines = {}

        for n in ast.walk(node):
            if hasattr(n, 'lineno'):
                index = n.lineno - 1
                if index not in op_lines:
                    op_lines[index] = []

            if isinstance(n, ast.BinOp):
                if type(n.op) in OP_MAP:
                    op_lines[index].append(OP_MAP[type(n.op)])

            elif isinstance(n, ast.Compare):
                for op in n.ops:
                    if type(op) in OP_MAP:
                        op_lines[index].append(OP_MAP[type(op)])

            elif isinstance(n, ast.Assign):
                op_lines[index].append('=')

        for line_index, ops in op_lines.items():
            if len(ops) != 0:
                regex = r'.*\s' + r'\s.*\s'.join([re.escape(op) for op in ops]) + r'\s.*'
                if not re.match(regex, lines[line_index]):
                    reporter.onCompilationError(line_index + 1, 0, 
                        'There should be a blank space before and after every operator')
                    passed = False

        return passed

    return _follorFormattingStyle   
