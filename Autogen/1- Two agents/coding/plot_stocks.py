# filename: plot_stocks.py
import yfinance as yf
import matplotlib.pyplot as plt

# Define the ticker symbols
meta_ticker = 'META'
tesla_ticker = 'TSLA'

# Fetch historical data
meta_data = yf.Ticker(meta_ticker)
tesla_data = yf.Ticker(tesla_ticker)

# Get historical closing prices
meta_hist = meta_data.history(period="1mo")['Close']
tesla_hist = tesla_data.history(period="1mo")['Close']

# Plotting the data
plt.figure(figsize=(14, 7))
plt.plot(meta_hist, label='META (Facebook)')
plt.plot(tesla_hist, label='TESLA')
plt.title('Stock Prices of META and TESLA Over the Last Month')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.legend()
plt.grid(True)
plt.show()