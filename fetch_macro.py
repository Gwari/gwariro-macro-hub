import yfinance as yf
import pandas as pd

print("🚀 MACRO HUB: Data Engine Initialized...")

# Define your core asset watchlist matching your preferences
CORE_PAIRS = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "EURGBP": "EURGBP=X",
    "EURJPY": "EURJPY=X",
    "EURAUD": "EURAUD=X",
    "EURCAD": "EURCAD=X",
    "USDMXN": "USDMXN=X",
    "MXNJPY": "MXNJPY=X"
}

def fetch_market_data():
    print("📊 Fetching latest weekly closes and changes for core FX pairs...")
    data_results = {}
    
    for symbol, ticker in CORE_PAIRS.items():
        try:
            # Download recent daily history
            df = yf.download(ticker, period="1mo", progress=False)
            if not df.empty:
                # Safely extract scalar float values to avoid pandas Series errors
                close_series = df['Close']
                if isinstance(close_series, pd.DataFrame):
                    close_series = close_series.iloc[:, 0]
                
                current_price = float(close_series.iloc[-1])
                prev_week_price = float(close_series.iloc[-5]) # roughly 5 trading days ago
                weekly_change = current_price - prev_week_price
                pct_change = (weekly_change / prev_week_price) * 100
                
                data_results[symbol] = {
                    "price": round(current_price, 4),
                    "weekly_change": round(weekly_change, 4),
                    "pct_change": round(pct_change, 2)
                }
                print(f"   ✅ Successfully pulled {symbol}: {current_price}")
            else:
                print(f"   ⚠️ No data found for {symbol}")
        except Exception as e:
            print(f"   ❌ Error fetching {symbol}: {e}")
            
    return data_results

if __name__ == "__main__":
    results = fetch_market_data()
    print("\n🎉 Test Run Complete! Here is the compiled data dictionary:")
    print(results)