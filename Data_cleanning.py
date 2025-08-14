#%%
import pandas as pd

# Đọc file CSV
df = pd.read_csv('VALUATION.csv')

# Lấy tên cột đầu tiên
first_column = df.columns[0]

# Xử lý cột đầu tiên để chỉ giữ lại 3 chữ cái đầu (bỏ "VN Equity")
df[first_column] = df[first_column].str[:3]

# Đổi tên các cột
column_mapping = {
    'PE_RATIO': 'PE',
    'PX_TO_BOOK_RATIO': 'PB',
    'PX_TO_SALES_RATIO': 'PS'
}
df = df.rename(columns=column_mapping)

# Lưu lại file CSV đã xử lý
df.to_csv('VALUATION_cleaned.csv', index=False)
print("Đã xử lý xong file CSV!")
