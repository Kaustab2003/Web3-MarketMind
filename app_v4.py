"""
Web3 MarketMind 4.0 — The Trader Sentiment Intelligence Dashboard
✨ Tagline: "Decode Greed. Predict Fear. Master the Market."

Features:
- Beautiful Sidebar Dashboard Layout
- Sentiment, Date, and Leverage Filters
- Live Analytics Cards (PnL, Leverage, Volume)
- Download Cleaned CSV Option
- PDF Report Generator (Auto Summary)
- Real-time BTC/ETH Price Integration (CoinGecko + Binance fallback)
- ML Model for Predicting Tomorrow's Sentiment
- User Authentication
- Enhanced Plotly Charts + Heatmaps
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import toml
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import base64
import os
import requests
import joblib
from datetime import datetime, timedelta
from dotenv import load_dotenv
import streamlit_authenticator as stauth
import yaml

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load environment variables
load_dotenv()

# -----------------------------------------------------------
# PAGE CONFIG & THEME
# -----------------------------------------------------------
st.set_page_config(
    page_title="Web3 MarketMind 4.0",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    body { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    .main-title {text-align:center; color:#1e3a8a; font-size:40px; font-weight:800; margin-bottom:10px;}
    .sub-title {text-align:center; color:#475569; font-size:18px; margin-bottom:20px;}
    .metric-card {background:linear-gradient(90deg,#3b82f6,#9333ea); color:white; padding:15px; border-radius:12px; text-align:center;}
    .stButton>button { 
        background-color:#3b82f6; 
        color:white; 
        border-radius:8px; 
        padding:0.6em 1em; 
        border:none;
        font-weight:600;
    }
    .stButton>button:hover {
        background-color:#2563eb;
        border:none;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# AUTHENTICATION SETUP
# -----------------------------------------------------------
def init_authenticator():
    """Initialize Streamlit Authenticator with demo credentials"""
    # Create .streamlit directory if it doesn't exist
    os.makedirs('.streamlit', exist_ok=True)
    
    # Create a simple config if it doesn't exist
    if not os.path.exists('.streamlit/config.toml'):
        with open('.streamlit/config.toml', 'w') as f:
            f.write("""
[theme]
primaryColor = "#00f2fe"
backgroundColor = "#1a1a2e"
secondaryBackgroundColor = "#16213e"
textColor = "#ffffff"
font = "sans serif"
""")
    
    # Create a simple secrets file if it doesn't exist
    if not os.path.exists('.streamlit/secrets.toml'):
        with open('.streamlit/secrets.toml', 'w') as f:
            f.write("""
