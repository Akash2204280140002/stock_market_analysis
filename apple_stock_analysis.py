# Apple Stock Analysis Script
# This script fetches Apple's stock data, calculates 10-day SMA, saves to CSV, and visualizes results.

# Import necessary libraries
import yfinance as yf  # For fetching stock data from Yahoo Finance
import pandas as pd    # For data manipulation and analysis
import matplotlib.pyplot as plt  # For data visualization
from datetime import datetime, timedelta  # For date handling

def fetch_stock_data(ticker, days_back=365):
    """
    Fetch historical stock data for a given ticker.
    
    Parameters:
    - ticker (str): Stock symbol (e.g., 'AAPL')
    - days_back (int): Number of days of historical data to fetch
    
    Returns:
    - pandas.DataFrame: DataFrame containing OHLC data
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Download data using yfinance
    print(f"Fetching {days_back} days of historical data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Check if data was fetched successfully
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker}")
    
    print("Data fetched successfully!")
    return data

def calculate_sma(data, window=10):
    """
    Calculate Simple Moving Average for closing prices.
    
    Parameters:
    - data (pandas.DataFrame): DataFrame containing stock data with 'Close' column
    - window (int): Number of periods for SMA calculation
    
    Returns:
    - pandas.DataFrame: Original DataFrame with added SMA column
    """
    print(f"Calculating {window}-day SMA...")
    data[f'{window}_SMA'] = data['Close'].rolling(window=window).mean()
    return data

def process_and_save_data(data, filename='apple_stock_data.csv'):
    """
    Process data and save to CSV file.
    
    Parameters:
    - data (pandas.DataFrame): DataFrame containing stock data
    - filename (str): Name of the output CSV file
    
    Returns:
    - None
    """
    # Select only the required columns
    processed_data = data[['Open', 'High', 'Low', 'Close', '10_SMA']].copy()
    
    # The date is in the index, so we reset it to make it a column
    processed_data.reset_index(inplace=True)
    
    # Save to CSV
    print(f"Saving data to {filename}...")
    processed_data.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename}!")

def visualize_data(data, ticker):
    """
    Create a visualization of closing prices and SMA.
    
    Parameters:
    - data (pandas.DataFrame): DataFrame containing stock data
    - ticker (str): Stock symbol for title
    
    Returns:
    - None
    """
    print("Creating visualization...")
    
    # Create figure and axis
    plt.figure(figsize=(12, 6))
    
    # Plot closing prices
    plt.plot(data.index, data['Close'], label='Closing Price', color='blue', alpha=0.5)
    
    # Plot SMA
    plt.plot(data.index, data['10_SMA'], label='10-Day SMA', color='red', linewidth=2)
    
    # Add title and labels
    plt.title(f'{ticker} Stock Price with 10-Day SMA (Last 365 Days)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plot_filename = f'{ticker.lower()}_chart.png'
    plt.savefig(plot_filename)
    print(f"Plot saved as {plot_filename}!")
    
    # Show the plot
    plt.show()

def main():
    """
    Main function to execute the stock analysis workflow.
    """
    # Configuration
    ticker = 'AAPL'
    sma_window = 10
    days_back = 365
    output_csv = 'apple_stock_data.csv'
    
    try:
        # Step 1: Fetch historical stock data
        stock_data = fetch_stock_data(ticker, days_back)
        
        # Step 2: Calculate SMA
        stock_data = calculate_sma(stock_data, sma_window)
        
        # Step 3: Process and save data
        process_and_save_data(stock_data, output_csv)
        
        # Step 4: Visualize data
        visualize_data(stock_data, ticker)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()