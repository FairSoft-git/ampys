from automarker.compilation import *
from automarker.functions import FunctionChecker
from automarker.marker import Assignment

if __name__ == '__main__':
    with open('assignment.py') as fin:
        a = Assignment(fin.read())

    compiled = CompilationChecker(a)\
        .should(FollowFormattingStyle(), 'Checking Format')\
        .should(NotUseImports(), 'Do not import any modules')\
        .should(NotUsePrint(), 'Do not use any output function')\
        .should(NotUseInput(), 'Do not use any input function')\
        .should(HaveDocstrings(), 'Should have docstring for the functions')\
        .check()

    if compiled:
        FunctionChecker(a, 'foo')\
            .newCase('type check').when().shouldNotReturn()

        FunctionChecker(a, 'bar')\
            .newCase('type check').when(1, 2).shouldReturnType(int)\
            .newCase('some test').when(1, 2).shouldReturn(3)

    print(a.generateReport(1))