[credentials]
usernames = { 
    "admin": {
        "name": "Admin User",
        "password": "$2b$12$KIXqRw8W3qN5YZ5YZ5YZ5uO5YZ5YZ5YZ5YZ5YZ5YZ5YZ5YZ5YZ5YZ"  # hashed 'admin123'
    },
    "demo": {
        "name": "Demo User",
        "password": "$2b$12$KIXqRw8W3qN5YZ5YZ5YZ5uO5YZ5YZ5YZ5YZ5YZ5YZ5YZ5YZ5YZ5YZ"  # hashed 'demo123'
    }
}
""")
    
    # Define default credentials with properly hashed passwords and required email field
    default_credentials = {
        "usernames": {
            "demo": {
                "name": "Demo User",
                "email": "demo@example.com",
                "password": "$2b$12$Tx7BSNS52urzmtxPp3vanecv2ayiwrCSP8ChceDRt9xutWt.eAT8C"  # demo123
            },
            "admin": {
                "name": "Admin User",
                "email": "admin@example.com",
                "password": "$2b$12$cmgp4doYXXpNxL7Bx0LS6uGjmtjCAOnUQJ7kFILGwe89QjJbbl1iK"  # admin123
            }
        }
    }
    
    # Initialize the authenticator with default credentials
    authenticator = stauth.Authenticate(
        default_credentials,
        "marketmind_cookie",
        "marketmind_signature_key",
        cookie_expiry_days=7,
        preauthorized=None
    )
    
    return authenticator

# -----------------------------------------------------------
# CRYPTO PRICE API FUNCTIONS
# -----------------------------------------------------------
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_coingecko_market_chart(coin_id="bitcoin", vs_currency="usd", days="max"):
    """Fetch historical daily prices from CoinGecko"""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {"vs_currency": vs_currency, "days": days}
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # data['prices'] = list of [timestamp_ms, price]
        prices = pd.DataFrame(data['prices'], columns=['ts', 'price'])
        prices['date'] = pd.to_datetime(prices['ts'], unit='ms').dt.date
        daily = prices.groupby('date').price.last().reset_index()
        daily.columns = ['date', f'{coin_id}_close']
        return daily
    except Exception as e:
        st.warning(f"CoinGecko API error: {e}. Trying Binance fallback...")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_binance_daily(symbol='BTCUSDT', limit=1000):
    """Fetch daily klines from Binance as fallback"""
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": "1d", "limit": limit}
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # kline: [openTime, open, high, low, close, ...]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df[0], unit='ms').dt.date
        df['btc_close'] = df[4].astype(float)
        return df[['date', 'btc_close']]
    except Exception as e:
        st.error(f"Binance API also failed: {e}")
        return pd.DataFrame()

def get_crypto_prices(coin="bitcoin", days=365):
    """Get crypto prices with fallback logic"""
    df = fetch_coingecko_market_chart(coin_id=coin, days=days)
    
    if df.empty and coin == "bitcoin":
        df = fetch_binance_daily(symbol='BTCUSDT', limit=min(days, 1000))
    
    return df

# -----------------------------------------------------------
# ML MODEL FUNCTIONS
# -----------------------------------------------------------
def prepare_ml_dataset(df, n_lags=3):
    """Prepare dataset for ML model with lag features"""
    df = df.sort_values('date').reset_index(drop=True)
    ml = df[['date', 'closedPnL', 'leverage', 'size', 'btc_return', 'Sentiment']].copy()
    
    # Encode sentiment labels
    le = LabelEncoder()
    ml['label'] = le.fit_transform(ml['Sentiment'])
    
    # Create lag features
    for lag in range(1, n_lags + 1):
        ml[f'closedPnL_lag{lag}'] = ml['closedPnL'].shift(lag)
        ml[f'leverage_lag{lag}'] = ml['leverage'].shift(lag)
        ml[f'size_lag{lag}'] = ml['size'].shift(lag)
        ml[f'btc_return_lag{lag}'] = ml['btc_return'].shift(lag)
    
    # Drop rows with NaN from lagging
    ml = ml.dropna().reset_index(drop=True)
    
    # Feature columns
    feature_cols = [c for c in ml.columns if 'lag' in c]
    X = ml[feature_cols]
    y = ml['label']
    
    return X, y, le, ml

def train_and_evaluate_model(X, y):
    """Train Random Forest classifier and return metrics"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False, random_state=42
    )
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    clf_report = classification_report(y_test, preds, output_dict=True)
    cm = confusion_matrix(y_test, preds)
    
    return model, acc, clf_report, cm, X_train, X_test, y_train, y_test

def predict_next_day(model, label_encoder, ml_df, n_lags=3):
    """Predict tomorrow's sentiment"""
    X_next = ml_df.filter(regex='lag').tail(1)
    
    if X_next.empty:
        return "Unknown", [0.5, 0.5]
    
    pred = model.predict(X_next)[0]
    prob = model.predict_proba(X_next)[0]
    label = label_encoder.inverse_transform([pred])[0]
    
    return label, prob

# -----------------------------------------------------------
# PDF REPORT GENERATOR
# -----------------------------------------------------------
def create_pdf_report(dataframe, metrics_dict):
    """Generate PDF report with summary statistics"""
    buffer = io.BytesIO()
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Web3 MarketMind 4.0 - Analytics Report", ln=True, align="C")
    pdf.ln(5)
    
    # Date
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)
    
    # Key Metrics
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Key Metrics", ln=True)
    pdf.set_font("Arial", "", 11)
    
    for key, value in metrics_dict.items():
        pdf.cell(0, 8, f"{key}: {value}", ln=True)
    
    pdf.ln(10)
    
    # Data Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Data Summary (First 20 rows)", ln=True)
    pdf.set_font("Arial", "", 9)
    
    for idx, row in dataframe.head(20).iterrows():
        line = f"{row['date']} | {row['Sentiment']}: PnL={row['closedPnL']:.2f}, Lev={row['leverage']:.2f}, Vol={row['size']:.2f}"
        pdf.cell(0, 6, line, ln=True)
    
    pdf.output(buffer)
    return buffer.getvalue()

