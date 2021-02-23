"""
===============
Stream handlers
===============
"""

import os
import sys
from datetime import datetime
from typing import Optional, Literal, List, Callable

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTimer, Qt
from PySide2.QtWidgets import QMdiSubWindow, QMenu, QAction, QMenuBar

from .subprocess_handler import LoadSubprocess
from .config_manager import ConfigManager


########################################################################
class ExtensionMenu:
    """MDIArea menu for extensions."""

    # ----------------------------------------------------------------------
    def build_menu_visualization(self, visualization: bool, debugger: Optional[bool] = False) -> None:
        """Menu for visualizations."""
        self.menubar = QMenuBar(self)
        self.menubar.clear()
        self.menubar.setMinimumWidth(1e4)

        self.accent_menubar = QMenuBar(self)

        # Title
        if debugger:
            menu_stimuli = QMenu(f"Debugging: {visualization}")
        else:
            if visualization:
                menu_stimuli = QMenu(f'{visualization } 🞃')
            else:
                menu_stimuli = QMenu('Data analysis 🞃')

        # Add visualizations
        for viz in self.extensions_list:
            if viz != visualization:
                menu_stimuli.addAction(QAction(viz, menu_stimuli,
                                               triggered=self.set_extension(viz)))

        self.accent_menubar.addMenu(menu_stimuli)

        # Menu with accent color
        self.accent_menubar.setStyleSheet(f"""
        QMenuBar::item {{
            background-color: {os.getenv('QTMATERIAL_PRIMARYCOLOR', '#ffffff')};
            color: {os.getenv('QTMATERIAL_PRIMARYTEXTCOLOR', '#ffffff')};
            }}""")

        # Set the menu in first position
        self.menubar.setCornerWidget(
            self.accent_menubar, corner=Qt.TopLeftCorner)

        # View
        menu_view = QMenu("View")
        if visualization:

            menu_view.addAction(
                QAction('Reload', menu_view, triggered=self.reload))

            menu_view.addAction(
                QAction('Save capture', menu_view, triggered=self.save_img))
            if not debugger:
                menu_view.addSeparator()
                menu_view.addAction(
                    QAction('Close', menu_view, triggered=self.remove))
        else:
            menu_view.setEnabled(False)
        self.menubar.addMenu(menu_view)

        # DPI
        menu_dpi = QMenu("DPI (60)")
        if visualization:
            for dpi in [60, 70, 80, 90, 100, 110, 120, 130]:
                menu_dpi.addAction(QAction(
                    f'{dpi}', menu_dpi, checkable=True, triggered=self.set_dpi(menu_dpi, f'{dpi}', dpi)))
                if dpi == 60:
                    self.set_dpi(menu_dpi, f'{dpi}', dpi)()
        else:
            menu_dpi.setEnabled(False)
        self.menubar.addMenu(menu_dpi)

    # ----------------------------------------------------------------------
    def build_menu_stimuli(self, visualization: bool, debugger: Optional[bool] = False) -> None:
        """Menu for stimuli delivery."""
        self.menubar = QMenuBar(self)
        self.menubar.clear()

        self.accent_menubar = QMenuBar(self)
        self.accent_menubar.clear()
        self.menubar.setMinimumWidth(1e4)

        # Title
        if debugger:
            menu_stimuli = QMenu(f"Debugging: {visualization}")
        else:
            if visualization:
                menu_stimuli = QMenu(visualization + ' 🞃')
            else:
                menu_stimuli = QMenu('Stimuli' + ' 🞃')

        for viz in self.extensions_list:
            if viz != visualization:
                menu_stimuli.addAction(QAction(viz, menu_stimuli,
                                               triggered=self.set_extension(viz)))
        # self.menubar.addMenu(menu_stimuli)
        self.accent_menubar.addMenu(menu_stimuli)

        self.accent_menubar.setStyleSheet(f"""
        QMenuBar::item {{
            background-color: {os.getenv('QTMATERIAL_PRIMARYCOLOR', '#ffffff')};
            color: {os.getenv('QTMATERIAL_PRIMARYTEXTCOLOR', '#ffffff')};
        }}

        """)

        # self.menubar.addMenu(menu_stimuli)
        self.menubar.setCornerWidget(
            self.accent_menubar, corner=Qt.TopLeftCorner)

        # View
        menu_view = QMenu("View")
        if visualization:

            menu_view.addAction(
                QAction('Reload', menu_view, triggered=self.reload))

            if debugger:
                menu_view.addAction(
                    QAction('Open subwindow delivery', menu_view, triggered=debugger.open_subwindow))
            if not debugger:
                menu_view.addSeparator()
                menu_view.addAction(
                    QAction('Close', menu_view, triggered=self.remove))
        else:
            menu_view.setEnabled(False)
        self.menubar.addMenu(menu_view)

    # ----------------------------------------------------------------------
    def set_dpi(self, menu_dpi, text: str, dpi: int) -> Callable:
        """Set the DPI value for matplotlib figures."""
        def wrap():
            [action.setChecked(False) for action in menu_dpi.actions()]
            [action.setChecked(
                True) for action in menu_dpi.actions() if action.text() == text]
            self.main.DPI = dpi
            menu_dpi.setTitle(f'DPI ({dpi})')
        return wrap

    # ----------------------------------------------------------------------
    def set_extension(self, visualization: str) -> Callable:
        """Load extension from menu."""
        def wrap():
            self.load_extension(visualization)
        return wrap


