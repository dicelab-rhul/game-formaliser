# Autoformalization of Game Descriptions using Large Language Models

## Overview

This is a framework for autoformalising natural language game-theoretical scenarios into their Prolog specification using Large Language Models. The framework and its evaluation are described in more detail in this [paper](https://arxiv.org/abs/2409.12300).

## Installation

To install the required dependencies run:

```bash
pip install -r requirements.txt
```
The framework requires also [SWI-Prolog](https://www.swi-prolog.org/) to be [installed](https://wwu-pi.github.io/tutorials/lectures/lsp/010_install_swi_prolog.html).

## Usage

To run the sample experiment, use the following command in your terminal:

```bash
python experiment.py
```
You can modify the parameters of the experiment by modifying [params.ini](CONFIG/params.ini). To use GPT-4 used by default in the experiment, the API key has to be stored in an environment variable.  

## Project Structure

The structure of the project is as follows:
```bash
.
├── CONFIG/
├── DATA/
├── GAMES/
│   └── 2x2/
│   └── GENERALISATION/
|   └── INCOMPLETE/
├── OUTPUT/
│   └── axioms/
│   └── logs/
|   └── prompts/
├── llms/
│   ├── gpt4.py
├── src/
│   ├── GameStatus.py
│   ├── base_llm.py
│   ├── game_formaliser.py
│   ├── setup_logger.py
│   ├── solver.pl
│   ├── solver.py
│   ├── utils.py
├── experiment.py
```

## Authors

Agnieszka Mensfelt </br>
Kostas Stathis </br>
Vince Trencsenyi

## Citing This Work

```bibtex
@inproceedings{mensfelt24a,
  author       = {Agnieszka Mensfelt and
                  Kostas Stathis and
                  Vince Tencsenyi},
  title        = {Autoformalization of {G}ame {D}escriptions Using {L}arge {L}anguage {M}odels},
  booktitle    = {1st {I}nternational {W}orkshop on {N}ext-{G}eneration {L}anguage {M}odels for {K}nowledge {R}epresentation and {R}easoning},
  address      = {Hanoi, Vietnam},
  publisher    = {ArXiv},
  year         = {2024},
}
```
