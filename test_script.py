"""
Test Script - Kiểm thử External Merge Sort
"""

import os
import time
from external_merge_sort import ExternalMergeSort
from data_generator import generate_random_binary_file, read_binary_file, get_file_size_mb


def print_separator(title=""):
    """In đường phân cách"""
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
        print("="*70)
    print()


def test_external_merge_sort():
    """Kiểm thử External Merge Sort"""
    
    print_separator("EXTERNAL MERGE SORT - KIỂM THỬ")
    
    test_cases = [
        ("test_small.bin", 50, "Nhỏ"),
        ("test_medium.bin", 500, "Trung bình"),
        ("test_large.bin", 5000, "Lớn"),
    ]
    
    for test_file, count, description in test_cases:
        print_separator(f"TEST: {description} ({count} số thực)")
        
        # Tạo tập tin test
        print(f"1. Tạo tập tin test: {test_file}")
        print(f"   - Số lượng: {count} số thực")
        if generate_random_binary_file(test_file, count, -10000, 10000):
            size_mb = get_file_size_mb(test_file)
            print(f"   - Kích thước: {size_mb*1024:.2f} KB ({size_mb:.6f} MB)")
            print(f"   ✓ Tạo thành công")
        else:
            print(f"   ✗ Lỗi tạo file!")
            continue
        
        # Đọc dữ liệu gốc
        print(f"\n2. Đọc dữ liệu gốc")
        original = read_binary_file(test_file)
        print(f"   - Số lượng đọc được: {len(original)}")
        if original:
            print(f"   - Min: {min(original):.2f}")
            print(f"   - Max: {max(original):.2f}")
            print(f"   - Dữ liệu mẫu: {original[:3]}...{original[-2:]}")
        
        # Sắp xếp
        print(f"\n3. Thực hiện External Merge Sort")
        output_file = test_file.replace(".bin", "_sorted.bin")
        
        start_time = time.time()
        sorter = ExternalMergeSort(test_file, output_file, chunk_size=10)
        success = sorter.execute()
        elapsed_time = time.time() - start_time
        
        if success:
            print(f"\n   ✓ Sắp xếp thành công ({elapsed_time:.3f}s)")
            
            # Hiển thị log
            for log_line in sorter.step_log:
                print(f"   {log_line}")
            
            # Kiểm tra kết quả
            print(f"\n4. Kiểm tra kết quả")
            sorted_data = read_binary_file(output_file)
            
            is_sorted = all(sorted_data[i] <= sorted_data[i+1] for i in range(len(sorted_data)-1))
            print(f"   - Đã được sắp xếp: {'✓ Có' if is_sorted else '✗ Không'}")
            print(f"   - Số lượng: {len(sorted_data)}")
            print(f"   - Min: {min(sorted_data):.2f}")
            print(f"   - Max: {max(sorted_data):.2f}")
            print(f"   - Dữ liệu mẫu: {sorted_data[:3]}...{sorted_data[-2:]}")
            
            # Kiểm tra tính chất bảo toàn
            if len(sorted_data) == len(original):
                print(f"   - Lưu giữ số lượng: ✓ Có")
            else:
                print(f"   - Lưu giữ số lượng: ✗ Không ({len(original)} -> {len(sorted_data)})")
            
            # Dọn dẹp
            sorter.cleanup_temp_files()
            if os.path.exists(test_file):
                os.remove(test_file)
            if os.path.exists(output_file):
                os.remove(output_file)
            
        else:
            print(f"   ✗ Lỗi sắp xếp!")
            sorter.cleanup_temp_files()


def test_chunk_sizes():
    """Kiểm thử các kích thước chunk khác nhau"""
    print_separator("TEST: ẢNH HƯỞNG CỦA KÍCH THƯỚC CHUNK")
    
    test_file = "test_chunk_effect.bin"
    count = 1000
    
    print(f"Tạo tập tin test: {count} số thực")
    generate_random_binary_file(test_file, count)
    
    chunk_sizes = [5, 10, 20, 50, 100]
    
    for chunk_size in chunk_sizes:
        output_file = f"sorted_chunk_{chunk_size}.bin"
        
        print(f"\nChunk size: {chunk_size}")
        
        start_time = time.time()
        sorter = ExternalMergeSort(test_file, output_file, chunk_size=chunk_size)
        success = sorter.execute()
        elapsed_time = time.time() - start_time
        
        if success:
            print(f"  ✓ Hoàn thành ({elapsed_time:.4f}s)")
            sorted_data = read_binary_file(output_file)
            is_sorted = all(sorted_data[i] <= sorted_data[i+1] for i in range(len(sorted_data)-1))
            print(f"  - Đã sắp xếp: {'✓' if is_sorted else '✗'}")
            
            sorter.cleanup_temp_files()
            if os.path.exists(output_file):
                os.remove(output_file)
        else:
            print(f"  ✗ Lỗi!")
            sorter.cleanup_temp_files()
    
    if os.path.exists(test_file):
        os.remove(test_file)


if __name__ == "__main__":
    try:
        print("\n")
        test_external_merge_sort()
        test_chunk_sizes()
        
        print_separator("KIỂM THỬ HOÀN THÀNH")
        
    except Exception as e:
        print(f"\nLỗi: {e}")
        import traceback
        traceback.print_exc()
