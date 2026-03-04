"""
Demo Command Line - Minh họa External Merge Sort qua dòng lệnh
"""

import os
import sys
from external_merge_sort import ExternalMergeSort
from data_generator import generate_random_binary_file, read_binary_file, get_file_size_mb


def print_header(text):
    """In tiêu đề"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_data_sample(numbers, max_display=10):
    """In mẫu dữ liệu"""
    if not numbers:
        return "[]"
    
    if len(numbers) <= max_display:
        return str([f"{x:.2f}" for x in numbers])
    else:
        first = [f"{x:.2f}" for x in numbers[:3]]
        last = [f"{x:.2f}" for x in numbers[-3:]]
        return f"[{', '.join(first)}, ..., {', '.join(last)}]"


def demo_interactive():
    """Demo tương tác"""
    print_header("DEMO INTERACTIVE - EXTERNAL MERGE SORT")
    
    while True:
        print("\n1. Tạo tệp dữ liệu mới")
        print("2. Sắp xếp tệp")
        print("3. Xem kết quả")
        print("4. Thoát")
        
        choice = input("\nChọn lựa (1-4): ").strip()
        
        if choice == "1":
            demo_create_file()
        elif choice == "2":
            demo_sort()
        elif choice == "3":
            demo_view()
        elif choice == "4":
            print("\nTạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ!")


def demo_create_file():
    """Demo tạo tệp"""
    print_header("TẠO TỆP DỮ LIỆU")
    
    try:
        filename = input("Tên tệp (mặc định: demo.bin): ").strip() or "demo.bin"
        
        print(f"\nKích thước tệp:")
        print("  1. Nhỏ (100 số = 800B)")
        print("  2. Trung bình (1000 số = 8KB)")
        print("  3. Lớn (10000 số = 80KB)")
        print("  4. Rất lớn (100000 số = 800KB)")
        
        size_choice = input("\nChọn (1-4): ").strip()
        
        sizes = {
            "1": (100, "Nhỏ"),
            "2": (1000, "Trung bình"),
            "3": (10000, "Lớn"),
            "4": (100000, "Rất lớn")
        }
        
        if size_choice not in sizes:
            print("Lựa chọn không hợp lệ!")
            return
        
        count, size_name = sizes[size_choice]
        
        print(f"\nTạo {size_name}: {count} số thực...")
        if generate_random_binary_file(filename, count):
            size_mb = get_file_size_mb(filename)
            print(f"✓ Tạo thành công!")
            print(f"  - Tệp: {filename}")
            print(f"  - Số lượng: {count}")
            print(f"  - Kích thước: {size_mb*1024:.2f} KB")
        else:
            print("✗ Lỗi tạo tệp!")
            
    except Exception as e:
        print(f"Lỗi: {e}")


def demo_sort():
    """Demo sắp xếp"""
    print_header("SẮP XẾP TỆP")
    
    try:
        filename = input("Tên tệp cần sắp xếp: ").strip()
        
        if not os.path.exists(filename):
            print(f"✗ Tệp '{filename}' không tồn tại!")
            return
        
        output_file = input(f"Tệp kết quả (mặc định: {filename.replace('.bin', '_sorted.bin')}): ").strip()
        if not output_file:
            output_file = filename.replace(".bin", "_sorted.bin")
        
        chunk_size_input = input("Kích thước chunk (mặc định: 10): ").strip()
        chunk_size = int(chunk_size_input) if chunk_size_input else 10
        
        print(f"\nThông tin tệp:")
        print(f"  - Tệp: {filename}")
        print(f"  - Kích thước: {get_file_size_mb(filename)*1024:.2f} KB")
        print(f"  - Chunk size: {chunk_size}")
        
        print(f"\n⏳ Đang sắp xếp...")
        
        sorter = ExternalMergeSort(filename, output_file, chunk_size=chunk_size)
        success = sorter.execute()
        
        if success:
            print(f"\n✓ Sắp xếp thành công!")
            print(f"\nChi tiết quá trình:")
            for log_line in sorter.step_log:
                if log_line.startswith("="):
                    print(f"\n{log_line}")
                else:
                    print(log_line)
            
            sorter.cleanup_temp_files()
        else:
            print(f"\n✗ Lỗi sắp xếp!")
            sorter.cleanup_temp_files()
            
    except ValueError:
        print("Lỗi: Vui lòng nhập giá trị hợp lệ!")
    except Exception as e:
        print(f"Lỗi: {e}")


def demo_view():
    """Demo xem kết quả"""
    print_header("XEM DỮ LIỆU")
    
    try:
        filename = input("Tên tệp cần xem: ").strip()
        
        if not os.path.exists(filename):
            print(f"✗ Tệp '{filename}' không tồn tại!")
            return
        
        print(f"\nĐang đọc {filename}...")
        numbers = read_binary_file(filename)
        
        if not numbers:
            print("Tệp trống!")
            return
        
        is_sorted = all(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1))
        
        print(f"\nThông tin dữ liệu:")
        print(f"  - Số lượng: {len(numbers)} số")
        print(f"  - Min: {min(numbers):.4f}")
        print(f"  - Max: {max(numbers):.4f}")
        print(f"  - Trung bình: {sum(numbers)/len(numbers):.4f}")
        print(f"  - Đã sắp xếp: {'✓ Có' if is_sorted else '✗ Không'}")
        
        print(f"\nDữ liệu mẫu:")
        print(f"  {print_data_sample(numbers, 20)}")
        
    except Exception as e:
        print(f"Lỗi: {e}")


def demo_quick_test():
    """Demo nhanh"""
    print_header("DEMO NHANH")
    
    test_file = "quick_demo.bin"
    output_file = "quick_demo_sorted.bin"
    
    print("Bước 1: Tạo tệp test (100 số)")
    if not generate_random_binary_file(test_file, 100):
        print("✗ Lỗi tạo tệp!")
        return
    
    original = read_binary_file(test_file)
    print(f"✓ Tạo thành công")
    print(f"  Dữ liệu: {print_data_sample(original)}")
    
    print(f"\nBước 2: Sắp xếp")
    sorter = ExternalMergeSort(test_file, output_file, chunk_size=10)
    
    if not sorter.execute():
        print("✗ Lỗi sắp xếp!")
        sorter.cleanup_temp_files()
        return
    
    print(f"✓ Hoàn thành")
    
    sorted_data = read_binary_file(output_file)
    print(f"\nBước 3: Kiểm tra kết quả")
    print(f"  - Số lượng: {len(sorted_data)}")
    print(f"  - Min: {min(sorted_data):.4f}")
    print(f"  - Max: {max(sorted_data):.4f}")
    print(f"  - Đã sắp xếp: {'✓ Có' if all(sorted_data[i] <= sorted_data[i+1] for i in range(len(sorted_data)-1)) else '✗ Không'}")
    print(f"  Dữ liệu: {print_data_sample(sorted_data)}")
    
    # Dọn dẹp
    sorter.cleanup_temp_files()
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(output_file):
        os.remove(output_file)
    
    print(f"\n✓ Demo nhanh hoàn thành!")


def main():
    """Hàm chính"""
    print("\n" + "="*70)
    print("  EXTERNAL MERGE SORT - DEMO COMMAND LINE")
    print("="*70)
    print("\nChế độ:")
    print("  1. Interactive (tương tác)")
    print("  2. Quick Demo (demo nhanh)")
    
    choice = input("\nChọn chế độ (1-2): ").strip()
    
    if choice == "1":
        demo_interactive()
    elif choice == "2":
        demo_quick_test()
    else:
        print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nĐã hủy.")
    except Exception as e:
        print(f"\nLỗi: {e}")
        import traceback
        traceback.print_exc()
