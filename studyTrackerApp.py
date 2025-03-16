from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QCheckBox, QHBoxLayout, QLineEdit, QDialog, QLabel, QComboBox
from PyQt6.QtCore import QTimer
import time
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

DATA_FILE = os.path.join(os.getenv("APPDATA"), "StudyTracker", "study_data.json")

class StudyTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Tracker")
        self.setGeometry(100, 100, 500, 300)
        with open("styles/style_studyTrackerApp.qss", "r", encoding="utf-8") as file:
            self.setStyleSheet(file.read())
        layout = QVBoxLayout()
        
        # Bảng hiển thị môn học
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # 3 cột: Chọn, Môn học, Giờ học
        self.table.setHorizontalHeaderLabels(["Chọn", "Môn học", "Giờ học"])
        
        layout.addWidget(self.table)
        
        # Hàng chứa các nút chức năng
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Bắt đầu")
        self.start_btn.setObjectName("start_btn")
        self.pause_btn = QPushButton("Dừng")
        self.pause_btn.setObjectName("pause_btn")
        self.save_btn = QPushButton("Lưu dữ liệu")
        self.save_btn.setObjectName("save_btn")
         
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.save_btn)
         
        layout.addLayout(button_layout)
        
        # Hàng thêm môn học
        add_subject_layout = QHBoxLayout()
        self.subject_input = QLineEdit()
        self.subject_input.setObjectName("subject_input")
        self.subject_input.setPlaceholderText("Nhập tên môn học")

        self.add_subject_btn = QPushButton("Thêm môn học")
        self.add_subject_btn.setObjectName("add_subject_btn")
        self.add_subject_btn.clicked.connect(self.add_subject)
        
        add_subject_layout.addWidget(self.subject_input)
        add_subject_layout.addWidget(self.add_subject_btn)
        
        layout.addLayout(add_subject_layout)
        
        self.setLayout(layout)
        
        # Timer để cập nhật thời gian học
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_study_time)
        self.start_time = None
        
        # Kết nối sự kiện
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.save_btn.clicked.connect(self.save_data)
          
        # Load dữ liệu từ file nếu có
        self.load_data()
    










    def load_data(self):
        if not os.path.exists(os.path.dirname(DATA_FILE)):
            os.makedirs(os.path.dirname(DATA_FILE))
        
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                self.table.setRowCount(len(data))
                self.checkboxes = []
                self.study_times = []
                for row, entry in enumerate(data):
                    checkbox = QCheckBox()
                    checkbox.setObjectName("tableCheckbox")  # Gán ID chung cho checkbox trong cột 1
                    self.checkboxes.append(checkbox)
                    self.study_times.append(self.parse_time(entry["time_spent"]))
                    self.table.setCellWidget(row, 0, checkbox)
                    self.table.setItem(row, 1, QTableWidgetItem(entry["subject"]))
                    self.table.setItem(row, 2, QTableWidgetItem(entry["time_spent"]))
        else:
            self.checkboxes = []
            self.study_times = []
    
    def start_timer(self):
        if self.start_time is None:
            self.start_time = time.time()
        self.timer.start(1000)
    
    def pause_timer(self):
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            for row, checkbox in enumerate(self.checkboxes):
                if checkbox.isChecked():
                    self.study_times[row] += elapsed
                    hours, remainder = divmod(self.study_times[row], 3600)
                    minutes, seconds = divmod(remainder, 60)
                    self.table.setItem(row, 2, QTableWidgetItem(f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"))
            self.start_time = None
        self.timer.stop()
    
    def update_study_time(self):
        elapsed = time.time() - self.start_time
        for row, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                self.study_times[row] += elapsed
                hours, remainder = divmod(self.study_times[row], 3600)
                minutes, seconds = divmod(remainder, 60)
                self.table.setItem(row, 2, QTableWidgetItem(f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"))
        self.start_time = time.time()
    
    def add_subject(self):
        subject_name = self.subject_input.text().strip()
        if subject_name:
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            checkbox = QCheckBox()
            self.checkboxes.append(checkbox)
            self.study_times.append(0)
            self.table.setCellWidget(row_count, 0, checkbox)
            self.table.setItem(row_count, 1, QTableWidgetItem(subject_name))
            self.table.setItem(row_count, 2, QTableWidgetItem("00:00:00"))
            self.subject_input.clear()
    
    def save_data(self):
        data = []
        for row in range(self.table.rowCount()):
            subject = self.table.item(row, 1).text()
            time_spent = self.table.item(row, 2).text()
            data.append({"subject": subject, "time_spent": time_spent})
        
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print("Dữ liệu đã được lưu vào study_data.json")
    
    def parse_time(self, time_str):
        hours, minutes, seconds = map(int, time_str.split(":"))
        return hours * 3600 + minutes * 60 + seconds
    