########################################################################
class ExtensionWidget(QMdiSubWindow, ExtensionMenu):
    """MDIArea with extension."""

    # ----------------------------------------------------------------------
    def __init__(self, mdi_area, extensions_list: List[str], mode: str):
        """"""
        super().__init__(None)
        ui = os.path.realpath(os.path.join(
            os.environ['BCISTREAM_ROOT'], 'framework', 'qtgui', 'visualization_widget.ui'))
        self.main = QUiLoader().load(ui, self)
        self.mdi_area = mdi_area

        self.main.DPI = 60
        self.mode = mode
        self.current_viz = None
        self.extensions_list = extensions_list

        if '--local' in sys.argv:
            self.projects_dir = os.path.join(
                os.getenv('BCISTREAM_ROOT'), 'default_projects')
        else:
            self.projects_dir = os.path.join(
                os.getenv('BCISTREAM_HOME'), 'projects')

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWidget(self.main)
        self.config = ConfigManager()

        self.setStyleSheet(f"""
        * {{
        border: 2px solid {os.getenv('QTMATERIAL_SECONDARYCOLOR', '#000000')};
        border-width: 0px 2px 2px 2px;
        }}
        QMenuBar {{
        background: {os.getenv('QTMATERIAL_SECONDARYCOLOR', '#000000')};
        border-width: 0;
        }}
        """)

    # ----------------------------------------------------------------------
    @property
    def is_visualization(self) -> str:
        """"""
        return self.mode == 'visualization'

    # ----------------------------------------------------------------------
    @property
    def is_stimuli(self) -> str:
        """"""
        return self.mode == 'stimuli'

    # ----------------------------------------------------------------------
    @property
    def is_analysis(self) -> str:
        """"""
        return self.mode == 'analysis'

    # ----------------------------------------------------------------------
    def load_extension(self, extension: str, debugger: Optional[bool] = False) -> None:
        """Load project."""
        self.current_viz = extension
        module = os.path.join(self.projects_dir, extension, 'main.py')
        self.stream_subprocess = LoadSubprocess(
            self.main, module, use_webview=not self.is_analysis)
        self.update_menu_bar(extension, debugger)
        self.update_ip(self.stream_subprocess.port)
        self.loaded()

    # ----------------------------------------------------------------------
    def loaded(self, *args, **kwargs) -> None:
        """Method to connect events."""
        # keep this

    # ----------------------------------------------------------------------
    def update_ip(self, *args, **kwargs) -> None:
        """Method to connect events."""
        # keep this

    # ----------------------------------------------------------------------
    def remove(self) -> None:
        """Remove active extension."""
        self.stop_preview()
        if hasattr(self, 'stream_subprocess'):
            del self.stream_subprocess

        if self.is_visualization:
            self.deleteLater()
            QTimer().singleShot(1000 / 50, self.mdi_area.tileSubWindows)
        elif self.is_stimuli:
            self.update_menu_bar()
            self.loaded()

    # ----------------------------------------------------------------------
    def save_img(self) -> None:
        """Save capture of visualization in the project directory."""
        name = f"{self.current_viz.replace(' ', '')} {str(datetime.now()).replace(':', '_')}.jpg"
        # filename = os.path.join(os.getenv('BCISTREAM_TMP'), name)
        captures_dir = os.path.join(
            self.projects_dir, self.current_viz, 'captures')
        filename = os.path.join(captures_dir, name)
        if not os.path.exists(captures_dir):
            os.makedirs(captures_dir, exist_ok=True)
        self.stream_subprocess.main.web_engine.grab().save(filename, 'JPG')

    # ----------------------------------------------------------------------
    def update_menu_bar(self, visualization: Optional[bool] = None, debugger: Optional[bool] = False) -> None:
        """Create menubar."""
        if self.is_visualization:
            self.build_menu_visualization(visualization, debugger)
        elif self.is_stimuli:
            self.build_menu_stimuli(visualization, debugger)

        if not self.is_analysis:
            self.main.gridLayout_menubar.setMenuBar(self.menubar)
            self.menubar.adjustSize()
            self.menubar.setStyleSheet(
                self.menubar.styleSheet() + """QMenuBar::item {width: 10000px;}""")

    # ----------------------------------------------------------------------
    def stop_preview(self) -> None:
        """Stop process."""
        if hasattr(self, 'stream_subprocess'):
            self.stream_subprocess.stop_preview()

    # ----------------------------------------------------------------------
    def reload(self) -> None:
        """Restart process."""
        self.stream_subprocess.reload()