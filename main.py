import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, 
                             QPushButton, QListWidget, QTextEdit, QFileDialog, QLineEdit, 
                             QHBoxLayout, QSplitter, QComboBox, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont, QPainter, QBrush, QPaintEvent, QIcon

CONFIG_FILE = "config.json"

class SearchThread(QThread):
    match_found = pyqtSignal(str)
    current_file = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, directory, keyword):
        super().__init__()
        self.directory = directory
        self.keyword = keyword
        self.running = True

    def run(self):
        if not self.directory or not self.keyword:
            self.finished.emit()
            return
        
        # Prepare keywords (split by whitespace, remove empty)
        keywords = [k.strip().lower() for k in self.keyword.split() if k.strip()]
        
        if not keywords:
             self.finished.emit()
             return

        # Extensions to consider as text files
        text_extensions = {
            '.txt', '.htm', '.html'
        }

        for root, dirs, files in os.walk(self.directory):
            if not self.running:
                break
            
            # Update status for directory to show progress through structure
            self.current_file.emit(f"正在扫描目录: {root}")
            
            for file in files:
                if not self.running:
                    break
                
                # Check extension FIRST
                _, ext = os.path.splitext(file)
                if ext.lower() not in text_extensions:
                    continue

                start_path = os.path.join(root, file)
                self.current_file.emit(f"正在扫描文件: {start_path}")
                
                # Check FILENAME first
                file_lower = file.lower()
                if all(k in file_lower for k in keywords):
                    self.match_found.emit(os.path.abspath(start_path))
                    continue # Found by filename, skip content check

                # Try to read file to check if it contains the keyword
                found = False
                encodings_to_try = ['utf-8', 'gb18030', 'utf-16', 'gbk', 'big5']
                
                for enc in encodings_to_try:
                    try:
                        with open(start_path, 'r', encoding=enc) as f:
                            content = f.read()
                            content_lower = content.lower()
                            # Check if ALL keywords are in content
                            if all(k in content_lower for k in keywords):
                                self.match_found.emit(os.path.abspath(start_path))
                                found = True
                        if found:
                            break
                    except Exception:
                        continue
        
        self.finished.emit()
                        
    def stop(self):
        self.running = False

