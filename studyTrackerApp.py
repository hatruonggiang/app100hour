import sqlite3
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QCheckBox, QHBoxLayout, QLineEdit
)
from PyQt6.QtCore import QTimer
from database import Database  # Import class Database

class StudyTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Tracker")
        self.setGeometry(100, 100, 500, 300)

        # Khởi tạo database
        self.db = Database()  
        self.db.create_table()  # Đảm bảo bảng đã tồn tại

        layout = QVBoxLayout()

        # Tạo bảng hiển thị dữ liệu
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Chọn", "Môn học", "Giờ học"])
        layout.addWidget(self.table)

        # Các nút điều khiển
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Bắt đầu")
        self.pause_btn = QPushButton("Dừng")
        self.save_btn = QPushButton("Lưu dữ liệu")

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.save_btn)
        layout.addLayout(button_layout)

        # Ô nhập liệu thêm môn học
        add_subject_layout = QHBoxLayout()
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Nhập tên môn học")
        self.add_subject_btn = QPushButton("Thêm môn học")

        add_subject_layout.addWidget(self.subject_input)
        add_subject_layout.addWidget(self.add_subject_btn)
        layout.addLayout(add_subject_layout)

        self.setLayout(layout)

        # Timer theo dõi thời gian học
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_study_time)
        self.start_time = None

        # Kết nối nút bấm với chức năng
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.save_btn.clicked.connect(self.save_data)
        self.add_subject_btn.clicked.connect(self.add_subject)

        # Khởi tạo danh sách checkbox & thời gian học
        self.checkboxes = []
        self.study_times = []

        # Load dữ liệu từ DB khi mở ứng dụng
        self.load_data()
<<<<<<< HEAD
    





=======
>>>>>>> 392be72 (hehe commit)

    def load_data(self):
        """Nạp dữ liệu từ database vào bảng"""
        self.table.setRowCount(0)  # Xóa dữ liệu cũ trước khi nạp mới
        self.checkboxes.clear()
        self.study_times.clear()

        data = self.db.load_data()  # Lấy dữ liệu từ database
        for row, (subject, time_spent) in enumerate(data):
            self.table.insertRow(row)
            checkbox = QCheckBox()
            self.checkboxes.append(checkbox)
            self.study_times.append(time_spent)

            self.table.setCellWidget(row, 0, checkbox)
            self.table.setItem(row, 1, QTableWidgetItem(subject))
            self.table.setItem(row, 2, QTableWidgetItem(self.format_time(time_spent)))

    def start_timer(self):
        """Bắt đầu đếm thời gian học"""
        if self.start_time is None:
            self.start_time = time.time()
        self.timer.start(1000)

    def pause_timer(self):
        """Tạm dừng và cập nhật thời gian"""
        if self.start_time is not None:
            elapsed = int(time.time() - self.start_time)
            for row, checkbox in enumerate(self.checkboxes):
                if checkbox.isChecked():
                    self.study_times[row] += elapsed
                    self.table.setItem(row, 2, QTableWidgetItem(self.format_time(self.study_times[row])))
            self.start_time = None
        self.timer.stop()

    def update_study_time(self):
        """Cập nhật thời gian học mỗi giây"""
        elapsed = int(time.time() - self.start_time)
        for row, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                self.study_times[row] += elapsed
                self.table.setItem(row, 2, QTableWidgetItem(self.format_time(self.study_times[row])))
        self.start_time = time.time()

    def add_subject(self):
        """Thêm môn học mới vào database và hiển thị trên bảng"""
        subject_name = self.subject_input.text().strip()
        if subject_name:
            try:
                self.db.insert_subject(subject_name)  # Thêm vào database
                row_count = self.table.rowCount()
                self.table.insertRow(row_count)

                checkbox = QCheckBox()
                self.checkboxes.append(checkbox)
                self.study_times.append(0)

                self.table.setCellWidget(row_count, 0, checkbox)
                self.table.setItem(row_count, 1, QTableWidgetItem(subject_name))
                self.table.setItem(row_count, 2, QTableWidgetItem("00:00:00"))

                self.subject_input.clear()
            except sqlite3.IntegrityError:
                print("⚠️ Môn học đã tồn tại!")

    def save_data(self):
        """Lưu thời gian học vào database"""
        for row in range(self.table.rowCount()):
            subject = self.table.item(row, 1).text()
            time_spent = self.study_times[row]
            self.db.update_time(subject, time_spent)

        print("✅ Dữ liệu đã được lưu vào SQLite")

    def format_time(self, seconds):
        """Chuyển đổi giây thành định dạng HH:MM:SS"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

