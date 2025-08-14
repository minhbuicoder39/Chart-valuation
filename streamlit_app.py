import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def load_data():
    """Load and prepare data"""
    try:
        # Read data
        df = pd.read_csv('VALUATION_cleaned.csv')
        
        # Convert date column to datetime
        df['TRADE_DATE'] = pd.to_datetime(df['TRADE_DATE'])
        
        # Sort data by date and ticker
        df = df.sort_values(['PRIMARYSECID', 'TRADE_DATE'])
        
        # Reset index after sorting
        df = df.reset_index(drop=True)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def calculate_ema(data, periods):
    """Calculate Exponential Moving Average"""
    return data.ewm(span=periods, adjust=False).mean()

def plot_valuation_chart(df, ticker, metric, start_year=2021):
    """Plot valuation chart (PE, PB, or PS) for a specific ticker with EMA lines"""
    try:
        # Filter data for specific ticker
        ticker_data = df[df['PRIMARYSECID'] == ticker].copy()
        
        if ticker_data.empty:
            st.error(f"No data found for {ticker}")
            return None, None
        
        # Filter by year and sort by date
        ticker_data = ticker_data[ticker_data['TRADE_DATE'].dt.year >= start_year]
        ticker_data = ticker_data.sort_values('TRADE_DATE')
        
        # Remove any NaN values in the selected metric column
        ticker_data = ticker_data.dropna(subset=[metric])
        
        # Calculate EMAs
        ticker_data['EMA20'] = calculate_ema(ticker_data[metric], 20)
        ticker_data['EMA200'] = calculate_ema(ticker_data[metric], 200)
            
        # Create plotly figure
        metric_names = {'PE': 'P/E', 'PB': 'P/B', 'PS': 'P/S'}
        
        fig = go.Figure()
        
        # Add main metric line
        fig.add_trace(go.Scatter(
            x=ticker_data['TRADE_DATE'],
            y=ticker_data[metric],
            name=metric_names[metric],
            line=dict(color='rgb(49,130,189)', width=2)
        ))
        
        # Add EMA lines
        fig.add_trace(go.Scatter(
            x=ticker_data['TRADE_DATE'],
            y=ticker_data['EMA20'],
            name='EMA20',
            line=dict(color='orange', width=1.5, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=ticker_data['TRADE_DATE'],
            y=ticker_data['EMA200'],
            name='EMA200',
            line=dict(color='red', width=1.5, dash='dash')
        ))
        
        # Update layout
        fig.update_layout(
            title=f'Chỉ số {metric_names[metric]} của {ticker} từ {start_year} đến nay',
            yaxis_title=metric_names[metric],
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            ),
            plot_bgcolor='white',  # White background
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray'
            )
        )
        
        return fig, ticker_data
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None, None
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None, None
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def display_statistics(ticker_data, metric):
    """Display statistics for the selected metric"""
    if ticker_data is not None and not ticker_data.empty:
        recent_data = ticker_data.iloc[-1]
        
        # Current values
        st.write("Giá trị hiện tại:")
        st.write(f"- {metric}: {recent_data[metric]:.2f}")
        st.write(f"- EMA20: {recent_data['EMA20']:.2f}")
        st.write(f"- EMA200: {recent_data['EMA200']:.2f}")
        
        st.write("\nThống kê chung:")
        avg_value = ticker_data[metric].mean()
        st.write(f"- {metric} trung bình: {avg_value:.2f}")
        
        max_value = ticker_data[metric].max()
        st.write(f"- {metric} cao nhất: {max_value:.2f}")
        
        min_value = ticker_data[metric].min()
        st.write(f"- {metric} thấp nhất: {min_value:.2f}")

def main():
    st.title('Vietnam Stock Valuation Charts')
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar controls
    st.sidebar.header('Chart Controls')
    
    # Get unique tickers
    tickers = sorted(df['PRIMARYSECID'].unique())
    
    # Ticker selection
    selected_ticker = st.sidebar.selectbox(
        'Chọn mã cổ phiếu:',
        tickers
    )
    
    # Metric selection
    selected_metric = st.sidebar.selectbox(
        'Chọn chỉ số:',
        ['PE', 'PB', 'PS'],
        format_func=lambda x: {'PE': 'P/E', 'PB': 'P/B', 'PS': 'P/S'}[x]
    )
    
    # Year selection
    min_year = df['TRADE_DATE'].dt.year.min()
    max_year = df['TRADE_DATE'].dt.year.max()
    start_year = st.sidebar.slider(
        'Chọn năm bắt đầu:',
        min_value=min_year,
        max_value=max_year,
        value=2021
    )
    
    # Create and display chart
    fig, ticker_data = plot_valuation_chart(df, selected_ticker, selected_metric, start_year)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
        
        # Display statistics
        st.subheader(f'Thống kê {selected_metric}')
        display_statistics(ticker_data, selected_metric)

if __name__ == '__main__':
    main()
