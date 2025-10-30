# 💎 Web3 MarketMind 4.0

**The Trader Sentiment Intelligence Dashboard**

✨ *"Decode Greed. Predict Fear. Master the Market."*

---

## 🔥 What's New in Version 4.0

✅ **Beautiful Sidebar Dashboard Layout**  
✅ **Sentiment, Date, and Leverage Filters**  
✅ **Live Analytics Cards** (PnL, Leverage, Volume)  
✅ **Download Cleaned CSV Option**  
✅ **PDF Report Generator** (Auto Summary)  
✅ **Real-time Crypto Prices** (CoinGecko + Binance fallback)  
✅ **ML Sentiment Predictor** (Random Forest Classifier)  
✅ **User Authentication** (Streamlit Authenticator)  
✅ **Enhanced Plotly Charts + Heatmaps**  
✅ **Smarter Insight Engine** (dynamic insights)  
✅ **Polished UI** with Gradient Header & Metrics Grid  
✅ **Cloud Deployment Ready** (Streamlit Cloud & Render)

---

## 📂 Project Structure

```
Web3 MarketMind/
├── app_v4.py                 # Main application (Version 4.0)
├── requirements.txt          # Python dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml         # Secrets (DO NOT COMMIT!)
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── Procfile                 # Render deployment config
├── setup.sh                 # Deployment setup script
├── models/                  # ML models (auto-generated)
│   └── sentiment_rf.joblib
├── csv_files/               # Your data files
│   ├── trader_data.csv
│   └── sentiment_data.csv
└── README_V4.md             # This file
```

---

## 🚀 Quick Start

### 1. **Clone or Download the Repository**

```bash
git clone <your-repo-url>
cd Web3\ MarketMind
```

### 2. **Create Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Set Up Environment Variables**

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials (optional)
```

### 5. **Run the Application**

```bash
streamlit run app_v4.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🔐 Authentication

**Default Demo Credentials:**
- **Username:** `demo`
- **Password:** `demo123`

**Admin Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

> ⚠️ **Security Note:** Change these passwords in production! Set them via environment variables:
> - `DEMO_PASSWORD`
> - `ADMIN_PASSWORD`

---

## 📊 Features Overview

### 1. **Real-time Crypto Price Integration**

- Fetches BTC/ETH prices from **CoinGecko API**
- Automatic fallback to **Binance API** if CoinGecko fails
- Overlays price data with sentiment analysis
- Calculates daily returns for ML features

### 2. **ML Sentiment Predictor**

- **Algorithm:** Random Forest Classifier
- **Features:** Lagged PnL, leverage, volume, BTC returns
- **Output:** Predicts tomorrow's sentiment (Fear/Greed/Neutral)
- **Metrics:** Accuracy, confusion matrix, feature importance
- **Persistence:** Models saved to `models/` directory

### 3. **Interactive Analytics**

- **PnL Distribution:** Box plots by sentiment
- **Correlation Heatmap:** Relationship between metrics
- **Sentiment Timeline:** Daily PnL trends
- **BTC Price Overlay:** Dual-axis chart with trading data

### 4. **Export & Reporting**

- **CSV Export:** Download filtered data
- **PDF Reports:** Auto-generated summary with key metrics
- **Email Reports:** (Optional) Send reports via SMTP

### 5. **Advanced Filters**

- Sentiment type selection
- Date range picker
- Leverage range slider
- Real-time record count

---

## 🤖 ML Model Training

### How It Works

1. **Feature Engineering:**
   - Creates lagged features (3-day lookback)
   - Includes: PnL, leverage, volume, BTC returns
   
2. **Model Training:**
   - Random Forest with 200 estimators
   - 80/20 train-test split
   - No data leakage (time-series aware)

3. **Prediction:**
   - Uses last 3 days of data
   - Outputs sentiment label + probabilities

### Training the Model

Click the **"🔄 Train/Retrain Model"** button in the app to:
- Train a new model on current data
- Save to `models/sentiment_rf.joblib`
- Display accuracy and feature importance

---

## ☁️ Cloud Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app_v4.py` as the main file
   - Add secrets in the dashboard (Settings → Secrets):
     ```toml
     DEMO_PASSWORD = "your-secure-password"
     ADMIN_PASSWORD = "your-admin-password"
     ```

