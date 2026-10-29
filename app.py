
import json
import subprocess
import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ENGINE_FILE = BASE_DIR / "mutation_engine.py"
REPORT_FILE = BASE_DIR / "mutation_report.json"

st.set_page_config(
    page_title="Intelligent Mutation Testing",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Intelligent Microservice Mutation Testing")
st.write(
    "Analyze test quality by generating mutants "
    "and evaluating their test results."
)

st.sidebar.header("Project Information")
st.sidebar.write("**Project:** PT436")
st.sidebar.write("**Engine:** Python + pytest")
st.sidebar.write("**Dashboard:** Streamlit")

if st.button("▶ Run Mutation Testing", type="primary"):
    if not ENGINE_FILE.exists():
        st.error("mutation_engine.py was not found in the project folder.")
    else:
        with st.spinner("Running mutation tests..."):
            try:
                result = subprocess.run(
                    [sys.executable, str(ENGINE_FILE)],
                    cwd=BASE_DIR,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                if result.stdout:
                    st.code(result.stdout, language="text")

                if result.stderr:
                    st.text_area(
                        "Test logs / errors",
                        result.stderr,
                        height=150
                    )

                if result.returncode != 0:
                    st.error("The mutation engine exited with an error.")
                elif REPORT_FILE.exists():
                    st.success("Mutation testing finished.")
                else:
                    st.warning("No JSON report was generated.")

            except subprocess.TimeoutExpired:
                st.error("Testing timed out after 120 seconds.")
            except Exception as error:
                st.error(f"Could not run the engine: {error}")

st.divider()
st.subheader("Mutation Testing Results")

if REPORT_FILE.exists():
    try:
        with REPORT_FILE.open("r", encoding="utf-8") as file:
            report = json.load(file)

        score = report.get("mutation_score_percent")
        killed = report.get("killed_mutants", 0)
        survived = report.get("survived_mutants", 0)
        invalid = report.get("invalid_mutants", 0)
        total = report.get("total_mutants", 0)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Mutation Score",
            f"{score:.2f}%" if isinstance(score, (int, float))
            else "N/A"
        )
        col2.metric("Killed", killed)
        col3.metric("Survived", survived)
        col4.metric("Invalid", invalid)

        st.progress(
            min(max(float(score or 0) / 100, 0), 1)
        )

        st.write(f"**Total mutants:** {total}")

        st.subheader("Detailed Report")
        st.json(report)

        st.download_button(
            "⬇ Download JSON Report",
            data=json.dumps(report, indent=4),
            file_name="mutation_report.json",
            mime="application/json"
        )

    except (json.JSONDecodeError, OSError) as error:
        st.error(f"Could not read the JSON report: {error}")
else:
    st.info(
        "No report found yet. Click 'Run Mutation Testing' "
        "to generate results."
    )

st.caption("PT436 | Intelligent Microservice Mutation Testing Framework")
