"""
External Merge Sort Implementation
Sắp xếp dữ liệu từ tập tin nhị phân chứa số thực (8 bytes)
"""

import struct
import os
import heapq
from pathlib import Path


class ExternalMergeSort:
    """Lớp thực hiện External Merge Sort"""
    
    def __init__(self, input_file, output_file, memory_limit=1000, chunk_size=10):
        """
        Khởi tạo External Merge Sort
        
        Args:
            input_file (str): Đường dẫn tập tin đầu vào
            output_file (str): Đường dẫn tập tin kết quả
            memory_limit (int): Số lượng số thực có thể lưu trong bộ nhớ
            chunk_size (int): Kích thước chunk cho việc đọc
        """
        self.input_file = input_file
        self.output_file = output_file
        self.memory_limit = memory_limit
        self.chunk_size = chunk_size
        self.temp_files = []
        self.step_log = []
        self.total_numbers = 0
        
    def read_binary_file(self, filename, limit=None):
        """
        Đọc số thực từ tập tin nhị phân
        
        Args:
            filename (str): Tên tập tin
            limit (int): Giới hạn số lượng đọc
            
        Returns:
            list: Danh sách số thực
        """
        numbers = []
        try:
            with open(filename, 'rb') as f:
                count = 0
                while True:
                    data = f.read(8)  # 8 bytes = double precision float
                    if not data:
                        break
                    number = struct.unpack('d', data)[0]
                    numbers.append(number)
                    count += 1
                    if limit and count >= limit:
                        break
        except IOError as e:
            self.step_log.append(f"Lỗi đọc file: {e}")
        
        return numbers
    
    def write_binary_file(self, filename, numbers, mode='wb'):
        """
        Ghi số thực vào tập tin nhị phân
        
        Args:
            filename (str): Tên tập tin
            numbers (list): Danh sách số thực
            mode (str): Chế độ ghi
        """
        try:
            with open(filename, mode) as f:
                for num in numbers:
                    f.write(struct.pack('d', num))
        except IOError as e:
            self.step_log.append(f"Lỗi ghi file: {e}")
    
    def count_numbers_in_file(self, filename):
        """
        Đếm số lượng số thực trong tập tin
        
        Args:
            filename (str): Tên tập tin
            
        Returns:
            int: Số lượng số thực
        """
        try:
            file_size = os.path.getsize(filename)
            return file_size // 8
        except IOError as e:
            self.step_log.append(f"Lỗi lấy kích thước file: {e}")
            return 0
    
    def phase1_create_sorted_chunks(self):
        """
        Giai đoạn 1: Chia tập tin đầu vào thành các chunk và sắp xếp
        """
        self.step_log.append("=" * 60)
        self.step_log.append("GIAI ĐOẠN 1: Tạo các chunk được sắp xếp")
        self.step_log.append("=" * 60)
        
        self.total_numbers = self.count_numbers_in_file(self.input_file)
        self.step_log.append(f"Tổng số lượng: {self.total_numbers} số thực")
        
        chunk_index = 0
        
        with open(self.input_file, 'rb') as f:
            while True:
                # Đọc chunk_size số thực
                numbers = []
                for _ in range(self.chunk_size):
                    data = f.read(8)
                    if not data:
                        break
                    number = struct.unpack('d', data)[0]
                    numbers.append(number)
                
                if not numbers:
                    break
                
                # Sắp xếp chunk
                numbers.sort()
                
                # Tạo tập tin tạm cho chunk
                temp_file = f"temp_chunk_{chunk_index}.bin"
                self.temp_files.append(temp_file)
                self.write_binary_file(temp_file, numbers)
                
                self.step_log.append(f"\nChunk {chunk_index}:")
                self.step_log.append(f"  - Số lượng: {len(numbers)}")
                self.step_log.append(f"  - Dữ liệu: {numbers[:5]}" + 
                                   (f"...{numbers[-2:]}" if len(numbers) > 5 else ""))
                self.step_log.append(f"  - Tập tin: {temp_file}")
                
                chunk_index += 1
        
        self.step_log.append(f"\nTổng chunk tạo ra: {chunk_index}")
        return chunk_index
    
    def phase2_merge_sorted_chunks(self):
        """
        Giai đoạn 2: Merge các chunk được sắp xếp
        """
        self.step_log.append("\n" + "=" * 60)
        self.step_log.append("GIAI ĐOẠN 2: Merge các chunk")
        self.step_log.append("=" * 60)
        
        if not self.temp_files:
            self.step_log.append("Không có chunk để merge")
            return
        
        if len(self.temp_files) == 1:
            self.step_log.append(f"Chỉ có 1 chunk, sao chép trực tiếp: {self.temp_files[0]} -> {self.output_file}")
            os.rename(self.temp_files[0], self.output_file)
            self.temp_files = []
            return
        
        # Merge các chunk
        merge_level = 0
        files_to_merge = self.temp_files[:]
        
        while len(files_to_merge) > 1:
            merge_level += 1
            self.step_log.append(f"\nMerge Level {merge_level}:")
            self.step_log.append(f"  - Số file cần merge: {len(files_to_merge)}")
            
            next_level_files = []
            
            # Merge từng cặp files
            for i in range(0, len(files_to_merge), 2):
                if i + 1 < len(files_to_merge):
                    # Có cặp đầy đủ
                    file1 = files_to_merge[i]
                    file2 = files_to_merge[i + 1]
                    
                    merged_file = f"merged_level{merge_level}_{len(next_level_files)}.bin"
                    self._merge_two_files(file1, file2, merged_file)
                    
                    next_level_files.append(merged_file)
                    self.step_log.append(f"  - Merge {file1} + {file2} -> {merged_file}")
                    
                    # Xóa files cũ
                    os.remove(file1)
                    os.remove(file2)
                else:
                    # File lẻ
                    file1 = files_to_merge[i]
                    merged_file = f"merged_level{merge_level}_{len(next_level_files)}.bin"
                    os.rename(file1, merged_file)
                    next_level_files.append(merged_file)
                    self.step_log.append(f"  - File lẻ: {file1} -> {merged_file}")
            
            files_to_merge = next_level_files
        
        # Đổi tên file cuối cùng
        if files_to_merge:
            os.rename(files_to_merge[0], self.output_file)
            self.step_log.append(f"\nFile kết quả final: {files_to_merge[0]} -> {self.output_file}")
    
    def _merge_two_files(self, file1, file2, output_file):
        """
        Merge hai tập tin đã được sắp xếp
        
        Args:
            file1 (str): Tập tin 1
            file2 (str): Tập tin 2
            output_file (str): Tập tin kết quả
        """
        with open(file1, 'rb') as f1, \
             open(file2, 'rb') as f2, \
             open(output_file, 'wb') as fout:
            
            # Đọc số đầu tiên từ mỗi file
            data1 = f1.read(8)
            data2 = f2.read(8)
            
            num1 = struct.unpack('d', data1)[0] if data1 else None
            num2 = struct.unpack('d', data2)[0] if data2 else None
            
            while num1 is not None or num2 is not None:
                if num1 is None:
                    # File 1 hết
                    fout.write(struct.pack('d', num2))
                    data2 = f2.read(8)
                    num2 = struct.unpack('d', data2)[0] if data2 else None
                elif num2 is None:
                    # File 2 hết
                    fout.write(struct.pack('d', num1))
                    data1 = f1.read(8)
                    num1 = struct.unpack('d', data1)[0] if data1 else None
                elif num1 <= num2:
                    # num1 nhỏ hơn hoặc bằng num2
                    fout.write(struct.pack('d', num1))
                    data1 = f1.read(8)
                    num1 = struct.unpack('d', data1)[0] if data1 else None
                else:
                    # num2 nhỏ hơn num1
                    fout.write(struct.pack('d', num2))
                    data2 = f2.read(8)
                    num2 = struct.unpack('d', data2)[0] if data2 else None
    
    def execute(self):
        """
        Thực thi External Merge Sort
        """
        try:
            self.step_log.clear()
            self.step_log.append(f"Nguồn dữ liệu: {self.input_file}")
            self.step_log.append(f"Tập tin tạm: chunk_size={self.chunk_size}")
            
            # Giai đoạn 1
            chunk_count = self.phase1_create_sorted_chunks()
            
            if chunk_count == 0:
                self.step_log.append("Tập tin đầu vào trống!")
                return False
            
            # Giai đoạn 2
            self.phase2_merge_sorted_chunks()
            
            self.step_log.append("\n" + "=" * 60)
            self.step_log.append("HOÀN THÀNH!")
            self.step_log.append("=" * 60)
            self.step_log.append(f"Kết quả được lưu tại: {self.output_file}")
            
            # Xác minh kết quả
            result = self.read_binary_file(self.output_file)
            self.step_log.append(f"\nKết quả cuối cùng ({len(result)} số):")
            self.step_log.append(f"  - Min: {min(result) if result else 'N/A'}")
            self.step_log.append(f"  - Max: {max(result) if result else 'N/A'}")
            self.step_log.append(f"  - Đầu: {result[:5]}" + 
                               (f"...{result[-2:]}" if len(result) > 5 else ""))
            
            # Kiểm tra tính chất đã sắp xếp
            is_sorted = all(result[i] <= result[i+1] for i in range(len(result)-1))
            self.step_log.append(f"  - Đã sắp xếp: {'✓ Có' if is_sorted else '✗ Không'}")
            
            return True
            
        except Exception as e:
            self.step_log.append(f"Lỗi: {str(e)}")
            return False
    
    def cleanup_temp_files(self):
        """Xóa các tập tin tạm"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        self.temp_files = []