3. **Deploy!** Your app will be live at `https://your-app.streamlit.app`

### Option 2: Render

1. **Create `render.yaml`** (already included)

2. **Push to GitHub**

3. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repo
   - Render will auto-detect `Procfile`

4. **Add Environment Variables:**
   - `DEMO_PASSWORD`
   - `ADMIN_PASSWORD`
   - Any API keys

5. **Deploy!** Your app will be live at `https://your-app.onrender.com`

### Option 3: Heroku

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set DEMO_PASSWORD=your-password
heroku config:set ADMIN_PASSWORD=your-admin-password

# Deploy
git push heroku main
```

---

## 🔧 Configuration

### Streamlit Secrets

Edit `.streamlit/secrets.toml` (local only - DO NOT COMMIT):

```toml
DEMO_PASSWORD = "demo123"
ADMIN_PASSWORD = "admin123"

# Optional: Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
```

### Environment Variables

For production, use environment variables instead of secrets file:

```bash
export DEMO_PASSWORD="your-secure-password"
export ADMIN_PASSWORD="your-admin-password"
```

---

## 📝 Data Format

### Trader Data CSV

Required columns:
- `time` (datetime): Trade timestamp
- `closedPnL` (float): Profit/Loss
- `leverage` (float): Leverage used
- `size` (float): Trade volume

Example:
```csv
time,closedPnL,leverage,size
2024-01-01 10:00:00,150.50,5.2,10000
2024-01-01 14:30:00,-75.25,3.8,5000
```

### Sentiment Data CSV

Required columns:
- `Date` (datetime): Date
- `Classification` (string): Sentiment label (Fear/Greed/Neutral)

Example:
```csv
Date,Classification
2024-01-01,Greed
2024-01-02,Fear
```

---

## 🛠️ Troubleshooting

### Issue: "No module named 'streamlit'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "API rate limit exceeded"
**Solution:** The app has built-in caching (5 min TTL). Wait or use Binance fallback.

### Issue: "Model training fails"
**Solution:** Ensure you have at least 20 data points with valid sentiment labels.

### Issue: "Authentication not working"
**Solution:** Check that passwords are set correctly in `.streamlit/secrets.toml` or environment variables.

---

## 🔒 Security Best Practices

1. **Never commit secrets:**
   - Add `.streamlit/secrets.toml` to `.gitignore`
   - Use environment variables in production

2. **Use strong passwords:**
   - Change default credentials immediately
   - Use password managers

3. **API Key Protection:**
   - Store API keys in secrets/env vars
   - Never hardcode in source files

4. **HTTPS Only:**
   - Always deploy with HTTPS enabled
   - Streamlit Cloud and Render provide this by default

---

## 📚 API Documentation

### CoinGecko API
- **Endpoint:** `https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart`
- **Rate Limit:** 10-50 calls/minute (free tier)
- **Docs:** [coingecko.com/api](https://www.coingecko.com/en/api)

### Binance API
- **Endpoint:** `https://api.binance.com/api/v3/klines`
- **Rate Limit:** 1200 requests/minute
- **Docs:** [binance-docs.github.io](https://binance-docs.github.io/apidocs/)

---

## 🎯 Roadmap / Future Enhancements

- [ ] Multi-coin support (ETH, SOL, etc.)
- [ ] Advanced ML models (LSTM, XGBoost)
- [ ] Real-time WebSocket data streaming
- [ ] Portfolio tracking and management
- [ ] Social sentiment analysis (Twitter/Reddit)
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support
- [ ] Dark mode toggle

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## ⚠️ Disclaimer

**This tool is for educational and research purposes only.**

- Not financial advice
- Past performance does not guarantee future results
- Cryptocurrency trading involves substantial risk
- Always do your own research (DYOR)
- Never invest more than you can afford to lose

---

## 📧 Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Email: support@marketmind.ai (example)
- Discord: [Join our community](#)

---

## 🙏 Acknowledgments

- **Streamlit** - Amazing framework for data apps
- **CoinGecko** - Free crypto price API
- **Binance** - Reliable fallback API
- **scikit-learn** - ML library
- **Plotly** - Interactive charts

---

**Built with ❤️ by the Web3 MarketMind Team**

*Last Updated: 2024*
