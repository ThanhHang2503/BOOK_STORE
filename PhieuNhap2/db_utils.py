import pyodbc

class DBUtils:
    @staticmethod
    def get_connection():
        """Get a connection to the database"""
        try:
            # Connection string
            conn_str = (
                "DRIVER={SQL Server};"
                "SERVER=DESKTOP-SG8M886\\SQLEXPRESS;"
                "DATABASE=DOANPYTHON;"
                "UID=sa;"
                "PWD=hang2503;"
            )
            
            # Connect to the database
            conn = pyodbc.connect(conn_str)
            
            return conn
            
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None