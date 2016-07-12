from automarker import *
from automarker.compilation import *
from automarker.functions import *

def mark_battleships(assignment):
	#check compilation and format
	compiled = CompilationChecker(assignment)\
		.should(FollowFormattingStyle(),'Checking Format')\
		.should(NotUseImports(), 'Do not import any modules')\
		.should(NotUsePrint(), 'Do not use any output functions')\
		.should(NotUseInput(), 'Do not use any input functions')\
		.should(HaveDocstrings(), 'Should have docstring for the functions')\
		.check()

	if not compiled:
		return

	#unittest
	FunctionChecker(assignment, 'has_ship')\
		.newCase('TypeChecking').when([['.','.','.'],['.','a','.'],['.','.','.']], 1, 1, 'a', 2).shouldReturnType(bool)




if __name__ == '__main__':
	marker = Marker()
	marker.batch_mark('battleships',mark_battleships)