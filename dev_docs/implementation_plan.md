# Data & Search Implementation Plan

## Goal
Enhance the FileFinder application with larger fonts, search progress feedback, a stop button, and window state persistence.

## Proposed Changes
### Core Application Logic
#### [MODIFY] [main.py](file:///C:/Users/shenl/Documents/FileFinder/main.py)
- **Global Font**:
    - In `main()`, before creating `MainWindow`, set `app.setFont(QFont("Segoe UI", 12))` (or similar readable font, size 12-14).
- **Search Logic (`SearchThread`)**:
    - Add signal `current_file_checked(str)`.
    - Is `os.walk` loop, emit `current_file_checked(path)` for every file visited (or every N files to avoid UI flooding, but for now every file is requested).
    - Add check `if not self.running: break` inside the inner file loop.
- **UI Update (`MainWindow`)**:
    - **Stop Button**: Add `self.stop_btn` next to `Search`. Initially disabled.
    - **Status Bar**: Connect `current_file_checked` signal to `self.status_label.setText`.
- **Window Persistence**:
    - **Save**: In `save_settings`, save `self.geometry()` and `self.isMaximized()` (or `windowState`).
        - Use `saveGeometry().toHex()` for storage in JSON.
    - **Load**: In `load_settings`:
        - Check for saved geometry.
        - If found, `restoreGeometry`.
        - If NOT found, `self.showMaximized()`.

## Verification Plan
### Manual Verification
- **Test 1**: **Font**: Launch app, verify text is significantly larger.
- **Test 2**: **Stop**: Start search in a large folder. Click Stop. Verify status says "Stopped" (or similar) and search allows restarting.
- **Test 3**: **Status**: Watch status bar during search. Verify it updates with paths.
- **Test 4**: **Window**:
    - First run (no config): App should start maximized.
    - Resize/Move, Close. Reopen. App should restore position/size.
