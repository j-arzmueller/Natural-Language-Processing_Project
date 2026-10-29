# Setup

Each assignment is distributed in Moodle as a ZIP archive, for example
`assignment_01_ws2627.zip`. After unpacking it you have:

```
assignment_01/assignment_01.ipynb     the notebook
assignment_01/data/                   the data
START_HERE.md                         short instructions for this assignment
SETUP.md                              this file
pyproject.toml, uv.lock               package versions for a local installation
requirements.txt                      the same packages for pip
tools/check_notebook.py               a completeness check for your notebook
```

You can work on Google Colab, which needs no installation, or on your own computer, which
takes about ten minutes to set up once. Both are supported.

Teams of two submit one notebook, named with both matriculation numbers including leading
zeros:

```
assignment_01_<matriculation 1>_<matriculation 2>.ipynb      for example assignment_01_01234567_12345678.ipynb
```

---

## Option A: Google Colab

You need a Google account.

1. Open <https://colab.research.google.com> and sign in.
2. Upload the notebook with *File → Upload notebook* and select
   `assignment_01/assignment_01.ipynb` from the unpacked folder. Colab saves it in your Google
   Drive, in the folder *Colab Notebooks*.
3. Rename it to `assignment_01_<matriculation 1>_<matriculation 2>.ipynb` (*File → Rename*).
4. Run the notebook from top to bottom. The first cell installs missing packages and prints
   `Running on: Google Colab`. The notebook downloads the data itself; upload files from the
   ZIP only if the assignment's `START_HERE.md` says so.

To continue later, open your renamed notebook from Google Drive (*File → Open notebook*).
Uploading the original again gives you an empty notebook.

To submit, run all cells so that the outputs are saved, download the notebook
(*File → Download → Download .ipynb*) and upload it to Moodle.

Two points to note:

- Colab resets the runtime after some idle time. Variables and downloaded files are lost;
  your code is kept. Use *Runtime → Restart and run all* to continue.
- Assignments 1 and 2 run on the CPU. For Assignments 3 and 4, select a GPU with
  *Runtime → Change runtime type → T4 GPU*.

---

## Option B: your own computer

The course uses `uv`, which installs Python and the required packages into a folder `.venv`
inside the assignment folder, separate from anything else on your computer. You do not need
Anaconda or a separate Python installation.

### 1. Unpack the archive

Unpack the ZIP into a folder you can find again, for example
`Documents/NLP/assignment_01_ws2627`.

### 2. Install uv (once per computer)

macOS and Linux (Terminal):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close the terminal, open a new one and check the installation with `uv --version`.

### 3. Install the packages

Change into the unpacked folder (it contains `pyproject.toml`) and run:

```bash
cd path/to/assignment_01_ws2627
uv sync                       # Assignments 1 and 2
uv sync --extra deep          # Assignments 3 and 4 (adds PyTorch and transformers, a large download)
```

The first run downloads the packages and takes a few minutes. Repeat this step in the folder
of each new assignment; later runs reuse the downloaded packages and are fast.

### 4. Start JupyterLab

```bash
uv run jupyter lab
```

Open `assignment_01/assignment_01.ipynb` and save a copy under your team's file name
(*File → Save Notebook As…*) in the same folder, so that the notebook finds its `data`
folder. Work in that copy.

Stop JupyterLab with `Ctrl+C` in the terminal. To continue later, change into the folder and
run `uv run jupyter lab` again; `uv sync` is not needed a second time.

### 5. Submit

Upload the notebook to Moodle with its outputs saved; one upload per team. Before that you
can run the same completeness check that is used for grading:

```bash
uv run --with nbconvert --with ipykernel jupyter nbconvert --to notebook --execute \
    --allow-errors --output executed.ipynb assignment_01/assignment_01_01234567_12345678.ipynb
uv run python tools/check_notebook.py assignment_01/executed.ipynb
```

Use your own file name in the first command. The check reports errors, unfinished tasks,
failed visible tests and unanswered written blocks. It does not compute a grade.

---

## Working with the notebook

- Cells run in order and share their variables. A `NameError` usually means that a cell
  above has not been run.
- Replace every `### YOUR CODE HERE` / `raise NotImplementedError()` with your code and
  delete the `raise` line.
- Each task is followed by a test cell. `Task N.N passed` means that the visible tests pass;
  otherwise the `AssertionError` message states what was expected.
- Before submitting, restart the kernel and run all cells (*Kernel → Restart Kernel and Run
  All Cells*; on Colab *Runtime → Restart and run all*). Grading runs the notebook from top to
  bottom, and an error stops everything after it.

---

## Troubleshooting

**`uv: command not found` or `'uv' is not recognized`.** Open a new terminal after the
installation. On macOS and Linux, if the problem remains, run
`export PATH="$HOME/.local/bin:$PATH"`.

**`uv sync` cannot find `pyproject.toml`.** The terminal is not in the unpacked folder; see
step 3.

**`uv sync` fails with a network or SSL error.** This is often caused by a VPN or proxy. Try
a different network.

**JupyterLab shows "No Kernel", or the notebook reports `ModuleNotFoundError`.** JupyterLab
was not started with `uv run`. Stop it and start it again with `uv run jupyter lab` from the
unpacked folder. If the error remains, run `uv sync` again and check its output.

**`NameError: name '...' is not defined`.** A cell above was skipped or the kernel was
restarted. Run all cells again.

**`CERTIFICATE_VERIFY_FAILED` during a download.** Start JupyterLab with `uv run jupyter lab`;
the notebook then uses the certificates of the `certifi` package. On macOS, running
*Install Certificates.command* in the Python folder under *Applications* also solves it.

**The download cell fails.** On your own computer the data is included in the ZIP; make sure
the notebook is in the `assignment_01` folder next to `data`. On Colab, the error message
lists the download links: download the files, upload them into a folder `data` in the file
panel on the left, and run the cell again.

**Colab: your changes are missing.** You opened the original notebook instead of your renamed
copy. Open the copy from Google Drive.

**Colab: everything is slow.** The free tier limits heavy use. For Assignments 3 and 4, check
that a GPU runtime is selected.

**Other problems.** Post in the Moodle forum with the cell, the full error message as text,
and whether you use Colab or your own computer, including the operating system.

---

## Without uv

If `uv` cannot be used, Python 3.10 or newer with `pip` also works. This route is not
supported by the course staff. In the unpacked folder:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```
