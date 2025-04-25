import pyodbc
from CTPhieuNhapDTO import CTPhieuNhapDTO
from db_utils import DBUtils

class CTPhieuNhapDAO:
    def __init__(self):
        pass
    
    def lay_theo_ma_phieu_nhap(self, maPN):
        """Get all details for an import receipt"""
        ct_phieu_nhap_list = []
        
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Query to get all details for an import receipt
            query = """
                SELECT maPN, maSP, soLuongSP, donGia, thanhTien
                FROM CHITIETPN
                WHERE maPN = ?
            """
            
            cursor.execute(query, (maPN,))
            rows = cursor.fetchall()
            
            for row in rows:
                maPN, maSP, soLuongSP, donGia, thanhTien = row
                
                # Create a ChiTietPhieuNhapDTO object
                ct_phieu_nhap = CTPhieuNhapDTO(maPN, maSP, soLuongSP, donGia, thanhTien)
                ct_phieu_nhap_list.append(ct_phieu_nhap)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error in lay_theo_ma_phieu_nhap: {e}")
        
        return ct_phieu_nhap_list
    
    def them(self, ct_phieu_nhap):
        """Add a new detail"""
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Insert the detail
            query = """
                INSERT INTO CHITIETPN (maPN, maSP, soLuongSP, donGia, thanhTien)
                VALUES (?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                ct_phieu_nhap.maPN,
                ct_phieu_nhap.maSP,
                ct_phieu_nhap.soLuongSP,
                ct_phieu_nhap.donGia,
                ct_phieu_nhap.thanhTien
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error in them: {e}")
            return False
    
    def xoa_theo_ma_phieu_nhap(self, maPN):
        """Delete all details for an import receipt"""
        try:
            conn = DBUtils.get_connection()
            cursor = conn.cursor()
            
            # Delete all details for an import receipt
            query = """
                DELETE FROM CHITIETPN
                WHERE maPN = ?
            """
            
            cursor.execute(query, (maPN,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error in xoa_theo_ma_phieu_nhap: {e}")
            return False