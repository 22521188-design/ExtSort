"""
GUI Application - Giao diện người dùng cho External Merge Sort
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from external_merge_sort import ExternalMergeSort
from data_generator import read_binary_file, get_file_size_mb


class ExternalMergeSortGUI:
    """Giao diện GUI cho External Merge Sort"""
    
    def __init__(self, root):
        """Khởi tạo giao diện"""
        self.root = root
        self.root.title("External Merge Sort - Sắp xếp dữ liệu nhị phân")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.selected_file = None
        self.output_file = None
        self.sorter = None
        
        self.create_widgets()
        
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        
        # Phần chọn file
        input_frame = ttk.LabelFrame(self.root, text="Chọn Tập Tin Đầu Vào", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn_select = ttk.Button(input_frame, text="Chọn Tập Tin", command=self.select_input_file)
        btn_select.pack(side=tk.LEFT, padx=5)
        
        self.label_file = ttk.Label(input_frame, text="Chưa chọn file", foreground="gray")
        self.label_file.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Phần thông tin tập tin
        info_frame = ttk.LabelFrame(self.root, text="Thông Tin Tập Tin", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        grid_row = 0
        
        ttk.Label(info_frame, text="Tên file:").grid(row=grid_row, column=0, sticky=tk.W)
        self.label_filename = ttk.Label(info_frame, text="-", foreground="blue")
        self.label_filename.grid(row=grid_row, column=1, sticky=tk.W)
        grid_row += 1
        
        ttk.Label(info_frame, text="Kích thước (MB):").grid(row=grid_row, column=0, sticky=tk.W)
        self.label_size = ttk.Label(info_frame, text="-")
        self.label_size.grid(row=grid_row, column=1, sticky=tk.W)
        grid_row += 1
        
        ttk.Label(info_frame, text="Số lượng số thực:").grid(row=grid_row, column=0, sticky=tk.W)
        self.label_count = ttk.Label(info_frame, text="-")
        self.label_count.grid(row=grid_row, column=1, sticky=tk.W)
        grid_row += 1
        
        ttk.Label(info_frame, text="Giá trị min:").grid(row=grid_row, column=0, sticky=tk.W)
        self.label_min = ttk.Label(info_frame, text="-")
        self.label_min.grid(row=grid_row, column=1, sticky=tk.W)
        grid_row += 1
        
        ttk.Label(info_frame, text="Giá trị max:").grid(row=grid_row, column=0, sticky=tk.W)
        self.label_max = ttk.Label(info_frame, text="-")
        self.label_max.grid(row=grid_row, column=1, sticky=tk.W)
        
        # Phần cài đặt tham số
        param_frame = ttk.LabelFrame(self.root, text="Cài Đặt Tham Số", padding=10)
        param_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(param_frame, text="Kích thước chunk (số lượng):").pack(side=tk.LEFT, padx=5)
        self.spinbox_chunk = ttk.Spinbox(param_frame, from_=1, to=10000, width=10)
        self.spinbox_chunk.set(10)
        self.spinbox_chunk.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(param_frame, text="Giới hạn memory (số lượng):").pack(side=tk.LEFT, padx=5)
        self.spinbox_memory = ttk.Spinbox(param_frame, from_=1, to=10000, width=10)
        self.spinbox_memory.set(1000)
        self.spinbox_memory.pack(side=tk.LEFT, padx=5)
        
        # Phần nút điều khiển
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.btn_sort = ttk.Button(btn_frame, text="Bắt Đầu Sắp Xếp", command=self.start_sorting, state=tk.DISABLED)
        self.btn_sort.pack(side=tk.LEFT, padx=5)
        
        btn_view_result = ttk.Button(btn_frame, text="Xem Kết Quả", command=self.view_result, state=tk.DISABLED)
        btn_view_result.pack(side=tk.LEFT, padx=5)
        self.btn_view_result = btn_view_result
        
        btn_create_sample = ttk.Button(btn_frame, text="Tạo Tập Tin Test", command=self.create_sample_file)
        btn_create_sample.pack(side=tk.LEFT, padx=5)
        
        # Phần hiển thị quá trình
        log_frame = ttk.LabelFrame(self.root, text="Quá Trình Sắp Xếp", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.text_log = scrolledtext.ScrolledText(log_frame, height=15, width=100, state=tk.DISABLED)
        self.text_log.pack(fill=tk.BOTH, expand=True)
        
        # Thanh trạng thái
        self.status_var = tk.StringVar(value="Sẵn sàng")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, padx=10, pady=5)
    
    def select_input_file(self):
        """Chọn tập tin đầu vào"""
        filename = filedialog.askopenfilename(
            title="Chọn tập tin dữ liệu",
            filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")]
        )
        
        if filename:
            self.selected_file = filename
            self.output_file = os.path.splitext(filename)[0] + "_sorted.bin"
            
            self.label_file.config(text=filename)
            self.label_filename.config(text=os.path.basename(filename))
            
            # Lấy thông tin tập tin
            self.update_file_info()
            
            self.btn_sort.config(state=tk.NORMAL)
            self.status_var.set(f"Đã chọn: {os.path.basename(filename)}")
    
    def update_file_info(self):
        """Cập nhật thông tin tập tin"""
        if not self.selected_file or not os.path.exists(self.selected_file):
            return
        
        try:
            # Kích thước
            size_mb = get_file_size_mb(self.selected_file)
            self.label_size.config(text=f"{size_mb:.4f}")
            
            # Đọc dữ liệu
            self.log_append("Đang đọc tập tin...\n")
            self.root.update()
            
            numbers = read_binary_file(self.selected_file)
            self.log_append(f"Hoàn thành!\n")
            
            if numbers:
                self.label_count.config(text=str(len(numbers)))
                self.label_min.config(text=f"{min(numbers):.2f}")
                self.label_max.config(text=f"{max(numbers):.2f}")
            else:
                self.label_count.config(text="0")
                self.label_min.config(text="-")
                self.label_max.config(text="-")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    
    def start_sorting(self):
        """Bắt đầu quá trình sắp xếp"""
        if not self.selected_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tập tin!")
            return
        
        try:
            chunk_size = int(self.spinbox_chunk.get())
            memory_limit = int(self.spinbox_memory.get())
            
            self.text_log.config(state=tk.NORMAL)
            self.text_log.delete('1.0', tk.END)
            self.text_log.config(state=tk.DISABLED)
            
            self.btn_sort.config(state=tk.DISABLED)
            self.status_var.set("Đang sắp xếp...")
            self.root.update()
            
            # Thực thi
            self.sorter = ExternalMergeSort(
                self.selected_file,
                self.output_file,
                memory_limit=memory_limit,
                chunk_size=chunk_size
            )
            
            success = self.sorter.execute()
            
            # Hiển thị log
            self.text_log.config(state=tk.NORMAL)
            for log_line in self.sorter.step_log:
                self.text_log.insert(tk.END, log_line + "\n")
            self.text_log.see(tk.END)
            self.text_log.config(state=tk.DISABLED)
            
            if success:
                self.status_var.set("Sắp xếp hoàn thành!")
                messagebox.showinfo("Thành công", 
                    f"Dữ liệu được sắp xếp thành công!\nKết quả: {self.output_file}")
                self.btn_view_result.config(state=tk.NORMAL)
            else:
                self.status_var.set("Lỗi sắp xếp!")
                messagebox.showerror("Lỗi", "Quá trình sắp xếp gặp lỗi!")
            
            self.btn_sort.config(state=tk.NORMAL)
            self.sorter.cleanup_temp_files()
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập các tham số hợp lệ!")
            self.btn_sort.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")
            self.btn_sort.config(state=tk.NORMAL)
    
    def view_result(self):
        """Xem kết quả sắp xếp"""
        if not self.output_file or not os.path.exists(self.output_file):
            messagebox.showwarning("Cảnh báo", "Tập tin kết quả không tồn tại!")
            return
        
        try:
            numbers = read_binary_file(self.output_file)
            
            # Tạo window mới
            result_window = tk.Toplevel(self.root)
            result_window.title("Kết Quả Sắp Xếp")
            result_window.geometry("600x400")
            
            # Thông tin
            info_text = f"""