# -----------------------------------------------------------
# MAIN APP
# -----------------------------------------------------------
def main():
    # Initialize authentication
    authenticator = init_authenticator()
    
    # Call login method (stores results in authenticator object)
    authenticator.login(location="sidebar")
    
    # Access authentication status from the authenticator object
    if st.session_state.get("authentication_status") == False:
        st.sidebar.error("Username/password is incorrect")
        st.stop()
    elif st.session_state.get("authentication_status") == None:
        st.sidebar.warning("Please enter your username and password")
        st.info("👋 **Demo Credentials:** username: `demo` | password: `demo123`")
        st.stop()
    
    # Get user info from session state
    name = st.session_state.get("name")
    username = st.session_state.get("username")
    
    # Logout button
    with st.sidebar:
        st.success(f"Welcome, {name}!")
        authenticator.logout(location="sidebar")
        st.divider()
    
    # -----------------------------------------------------------
    # HEADER
    # -----------------------------------------------------------
    st.markdown("<h1 class='main-title'>💎 Web3 MarketMind 4.0</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='sub-title'>Trader Sentiment Intelligence Dashboard</h4>", unsafe_allow_html=True)
    st.divider()
    
    # -----------------------------------------------------------
    # SIDEBAR - CONTROLS
    # -----------------------------------------------------------
    st.sidebar.header("⚙️ Controls")
    
    demo_mode = st.sidebar.toggle("Use Demo Data (Sample)", value=True)
    trader_file = st.sidebar.file_uploader("📂 Upload Trader Data", type=["csv"])
    sentiment_file = st.sidebar.file_uploader("📂 Upload Sentiment Data", type=["csv"])
    
    # Load data
    if demo_mode:
        # Create sample data for demo
        st.sidebar.info("Using generated demo data")
        dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
        trader_df = pd.DataFrame({
            'time': dates,
            'closedPnL': np.random.randn(90) * 100 + 50,
            'leverage': np.random.uniform(1, 20, 90),
            'size': np.random.uniform(1000, 50000, 90)
        })
        
        sentiment_df = pd.DataFrame({
            'Date': dates,
            'Classification': np.random.choice(['Fear', 'Greed', 'Neutral'], 90, p=[0.3, 0.3, 0.4])
        })
    elif trader_file and sentiment_file:
        trader_df = pd.read_csv(trader_file)
        sentiment_df = pd.read_csv(sentiment_file)
    else:
        st.warning("⚠️ Upload both CSV files or enable demo mode to continue.")
        st.stop()
    
    # -----------------------------------------------------------
    # DATA CLEANING & MERGE
    # -----------------------------------------------------------
    with st.spinner("Processing data..."):
        trader_df['time'] = pd.to_datetime(trader_df['time'], errors='coerce')
        sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'], errors='coerce')
        
        trader_df.dropna(subset=['closedPnL', 'leverage', 'size'], inplace=True)
        trader_df = trader_df[trader_df['leverage'] > 0]
        trader_df['date'] = trader_df['time'].dt.date
        sentiment_df['date'] = sentiment_df['Date'].dt.date
        
        merged_df = trader_df.groupby('date').agg({
            'closedPnL': 'mean',
            'leverage': 'mean',
            'size': 'sum'
        }).reset_index()
        
        merged_df = merged_df.merge(
            sentiment_df[['date', 'Classification']], 
            on='date', 
            how='left'
        )
        merged_df.rename(columns={'Classification': 'Sentiment'}, inplace=True)
        merged_df.dropna(subset=['Sentiment'], inplace=True)
        
        # Fetch BTC prices
        btc_daily = get_crypto_prices(coin="bitcoin", days=365)
        
        if not btc_daily.empty:
            btc_daily['date'] = pd.to_datetime(btc_daily['date']).dt.date
            merged_df = merged_df.merge(btc_daily, on='date', how='left')
            
            # Compute BTC daily return
            merged_df = merged_df.sort_values('date')
            merged_df['btc_return'] = merged_df['bitcoin_close'].pct_change().fillna(0)
        else:
            merged_df['bitcoin_close'] = np.nan
            merged_df['btc_return'] = 0
    
    # -----------------------------------------------------------
    # FILTERS
    # -----------------------------------------------------------
    st.sidebar.subheader("🔍 Filters")
    
    sentiment_options = merged_df['Sentiment'].unique().tolist()
    sentiment_filter = st.sidebar.multiselect(
        "Select Sentiment:", 
        sentiment_options, 
        default=sentiment_options
    )
    
    date_min = merged_df['date'].min()
    date_max = merged_df['date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range:", 
        [date_min, date_max],
        min_value=date_min,
        max_value=date_max
    )
    
    lev_min = float(merged_df['leverage'].min())
    lev_max = float(merged_df['leverage'].max())
    lev_range = st.sidebar.slider(
        "Leverage Range:", 
        lev_min, 
        lev_max, 
        (lev_min, lev_max)
    )
    
    # Apply filters
    filtered_df = merged_df[
        (merged_df['Sentiment'].isin(sentiment_filter)) &
        (merged_df['date'] >= date_range[0]) & 
        (merged_df['date'] <= date_range[1]) &
        (merged_df['leverage'].between(lev_range[0], lev_range[1]))
    ]
    
    st.sidebar.success(f"✅ {len(filtered_df)} records after filtering")
    
    # -----------------------------------------------------------
    # METRICS SECTION
    # -----------------------------------------------------------
    st.subheader("📊 Key Market Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    avg_pnl = filtered_df['closedPnL'].mean()
    avg_lev = filtered_df['leverage'].mean()
    total_vol = filtered_df['size'].sum()
    
    col1.metric("💰 Avg PnL", f"${avg_pnl:.2f}")
    col2.metric("📈 Avg Leverage", f"{avg_lev:.2f}x")
    col3.metric("📊 Total Volume", f"${total_vol:,.0f}")
    
    if 'bitcoin_close' in filtered_df.columns and not filtered_df['bitcoin_close'].isna().all():
        latest_btc = filtered_df['bitcoin_close'].iloc[-1]
        col4.metric("₿ BTC Price", f"${latest_btc:,.2f}")
    else:
        col4.metric("₿ BTC Price", "N/A")
    
    # -----------------------------------------------------------
    # INSIGHTS
    # -----------------------------------------------------------
    st.subheader("🧠 AI-Style Market Insights")
    
    if 'Fear' in filtered_df['Sentiment'].values and 'Greed' in filtered_df['Sentiment'].values:
        fear_df = filtered_df[filtered_df['Sentiment'] == 'Fear']
        greed_df = filtered_df[filtered_df['Sentiment'] == 'Greed']
        
        if len(fear_df) > 0 and len(greed_df) > 0:
            lev_ratio = greed_df['leverage'].mean() / fear_df['leverage'].mean()
            pnl_ratio = greed_df['closedPnL'].mean() / fear_df['closedPnL'].mean()
            
            st.markdown(f"""
            - 📊 **Leverage Ratio:** Traders used **{lev_ratio:.2f}×** more leverage in *Greed* periods.
            - 💹 **PnL Impact:** Profitability changed by **{pnl_ratio:.2f}×** during *Greed* vs *Fear*.
            - 🧩 **Interpretation:** Greedy markets drive higher risks — amplifying both gains and losses.
            - 🎯 **Recommendation:** {'Consider risk management strategies' if lev_ratio > 1.5 else 'Current leverage levels appear balanced'}.
            """)
        else:
            st.info("Not enough data in both sentiment categories for comparison.")
    else:
        st.info("Not enough data to compare sentiment states.")
    
    # -----------------------------------------------------------
    # VISUALS
    # -----------------------------------------------------------
    st.subheader("📈 Interactive Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "PnL Distribution", 
        "Leverage Correlation", 
        "Sentiment Timeline",
        "BTC Price Overlay"
    ])
    
    with tab1:
        fig1 = px.box(
            filtered_df, 
            x='Sentiment', 
            y='closedPnL', 
            color='Sentiment',
            title="PnL Distribution by Sentiment",
            color_discrete_map={'Fear': '#ef4444', 'Greed': '#22c55e', 'Neutral': '#6b7280'}
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        corr_data = filtered_df[['closedPnL', 'leverage', 'size']].corr()
        fig2, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_data, annot=True, cmap='YlGnBu', ax=ax, fmt='.2f')
        ax.set_title("Correlation Heatmap")
        st.pyplot(fig2)
    
    with tab3:
        fig3 = px.line(
            filtered_df, 
            x='date', 
            y='closedPnL', 
            color='Sentiment',
            title="Daily PnL vs Sentiment",
            markers=True
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab4:
        if 'bitcoin_close' in filtered_df.columns and not filtered_df['bitcoin_close'].isna().all():
            # Create dual-axis chart
            fig4 = go.Figure()
            
            fig4.add_trace(go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['bitcoin_close'],
                name='BTC Price',
                yaxis='y',
                line=dict(color='#f7931a', width=2)
            ))
            
            fig4.add_trace(go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['closedPnL'],
                name='Avg PnL',
                yaxis='y2',
                line=dict(color='#3b82f6', width=2)
            ))
            
            fig4.update_layout(
                title='BTC Price vs Trading PnL',
                xaxis=dict(title='Date'),
                yaxis=dict(title='BTC Price (USD)', side='left'),
                yaxis2=dict(title='Avg PnL', overlaying='y', side='right'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("BTC price data not available")
    
    # -----------------------------------------------------------
    # ML MODEL SECTION
    # -----------------------------------------------------------
    st.subheader("🤖 ML Sentiment Predictor")
    
    model_path = "models/sentiment_rf.joblib"
    os.makedirs("models", exist_ok=True)
    
    col_ml1, col_ml2 = st.columns([2, 1])
    
    with col_ml1:
        if st.button("🔄 Train/Retrain Model", type="primary"):
            with st.spinner("Training Random Forest model..."):
                try:
                    X, y, label_encoder, ml_df = prepare_ml_dataset(merged_df, n_lags=3)
                    
                    if len(X) < 20:
                        st.warning("Not enough data to train model (need at least 20 samples)")
                    else:
                        model, acc, clf_report, cm, X_train, X_test, y_train, y_test = train_and_evaluate_model(X, y)
                        
                        # Save model
                        joblib.dump({
                            'model': model,
                            'label_encoder': label_encoder,
                            'feature_names': X.columns.tolist()
                        }, model_path)
                        
                        st.success(f"✅ Model trained! Test accuracy: {acc:.2%}")
                        
                        # Show confusion matrix
                        st.write("**Confusion Matrix:**")
                        fig_cm, ax_cm = plt.subplots(figsize=(6, 4))
                        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax_cm)
                        ax_cm.set_xlabel('Predicted')
                        ax_cm.set_ylabel('Actual')
                        st.pyplot(fig_cm)
                        
                        # Feature importance
                        feature_importance = pd.DataFrame({
                            'feature': X.columns,
                            'importance': model.feature_importances_
                        }).sort_values('importance', ascending=False).head(10)
                        
                        st.write("**Top 10 Feature Importances:**")
                        st.dataframe(feature_importance, use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Error training model: {e}")
    
    with col_ml2:
        if os.path.exists(model_path):
            st.info("✅ Model loaded from disk")
            
            try:
                model_bundle = joblib.load(model_path)
                X, y, label_encoder, ml_df = prepare_ml_dataset(merged_df, n_lags=3)
                
                pred_label, pred_prob = predict_next_day(
                    model_bundle['model'],
                    model_bundle['label_encoder'],
                    ml_df,
                    n_lags=3
                )
                
                st.metric("📅 Tomorrow's Prediction", pred_label)
                
                # Show probabilities
                prob_df = pd.DataFrame({
                    'Sentiment': model_bundle['label_encoder'].classes_,
                    'Probability': pred_prob
                })
                st.dataframe(prob_df, use_container_width=True)
                
            except Exception as e:
                st.warning(f"Could not make prediction: {e}")
        else:
            st.warning("⚠️ No trained model found. Click 'Train Model' to create one.")
    
    # -----------------------------------------------------------
    # DOWNLOADABLES
    # -----------------------------------------------------------
    st.subheader("📦 Export Options")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        # CSV Export
        csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Download Cleaned Data (CSV)",
            csv_bytes,
            "cleaned_trader_data.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col_exp2:
        # PDF Export
        if st.button("📥 Generate PDF Report", use_container_width=True):
            with st.spinner("Generating PDF..."):
                metrics_dict = {
                    "Total Records": len(filtered_df),
                    "Average PnL": f"${avg_pnl:.2f}",
                    "Average Leverage": f"{avg_lev:.2f}x",
                    "Total Volume": f"${total_vol:,.0f}",
                    "Date Range": f"{date_range[0]} to {date_range[1]}"
                }
                
                pdf_data = create_pdf_report(filtered_df, metrics_dict)
                b64 = base64.b64encode(pdf_data).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="MarketMind_Report.pdf">📄 Click to Download PDF Report</a>'
                st.markdown(href, unsafe_allow_html=True)
                st.success("✅ PDF generated successfully!")
    
    # -----------------------------------------------------------
    # FOOTER
    # -----------------------------------------------------------
    st.divider()
    st.caption("🎯 Web3 MarketMind 4.0 | Powered by Streamlit | Data sources: CoinGecko, Binance")
    st.caption("⚠️ **Disclaimer:** This tool is for educational purposes only. Not financial advice.")

if __name__ == "__main__":
    main()
