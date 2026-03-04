"""
External Merge Sort - Ứng Dụng Chính
Chương trình minh họa External Merge Sort cho tập tin nhị phân
"""

import sys
import os
from gui_app import main


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Lỗi khi khởi động ứng dụng: {e}")
        sys.exit(1)
