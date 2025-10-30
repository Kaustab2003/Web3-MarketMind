import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("Generating sample CSV file (approximately 150 MB)...")

# Set random seed for reproducibility
np.random.seed(42)

# Generate approximately 750,000 rows for ~150MB file
n_rows = 750000

# Generate timestamps
start_date = datetime(2020, 1, 1)
dates = [start_date + timedelta(minutes=i) for i in range(n_rows)]

# Generate sample trading data
df = pd.DataFrame({
    'timestamp': dates,
    'symbol': np.random.choice(['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT'], n_rows),
    'open': np.random.uniform(20000, 70000, n_rows),
    'high': np.random.uniform(20000, 70000, n_rows),
    'low': np.random.uniform(20000, 70000, n_rows),
    'close': np.random.uniform(20000, 70000, n_rows),
    'volume': np.random.uniform(1000000, 10000000, n_rows),
    'sentiment': np.random.choice(['Bullish', 'Bearish', 'Neutral', 'Extreme Greed', 'Extreme Fear'], n_rows),
    'leverage': np.random.uniform(1, 100, n_rows),
    'pnl': np.random.uniform(-10000, 10000, n_rows),
    'trade_count': np.random.randint(1, 1000, n_rows),
    'trader_type': np.random.choice(['Retail', 'Institutional', 'Whale', 'Market Maker'], n_rows),
    'risk_score': np.random.uniform(0, 100, n_rows)
})

# Save to CSV
output_file = 'sample_trading_data_150mb.csv'
df.to_csv(output_file, index=False)

# Get file size
import os
file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print(f"✅ Created CSV file: {output_file}")
print(f"📊 Rows: {len(df):,}")
print(f"📁 File size: {file_size_mb:.2f} MB")
print(f"📋 Columns: {', '.join(df.columns)}")
