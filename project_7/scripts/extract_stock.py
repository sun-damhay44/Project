import requests
import pandas as pd
import time
import os
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = os.getenv('ALPHA_VANTAGE_KEY')
SYMBOLS = ['IBM', 'AAPL', 'TSLA', 'MSFT', 'GOOGL']
FUNCTION = 'TIME_SERIES_DAILY'

# 1. สร้างตัวแปรวันที่ปัจจุบัน
today = datetime.now().strftime('%Y-%m-%d')

# 2. ระบุโฟลเดอร์ปลายทางเป็นชั้น bronze
output_dir = 'project_7/bronze'

# 3. แก้ไขชื่อไฟล์ให้มีวันที่ต่อท้าย (เช่น stock_data_2026-04-25.csv)
master_file_path = os.path.join(output_dir, f'stock_data_{today}.csv')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- FUNCTIONS ---
def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function={FUNCTION}&symbol={symbol}&apikey={API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()

        if "Time Series (Daily)" in data:
            # ดึงเฉพาะข้อมูลวันล่าสุด (แถวแรก)
            last_refreshed = data["Meta Data"]["3. Last Refreshed"]
            latest_data = data["Time Series (Daily)"][last_refreshed]

            df = pd.DataFrame([latest_data])
            df.columns = ['open', 'high', 'low', 'close', 'volume']
            df.insert(0, 'date', last_refreshed)
            df['symbol'] = symbol
            return df
        else:
            print(f"⚠️ Warning {symbol}: Check API Limit")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# --- MAIN EXECUTION ---
all_dfs = []
for s in SYMBOLS:
    print(f"🚀 Fetching {s}...")
    stock_df = fetch_stock_data(s)
    if stock_df is not None:
        all_dfs.append(stock_df)
    time.sleep(15) # รอตามกฎ API Free Limit

if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    # 4. บันทึกไฟล์รวมที่มีวันที่ในชื่อไฟล์
    final_df.to_csv(master_file_path, index=False)
    print(f"\n✨ Successfully saved daily data to: {master_file_path}")