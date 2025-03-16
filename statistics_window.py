from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox, QWidget
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json
import os
import matplotlib.pyplot as plt
 
DATA_FILE = os.path.join(os.getenv("APPDATA"), "StudyTracker", "study_data.json")

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        super().__init__(self.fig)
        self.setParent(parent)


class StatisticsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thống kê học tập")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # Bộ lọc thời gian
        self.time_filter = QComboBox()
        self.time_filter.addItems(["Tổng", "Ngày", "Tuần", "Tháng", "Năm"])
        layout.addWidget(QLabel("Chọn mốc thời gian:"))
        layout.addWidget(self.time_filter)

        # Nút chọn biểu đồ
        self.pie_chart_btn = QPushButton("Biểu đồ tròn")
        self.bar_chart_btn = QPushButton("Biểu đồ cột")
        self.pie_chart_btn.clicked.connect(self.show_pie_chart)
        self.bar_chart_btn.clicked.connect(self.show_bar_chart)

        layout.addWidget(self.pie_chart_btn)
        layout.addWidget(self.bar_chart_btn)

        # Khu vực hiển thị đồ thị
        self.chart_widget = QWidget()
        self.chart_layout = QVBoxLayout()
        self.chart_canvas = MatplotlibCanvas(self.chart_widget)
        self.chart_layout.addWidget(self.chart_canvas)
        self.chart_widget.setLayout(self.chart_layout)
        layout.addWidget(self.chart_widget)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                self.data = json.load(file)
        else:
            self.data = []

    def show_pie_chart(self):
        subjects, times = self.get_chart_data()
        
        if not subjects or not times:
            print("⚠️ Không có dữ liệu để hiển thị!")
            return
        
        # Sắp xếp theo thời gian giảm dần
        sorted_data = sorted(zip(times, subjects), reverse=True)
        times, subjects = zip(*sorted_data)

        # Chọn màu sắc tự động
        colors = plt.cm.Paired(range(len(subjects)))

        # Xóa biểu đồ cũ
        self.chart_canvas.ax.clear()

        # Vẽ biểu đồ tròn
        wedges, texts, autotexts = self.chart_canvas.ax.pie(
            times, labels=subjects, autopct='%1.1f%%', colors=colors, startangle=140
        )

        # Tạo chú thích với màu sắc tương ứng
        legend_labels = [f"{subjects[i]} - {times[i]} phút ({autotexts[i].get_text()})" for i in range(len(subjects))]
        self.chart_canvas.ax.legend(wedges, legend_labels, title="Chú thích", loc="best", bbox_to_anchor=(1, 0.5))

        # Đặt tiêu đề và vẽ lại biểu đồ
        self.chart_canvas.ax.set_title("Tỷ lệ thời gian học theo môn")
        self.chart_canvas.draw()

    def show_bar_chart(self):
        subjects, times = self.get_chart_data()
        self.chart_canvas.ax.clear()
        self.chart_canvas.ax.bar(subjects, times, color='skyblue')
        self.chart_canvas.ax.set_xlabel("Môn học")
        self.chart_canvas.ax.set_ylabel("Thời gian học (giây)")
        self.chart_canvas.ax.set_title("Thời gian học theo từng môn")
        self.chart_canvas.ax.tick_params(axis='x', rotation=45)
        self.chart_canvas.draw()

    def get_chart_data(self):
        subjects = [entry["subject"] for entry in self.data]
        times = [self.parse_time(entry["time_spent"]) for entry in self.data]
        return subjects, times

    def parse_time(self, time_str):
        hours, minutes, seconds = map(int, time_str.split(":"))
        return hours * 3600 + minutes * 60 + seconds

