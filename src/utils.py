import os
import re


def parse_axioms(response, game_axioms_filename):
	"""
	Parses game axioms from the given response and saves them to a .pl file.

	Args:
		response (str): The response containing the game axioms to be parsed.
		game_axioms_filename (str): name of the file to which the axioms will be saved

	Returns:
		str: The filename of the saved .pl file containing the game axioms.
	"""
	pattern = r'(?m)^@([^@]+)@'
	match = re.search(pattern, response)
	assert match is not None
	game_axioms = match.group(1)

	with open(os.path.join('OUTPUT', 'axioms', game_axioms_filename), 'w') as f_out:
		f_out.write(game_axioms)

	return game_axioms_filename


def create_feedback_prompt(trace):
	"""
	Creates feedback prompt based on the provided trace.

	Args:
		trace (str): The trace information used to create feedback.

	Returns:
		str: The generated feedback.
	"""

	feedback_prompt = f"Your Prolog code produced the following error(s):\n{trace}\nYour faulty code equires careful review and debugging.\
		An error trace has been provided, which is a crucial tool in identifying and resolving issues in your code. Fix your code based on the trace and the suggestion below. \n\
		1. Error Location:\n\
		Use the line numbers and predicate names mentioned in the error trace to pinpoint the exact location of the error in your code.\n\
		Examine the surrounding context of the error to understand how it might be affecting or be affected by other parts of your code.\n\
		2. Error Type:\n\
		Identify the specific type of error indicated in the trace (e.g., syntax error, undefined predicate, argument mismatch, etc.).\n\
		Research this error type if you're unfamiliar with it to understand its common causes and solutions.\n\
		3. Syntax Conformity:\n\
		In light of the error trace, double-check that all predicates are correctly defined with proper arity, especially near the error location.\n\
		Ensure all clauses end with a period (.), paying extra attention to the area indicated by the error.\n\
		Verify the correct use of Prolog punctuation, including commas, semicolons, and parentheses.\n\
		4. Logical Consistency:\n\
		Review the logical structure of your predicates, focusing on the area highlighted in the error trace.\n\
		Check for proper use of logical operators such as AND (,), OR (;), and NOT (+), ensuring they align with your intended logic.\n\
		5. Variable Handling:\n\
		Examine variable names and scopes, particularly those mentioned in the error trace.\n\
		Look for potential issues with variable instantiation or unification.\n\
		6. Predicate Definitions and Calls:\n\
		Verify that all predicates used in the program, especially those mentioned in the error trace, are properly defined or imported.\n\
		Check for consistency in predicate names and arities across the entire program.\n\
		7. Module-Related Issues:\n\
		If the error involves modules, check module declarations, imports, and exports.\n\
		8. Data Type Mismatches:\n\
		Look for any type mismatches or improper type handling, particularly if the error suggests type-related issues.\n\
		9. Cut (!) Usage:\n\
		If the error trace suggests issues with choice points or backtracking, review any use of the cut operator (!).\n\
		10. I/O and File Operations:\n\
		For errors related to file operations, verify file paths and the correct usage of I/O predicates.\n\
		11. Built-in Predicate Usage:\n\
		Confirm that built-in predicates are used correctly and with the right arity, especially those flagged in the error trace.\n\
		12. Character Encoding:\n\
		Check for any non-ASCII or special characters that might be causing issues, particularly if the error suggests encoding problems."

	return feedback_prompt
