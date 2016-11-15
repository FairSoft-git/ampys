#! /usr/bin/env python3
import os

from automarker.compilation import *
from automarker.functions import FunctionChecker
from automarker.marker import Assignment
import string
from pprint import pprint

def mark(code):
    # create an assignment
    a = Assignment(code)

    # write compilation and code style check here
    # Rules can be found in automarker/compilation.py
    compiled = CompilationChecker(a)\
        .should(FollowFormattingStyle(), 'Checking Format')\
        .should(NotUseImports(['doctest']), 'Do not import any modules')\
        .should(NotUsePrint(), 'Do not use any output function')\
        .should(NotUseInput(), 'Do not use any input function')\
        .should(HaveDocstrings(), 'Should have docstring for the functions')\
        .check()

    # write unit test here
    if compiled:
        FunctionChecker(a, 'extract_mentions')\
            .newCase().when('').shouldReturnType(list)\
            .newCase().when('').shouldReturn([])\
            .newCase().when('@a').shouldReturn(['a'])\
            .newCase().when(' @ab').shouldReturn(['ab'])

        FunctionChecker(a, 'extract_hashtags')\
            .newCase().when('').shouldReturnType(list)\
            .newCase().when('').shouldReturn([])

        FunctionChecker(a, 'count_words')\
            .newCase().when('aaa bbb aaa', {}).shouldNotReturn()\
            .newCase().when('aaa bbb aaa', {}).shouldModifyParams('aaa bbb aaa', {'aaa' : 2, 'bbb' : 1})


    # generate report
    return a.generateReport()


if __name__ == '__main__':
    code_filename = 'assignment.py' # change this to your target assignment code file
    with open(code_filename) as fin: 
        code = fin.read()
        pprint(mark(code))