class ScrollBarHighlighter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(8) # Width of the highlighter strip
        self.positions = [] # List of relative positions (0.0 to 1.0)

    def set_matches(self, positions):
        self.positions = positions
        self.update()

    def paintEvent(self, event):
        if not self.positions:
            return
            
        painter = QPainter(self)
        brush = QBrush(QColor("yellow")) # Color of the highlights
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        
        h = self.height()
        for pos in self.positions:
            y = int(pos * h)
            # Draw a small rectangle
            painter.drawRect(0, y, self.width(), 3) 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("文件搜索器 - 3S Lab")
        self.resize(800, 600)
        
        # Set application icon if available
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Config Data
        self.history = []
        self.last_path = ""

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- Directory Selection Section ---
        dir_layout = QHBoxLayout()
        
        dir_label = QLabel("目录:")
        dir_layout.addWidget(dir_label)

        self.dir_combo = QComboBox()
        self.dir_combo.setEditable(True)
        dir_layout.addWidget(self.dir_combo, 1)

        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)

        main_layout.addLayout(dir_layout)

        # --- Search Section ---
        search_layout = QHBoxLayout()
        
        keyword_label = QLabel("关键字:")
        search_layout.addWidget(keyword_label)

        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("请输入要搜索的文本...")
        self.keyword_input.returnPressed.connect(self.start_search)
        search_layout.addWidget(self.keyword_input, 1)

        self.search_btn = QPushButton("搜索")
        self.search_btn.clicked.connect(self.start_search)
        search_layout.addWidget(self.search_btn)

        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_search)
        self.stop_btn.setEnabled(False)
        search_layout.addWidget(self.stop_btn)

        main_layout.addLayout(search_layout)

        # --- Splitter for Results and Content ---
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: File List
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.display_file_content)
        splitter.addWidget(self.file_list)

        # Right: Content Viewer + Scrollbar Highlighter
        # We need a container widget to hold the text edit and the highlighter side-by-side
        right_widget = QWidget()
        right_layout = QHBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(2)

        self.content_viewer = QTextEdit()
        self.content_viewer.setReadOnly(True)
        # Widen the vertical scrollbar
        self.content_viewer.setStyleSheet("""
            QScrollBar:vertical {
                width: 30px;
            }
        """)
        right_layout.addWidget(self.content_viewer)
        
        self.highlighter = ScrollBarHighlighter()
        right_layout.addWidget(self.highlighter)

        splitter.addWidget(right_widget)
        
        # Adjust splitter sizes (30% list, 70% content)
        splitter.setSizes([240, 560])

        main_layout.addWidget(splitter)
        
        # Status Bar
        self.status_label = QLabel("就绪")
        self.statusBar().addWidget(self.status_label)

    def browse_directory(self):
        current_path = self.dir_combo.currentText()
        if not os.path.isdir(current_path):
            current_path = os.getcwd()
            
        directory = QFileDialog.getExistingDirectory(self, "选择目录", current_path)
        if directory:
            # Update combo box
            self.update_directory_combo(directory)

    def update_directory_combo(self, directory):
        # Prevent duplicates
        if self.dir_combo.findText(directory) == -1:
            self.dir_combo.insertItem(0, directory)
        self.dir_combo.setCurrentText(directory)

    def start_search(self):
        directory = self.dir_combo.currentText().strip()
        keyword = self.keyword_input.text().strip()

        if not directory or not os.path.isdir(directory):
            QMessageBox.warning(self, "错误", "请选择一个有效的目录。")
            return
        
        if not keyword:
            QMessageBox.warning(self, "错误", "请输入关键字。")
            return

        # Prepare UI
        self.file_list.clear()
        self.content_viewer.clear()
        self.highlighter.set_matches([]) # Clear highlighter
        self.search_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("正在搜索...")
        self.save_settings() # Save history on search

        # Start Thread
        self.search_thread = SearchThread(directory, keyword)
        self.search_thread.match_found.connect(self.add_file_to_list)
        self.search_thread.current_file.connect(self.update_status)
        self.search_thread.finished.connect(self.search_finished)
        self.search_thread.start()

    def stop_search(self):
        if hasattr(self, 'search_thread') and self.search_thread.isRunning():
            self.search_thread.stop()
            self.status_label.setText("正在停止...")

    def update_status(self, message):
        self.status_label.setText(message)

    def add_file_to_list(self, file_path):
        self.file_list.addItem(file_path)

    def search_finished(self):
        self.search_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        count = self.file_list.count()
        self.status_label.setText(f"搜索完成。找到 {count} 个文件。")

    def display_file_content(self, item):
        file_path = item.text()
        keyword = self.keyword_input.text()

        content = ""
        encodings_to_try = ['utf-8', 'gb18030', 'utf-16', 'gbk', 'big5']
        
        for enc in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                break # Success
            except Exception:
                continue
        
        if content:
            self.content_viewer.setPlainText(content)
            self.highlight_keyword(keyword)
            self.status_label.setText(f"正在查看: {file_path}")
        else:
            self.content_viewer.setPlainText(f"读取文件错误: 无法解码 {encodings_to_try}")
            self.highlighter.set_matches([])

    def highlight_keyword(self, keyword_msg):
        if not keyword_msg:
            self.highlighter.set_matches([])
            self.content_viewer.setExtraSelections([])
            return
            
        keywords = [k.strip() for k in keyword_msg.split() if k.strip()]
        if not keywords:
            self.highlighter.set_matches([])
            self.content_viewer.setExtraSelections([])
            return

        # Prepare for highlighting using ExtraSelections (non-destructive)
        extra_selections = []
        
        # We'll use a specific format for the highlight
        selection_format = QTextCharFormat()
        selection_format.setBackground(QColor("yellow"))
        selection_format.setForeground(QColor("black"))

        doc = self.content_viewer.document()
        total_length = doc.characterCount()
        match_positions = []

        # Iterate over all keywords
        for key in keywords:
            # Use a fresh cursor for searching to avoid focus/selection side effects
            cursor = QTextCursor(doc)
            
            while True:
                cursor = doc.find(key, cursor)
                if cursor.isNull():
                    break
                
                # Create an extra selection for this match
                selection = QTextEdit.ExtraSelection()
                selection.format = selection_format
                selection.cursor = cursor
                extra_selections.append(selection)
                
                # Calculate relative position for scrollbar
                pos = cursor.position()
                if total_length > 0:
                    match_positions.append(pos / total_length)
        
        # Apply all highlights at once
        self.content_viewer.setExtraSelections(extra_selections)
        self.highlighter.set_matches(match_positions)

    def load_settings(self):
        if not os.path.exists(CONFIG_FILE):
            return

        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                
            history = data.get("history", [])
            last_path = data.get("last_path", "")

            # Filter out non-existent paths from history? Maybe not, just prompt if invalid.
            # But requirement says "If cannot find, path is empty". 
            
            # Load history items
            if isinstance(history, list):
                for path in history:
                    if os.path.isdir(path):
                        self.dir_combo.addItem(path)

            # Set last path if valid
            if last_path and os.path.isdir(last_path):
                index = self.dir_combo.findText(last_path)
                if index != -1:
                    self.dir_combo.setCurrentIndex(index)
                else:
                    self.dir_combo.addItem(last_path)
                    self.dir_combo.setCurrentText(last_path)
            else:
                 self.dir_combo.setCurrentIndex(-1)
                 
            # Restore window geometry
            geometry_hex = data.get("geometry")
            if geometry_hex:
                 from PyQt5.QtCore import QByteArray
                 self.restoreGeometry(QByteArray.fromHex(geometry_hex.encode()))
            else:
                 self.showMaximized()
                 
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.showMaximized() # Fallback

    def save_settings(self):
        current_path = self.dir_combo.currentText()
        
        # Get current items
        items = [self.dir_combo.itemText(i) for i in range(self.dir_combo.count())]
        
        # Ensure current path is at top and unique
        if current_path in items:
            items.remove(current_path)
        items.insert(0, current_path)
        
        # Limit history
        items = items[:10]

        # Save geometry
        from PyQt5.QtCore import QByteArray
        geometry = self.saveGeometry().toHex().data().decode()

        data = {
            "history": items,
            "last_path": current_path,
            "geometry": geometry
        }
        
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def closeEvent(self, event):
        # Save on exit as well
        self.save_settings()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Increase global font size for better visibility
    font = QFont()
    font.setPointSize(18)
    app.setFont(font)
    
    window = MainWindow()
    # Note: window.show() is called inside load_settings logic (maximized or restored)
    # But checking logic above: self.showMaximized() is called in load_settings if no geometry.
    # We should ensure window is shown. 
    if not window.isVisible():
         window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
