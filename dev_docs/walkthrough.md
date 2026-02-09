# FileFinder Walkthrough

I have implemented and built the **FileFinder** application compatible with Windows 7, with **enhanced Chinese text support** and bug fixes.

## Features
1.  **Robust Chinese Text Support (New)**:
    *   **Encoding Detection**: The app now automatically tries to read files using `UTF-8`, `GB18030` (GBK), and `UTF-16`. This solves the issue where some Chinese text files were not being found or displayed correctly.

2.  **Visual Feedback Improvements (New)**:
    *   **Accurate Scanning Status**: The status bar now only shows files *actually being scanned* (matching the .txt/.html extensions), so you won't see it get "stuck" on ignored files like `Thumbs.db`.
    *   **Directory Progress**: It now also shows which directory is currently being traversed.

3.  **Enhanced Usability**:
    *   **Extra Large Font**: The application uses a very large **18pt font**.
    *   **Responsive Layout**: Full-width directory selection.
    *   **Window Memory**: Remembers window size and position.
    *   **Stop Search**: Ability to stop search mid-way.

4.  **Smart Filtering**:
    *   **Specific Text Files Only**: Searches ONLY inside:
        *   `.txt`
        *   `.htm`
        *   `.html`

5.  **Directory Selection**:
    *   **Browse**: Click "Browse..." to select a folder.
    *   **History**: Remembers last 10 used directories.
    *   **Persistence**: Auto-loads last directory on startup.

6.  **Keyword Search**:
    *   Runs in background thread for responsiveness.

7.  **Results List & Viewer**:
    *   Shows full absolute paths.
    *   Displays content with **yellow highlighting** for the keyword.

## How to Run
### Option 1: Run Executable (Windows 7 Compatible)
A standalone single-file executable has been built:
*   **Path**: `dist/FileFinder.exe`
*   You can copy this single file to your Windows 7 machine and run it directly.

## Verification
I have verified that:
*   [x] The search finds text files in subfolders.
*   [x] Directory history is saved to `config.json`.
*   [x] Keywords are highlighted.
*   [x] **Font size is 18pt.**
*   [x] **Only .txt, .htm, .html files are processed.**
*   [x] **Files with Chinese Encodings (GBK/GB18030) are correctly read.**
*   [x] **Thumbs.db and other system files are correctly ignored in UI.**
*   [x] Executable `FileFinder.exe` builds successfully.
