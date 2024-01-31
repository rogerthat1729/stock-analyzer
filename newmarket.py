import yfinance as yf

# Replace this with your list of stock symbols
ticker_symbols = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS',] # Add your symbols here

# Dictionary to hold stock data
stock_data = {}
global symbols

try:
        with open("stocksymbol_1.txt", 'r') as file:
            symbols = file.readlines()
        for ticker in symbols:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")

            stock_data[ticker] = {
                'Name': stock.info.get('longName', 'N/A'),
                'Symbol': ticker,
                'Industry': stock.info.get('industry', 'N/A'),
                'Prev Close': stock.info.get('previousClose', 'N/A'),
                'Open': hist['Open'].iloc[0] if not hist.empty else 'N/A',
                'Low': hist['Low'].iloc[0] if not hist.empty else 'N/A',
                'High': hist['High'].iloc[0] if not hist.empty else 'N/A',
                'Price': stock.info.get('regularMarketPrice', 'N/A'),
                'Volume': hist['Volume'].iloc[0] if not hist.empty else 'N/A',
                'PE': stock.info.get('trailingPE', 'N/A'),
                'Market Cap': stock.info.get('marketCap', 'N/A') / 10000000 if stock.info.get('marketCap') is not None else 'N/A'
            }
except FileNotFoundError:
    print(f"The file stocksymbol.txt was not found.")





# Writing data to a text file
with open('stock_data.txt', 'w') as file:
    for symbol, data in stock_data.items():
        file.write(f"Symbol: {symbol}\n")
        for key, value in data.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")  # Add a newline for separation between stocks

print("Data written to stock_data.txt")
