import os.path
from src.solver import Solver
import logging
from src.GameStatus import GameStatus
from src.utils import parse_axioms, create_feedback_prompt


class GameFormaliser:
	"""
	GameFormaliser class for games autoformalisation.
	"""

	def __init__(self, llm_instance, solver, game_name, max_attempts=10, log_file=None, timestamp=None):
		"""
		Initialize the GameFormaliser with an LLM and a formal solver

		Args:
			llm_instance (LLM): an LLM instance to create game description.
			solver (Solver): a Solver instance.
			max_attempts (int): maximum number of attempts of correcting the code
			log_file (str): name of the log file
		"""
		self.llm = llm_instance
		self.solver = solver
		self.max_attempts = max_attempts
		self.log_file = log_file
		self.formalising_log_handler = None
		self.game_name = game_name
		self.timestamp = timestamp

	def __init_logging(self, reasoning_logger):
		"""
		Initializes logging for reasoning.

		Args:
		- reasoning_logger: The logger object to be configured.
		"""

		# Create a file handler for logging
		reasoning_handler = logging.FileHandler(self.log_file)
		# Set logging level for the handler to INFO
		reasoning_handler.setLevel(logging.INFO)
		self.formalising_log_handler = reasoning_handler
		# Define the log message format with '~' as separator between log parts
		formatter = logging.Formatter('%(message)s' + '~\n')
		# Set the formatter for the handler
		reasoning_handler.setFormatter(formatter)
		# Add the handler to the logger
		reasoning_logger.addHandler(reasoning_handler)

	def __remove_handler(self, reasoning_logger):
		"""
		Closes and removes file handler from the logger.

		Args:
		- reasoning_logger: The logger object from which the handler will be removed.
		"""
		if self.formalising_log_handler in reasoning_logger.handlers:
			self.formalising_log_handler.close()
			reasoning_logger.removeHandler(self.formalising_log_handler)
			self.formalising_log_handler = None

		for handler in reasoning_logger.handlers[:]:
			handler.flush()
			handler.close()
			reasoning_logger.removeHandler(handler)

		import gc
		gc.collect()

	def formalise(self, game_description, log_file=None, template_file_path="DATA/prompt_template.txt") -> GameStatus:
		"""
		The self-correcting loop for creating formal game specifications

		Args:
			game_description (str): game description in natural language.
			log_file (str): Name of a log_file
			template_file_path (str): path to a template file

		Returns:
			GameStatus: Correctness status.
		"""
		# Clear context before each translation loop
		self.llm.clear_context()

		# Setup logger
		logging.debug('Debug info')
		if log_file is not None:
			self.log_file = log_file
		reasoning_logger = logging.getLogger('GameFormaliser')
		# Set logging level to INFO
		reasoning_logger.setLevel(logging.INFO)
		if self.log_file is not None:
			self.__init_logging(reasoning_logger)

		# Prepare prompt
		with open(template_file_path, 'r') as file:
			prompt = file.read()
		prompt = prompt.replace('{game_description}', game_description)

		status = GameStatus.START

		base_game_name = os.path.splitext(self.game_name)[0]
		game_axioms_filename = f"{base_game_name}_game_axioms_{self.timestamp}.pl"
		prompt_filename = game_axioms_filename.replace(".pl", ".txt")

		with open(os.path.join('OUTPUT', 'prompts', prompt_filename), 'w') as prompt_file:
			prompt_file.write(prompt)

		for attempt in range(self.max_attempts):
			# Get game formalisation
			response = self.llm.prompt(prompt)

			parse_axioms(response, game_axioms_filename)

			if status is GameStatus.START:
				reasoning_logger.info(
					"###PROMPT##\n" +
					prompt)

			reasoning_logger.info(
					"\n###ATTEMPT##" +
					str(attempt) +
					"~\nRESPONSE##\n"
					+ response
				)

			correct, trace = self.solver.make_query(game_axioms_filename)
			reasoning_logger.info(f"TRACE##\n{trace}")

			if correct:  # syntactically correct game description
				if status is GameStatus.START:  # if we get it right in the first iter
					status = GameStatus.CORRECT
				else:  # if we get it right in the subsequent iterations
					status = GameStatus.FIXED
				break
			else:
				# Add erroneous translation to the conversation context
				status = GameStatus.FAULTY
				self.llm.add_response(response)
				feedback_prompt = create_feedback_prompt(trace)
				reasoning_logger.info("CORRECTING PROMPT##\n" + str(feedback_prompt))

		self.__remove_handler(reasoning_logger)

		return status
