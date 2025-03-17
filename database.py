import sqlite3

DB_FILE = "study_data.db"  # Đường dẫn file DB

class Database:
    def __init__(self):
        """Khởi tạo kết nối đến SQLite"""
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Tạo bảng nếu chưa có"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT UNIQUE NOT NULL,
            time_spent INTEGER DEFAULT 0
        )
        """)
        self.conn.commit()

    def insert_subject(self, subject):
        """Thêm môn học mới"""
        try:
            self.cursor.execute("INSERT INTO study_data (subject, time_spent) VALUES (?, ?)", (subject, 0))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("⚠️ Môn học đã tồn tại!")

    def update_time(self, subject, time_spent):
        """Cập nhật thời gian học"""
        self.cursor.execute("UPDATE study_data SET time_spent = ? WHERE subject = ?", (time_spent, subject))
        self.conn.commit()

    def load_data(self):
        """Lấy dữ liệu từ DB"""
        self.cursor.execute("SELECT subject, time_spent FROM study_data")
        return self.cursor.fetchall()

    def close(self):
        """Đóng kết nối"""
        self.conn.close()
