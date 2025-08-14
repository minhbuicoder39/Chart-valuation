
    #%%
import pandas as pd

def get_valuation_data(ticker: str, columns: list) -> dict:
    
    try:
        # Đọc file CSV
        df = pd.read_csv('VALUATION_cleaned.csv')
        
        # Kiểm tra xem ticker có tồn tại trong dữ liệu không
        ticker_data = df[df.iloc[:, 0] == ticker.upper()]
        if ticker_data.empty:
            return f"Không tìm thấy dữ liệu cho mã {ticker}"
        
        # Kiểm tra tên cột hợp lệ
        valid_columns = ['PE', 'PB', 'PS']
        columns = [col.upper() for col in columns]
        invalid_columns = [col for col in columns if col not in valid_columns]
        if invalid_columns:
            return f"Các cột không hợp lệ: {invalid_columns}. Chỉ chấp nhận: PE, PB, PS"
        
        # Lấy dữ liệu cho các cột được yêu cầu
        result = {}
        for col in columns:
            if col in df.columns:
                result[col] = ticker_data[col].iloc[0]
            
        return result
        
    except FileNotFoundError:
        return "Không tìm thấy file VALUATION_cleaned.csv"
    except Exception as e:
        return f"Lỗi: {str(e)}"

