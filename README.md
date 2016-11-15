# AutoMarker
This is an automarker program which can:
* check the format (act like pylint)
* check compilation error
* check accuracy of functions by unit tests
* generate marking report

# Usage
First you need to write a function which can accept one parameter (assignment). Then you have two options, one is marking a single assignment and print the result in console; another is to mark all the files insider a folder and generate the report for each file in the same folder.

demo.py is an example to show how to write the marking function. There are two stages, compilation checking and unit tests checking.

## Compilation Checking
```Python
compiled = CompilationChecker(a)\
    .should(FollowFormattingStyle(), 'Checking Format')\
    .should(NotUseImports(['doctest']), 'Do not import any modules')\
    .should(NotUsePrint(), 'Do not use any output function')\
    .should(NotUseInput(), 'Do not use any input function')\
    .should(HaveDocstrings(), 'Should have docstring for the functions')\
    .check()
```

You can also create your own should requirments (see automarker/compilation.py for more details and examples).

## Unit Test
```Python
FunctionChecker(a, 'extract_mentions')\
    .newCase().when('').shouldReturnType(list)\
    .newCase().when('').shouldReturn([])\
    .newCase().when('@a').shouldReturn(['a'])\
    .newCase().when(' @ab').shouldReturn(['ab'])
```

First create a function checker and set the target assignment and function. And then create some test cases using **newCase()**. **when()** is used to set the input parameters; **shouldReturnType()**, **shouldReturn()**, **shouldNotReturn()** and **shouldModifyParams()** are used to set the expected returning type and value.

See **demo.py** for more information.