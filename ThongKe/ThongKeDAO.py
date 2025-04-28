import pyodbc
from datetime import date

class ThongKeDAO:
    def __init__(self):
        self.dshd = []  
        self.conn = self.connect_db()  

    def connect_db(self):
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-NRE55H1;"
            "DATABASE=DOANPYTHON;"
            "Trusted_Connection=yes;"
            "Connection Timeout=30;"
        )
        return conn

    def lay_du_lieu_tu_sql(self):
        cursor = self.conn.cursor()  
        query = "SELECT maHD, ngayTaoHD, maNV , tongTien FROM HoaDon"
        cursor.execute(query) 
        dshd = cursor.fetchall() 
        cursor.close()  
        return dshd  
