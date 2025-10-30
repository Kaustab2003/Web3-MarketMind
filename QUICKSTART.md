# ⚡ Web3 MarketMind 4.0 - Quick Start Guide

Get up and running in 5 minutes!

---

## 🚀 Option 1: One-Command Start (Windows)

```bash
run.bat
```

That's it! The script will:
- Create virtual environment
- Install dependencies
- Create necessary folders
- Launch the app

**Access at:** `http://localhost:8501`

---

## 🚀 Option 2: One-Command Start (Mac/Linux)

```bash
chmod +x run.sh
./run.sh
```

**Access at:** `http://localhost:8501`

---

## 🚀 Option 3: Manual Setup

### Step 1: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the App

```bash
streamlit run app_v4.py
```

---

## 🔐 Login Credentials

**Demo User:**
- Username: `demo`
- Password: `demo123`

**Admin User:**
- Username: `admin`
- Password: `admin123`

---

## 📊 Using the Dashboard

### 1. **Enable Demo Mode** (Sidebar)
- Toggle "Use Demo Data" to ON
- App will generate sample data automatically

### 2. **Or Upload Your Data**
- Toggle "Use Demo Data" to OFF
- Upload two CSV files:
  - **Trader Data**: `time, closedPnL, leverage, size`
  - **Sentiment Data**: `Date, Classification`

### 3. **Apply Filters** (Sidebar)
- Select sentiments (Fear/Greed/Neutral)
- Choose date range
- Adjust leverage range

### 4. **View Analytics**
- Check key metrics at the top
- Read AI-generated insights
- Explore interactive charts (4 tabs)

### 5. **Train ML Model**
- Scroll to "ML Sentiment Predictor"
- Click "Train/Retrain Model"
- Wait ~10 seconds
- View tomorrow's prediction

### 6. **Export Data**
- Click "Download Cleaned Data (CSV)"
- Or click "Generate PDF Report"

---

## 🌐 Deploy to Cloud (5 Minutes)

### Streamlit Cloud (Easiest)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/web3-marketmind.git
   git push -u origin main
   ```

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repo
   - Main file: `app_v4.py`
   - Click "Deploy"

3. **Add Secrets:**
   - Click "Advanced settings"
   - Add:
     ```toml
     DEMO_PASSWORD = "your-password"
     ADMIN_PASSWORD = "your-admin-password"
     ```

**Done!** Your app is live in ~3 minutes.

---

## 📁 Project Structure

```
Web3 MarketMind/
├── app_v4.py              ← Main app (run this!)
├── requirements.txt       ← Dependencies
├── run.bat / run.sh       ← Quick start scripts
├── .streamlit/
│   ├── config.toml        ← Streamlit config
│   └── secrets.toml       ← Your secrets (don't commit!)
├── models/                ← ML models (auto-created)
├── data/                  ← Sample data
└── README_V4.md           ← Full documentation
```

---

## 🔧 Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
streamlit run app_v4.py --server.port 8502
```

### "API rate limit"
- Wait 5 minutes (cache will refresh)
- Or restart the app

### "Login not working"
- Check `.streamlit/secrets.toml` exists
- Verify passwords are set correctly

---

## 📚 Next Steps

1. **Read Full Docs:** `README_V4.md`
2. **Deployment Guide:** `DEPLOYMENT_GUIDE.md`
3. **Feature List:** `FEATURES.md`
4. **Customize:** Edit `app_v4.py` to add your features

---

## 💡 Pro Tips

- **Demo Mode**: Perfect for testing without data
- **Caching**: API calls cached for 5 minutes
- **Model Persistence**: Trained models saved automatically
- **Filters**: Combine multiple filters for deep analysis
- **Export**: Download data before closing the app

---

## 🎯 Key Features at a Glance

✅ User Authentication  
✅ Real-time BTC Prices (CoinGecko + Binance)  
✅ ML Sentiment Predictor (Random Forest)  
✅ Interactive Charts (Plotly)  
✅ PDF Report Generator  
✅ CSV Export  
✅ Advanced Filters  
✅ AI-Powered Insights  
✅ Cloud Deployment Ready  

---

## 📞 Need Help?

- **Documentation**: Check `README_V4.md`
- **Deployment**: See `DEPLOYMENT_GUIDE.md`
- **Features**: Read `FEATURES.md`
- **Issues**: Open GitHub issue

---

**Happy Trading! 💎📈**

*Built with ❤️ using Streamlit*
