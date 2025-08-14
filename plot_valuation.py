import pandas as pd
import matplotlib.pyplot as plt
import datetime

def plot_pe_historical(ticker, start_year=2021):
    """
    Vẽ đồ thị PE theo thời gian của một mã cổ phiếu
    """
    try:
        # Đọc dữ liệu
        df = pd.read_csv('VALUATION_cleaned.csv')
        
        # Kiểm tra xem ticker có tồn tại không
        if ticker not in df['PRIMARYSECID'].values:
            print(f"Không tìm thấy dữ liệu cho mã {ticker}")
            return
            
        # Lọc dữ liệu cho ticker cụ thể
        ticker_data = df[df['PRIMARYSECID'] == ticker]
        
        # Kiểm tra xem có cột PE không
        if 'PE' not in df.columns:
            print("Không tìm thấy cột PE trong dữ liệu")
            return
            
        # Sử dụng cột TRADE_DATE
        date_column = 'TRADE_DATE'
        if date_column in df.columns:
            # Chuyển đổi cột ngày sang datetime
            ticker_data[date_column] = pd.to_datetime(ticker_data[date_column])
            
            # Lọc từ năm start_year đến nay và sắp xếp theo ngày
            ticker_data = ticker_data[ticker_data[date_column].dt.year >= start_year]
            ticker_data = ticker_data.sort_values(by=date_column)
            
            # Loại bỏ các giá trị NaN trong cột PE
            ticker_data = ticker_data.dropna(subset=['PE'])
            
            x_values = ticker_data[date_column]
            plt.figure(figsize=(12, 6))
            plt.plot(x_values, ticker_data['PE'], linestyle='-', linewidth=2)
            plt.gcf().autofmt_xdate()  # Tự động xoay nhãn ngày
        else:
            print("Không tìm thấy cột ngày trong dữ liệu")
            return
            
        # Tùy chỉnh đồ thị
        plt.title(f'Chỉ số P/E của {ticker} từ {start_year} đến nay')
        plt.ylabel('P/E')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.show()
        
    except FileNotFoundError:
        print("Không tìm thấy file VALUATION_cleaned.csv")
    except Exception as e:
        print(f"Lỗi: {str(e)}")

# Vẽ đồ thị PE cho HPG từ 2021 đến nay
plot_pe_historical("HPG", 2021)
