"""
Data Generator - Tạo tập tin nhị phân chứa số thực ngẫu nhiên
"""

import struct
import random
import os


def generate_random_binary_file(filename, count, min_value=-1000, max_value=1000):
    """
    Tạo tập tin nhị phân chứa các số thực ngẫu nhiên
    
    Args:
        filename (str): Tên tập tin
        count (int): Số lượng số thực
        min_value (float): Giá trị tối thiểu
        max_value (float): Giá trị tối đa
        
    Returns:
        bool: Thành công hay không
    """
    try:
        with open(filename, 'wb') as f:
            for _ in range(count):
                num = random.uniform(min_value, max_value)
                f.write(struct.pack('d', num))
        return True
    except IOError as e:
        print(f"Lỗi tạo file: {e}")
        return False


def generate_unsorted_test_file(filename, count):
    """
    Tạo tập tin test không được sắp xếp
    
    Args:
        filename (str): Tên tập tin
        count (int): Số lượng số thực
        
    Returns:
        bool: Thành công hay không
    """
    return generate_random_binary_file(filename, count, -10000, 10000)


def generate_partially_sorted_file(filename, count):
    """
    Tạo tập tin test được sắp xếp một phần
    
    Args:
        filename (str): Tên tập tin
        count (int): Số lượng số thực
        
    Returns:
        bool: Thành công hay không
    """
    try:
        # Tạo dãy số đã sắp xếp
        numbers = sorted([random.uniform(-10000, 10000) for _ in range(count)])
        
        # Xáo trộn một phần
        shuffle_count = count // 4
        for _ in range(shuffle_count):
            i = random.randint(0, count - 1)
            j = random.randint(0, count - 1)
            numbers[i], numbers[j] = numbers[j], numbers[i]
        
        with open(filename, 'wb') as f:
            for num in numbers:
                f.write(struct.pack('d', num))
        return True
    except IOError as e:
        print(f"Lỗi tạo file: {e}")
        return False


def read_binary_file(filename):
    """
    Đọc tập tin nhị phân và trả về danh sách số thực
    
    Args:
        filename (str): Tên tập tin
        
    Returns:
        list: Danh sách số thực
    """
    numbers = []
    try:
        with open(filename, 'rb') as f:
            while True:
                data = f.read(8)
                if not data:
                    break
                number = struct.unpack('d', data)[0]
                numbers.append(number)
    except IOError as e:
        print(f"Lỗi đọc file: {e}")
    
    return numbers


def get_file_size_mb(filename):
    """
    Lấy kích thước tập tin (MB)
    
    Args:
        filename (str): Tên tập tin
        
    Returns:
        float: Kích thước (MB)
    """
    try:
        size_bytes = os.path.getsize(filename)
        return size_bytes / (1024 * 1024)
    except:
        return 0


def create_sample_files():
    """
    Tạo các tập tin mẫu để test
    """
    print("Tạo tập tin test...")
    
    # Tập tin nhỏ (100 số)
    if generate_random_binary_file("sample_small.bin", 100):
        print("✓ Created: sample_small.bin (100 numbers)")
    
    # Tập tin trung bình (1000 số)
    if generate_random_binary_file("sample_medium.bin", 1000):
        print("✓ Created: sample_medium.bin (1000 numbers)")
    
    # Tập tin được sắp xếp một phần
    if generate_partially_sorted_file("sample_partial.bin", 100):
        print("✓ Created: sample_partial.bin (100 numbers, partially sorted)")


if __name__ == "__main__":
    create_sample_files()
