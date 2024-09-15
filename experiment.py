import configparser
import os
from llms.gpt4 import GPT4
from src.setup_logger import logger
from src.solver import Solver
from src.game_formaliser import GameFormaliser
from src.GameStatus import GameStatus
from datetime import datetime


def main():
	# Read experiment parameters
	config = configparser.ConfigParser()
	config.read("CONFIG/params.ini")

	GAME_DIR = config.get("Paths", "GAME_DIR")
	OUT_DIR = config.get("Paths", "OUT_DIR")
	if not os.path.exists(OUT_DIR):
		os.makedirs(OUT_DIR)

	solver_path = config.get("Paths", "SOLVER_PATH")
	repetitions = config.getint("General", "repetitions")
	max_attempts = config.getint("General", "max_attempts")

	# Instantiate components
	solver = Solver(solver_path)
	llm_instance = GPT4(save_history=True)

	# Main experimental loop
	ext = ".txt"
	for game_fname in os.listdir(GAME_DIR):
		game_base_name = os.path.splitext(game_fname)[0]
		now = datetime.now()
		timestamp = now.strftime("%Y%m%d_%H%M")
		log_file_name_base = f"log_{game_base_name}_{timestamp}"
		log_file_name = os.path.join(OUT_DIR, "logs", log_file_name_base + ext)
		game_formaliser = GameFormaliser(llm_instance, solver, game_fname, max_attempts, log_file=log_file_name,
									 timestamp=timestamp)
		with open(os.path.join(GAME_DIR, game_fname), 'r') as file:
			game_description = file.read()

		status = GameStatus.START

		# Repeat repetitions times
		for rep in range(repetitions):
			try:  # We don't want to break the loop
				status = game_formaliser.formalise(game_description)
			except Exception as error:
				logger.exception(error)

		new_file_name = os.path.join(OUT_DIR, "logs", log_file_name_base + "_" + status.name + ext)
		os.rename(log_file_name, new_file_name)


if __name__ == '__main__':
	main()
