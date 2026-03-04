# External Merge Sort - Ứng Dụng Python

## Mô Tả Dự Án

Ứng dụng này minh họa **External Merge Sort** - một thuật toán sắp xếp được sử dụng khi dữ liệu quá lớn để lưu trữ trong bộ nhớ. Ứng dụng cho phép người dùng:

- ✓ Chọn tệp dữ liệu nhị phân chứa số thực (8 bytes)
- ✓ Sắp xếp dữ liệu theo thứ tự tăng dần
- ✓ Quan sát chi tiết quá trình sắp xếp
- ✓ Tạo tệp dữ liệu test tự động

## Cấu Trúc Dự Án

```
.
├── external_merge_sort.py    # Module chính: triển khai External Merge Sort
├── data_generator.py          # Module tạo tệp dữ liệu test
├── gui_app.py                 # Giao diện người dùng (Tkinter)
├── main.py                    # Điểm vào chương trình
├── test_script.py             # Script kiểm thử
└── README.md                  # Tài liệu này
```

## External Merge Sort - Giải Thích Thuật Toán

### Tại sao cần External Merge Sort?

Khi dữ liệu quá lớn (lớn hơn RAM có sẵn), các thuật toán sắp xếp thông thường (QuickSort, MergeSort) không hoạt động hiệu quả. External Merge Sort giải quyết vấn đề này bằng cách chia dữ liệu thành các chunk nhỏ và xử lý từng chunk trong bộ nhớ.

### Các Giai Đoạn

#### Giai Đoạn 1: Tạo Sorted Chunks
```
Tệp Input (không sắp xếp): [7, 3, 9, 1, 4, 8, 2, 6]
                               ↓
Chia thành chunks (chunk_size=2):
  Chunk 0: [7, 3] → Sort → [3, 7]
  Chunk 1: [9, 1] → Sort → [1, 9]
  Chunk 2: [4, 8] → Sort → [4, 8]
  Chunk 3: [2, 6] → Sort → [2, 6]
```

#### Giai Đoạn 2: Merge Sorted Chunks
```
Level 1:
  [3, 7] + [1, 9] → Merge → [1, 3, 7, 9]
  [4, 8] + [2, 6] → Merge → [2, 4, 6, 8]

Level 2:
  [1, 3, 7, 9] + [2, 4, 6, 8] → Merge → [1, 2, 3, 4, 6, 7, 8, 9]
```

### Độ Phức Tạp

- **Thời gian**: O(n log(n/M)) khi M là số phần tử có thể sắp xếp trong bộ nhớ
- **Không gian disk**: O(n) cho các tệp tạm
- **Không gian memory**: O(M) - không phụ thuộc vào kích thước tệp

## Định Dạng Dữ Liệu

### Tệp Nhị Phân
- **Định dạng**: 8 bytes cho mỗi số thực (double precision - IEEE 754)
- **Byte Order**: Little-endian (mặc định trên Windows)
- **Ví dụ**:
  - 100 số → 800 bytes
  - 1,000 số → 8 KB
  - 1,000,000 số → 8 MB

### Cách Tạo Tệp Nhị Phân (Python)
```python
import struct

# Ghi dữ liệu
with open('data.bin', 'wb') as f:
    numbers = [3.14, 2.71, 1.41]
    for num in numbers:
        f.write(struct.pack('d', num))

# Đọc dữ liệu
with open('data.bin', 'rb') as f:
    while True:
        data = f.read(8)
        if not data:
            break
        num = struct.unpack('d', data)[0]
        print(num)
```

## Hướng Dẫn Sử Dụng

### 1. Cài Đặt
```bash
# Không cần cài đặt thêm thư viện ngoài
# Chỉ cần Python 3.6+
python --version
```

### 2. Chạy Giao Diện GUI
```bash
python main.py
# hoặc
python gui_app.py
```

### 3. Chọn Tệp và Sắp Xếp
1. Nhấp "Chọn Tập Tin" để chọn tệp nhị phân
   - Nếu chưa có, nhấp "Tạo Tập Tin Test"
   - Chọn kích thước (Nhỏ, Trung bình, Lớn, Rất lớn)

2. Điều chỉnh tham số (tùy chọn):
   - **Kích thước chunk**: Số lượng phần tử trong mỗi chunk
   - **Giới hạn memory**: Tối đa số phần tử trong bộ nhớ

3. Nhấp "Bắt Đầu Sắp Xếp"

4. Xem quá trình trong phần "Quá Trình Sắp Xếp"

5. Nhấp "Xem Kết Quả" để xem thống kê kết quả

### 4. Chạy Kiểm Thử
```bash
python test_script.py
```

Điều này sẽ:
- Tạo tệp test với kích thước khác nhau
- Sắp xếp từng tệp
- Hiển thị thời gian xử lý
- Kiểm tra tính chính xác của kết quả

### 5. Sử Dụng Trong Code
```python
from external_merge_sort import ExternalMergeSort
from data_generator import generate_random_binary_file

# Tạo tệp dữ liệu
generate_random_binary_file("input.bin", 1000)

# Sắp xếp
sorter = ExternalMergeSort("input.bin", "output.bin", chunk_size=10)
success = sorter.execute()

if success:
    # In log
    for line in sorter.step_log:
        print(line)
    
    # Xóa tệp tạm
    sorter.cleanup_temp_files()
```

## Các Module

### external_merge_sort.py

Lớp `ExternalMergeSort` chính:

```python
sorter = ExternalMergeSort(
    input_file="data.bin",
    output_file="sorted.bin",
    memory_limit=1000,      # Số phần tử
    chunk_size=10           # Kích thước mỗi chunk
)

# Thực thi sắp xếp
sorter.execute()

# Xem log chi tiết
for log_line in sorter.step_log:
    print(log_line)

# Dọn dẹp tệp tạm
sorter.cleanup_temp_files()
```

