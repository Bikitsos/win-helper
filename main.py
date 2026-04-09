from __future__ import annotations

import ctypes
import os
import shutil
import sys
from pathlib import Path
from subprocess import list2cmdline

from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QPlainTextEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


APP_VERSION = "1.0.0"

SCRIPT_DEFINITIONS = (
    (
        "Install VC Redistributables",
        "Install-VC-Redist.ps1",
    ),
    (
        "Install Winget",
        "Install-Winget.ps1",
    ),
    (
        "Set Cyprus Regional Settings",
        "Set-Cyprus-Regional-Settings.ps1",
    ),
    (
        "Install NetBird",
        "Install-NetBird.ps1",
    ),
    (
        "Activate Windows",
        "activate.cmd",
    ),
    (
        "Set Power to Ultimate",
        "Set-Ultimate-Power.ps1",
    ),
    (
        "Set Windows Light Theme",
        "Set-Windows-Light-Theme.ps1",
    ),
    (
        "Set Time Zone (Athens)",
        "Set-Time-Zone-Athens.ps1",
    ),
    (
        "Disable Windows Update",
        "Disable-Windows-Update.ps1",
    ),
)


class ScriptRunnerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Windows Helper v{APP_VERSION}")
        self.resize(780, 560)
        self.setMinimumSize(720, 520)

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.project_root = Path(sys._MEIPASS)
        else:
            self.project_root = Path(__file__).resolve().parent
            
        icon_path = self.project_root / "icon" / "app.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
            
        self.scripts_dir = self.project_root / "scripts"
        self.process: QProcess | None = None
        self.active_button: QPushButton | None = None
        self.active_button_title = ""

        app_font = QFont("Tahoma", 9)
        self.setFont(app_font)
        self.setStyleSheet(self._build_stylesheet())

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusValue")
        self.output_box = QPlainTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.output_box.setFont(QFont("Courier New", 9))
        self.output_box.setObjectName("outputBox")

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        main_layout.addWidget(self._build_header_panel())
        main_layout.addWidget(self._build_action_cards())
        main_layout.addWidget(self._build_status_panel())
        main_layout.addWidget(self._build_log_panel(), 1)

        self.setCentralWidget(central_widget)
        self._append_output(f"Project root: {self.project_root}")
        self._append_output("Running with administrator privileges.")

    def _build_stylesheet(self) -> str:
        return """
        QMainWindow {
            background: #c0c0c0;
        }
        QWidget#centralWidget {
            background: #c0c0c0;
        }
        QFrame#heroPanel, QFrame#sectionPanel, QFrame#statusPanel, QFrame#logPanel {
            background: #d4d0c8;
            border: 1px solid #808080;
        }
        QLabel#heroTitle {
            color: #000000;
            font-size: 12pt;
            font-weight: 700;
        }
        QLabel#heroSubtitle {
            color: #000000;
            font-size: 9pt;
        }
        QLabel#sectionLabel {
            color: #000000;
            font-size: 9pt;
            font-weight: 700;
        }
        QLabel#statusCaption {
            color: #000000;
            font-weight: 700;
        }
        QLabel#statusValue {
            color: #000000;
            font-weight: 700;
        }
        QPushButton {
            background: #d4d0c8;
            color: #000000;
            border-top: 1px solid #ffffff;
            border-left: 1px solid #ffffff;
            border-right: 1px solid #404040;
            border-bottom: 1px solid #404040;
            padding: 6px 10px;
            min-width: 96px;
        }
        QPushButton:hover {
            background: #d4d0c8;
        }
        QPushButton:pressed {
            border-top: 1px solid #404040;
            border-left: 1px solid #404040;
            border-right: 1px solid #ffffff;
            border-bottom: 1px solid #ffffff;
            padding-top: 7px;
            padding-left: 11px;
        }
        QPushButton:disabled {
            color: #6d6d6d;
        }
        QPushButton[actionCard="true"] {
            background: #d4d0c8;
            color: #000000;
            padding: 10px 12px;
            min-height: 56px;
            text-align: left;
            font-size: 9pt;
            font-weight: 400;
        }
        QPushButton[actionCard="true"]:hover {
            background: #d4d0c8;
        }
        QPushButton[actionCard="true"]:pressed {
            background: #d4d0c8;
        }
        QPushButton[actionCard="true"]:disabled {
            background: #d4d0c8;
            color: #6d6d6d;
        }
        QPlainTextEdit#outputBox {
            background: #ffffff;
            color: #000000;
            border: 1px solid #808080;
            selection-background-color: #0a246a;
            selection-color: #ffffff;
        }
        """

    def _build_header_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("heroPanel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        title = QLabel(f"Windows Helper v{APP_VERSION}")
        title.setObjectName("heroTitle")

        subtitle = QLabel(
            "Administrative utility for system setup and workstation configuration."
        )
        subtitle.setObjectName("heroSubtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        return panel

    def _build_action_cards(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("sectionPanel")

        layout = QGridLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(8)

        title = QLabel("Available Actions")
        title.setObjectName("sectionLabel")
        layout.addWidget(title, 0, 0, 1, 2)

        for index, (title, script_name) in enumerate(SCRIPT_DEFINITIONS):
            button = QPushButton(title)
            button.setProperty("actionCard", True)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.clicked.connect(
                lambda checked=False, name=script_name, label=title, source=button: self.run_script(
                    name, label, source
                )
            )

            row = (index // 3) + 1
            column = index % 3
            layout.addWidget(button, row, column)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        return panel

    def _build_status_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("statusPanel")

        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        caption = QLabel("Status:")
        caption.setObjectName("statusCaption")
        privilege = QLabel("Administrator")
        privilege.setObjectName("heroSubtitle")

        layout.addWidget(caption)
        layout.addWidget(self.status_label, 1)
        layout.addWidget(privilege, alignment=Qt.AlignmentFlag.AlignRight)
        return panel

    def _build_log_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("logPanel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        title = QLabel("Output")
        title.setObjectName("sectionLabel")

        layout.addWidget(title)
        layout.addWidget(self.output_box, 1)
        return panel

    def closeEvent(self, event) -> None:
        if self.process is not None and self.process.state() != QProcess.ProcessState.NotRunning:
            self.process.kill()
            self.process.waitForFinished(2000)
        super().closeEvent(event)

    def run_script(self, script_name: str, display_name: str, button: QPushButton) -> None:
        if self.process is not None:
            self._append_output("A script is already running. Wait for it to finish before starting another.")
            return

        script_path = self.scripts_dir / script_name
        if getattr(sys, 'frozen', False):
            # PyInstaller unpacks into %TEMP%, which gets blocked by some scripts (like MAS).
            # We copy it to APPDATA before executing.
            runtime_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / "win-helper-runtime"
            runtime_dir.mkdir(parents=True, exist_ok=True)
            run_path = runtime_dir / script_name
            try:
                shutil.copy2(script_path, run_path)
                script_path = run_path
            except Exception as e:
                self._append_output(f"Failed to copy script to runtime dir: {e}")

        if not script_path.exists():
            self.status_label.setText(f"Missing script: {script_name}")
            self._append_output(f"Script not found: {script_path}")
            return

        self.process = QProcess(self)
        self.active_button = button
        self.active_button_title = display_name
        self._set_buttons_enabled(False)
        button.setText(f"> {display_name}")
        self.status_label.setText(f"Running {display_name}")
        self._append_output("")

        if script_path.suffix.lower() == ".ps1":
            self._append_output(f"> powershell -ExecutionPolicy Bypass -File {script_path}")
            self.process.setProgram("powershell.exe")
            self.process.setArguments(
                [
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(script_path),
                ]
            )
        elif script_path.suffix.lower() in [".cmd", ".bat"]:
            self._append_output(f"> cmd /c {script_path}")
            self.process.setProgram("cmd.exe")
            self.process.setArguments(
                [
                    "/c",
                    str(script_path),
                ]
            )
        else:
            self._append_output(f"Unsupported script file: {script_path.suffix}")
            self._handle_process_finished(QProcess.ExitStatus.CrashExit)
            return

        self.process.setWorkingDirectory(str(script_path.parent))
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self._drain_process_output)
        self.process.finished.connect(self._handle_process_finished)
        self.process.errorOccurred.connect(self._handle_process_error)
        self.process.start()

    def _set_buttons_enabled(self, enabled: bool) -> None:
        for button in self.findChildren(QPushButton):
            button.setEnabled(enabled)

    def _drain_process_output(self) -> None:
        if self.process is None:
            return
        chunk = bytes(self.process.readAllStandardOutput()).decode(errors="replace")
        if chunk:
            self._append_output(chunk.rstrip())

    def _handle_process_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        status_text = "finished successfully" if exit_code == 0 else f"failed with exit code {exit_code}"
        if exit_status != QProcess.ExitStatus.NormalExit:
            status_text = "terminated unexpectedly"

        self._append_output(f"Process {status_text}.")
        self.status_label.setText(status_text.capitalize())
        self._cleanup_process()

    def _handle_process_error(self, process_error: QProcess.ProcessError) -> None:
        self._append_output(f"Process error: {process_error.name}")
        self.status_label.setText(f"Process error: {process_error.name}")

    def _cleanup_process(self) -> None:
        if self.process is not None:
            self.process.deleteLater()
            self.process = None

        if self.active_button is not None:
            self.active_button.setText(self.active_button_title)
            self.active_button = None
            self.active_button_title = ""

        self._set_buttons_enabled(True)

    def _append_output(self, text: str) -> None:
        if not text:
            self.output_box.appendPlainText("")
            return

        for line in text.splitlines() or [text]:
            self.output_box.appendPlainText(line)
        self.output_box.verticalScrollBar().setValue(self.output_box.verticalScrollBar().maximum())


def main() -> int:
    if not ensure_admin():
        return 0

    app = QApplication(sys.argv)
    window = ScriptRunnerWindow()
    window.show()
    return app.exec()


def is_windows_admin() -> bool:
    if sys.platform != "win32":
        return True

    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except OSError:
        return False


def ensure_admin() -> bool:
    if is_windows_admin():
        return True

    if getattr(sys, "frozen", False):
        executable = sys.executable
        parameters = list2cmdline(sys.argv[1:])
    else:
        executable = sys.executable
        parameters = list2cmdline([str(Path(__file__).resolve()), *sys.argv[1:]])

    result = ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        executable,
        parameters,
        str(Path(__file__).resolve().parent),
        1,
    )
    if result <= 32:
        print("Failed to elevate application.", file=sys.stderr)
        return False

    return False


if __name__ == "__main__":
    raise SystemExit(main())
