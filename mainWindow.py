import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QStackedWidget, QToolButton, QMenu)
from PyQt6.QtGui import QAction
from statistics_window import StatisticsWindow
from studyTrackerApp import StudyTrackerApp

class MainApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()
        with open("styles/style_mainWindow.qss", "r", encoding="utf-8") as file:
            self.setStyleSheet(file.read())



        self.main_stacked_widget = QStackedWidget()

        # Tạo các trang
        self.statistics_page = StatisticsWindow()
        self.study_tracker_page = StudyTrackerApp()

        # Thêm các trang vào QStackedWidget
        self.main_stacked_widget.addWidget(self.study_tracker_page)
        self.main_stacked_widget.addWidget(self.statistics_page)
        

        # Tạo nút menu
        self.menu_button = QToolButton(self)
        self.menu_button.setText("Menu")
        self.menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        # Tạo menu
        menu = QMenu(self)

        # Tạo các hành động (menu items)
        study_tracker_action = QAction("Study Tracker", self)
        statistics_action = QAction("Statistics", self)
        

        # Kết nối hành động với các hàm xử lý
        study_tracker_action.triggered.connect(lambda: self.main_stacked_widget.setCurrentIndex(0))
        statistics_action.triggered.connect(lambda: self.main_stacked_widget.setCurrentIndex(1))
        

        # Thêm hành động vào menu
        menu.addAction(study_tracker_action)
        menu.addAction(statistics_action)
        

        # Gán menu cho nút menu
        self.menu_button.setMenu(menu)

        # Bố trí các widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.menu_button)  # Thêm nút menu vào bố cục
        main_layout.addWidget(self.main_stacked_widget)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApplicationWindow()
    main_window.show()
    sys.exit(app.exec())