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
compiled = CompilationChecker(assignment)\
        .should(FollowFormattingStyle(), 'Checking Format')\
        .should(NotUseImports(exceptions = ['math']), 'Do not import any modules (other than math)')\
        .should(NotUsePrint(), 'Do not use any output function')\
        .should(NotUseInput(), 'Do not use any input function')\
        .should(HaveDocstrings(), 'Should have docstring for the functions')\
        .check()
```

You can also create your own should requirments (see automarker/compilation.py for more details and examples).

## Unit Test
```Python
FunctionChecker(assignment, 'contains_owly_url')\
        .newCase('Type Checking').when('Test 123').shouldReturnType(bool)\
        .newCase('Empty String').when('').shouldReturn(False)\
        .newCase('Only URL').when('http://ow.ly/').shouldReturn(True)
```

First create a function checker and set the target assignment and function. And then create some test cases using **newCase()**. **when()** is used to set the input parameters; **shouldReturnType()** and **shouldReturn()** is used to set the expected returning type and value.

## Single Marking
```Python
marker = Marker()
marker.mark('assignment_file.py', mark_func)
```

## Batch Marking
```Python
marker = Marker()
marker.batch_mark('assignment_folder', mark_func)
```