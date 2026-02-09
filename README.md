# FileFinder (Windows 7 Compatible)

This project is designed to run on Windows 7 using Python 3.8 and PyQt5.

## Prerequisites

1.  **Python 3.8**: You must have Python 3.8 installed. Ensure it is added to your PATH.
    *   (Note: Newer versions like 3.9+ do not support Windows 7)

## Installation

1.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

```bash
python main.py
```

## Building executable for Windows 7

To create a standalone `.exe`:

```bash
pyinstaller --onefile --noconsole --name FileFinder main.py
```

The output executable will be inside the `dist` folder.
