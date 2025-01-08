import pandas as pd

def read_data(file_path):
    """Đọc dữ liệu từ file Excel."""
    return pd.read_excel(file_path)

def preprocess_data(data):
    """Tiền xử lý dữ liệu: loại bỏ giá trị null và chuyển đổi cột 'Kết quả'."""
    data['Kết quả'] = data['Kết quả'].astype(int)  # 1: Qua môn, 0: Rớt môn
    data = data.dropna()
    return data
