from datetime import date
import pyodbc
from PhieuNhapDTO import PhieuNhapDTO
from CTPhieuNhapDAO import CTPhieuNhapDAO
from db_utils import DBUtils

class PhieuNhapDAO:
    def __init__(self):
        self.ct_phieu_nhap_dao = CTPhieuNhapDAO()
    
    def lay_danh_sach(self):
        phieu_nhap_list = []
        
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Query to get all import receipts
            query = """
                SELECT maPN, maNV, ngayTaoPN, tongTien
                FROM PhieuNhap
                ORDER BY ngayTaoPN DESC
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            for row in rows:
                maPN, maNV, ngayTaoPN, tongTien = row
                
                # Get the details for this receipt
                ct_phieu_nhap_list = self.ct_phieu_nhap_dao.lay_theo_ma_phieu_nhap(maPN)
                
                # Create a PhieuNhapDTO object
                phieu_nhap = PhieuNhapDTO(maPN, maNV, ngayTaoPN, tongTien, ct_phieu_nhap_list)
                phieu_nhap_list.append(phieu_nhap)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error in lay_danh_sach: {e}")
        
        return phieu_nhap_list
    
    def tim_theo_ma(self, maPN):
        """Find an import receipt by ID"""
        phieu_nhap = None
        
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Query to find an import receipt by ID
            query = """
                SELECT maPN, maNV, ngayTaoPN, tongTien
                FROM PhieuNhap
                WHERE maPN = ?
            """
            
            cursor.execute(query, (maPN,))
            row = cursor.fetchone()
            
            if row:
                maPN, maNV, ngayTaoPN, tongTien = row
                
                # Get the details for this receipt
                ct_phieu_nhap_list = self.ct_phieu_nhap_dao.lay_theo_ma_phieu_nhap(maPN)
                
                # Create a PhieuNhapDTO object
                phieu_nhap = PhieuNhapDTO(maPN, maNV, ngayTaoPN, tongTien, ct_phieu_nhap_list)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error in tim_theo_ma: {e}")
        
        return phieu_nhap
    
    def tim_theo_nhan_vien(self, maNV):
        """Find import receipts by employee ID"""
        phieu_nhap_list = []
        
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Query to find import receipts by employee ID
            query = """
                SELECT maPN, maNV, ngayTaoPN, tongTien
                FROM PhieuNhap
                WHERE maNV = ?
                ORDER BY ngayTaoPN DESC
            """
            
            cursor.execute(query, (maNV,))
            rows = cursor.fetchall()
            
            for row in rows:
                maPN, maNV, ngayTaoPN, tongTien = row
                
                # Get the details for this receipt
                ct_phieu_nhap_list = self.ct_phieu_nhap_dao.lay_theo_ma_phieu_nhap(maPN)
                
                # Create a PhieuNhapDTO object
                phieu_nhap = PhieuNhapDTO(maPN, maNV, ngayTaoPN, tongTien, ct_phieu_nhap_list)
                phieu_nhap_list.append(phieu_nhap)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error in tim_theo_nhan_vien: {e}")
        
        return phieu_nhap_list
    
    def tim_theo_ngay(self, from_date, to_date):
        """Find import receipts by date range"""
        phieu_nhap_list = []
        
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Query to find import receipts by date range
            query = """
                SELECT maPN, maNV, ngayTaoPN, tongTien
                FROM PhieuNhap
                WHERE ngayTaoPN BETWEEN ? AND ?
                ORDER BY ngayTaoPN DESC
            """
            
            cursor.execute(query, (from_date, to_date))
            rows = cursor.fetchall()
            
            for row in rows:
                maPN, maNV, ngayTaoPN, tongTien = row
                
                # Get the details for this receipt
                ct_phieu_nhap_list = self.ct_phieu_nhap_dao.lay_theo_ma_phieu_nhap(maPN)
                
                # Create a PhieuNhapDTO object
                phieu_nhap = PhieuNhapDTO(maPN, maNV, ngayTaoPN, tongTien, ct_phieu_nhap_list)
                phieu_nhap_list.append(phieu_nhap)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error in tim_theo_ngay: {e}")
        
        return phieu_nhap_list
    
    def them(self, phieu_nhap):
        """Add a new import receipt"""
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Calculate the total amount
            tongTien = sum(ct.thanhTien for ct in phieu_nhap.dsCTPN)
            
            # Insert the import receipt
            query = """
                INSERT INTO PhieuNhap (maPN, maNV, ngayTaoPN, tongTien)
                VALUES (?, ?, ?, ?)
            """
            
            cursor.execute(query, (phieu_nhap.maPN, phieu_nhap.maNV, phieu_nhap.ngayTaoPN, tongTien))
            
            # Insert the details
            for ct in phieu_nhap.dsCTPN:
                self.ct_phieu_nhap_dao.them(ct)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error in them: {e}")
            return False
    
    def sua(self, phieu_nhap):
        """Update an import receipt"""
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Calculate the total amount
            tongTien = sum(ct.thanhTien for ct in phieu_nhap.dsCTPN)
            
            # Update the import receipt
            query = """
                UPDATE PhieuNhap
                SET maNV = ?, ngayTaoPN = ?, tongTien = ?
                WHERE maPN = ?
            """
            
            cursor.execute(query, (phieu_nhap.maNV, phieu_nhap.ngayTaoPN, tongTien, phieu_nhap.maPN))
            
            # Delete all existing details
            self.ct_phieu_nhap_dao.xoa_theo_ma_phieu_nhap(phieu_nhap.maPN)
            
            # Insert the new details
            for ct in phieu_nhap.dsCTPN:
                self.ct_phieu_nhap_dao.them(ct)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error in sua: {e}")
            return False
    
    def xoa(self, maPN):
        """Delete an import receipt"""
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Delete all details first
            self.ct_phieu_nhap_dao.xoa_theo_ma_phieu_nhap(maPN)
            
            # Delete the import receipt
            query = """
                DELETE FROM PhieuNhap
                WHERE maPN = ?
            """
            
            cursor.execute(query, (maPN,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error in xoa: {e}")
            return False
    
    def tao_ma_phieu_nhap_moi(self):
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT MAX(maPN) FROM PhieuNhap
            """
            
            cursor.execute(query)
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if row[0]:
                last_id = str(row[0])
                if last_id.startswith('PN'):
                    num = int(last_id[2:]) + 1
                    return f"PN{num:04d}"
            
            # Default if no receipts exist
            return "PN0001"
            
        except Exception as e:
            print(f"Error in tao_ma_phieu_nhap_moi: {e}")
            return "PN0001"