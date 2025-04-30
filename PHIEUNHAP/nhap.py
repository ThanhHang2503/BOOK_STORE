# # from PHIEUNHAP.PhieuNhapDAO import DSPhieuNhap
#
# def test_tim_kiem_phieu_nhap():
#     ds_phieu_nhap = DSPhieuNhap()
#
#     # Kiểm tra kết nối
#     if ds_phieu_nhap.conn is None:
#         print("❌ Lỗi: Không thể kết nối đến database!")
#         return
#
#     # Nhập mã phiếu nhập để kiểm thử
#     ma_pn = input("Nhập mã phiếu nhập để tìm: ").strip()
#
#     print(f"🔍 Kiểm tra tìm kiếm với mã: {ma_pn}")
#     phieu_nhap = ds_phieu_nhap.tim_kiem_phieu_nhap(ma_pn)
#
#     if phieu_nhap:
#         print("✅ Kết quả tìm kiếm:")
#         print(f"  - Mã Phiếu Nhập: {phieu_nhap['ma_phieu_nhap']}")
#         print(f"  - Mã Nhân Viên: {phieu_nhap['ma_nhan_vien']}")
#         print(f"  - Ngày Nhập: {phieu_nhap['ngay_nhap']}")
#         print(f"  - Tổng Tiền: {phieu_nhap['tong_tien']}")
#     else:
#         print("⚠️ Không tìm thấy phiếu nhập!")
#
# if __name__ == "__main__":
#     test_tim_kiem_phieu_nhap()