Kết Quả Sắp Xếp
{'='*50}
Tập tin: {os.path.basename(self.output_file)}
Số lượng: {len(numbers)} số thực
Min: {min(numbers):.4f}
Max: {max(numbers):.4f}
Trung bình: {sum(numbers)/len(numbers) if numbers else 0:.4f}

{'='*50}
Dữ liệu (20 số đầu tiên):
{numbers[:20]}

...

Dữ liệu (5 số cuối cùng):
{numbers[-5:]}
            """
            
            text_widget = scrolledtext.ScrolledText(result_window)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, info_text)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file kết quả: {str(e)}")
    
    def create_sample_file(self):
        """Tạo tập tin test"""
        dialog = SampleFileDialog(self.root)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            self.selected_file = dialog.result
            self.output_file = os.path.splitext(self.selected_file)[0] + "_sorted.bin"
            
            self.label_file.config(text=self.selected_file)
            self.label_filename.config(text=os.path.basename(self.selected_file))
            
            self.update_file_info()
            self.btn_sort.config(state=tk.NORMAL)
            self.status_var.set(f"Đã tạo: {os.path.basename(self.selected_file)}")
    
    def log_append(self, message):
        """Thêm message vào log"""
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, message)
        self.text_log.see(tk.END)
        self.text_log.config(state=tk.DISABLED)


class SampleFileDialog:
    """Dialog tạo tập tin mẫu"""
    
    def __init__(self, parent):
        self.result = None
        
        self.top = tk.Toplevel(parent)
        self.top.title("Tạo Tập Tin Test")
        self.top.geometry("400x250")
        self.top.grab_set()
        
        # Nội dung
        frame = ttk.Frame(self.top, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Chọn kích thước tập tin test:").pack(pady=5)
        
        self.size_var = tk.StringVar(value="small")
        
        ttk.Radiobutton(frame, text="Nhỏ (100 số)", variable=self.size_var, value="small").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(frame, text="Trung bình (1000 số)", variable=self.size_var, value="medium").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(frame, text="Lớn (10000 số)", variable=self.size_var, value="large").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(frame, text="Rất lớn (100000 số)", variable=self.size_var, value="xlarge").pack(anchor=tk.W, padx=20)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(btn_frame, text="Tạo", command=self.create_sample).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Hủy", command=self.top.destroy).pack(side=tk.LEFT, padx=5)
    
    def create_sample(self):
        """Tạo tập tin mẫu"""
        from data_generator import generate_random_binary_file
        
        size_map = {
            "small": 100,
            "medium": 1000,
            "large": 10000,
            "xlarge": 100000
        }
        
        size_name = self.size_var.get()
        count = size_map[size_name]
        filename = f"sample_{size_name}_{count}.bin"
        
        self.top.destroy()
        
        # Tạo file
        progress = tk.Toplevel()
        progress.title("Đang tạo...")
        progress.geometry("300x100")
        ttk.Label(progress, text=f"Đang tạo {filename}...").pack(pady=20)
        progress.update()
        
        if generate_random_binary_file(filename, count):
            progress.destroy()
            messagebox.showinfo("Thành công", f"Tạo thành công: {filename}")
            self.result = filename
        else:
            progress.destroy()
            messagebox.showerror("Lỗi", "Không thể tạo tập tin!")


def main():
    """Hàm chính"""
    root = tk.Tk()
    app = ExternalMergeSortGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
