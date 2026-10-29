
# Intelligent Microservice Mutation Testing Framework for Cloud-Native Applications

## Overview

The **Intelligent Microservice Mutation Testing Framework** is a Python-based prototype designed to evaluate the effectiveness of test cases by introducing small changes (mutations) into source code and checking whether automated tests detect them.

The project includes a mutation engine, automated test cases, JSON-based reporting, and a Streamlit dashboard for viewing mutation testing results.

## Features

- **Automated Mutation Testing:** Generates code mutants using predefined mutation operators.
- **Automated Test Execution:** Uses `pytest` to evaluate each mutant.
- **Mutant Classification:** Classifies mutants as killed, survived, or invalid.
- **Mutation Score Calculation:** Calculates the percentage of valid mutants killed by the tests.
- **JSON Report:** Saves testing results in `mutation_report.json`.
- **Interactive Dashboard:** Displays mutation testing results using Streamlit.

## Technology Stack

- Python
- pytest
- Streamlit
- JSON
- Git and GitHub

## Project Structure

```text
PT436/
├── app.py
├── service.py
├── test_service.py
├── mutation_engine.py
├── test_mutant_service.py
├── mutation_report.json
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/asif6544/Intelligent-Microservice-Mutation-Testing.git
```

### 2. Open the project directory

```bash
cd Intelligent-Microservice-Mutation-Testing
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install pytest streamlit
```

## How to Run

### Run the automated tests

```bash
python -m pytest -v test_service.py
```

### Run mutation testing

```bash
python mutation_engine.py
```

The engine executes the tests against generated mutants and saves the results in `mutation_report.json`.

### Launch the Streamlit dashboard

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

Click **Run Mutation Testing** in the dashboard to execute the mutation testing workflow and view the results.

## Understanding Mutation Testing

- **Killed mutant:** The test suite detects the introduced code change by failing.
- **Survived mutant:** The test suite passes despite the code change.
- **Invalid mutant:** The mutant cannot be evaluated successfully, for example, because of a syntax or test-collection error.

The mutation score is calculated as:

**Mutation Score = Killed Mutants / (Killed Mutants + Survived Mutants) × 100**

Invalid mutants are excluded from this calculation.

## Current Implementation Status

The current prototype includes a sample microservice, automated tests, a mutation engine, JSON reporting, and a Streamlit dashboard. Further work may include broader mutation operators, more complex microservices, performance benchmarking, and cloud-native or CI/CD integration.

Mutation score and experimental results should be taken from the latest successful test run rather than assumed in advance.

## Future Enhancements

- Support additional mutation operators.
- Improve mutant generation and classification.
- Expand test coverage for complex microservices.
- Add performance benchmarking and experimental analysis.
- Explore integration with CI/CD pipelines and cloud-native environments.

## Repository

GitHub: https://github.com/asif6544/Intelligent-Microservice-Mutation-Testing

## Author

**MD ASIF**

Bachelor of Technology (Computer Science and Engineering)

IILM University, Greater Noida

## License

A license has not yet been specified. Add a suitable license file if you intend to distribute the project for reuse.
