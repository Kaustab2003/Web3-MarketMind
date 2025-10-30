# 💎 Web3 MarketMind 4.0

**Trader Sentiment Intelligence Dashboard**

> *"Decode Greed. Predict Fear. Master the Market."*

A powerful, AI-driven cryptocurrency market analysis dashboard that combines real-time data, sentiment analysis, and machine learning predictions to help traders make informed decisions.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

### Core Functionality
- 🔐 **Secure Authentication** - User login system with session management
- 📊 **Real-time Crypto Prices** - Live BTC/ETH price integration via CoinGecko & Binance APIs
- 🎯 **Sentiment Analysis** - Advanced market sentiment tracking and visualization
- 🤖 **ML Predictions** - Machine learning model for next-day sentiment forecasting
- 📈 **Interactive Charts** - Beautiful Plotly visualizations with heatmaps
- 📑 **PDF Reports** - Auto-generated market summary reports
- 🎨 **Modern UI** - Dark-themed, responsive dashboard design

### Analytics Features
- **Live Analytics Cards** - Real-time PnL, Leverage, and Volume metrics
- **Sentiment Filters** - Filter by Bullish, Bearish, Neutral, Extreme Greed, Extreme Fear
- **Date Range Selection** - Analyze specific time periods
- **Leverage Analysis** - Track and analyze leverage usage patterns
- **Download Options** - Export cleaned CSV data

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Kaustab2003/Web3-MarketMind.git
cd Web3-MarketMind
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the test script** (optional but recommended)
```bash
python test_installation.py
```

5. **Start the application**
```bash
# Option 1: Direct command
streamlit run app_v4.py

# Option 2: Quick start script
# Windows
.\run.bat

# Mac/Linux
./run.sh
```

6. **Access the dashboard**
- Open your browser and navigate to: `http://localhost:8501`
- Login with demo credentials:
  - **Username**: `demo`
  - **Password**: `demo123`

## 📋 Project Structure

```
Web3-MarketMind/
├── app_v4.py                 # Main application file
├── requirements.txt          # Python dependencies
├── test_installation.py      # Installation verification script
├── run.bat                   # Windows quick start
├── run.sh                    # Mac/Linux quick start
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml         # Authentication secrets (gitignored)
├── data/                     # Data directory
├── models/                   # ML models directory
├── src/                      # Source code modules
├── DEPLOYMENT_GUIDE.md       # Deployment instructions
├── FEATURES.md              # Detailed features documentation
├── QUICKSTART.md            # Quick start guide
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional) for custom configuration:
```env
DEMO_PASSWORD=your_demo_password
ADMIN_PASSWORD=your_admin_password
COINGECKO_API_KEY=your_api_key
BINANCE_API_KEY=your_api_key
```

### Streamlit Configuration
The app uses a custom theme defined in `.streamlit/config.toml`:
- Primary Color: Cyan (#00f2fe)
- Background: Dark (#1a1a2e)
- Secondary Background: Navy (#16213e)

## Demo 
- [link](https://web3-marketmind-ubwh5vryrh5xffah7a5p2x.streamlit.app/)
  

## 📊 Data Sources

- **CoinGecko API** - Primary source for cryptocurrency price data
- **Binance API** - Fallback source for real-time market data
- **Custom ML Model** - Random Forest classifier for sentiment prediction

## 🤖 Machine Learning

The application includes a trained Random Forest model that:
- Analyzes historical price and sentiment data
- Uses lag features for time-series analysis
- Predicts next-day market sentiment
- Provides confidence scores for predictions

## 📖 Documentation

- [Features Documentation](FEATURES.md) - Detailed feature descriptions
- [Quick Start Guide](QUICKSTART.md) - Step-by-step setup instructions
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [Project Summary](PROJECT_SUMMARY.md) - Comprehensive project overview

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Machine Learning**: Scikit-learn
- **Authentication**: Streamlit-Authenticator
- **APIs**: CoinGecko, Binance
- **PDF Generation**: FPDF

## 🔒 Security

- Passwords are hashed using bcrypt
- Session-based authentication
- Environment variables for sensitive data
- Secrets management via Streamlit secrets

## 📝 Usage

1. **Login** - Use demo credentials or create your own
2. **Upload Data** - Upload CSV files with trading data (optional)
3. **Filter & Analyze** - Use sidebar filters to analyze specific segments
4. **View Insights** - Explore interactive charts and analytics
5. **ML Predictions** - Check AI-powered sentiment forecasts
6. **Export Reports** - Download PDF reports or CSV data

## 🎯 Use Cases

- **Crypto Traders** - Analyze market sentiment and make informed decisions
- **Portfolio Managers** - Track leverage and risk metrics
- **Market Researchers** - Study historical sentiment patterns
- **Data Analysts** - Explore cryptocurrency market trends

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Kaustab Das**
- GitHub: [@Kaustab2003](https://github.com/Kaustab2003)
- Repository: [Web3-MarketMind](https://github.com/Kaustab2003/Web3-MarketMind)

## 🙏 Acknowledgments

- CoinGecko for cryptocurrency data API
- Binance for market data
- Streamlit community for the amazing framework
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions:
1. Check the [documentation](FEATURES.md)
2. Run the test script: `python test_installation.py`
3. Open an issue on GitHub
4. Contact the maintainer

## 🗺️ Roadmap

- [ ] Add more cryptocurrency pairs
- [ ] Implement advanced ML models (LSTM, Transformer)
- [ ] Real-time WebSocket data streaming
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support
- [ ] Advanced portfolio tracking
- [ ] Social sentiment integration (Twitter, Reddit)

---

**Made with ❤️ for the crypto community**

*Star ⭐ this repository if you find it helpful!*
