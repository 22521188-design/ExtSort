"""
Quick Start Guide - Hướng Dẫn Nhanh
"""

# ===================================================================
# EXTERNAL MERGE SORT - HƯỚNG DẪN NHANH BẮT ĐẦU
# ===================================================================

# 1. CHẠY GIAO DIỆN ĐỒNG HỒ (GUI)
# ===================================================================
# Windows:
#   python main.py
#   hoặc
#   python gui_app.py

# Sau đó:
#   a. Nhấp "Tạo Tập Tin Test" để tạo dữ liệu test
#   b. Hoặc nhấp "Chọn Tập Tin" để chọn tệp hiện có
#   c. Nhấp "Bắt Đầu Sắp Xếp"
#   d. Xem quá trình trong vùng hiển thị


# 2. CHẠY DEMO TƯƠNG TÁC
# ===================================================================
# Windows:
#   python demo.py
#
# Lựa chọn:
#   1 = Tạo tệp dữ liệu
#   2 = Sắp xếp tệp
#   3 = Xem kết quả
#   4 = Thoát

# Ví dụ:
#   Nhập: 1
#   Tên tệp: mydata.bin
#   Chọn kích thước: 2 (1000 số)
#   Kết quả: Tệp mydata.bin được tạo
#
#   Nhập: 2
#   Tệp cần sắp xếp: mydata.bin
#   Chip size: 10
#   Kết quả: mydata_sorted.bin được tạo


# 3. CHẠY KIỂM THỬ
# ===================================================================
# Windows:
#   python test_script.py
#
# Sẽ tự động:
#   - Tạo 3 tệp test (nhỏ, trung bình, lớn)
#   - Sắp xếp từng tệp
#   - Hiển thị thời gian xử lý
#   - Kiểm tra tính chính xác


# 4. SỬ DỤNG TRONG CODE
# ===================================================================

# 4a. Ví dụ cơ bản
# ---
from data_generator import generate_random_binary_file
from external_merge_sort import ExternalMergeSort

# Tạo tệp dữ liệu
generate_random_binary_file("data.bin", count=1000)

# Sắp xếp
sorter = ExternalMergeSort(
    input_file="data.bin",
    output_file="sorted.bin",
    chunk_size=10
)
success = sorter.execute()

# In log
if success:
    for line in sorter.step_log:
        print(line)
    
    # Xóa tệp tạm
    sorter.cleanup_temp_files()

# 4b. Kiểm tra kết quả
# ---
from data_generator import read_binary_file

sorted_data = read_binary_file("sorted.bin")

# In thống kê
print(f"Số lượng: {len(sorted_data)}")
print(f"Min: {min(sorted_data):.2f}")
print(f"Max: {max(sorted_data):.2f}")

# Kiểm tra sắp xếp
is_sorted = all(sorted_data[i] <= sorted_data[i+1] 
                for i in range(len(sorted_data)-1))
print(f"Đã sắp xếp: {is_sorted}")

# 4c. Điều chỉnh chunk size
# ---

# Chunk nhỏ → Nhiều merge, chậm hơn
sorter_small = ExternalMergeSort("data.bin", "out1.bin", chunk_size=5)

# Chunk lớn → Ít merge, nhanh hơn
sorter_large = ExternalMergeSort("data.bin", "out2.bin", chunk_size=100)


# 5. HIỂU THUẬT TOÁN
# ===================================================================

# External Merge Sort diễn ra 2 giai đoạn:

# Giai Đoạn 1: TẠO SORTED CHUNKS
# ================================
# Đọc dữ liệu từ tệp lớn thành các chunk nhỏ
# Sắp xếp mỗi chunk trong bộ nhớ
# Ghi mỗi chunk vào tệp tạm

# Ví dụ với chunk_size = 2:
#   Tệp gốc: [7, 3, 9, 1, 4, 8]
#   Chunk 0: [7, 3] → Sort → [3, 7] → Lưu vào temp_chunk_0.bin
#   Chunk 1: [9, 1] → Sort → [1, 9] → Lưu vào temp_chunk_1.bin
#   Chunk 2: [4, 8] → Sort → [4, 8] → Lưu vào temp_chunk_2.bin

# Giai Đoạn 2: MERGE
# ==================
# Merge các chunk đã sắp xếp (k-way merge)
# Từng bước merge 2 tệp thành 1
# Lặp lại cho đến khi còn 1 tệp

# Ví dụ merge level 1:
#   [3, 7] + [1, 9] → Merge → [1, 3, 7, 9]
#   [4, 8] + (không có) → Copy → [4, 8]
#
# Level 2:
#   [1, 3, 7, 9] + [4, 8] → Merge → [1, 3, 4, 7, 8, 9]


# 6. CẤU TRÚC TỆP NHỊ PHÂN
# ===================================================================

# Mỗi số thực được lưu dưới dạng 8 bytes (double precision)

# Ví dụ tạo tệp:
import struct

numbers = [3.14, 2.71, 1.41]
with open('example.bin', 'wb') as f:
    for num in numbers:
        # Ghi mỗi số dưới dạng 8 bytes
        f.write(struct.pack('d', num))
# Kết quả: 24 bytes cho 3 số

# Ví dụ đọc tệp:
with open('example.bin', 'rb') as f:
    while True:
        data = f.read(8)  # Đọc 8 bytes
        if not data:
            break
        num = struct.unpack('d', data)[0]  # Giải mã thành số
        print(num)


# 7. TỐI ƯU HÓA
# ===================================================================

# Chọn chunk_size hợp lý:
#   - Nhỏ (5-10): Tiết kiệm memory nhưng slow
#   - Lớn (100+): Nhanh nhưng cần nhiều memory

# Kiểm tra hiệu năng:
import time
for chunk_size in [5, 10, 20, 50]:
    sorter = ExternalMergeSort("data.bin", f"out_{chunk_size}.bin", 
                               chunk_size=chunk_size)
    
    start = time.time()
    sorter.execute()
    elapsed = time.time() - start
    
    print(f"Chunk {chunk_size}: {elapsed:.3f}s")
    
print("""
╔════════════════════════════════════════════════════════════════════╗
║                   EXTERNAL MERGE SORT - READY                      ║
║                                                                    ║
║  Chạy một trong các lệnh sau:                                   ║
║  1. python main.py          → GUI Application                      ║
║  2. python demo.py          → Interactive Demo                     ║
║  3. python test_script.py   → Automated Tests                      ║
╚════════════════════════════════════════════════════════════════════╝
""")