### data_generator.py

Các hàm tạo dữ liệu:

```python
# Tạo tệp ngẫu nhiên
generate_random_binary_file("file.bin", count=1000, min_value=-100, max_value=100)

# Tạo tệp được sắp xếp một phần
generate_partially_sorted_file("file.bin", count=1000)

# Đọc tệp
numbers = read_binary_file("file.bin")

# Lấy kích thước (MB)
size = get_file_size_mb("file.bin")
```

### gui_app.py

Giao diện Tkinter:

- **ExternalMergeSortGUI**: Lớp giao diện chính
- **SampleFileDialog**: Dialog tạo tệp test

## Ví Dụ

### Ví Dụ 1: Sắp Xếp Tệp Nhỏ
```python
from external_merge_sort import ExternalMergeSort
from data_generator import generate_random_binary_file

# Tạo tệp 100 số
generate_random_binary_file("test.bin", 100)

# Sắp xếp
sorter = ExternalMergeSort("test.bin", "sorted.bin", chunk_size=10)
sorter.execute()

# Hiển thị kết quả
for line in sorter.step_log:
    print(line)
```

### Ví Dụ 2: Điều Chỉnh Chunk Size
```python
# Chunk nhỏ → Nhiều file tạm, nhiều lần merge
sorter1 = ExternalMergeSort("input.bin", "output1.bin", chunk_size=5)

# Chunk lớn → Ít file tạm, ít lần merge
sorter2 = ExternalMergeSort("input.bin", "output2.bin", chunk_size=100)
```

### Ví Dụ 3: Kiểm Tra Tính Chính Xác
```python
from data_generator import read_binary_file

sorted_data = read_binary_file("sorted.bin")

# Kiểm tra đã sắp xếp
is_sorted = all(sorted_data[i] <= sorted_data[i+1] 
                for i in range(len(sorted_data)-1))

print(f"Đã sắp xếp: {is_sorted}")
print(f"Min: {min(sorted_data)}")
print(f"Max: {max(sorted_data)}")
```

## Hiệu Năng

### Kích Thước Tệp và Thời Gian

| Số Lượng | Kích Thước | Chunk=10 | Chunk=50 | Chunk=100|
|----------|-----------|----------|----------|----------|
| 100      | 800B      | ~0.01s   | ~0.01s   | ~0.01s   |
| 1,000    | 8KB       | ~0.05s   | ~0.04s   | ~0.03s   |
| 10,000   | 80KB      | ~0.3s    | ~0.25s   | ~0.2s    |
| 100,000  | 800KB     | ~3s      | ~2.5s    | ~2.2s    |

*Lưu ý: Thời gian thực tế phụ thuộc vào tốc độ ổ đĩa và bộ xử lý*

## Tối Ưu Hóa

### Chọn Chunk Size
- **Nhỏ (5-10)**: Nếu RAM có hạn
- **Trung bình (20-50)**: Cân bằng hiệu năng/memory
- **Lớn (100+)**: Nếu RAM dư dả

### Cải Thiện Tốc Độ
```python
# 1. Tăng chunk_size
sorter = ExternalMergeSort(..., chunk_size=500)

# 2. Sử dụng SSD thay vì HDD
# 3. Tăng memory_limit nếu có thể
sorter = ExternalMergeSort(..., memory_limit=5000)
```

## Xử Lý Lỗi

### Tệp Không Tồn Tại
```python
import os
if not os.path.exists("input.bin"):
    print("Tệp không tồn tại!")
```

### Tệp Trống
```python
if sorter.total_numbers == 0:
    print("Tệp đầu vào trống!")
```

### Lỗi Ghi
```python
try:
    sorter.execute()
except IOError as e:
    print(f"Lỗi ghi/đọc file: {e}")
```

## Câu Hỏi Thường Gặp

**Q: Ứng dụng này có thể xử lý tệp bao lớn?**
A: Lý thuyết là không giới hạn, nhưng thực tế phụ thuộc vào dung lượng ổ đĩa.

**Q: Có thể sắp xếp theo thứ tự giảm dần không?**
A: Có, sửa hàm so sánh trong `_merge_two_files()` (đổi `<=` thành `>=`)

**Q: Có thể sắp xếp theo cột cụ thể không?**
A: Tệp hiện tại chỉ hỗ trợ số thực. Có thể mở rộng để hỗ trợ struct phức tạp.

**Q: Tại sao cần xóa tệp tạm?**
A: Để tiết kiệm không gian đĩa. Ứng dụng tự động xóa khi kết thúc.

## Phát Triển Tiếp Theo

Các tính năng có thể thêm:
- [ ] Sắp xếp song song (multi-threading)
- [ ] Hỗ trợ các kiểu dữ liệu khác (int, float, struct)
- [ ] Thanh tiến trình chi tiết
- [ ] So sánh hiệu năng với các thuật toán khác
- [ ] Export thống kê sang CSV

## Tác Giả & Giấy Phép

Ứng dụng học tập minh họa External Merge Sort.
Sử dụng tự do cho mục đích giáo dục.

## Liên Hệ & Hỗ Trợ

Nếu gặp lỗi, vui lòng kiểm tra:
1. Python version >= 3.6
2. Tệp input hợp lệ (8 bytes/số)
3. Dung lượng ổ đĩa đủ
4. Quyền ghi vào thư mục hiện tại

---

**Phiên Bản**: 1.0  
**Cập Nhật Lần Cuối**: 2026-03-04
