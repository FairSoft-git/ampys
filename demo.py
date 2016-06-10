from automarker import *
from automarker.compilation import *
from automarker.functions import *


def mark(assignment):
    # check compilation and format
    compiled = CompilationChecker(assignment)\
        .should(FollowFormattingStyle(), 'Checking Format')\
        .should(NotUseImports(exceptions = ['math']), 'Do not import any modules (other than math)')\
        .should(NotUsePrint(), 'Do not use any output function')\
        .should(NotUseInput(), 'Do not use any input function')\
        .should(HaveDocstrings(), 'Should have docstring for the functions')\
        .check()

    if not compiled:
        return

    # unit test
    FunctionChecker(assignment, 'contains_owly_url')\
        .newCase('Type Checking').when('Test 123').shouldReturnType(bool)\
        .newCase('Empty String').when('').shouldReturn(False)\
        .newCase('Only URL').when('http://ow.ly/').shouldReturn(True)\
        .newCase('Wrong Beginning URL').when('http://www.nhl.com').shouldReturn(False)\
        .newCase('Beginning URL').when('http://ow.ly/WXJFN Good Boy').shouldReturn(True)\
        .newCase('Wrong URL').when('Fairgrieve to play in goal http://www.nhl.com').shouldReturn(False)\
        .newCase('Without Space').when('Fairgrieve to play in goalhttp://ow.ly/WXJFN').shouldReturn(False)\
        .newCase('Multiple Space').when('Father      http://ow.ly/WXJFN   Mother').shouldReturn(True)

    FunctionChecker(assignment, 'is_valid_tweet')\
        .newCase('Type Checking').when('Test 123').shouldReturnType(bool)\
        .newCase('empty tweet').when('').shouldReturn(False)\
        .newCase('one char').when('a').shouldReturn(True)\
        .newCase('Valid tweet').when('The first midterm is on Feb. 24th! LOL!').shouldReturn(True)\
        .newCase('over length').when("They said this tweet will not be valid if it's length \
        is greater than fifty characters. I don't think so. That's why I \
        write this tweet. Is this tweet posted?").shouldReturn(False)

    FunctionChecker(assignment, 'add_hashtag')\
        .newCase('Type Checking').when('Wish everybody got 4.0', 'GPA4.0').shouldReturnType(str)\
        .newCase('add hash success').when('Wish everybody got 4.0', 'GPA4.0').shouldReturn('Wish everybody got 4.0 #GPA4.0')\
        .newCase('add hash fail').when("They said this tweet will not be valid if it's length \
        is greater than fifty characters. I don't think so. That's why I \
        write this tweet.", 'CSC108_A1').shouldReturn("They said this tweet will not be valid if it's length \
        is greater than fifty characters. I don't think so. That's why I \
        write this tweet.")\
        .newCase('50').when('It is good to write the program by yourself.GL', 'LL').shouldReturn('It is good to write the program by yourself.GL #LL')

    FunctionChecker(assignment, 'contains_hashtag')\
        .newCase('Type Checking').when('I like #csc108', '#csc108').shouldReturnType(bool)\
        .newCase('Has tag').when('I like #csc108', '#csc108').shouldReturn(True)\
        .newCase('not has').when('I like #csc108', 'csc108').shouldReturn(False)\
        .newCase('diif tag').when('I like #csc108', '#csc148').shouldReturn(False)\
        .newCase('close hash').when('I like #csc108', '#csc_108').shouldReturn(False)\
        .newCase('2 tag').when('I like #csc108 in #UofT', '#csc108').shouldReturn(True)\
        .newCase('UT tag').when('I like #csc108 in #UofT', '#UofT').shouldReturn(True)\
        .newCase('part tag').when('I liike #csc108 in #UofT', '#csc').shouldReturn(False)

    FunctionChecker(assignment, 'report_longest')\
        .newCase('Type Checking').when('I like #csc108', "I don't like #csc108").shouldReturnType(str)\
        .newCase('2 > 1').when('I like #csc108', "I don't like #csc108").shouldReturn('Tweet 2')\
        .newCase('1 > 2').when("I don't like #csc108", 'I like #csc108').shouldReturn('Tweet 1')\
        .newCase('Same').when('I like #csc108', 'I hate #csc108').shouldReturn('Same length')

    FunctionChecker(assignment, 'num_tweets_required')\
        .newCase('Type Checking').when('').shouldReturnType(int)\
        .newCase('0').when('').shouldReturn(0)\
        .newCase('1 character').when('A').shouldReturn(1)\
        .newCase('1').when('I like #csc108').shouldReturn(1)\
        .newCase('50').when('It is good to write the program by yourself.GL #LL').shouldReturn(1)\
        .newCase('140').when("They said this tweet will not be valid if it's length" + \
        "is greater than fifty characters. I don't think so. That's why I" + \
        "write this tweet.").shouldReturn(3)\
        .newCase('200').when("They said this tweet will not be valid if it's length" + \
        "is greater than fifty characters. I don't think so. That's why I" + \
        "write this tweet. It is good to write the program by yourself.GL #LL 12345678").shouldReturn(4)

    checker = FunctionChecker(assignment, 'get_nth_tweet')\
        .newCase('Type Checking').when('', 0).shouldReturnType(str)\
        .newCase('Empty 0').when('', 0).shouldReturn('')\
        .newCase('Empty 1').when('', 1).shouldReturn('')\
        .newCase('Empty 10').when('', 10).shouldReturn('')\
        .newCase('14 0').when('I like #csc108', 0).shouldReturn('')\
        .newCase('14 1').when('I like #csc108', 1).shouldReturn('I like #csc108')\
        .newCase('14 2').when('I like #csc108', 2).shouldReturn('')\
        .newCase('50 0').when('It is good to write the program by yourself.GL #LL', 0).shouldReturn('')\
        .newCase('50 1').when('It is good to write the program by yourself.GL #LL', 1).shouldReturn('It is good to write the program by yourself.GL #LL')\
        .newCase('50 2').when('It is good to write the program by yourself.GL #LL', 2).shouldReturn('')\
        .newCase('65 0').when('It is good to write the program by yourself.GL #LL I like #csc108', 0).shouldReturn('')\
        .newCase('65 1').when('It is good to write the program by yourself.GL #LL I like #csc108', 1).shouldReturn('It is good to write the program by yourself.GL #LL')\
        .newCase('65 2').when('It is good to write the program by yourself.GL #LL I like #csc108', 2).shouldReturn(' I like #csc108')\
        .newCase('65 10').when('It is good to write the program by yourself.GL #LL I like #csc108', 10).shouldReturn('')

    expected = ['', 'a' * 50, 'b' * 50, 'c' * 50, 'd' * 50, '', '', '']
    for i, ev in enumerate(expected):
        checker.newCase('200 ' + str(i))\
            .when('a' * 50 + 'b' * 50 + 'c' * 50 + 'd' * 50, i)\
            .shouldReturn(ev)


if __name__ == '__main__':
    marker = Marker()
    marker.batch_mark('assignment', mark, 1)