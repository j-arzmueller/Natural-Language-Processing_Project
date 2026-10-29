# Assignment 01: getting started

This archive contains the notebook, the data and a checking tool for Assignment 01. You
can work on Google Colab or on your own computer; `SETUP.md` describes both in detail.

## Google Colab

1. Open <https://colab.research.google.com> and upload
   `assignment_01/assignment_01.ipynb` (*File → Upload notebook*).
2. Rename it to `assignment_01_<matriculation 1>_<matriculation 2>.ipynb` (*File → Rename*).
   Colab stores it in your Google Drive under *Colab Notebooks*; open it from there when you
   continue later.
3. Run the cells from top to bottom. The first cell installs missing packages.
   The notebook downloads its own data if it is missing.
4. To submit, download the notebook (*File → Download → Download .ipynb*).

## Your own computer

Install `uv` as described in `SETUP.md`, then run in this folder:

```bash
uv sync
uv run jupyter lab
```

Open `assignment_01/assignment_01.ipynb`, save a copy as
`assignment_01_<matriculation 1>_<matriculation 2>.ipynb` (*File → Save Notebook As…*)
and work in that copy.

## Submission

Each team of two submits one notebook, named with both matriculation numbers including
leading zeros, for example `assignment_01_01234567_12345678.ipynb`. One team member
uploads it to Moodle; the grade applies to both. Submit only the notebook, with its outputs
saved.

Before submitting:

1. Restart the kernel and run all cells (*Kernel → Restart Kernel and Run All Cells*; on
   Colab *Runtime → Restart and run all*). The notebook must run without errors.
2. Every test cell prints `Task N.N passed`, and the submission check at the end prints
   `Submission check passed.`
3. All three written blocks (Tasks 2.4, 3.5 and Part 6) are answered, with no `_(write here)_` left.

If you work locally, you can run the same completeness check that is used for grading:

```bash
uv run --with nbconvert --with ipykernel jupyter nbconvert --to notebook --execute \
    --allow-errors --output executed.ipynb assignment_01/assignment_01_01234567_12345678.ipynb
uv run python tools/check_notebook.py assignment_01/executed.ipynb
```

## Grading

```
points = coding points (0-50) x mean of the three written-block weights (0.0-1.0)
```

The 16 coding tasks are graded automatically, including hidden tests on new
inputs; each task earns its full points or none. Each written block is read by the teaching
staff and given a weight between 0.0 and 1.0. The mean of these weights multiplies the coding
points, so a notebook without written answers receives 0 points. Answers must refer to the
results in your own notebook.

The course has 1000 points: 50 for each of the four assignments and 800 for the supervised
exercise exam, which must be passed on its own. AI tools are permitted for the assignments;
the exam tests the same skills without them.

## Content warning

The dataset contains real hate speech, including racism, sexism, religious hatred, slurs and
attacks on people with disabilities. Some printed examples are offensive. Use the data only
for this course and do not redistribute it.

## Questions

Post questions in the Moodle forum of the assignment. Include the full error message as
text, the cell it came from, and whether you work on Colab or on your own computer.
