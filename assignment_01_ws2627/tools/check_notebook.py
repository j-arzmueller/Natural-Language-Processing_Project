"""Check an executed notebook: did every visible test pass?

Students can run this themselves before uploading:

    uv run --with nbconvert --with ipykernel jupyter nbconvert --to notebook --execute \
        --output /tmp/executed.ipynb assignments/assignment_01/assignment_01_12345678.ipynb
    uv run python tools/check_notebook.py /tmp/executed.ipynb

It reports, in plain language:

* cells that raised an error,
* cells still containing `raise NotImplementedError()`,
* which `Task N.N passed` messages are missing,
* whether the three written blocks have been answered,
* whether the submission check at the end succeeded.

It does NOT compute a grade — the hidden tests are not part of this.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import nbformat

EXPECTED_TASKS = {
    "01": ["1.1", "2.1", "2.2", "2.3",
           "3.1", "3.2", "3.3", "3.4",
           "4.1", "4.2", "4.3", "4.4",
           "5.1", "5.2", "5.3", "5.4"],
    "02": ["1.1", "2.1", "2.2", "2.3", "2.4",
           "3.1", "3.2", "3.3", "4.1", "4.2"],
    "03": ["1.1", "1.2", "1.3", "2.1", "2.2", "3.1", "3.2",
           "4.1", "4.2", "4.3"],
    "04": ["1.1", "1.2", "1.3", "2.1", "2.2", "3.1", "3.2"],
}

# The written blocks: cell id in the master notebook -> what to call it. These are worth
# checking loudly, because their average multiplies the coding score: an unanswered block
# costs a third of the whole grade, and it is the one mistake a student cannot see from
# "all tests passed".
WRITTEN_BLOCKS = {
    "01": {"cell-041": "Task 2.4", "cell-055": "Task 3.5", "cell-097": "Part 6"},
    "02": {"cell-035": "Task 2.5", "cell-066": "Part 5"},
    "03": {"cell-035": "Task 2.3", "cell-065": "Part 5"},
    "04": {"cell-042": "Block 1 (LoRA)", "cell-049": "Block 2 (picture and groups)"},
}
# Colab and some converters drop cell ids, so fall back to the heading each answer
# cell starts with. Without this a perfectly correct notebook was reported "0/3 answered".
WRITTEN_HEADINGS = {
    "Task 1.3": "### Task 1.3 — question 1",
    "Task 3.4": "### Task 3.4 — question 1",
    "Task 2.4": "### Task 2.4 — question 1",
    "Task 2.6": "### Task 2.6 — question 1",
    "Task 3.5": "### Task 3.5 — question 1",
    "Task 3.6": "### Task 3.6 — question 1",
    "Part 6": "### Part 6 — question 1",
    "Task 2.5": "### Task 2.5 — question 1",
    "Part 5": "### Part 5 — question 1",
    "Task 2.3": "### Task 2.3 — question 1",
    "Block 1 (LoRA)": "### Block 1 — question 1",
    "Block 2 (picture and groups)": "### Block 2 — question 1",
}
PLACEHOLDER = "_(write here)_"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("notebook", type=Path, help="an already executed .ipynb")
    parser.add_argument("--assignment", default=None, choices=sorted(EXPECTED_TASKS),
                        help="defaults to the number in the file name, e.g. assignment_02_...")
    args = parser.parse_args()

    notebook = nbformat.read(args.notebook, as_version=4)

    errors, not_implemented, printed = [], [], set()
    submission_ok = False

    for number, cell in enumerate(notebook.cells, 1):
        if cell.cell_type != "code":
            continue
        if "raise NotImplementedError" in cell.source:
            not_implemented.append(number)
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                errors.append((number, output.get("ename", "Error"),
                               (output.get("evalue") or "").split("\n")[0][:200]))
            text = output.get("text", "")
            printed.update(re.findall(r"Task (\d+\.\d+) passed", text))
            if "Submission check passed" in text:
                submission_ok = True

    if args.assignment is None:
        match = re.search(r"assignment_(\d{2})", args.notebook.name)
        args.assignment = match.group(1) if match and match.group(1) in EXPECTED_TASKS else "01"
    expected = EXPECTED_TASKS[args.assignment]
    missing = [task for task in expected if task not in printed]

    # The written blocks. A block still holding placeholders is not finished; a block whose
    # cell is gone altogether cannot be graded at all.
    blocks = WRITTEN_BLOCKS.get(args.assignment, {})
    by_id = {cell.get("id"): cell for cell in notebook.cells}
    written_problems = []
    for cell_id, label in blocks.items():
        cell = by_id.get(cell_id)
        if cell is None:
            heading = WRITTEN_HEADINGS.get(label, "")
            cell = next((c for c in notebook.cells
                         if c.cell_type == "markdown" and heading and heading in c.source), None)
        if cell is None:
            written_problems.append((label, "the answer cell is missing from the notebook"))
            continue
        left = cell.source.count(PLACEHOLDER)
        if left:
            written_problems.append(
                (label, f"{left} `{PLACEHOLDER}` placeholder(s) still there")
            )

    print(f"Checked {args.notebook.name}\n")
    print(f"  visible tests passed : {len(printed)}/{len(expected)}")
    print(f"  cells with errors    : {len(errors)}")
    print(f"  unfinished cells     : {len(not_implemented)}")
    print(f"  written blocks       : {len(blocks) - len(written_problems)}/{len(blocks)} answered")
    print(f"  submission check     : {'passed' if submission_ok else 'did not pass'}\n")

    if not_implemented:
        print("Cells that still contain `raise NotImplementedError()`:")
        print(f"  cell number(s): {', '.join(map(str, not_implemented))}")
        print("  -> replace the placeholder with your own code and delete that line.\n")

    if errors:
        print("Cells that raised an error:")
        for number, name, message in errors[:10]:
            print(f"  cell {number}: {name}: {message}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
        print("  -> fix the first one; later errors are often only a consequence of it.\n")

    if missing:
        print(f"Missing test confirmations: {', '.join(missing)}")
        print("  -> those tasks are unsolved, or their test cell did not run.\n")

    if written_problems:
        print("Written blocks that are not finished:")
        for label, problem in written_problems:
            print(f"  {label}: {problem}")
        count_word, share = {2: ("two", "half"), 3: ("three", "a third")}.get(
            len(blocks), (str(len(blocks)), "part"))
        print(f"  -> these {count_word} blocks are a 0.0-1.0 MULTIPLIER on your coding points, not")
        print(f"     a few extra marks. An unanswered block costs you {share} of your grade,")
        print("     however many tests pass. Answer them with your own numbers.\n")

    if not (errors or not_implemented or missing or written_problems) and submission_ok:
        print("Everything is in order.")
        print("Hand in this .ipynb file (with outputs saved) in Moodle.")
        print("(This does not show your grade — hidden tests run after the deadline.)")
        return 0

    print("Your submission is NOT ready. Fix the points above, then restart and run")
    print("everything again (Jupyter: Kernel -> Restart Kernel and Run All Cells;")
    print("Colab: Runtime -> Restart and run all).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
