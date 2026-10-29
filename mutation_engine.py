
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SOURCE_FILE = BASE_DIR / "service.py"
TEST_FILE = BASE_DIR / "test_service.py"
MUTANT_FILE = BASE_DIR / "service_mutant.py"
MUTANT_TEST_FILE = BASE_DIR / "test_mutant_service.py"
REPORT_FILE = BASE_DIR / "mutation_report.json"


def generate_mutants(source_code):
    """Generate mutants using different mutation operators."""

    mutants = []

    operators = [
        ("== 200", "!= 200", "Equality operator"),
        ("!= 200", "== 200", "Inequality operator"),
        ("return True", "return False", "Boolean value"),
        ("return False", "return True", "Boolean value"),
    ]

    for original, replacement, name in operators:
        if original in source_code:
            mutated_code = source_code.replace(
                original, replacement, 1
            )

            if mutated_code != source_code:
                mutants.append({
                    "operator": name,
                    "original": original,
                    "replacement": replacement,
                    "code": mutated_code,
                })

    return mutants


def run_tests():
    """Run pytest against the current mutant."""

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            str(MUTANT_TEST_FILE),
        ],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        timeout=60,
    )

    output = result.stdout + "\n" + result.stderr

    if result.returncode == 0:
        return "SURVIVED", output

    if "ERROR collecting" in output or "ImportError" in output:
        return "INVALID", output

    if " failed" in output or "FAILED" in output:
        return "KILLED", output

    return "INVALID", output


def main():
    if not SOURCE_FILE.exists() or not TEST_FILE.exists():
        print("Error: service.py or test_service.py is missing.")
        return

    source_code = SOURCE_FILE.read_text(encoding="utf-8")
    test_code = TEST_FILE.read_text(encoding="utf-8")

    mutants = generate_mutants(source_code)

    results = []
    killed = 0
    survived = 0
    invalid = 0

    for index, mutant in enumerate(mutants, start=1):
        MUTANT_FILE.write_text(
            mutant["code"], encoding="utf-8"
        )

        mutated_test = test_code.replace(
            "from service import",
            "from service_mutant import",
        )

        MUTANT_TEST_FILE.write_text(
            mutated_test, encoding="utf-8"
        )

        status, output = run_tests()

        if status == "KILLED":
            killed += 1
        elif status == "SURVIVED":
            survived += 1
        else:
            invalid += 1

        results.append({
            "mutant_id": index,
            "operator": mutant["operator"],
            "change": (
                mutant["original"] + " -> "
                + mutant["replacement"]
            ),
            "status": status,
            "test_output": output.strip(),
        })

        print(f"Mutant {index}: {status} - {mutant['operator']}")

    total_valid = killed + survived
    score = (
        (killed / total_valid) * 100
        if total_valid > 0 else 0
    )

    report = {
        "total_mutants": len(mutants),
        "killed_mutants": killed,
        "survived_mutants": survived,
        "invalid_mutants": invalid,
        "mutation_score_percent": round(score, 2),
        "results": results,
    }

    REPORT_FILE.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print("\n--- Mutation Testing Report ---")
    print(f"Total mutants: {len(mutants)}")
    print(f"Killed mutants: {killed}")
    print(f"Survived mutants: {survived}")
    print(f"Invalid mutants: {invalid}")
    print(f"Mutation score: {score:.2f}%")
    print(f"Report saved to: {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
