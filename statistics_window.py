from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox, QWidget
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from database import Database  # Import class Database

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

        # Khởi tạo database
        self.db = Database()  
        self.db.create_table()  # Đảm bảo bảng đã tồn tại

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
        """Tải dữ liệu từ database thay vì JSON"""
        self.db.cursor.execute("SELECT subject, time_spent FROM study_data")
        self.data = self.db.cursor.fetchall()

    def show_pie_chart(self):
        """Hiển thị biểu đồ tròn"""
        subjects, times = self.get_chart_data()

        if not subjects or not times:
            print("⚠️ Không có dữ liệu để hiển thị!")
            return
        
        # Sắp xếp dữ liệu theo thời gian giảm dần
        sorted_data = sorted(zip(times, subjects), reverse=True)
        times, subjects = zip(*sorted_data)

        # Xóa biểu đồ cũ
        self.chart_canvas.ax.clear()

        # Vẽ biểu đồ tròn
        wedges, texts, autotexts = self.chart_canvas.ax.pie(
            times, labels=subjects, autopct='%1.1f%%', startangle=140
        )

        # Đặt tiêu đề và vẽ lại biểu đồ
        self.chart_canvas.ax.set_title("Tỷ lệ thời gian học theo môn")
        self.chart_canvas.draw()

    def show_bar_chart(self):
        """Hiển thị biểu đồ cột"""
        subjects, times = self.get_chart_data()
        
        if not subjects or not times:
            print("⚠️ Không có dữ liệu để hiển thị!")
            return

        self.chart_canvas.ax.clear()
        self.chart_canvas.ax.bar(subjects, times, color='skyblue')

        # Đặt tiêu đề và nhãn trục
        self.chart_canvas.ax.set_xlabel("Môn học")
        self.chart_canvas.ax.set_ylabel("Thời gian học (giây)")
        self.chart_canvas.ax.set_title("Thời gian học theo từng môn")
        self.chart_canvas.ax.tick_params(axis='x', rotation=45)

        # Hiển thị biểu đồ
        self.chart_canvas.draw()

    def get_chart_data(self):
        """Trích xuất dữ liệu từ database"""
        if not self.data:
            return [], []
        
        subjects = [entry[0] for entry in self.data]
        times = [entry[1] for entry in self.data]
        return subjects, times
