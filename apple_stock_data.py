import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for the given ticker and date range.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"No data found for ticker {ticker} in the given date range.")
            sys.exit(1)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        sys.exit(1)

def calculate_sma(data, window):
    """
    Calculate the simple moving average (SMA) for the closing price.
    """
    data[f'{window}_SMA'] = data['Close'].rolling(window=window).mean()
    return data

def save_to_csv(data, filename):
    """
    Save the DataFrame to a CSV file.
    """
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def plot_data(data, ticker, sma_window, save_image=True):
    """
    Plot the closing price and SMA, optionally save the plot as an image.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')
    plt.plot(data['Date'], data[f'{sma_window}_SMA'], label=f'{sma_window}-Day SMA', color='orange')

    plt.title(f'{ticker} - Closing Price & {sma_window}-Day SMA')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_image:
        image_filename = f'apple_chart.png'
        plt.savefig(image_filename)
        print(f"Plot saved as {image_filename}")

    plt.show()

def main():
    ticker = 'AAPL'
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    sma_window = 10

    print(f"Fetching data for {ticker} from {start_date.date()} to {end_date.date()}...")
    data = fetch_stock_data(ticker, start_date, end_date)

    data = calculate_sma(data, sma_window)

    data.reset_index(inplace=True)
    final_data = data[['Date', 'Open', 'High', 'Low', 'Close', f'{sma_window}_SMA']]

    csv_filename = 'apple_stock_data.csv'
    save_to_csv(final_data, csv_filename)

    plot_data(final_data, ticker, sma_window, save_image=True)

if __name__ == '__main__':
    main()
