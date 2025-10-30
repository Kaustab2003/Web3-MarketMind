import os
import time
from datetime import datetime, timedelta, timezone
from typing import Tuple

import numpy as np
import pandas as pd
import requests
import streamlit as st
import altair as alt
import streamlit_authenticator as stauth


# -----------------------------
# Authentication Configuration
# -----------------------------
def init_authenticator() -> Tuple[stauth.Authenticate, dict]:
	"""Initialize Streamlit Authenticator with a demo user.

	Password can be provided via DEMO_PASSWORD environment variable; defaults to 'demo'.
	"""
	password = os.getenv("DEMO_PASSWORD", "demo")
	hashed_password = stauth.Hasher([password]).generate()[0]
	credentials = {
		"usernames": {
			"demo_user": {
				"name": "Demo User",
				"password": hashed_password,
			}
		}
	}
	cookie = {"name": "marketmind_auth", "key": "abcdef", "expiry_days": 7}
	authenticator = stauth.Authenticate(credentials, cookie["name"], cookie["key"], cookie["expiry_days"])
	return authenticator, credentials


# -----------------------------
# Data Fetching Utilities
# -----------------------------
@st.cache_data(ttl=300)
def fetch_coingecko_btc_market_chart(days: int = 90) -> pd.DataFrame:
	"""Fetch BTC market chart (prices) from CoinGecko for the last `days` days."""
	url = (
		"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days="
		+ str(days)
	)
	resp = requests.get(url, timeout=20)
	resp.raise_for_status()
	data = resp.json()
	prices = data.get("prices", [])
	if not prices:
		return pd.DataFrame(columns=["timestamp", "price"])
	df = pd.DataFrame(prices, columns=["timestamp_ms", "price"])  # [ms, price]
	df["timestamp"] = pd.to_datetime(df["timestamp_ms"], unit="ms", utc=True).dt.tz_convert(None)
	df = df.drop(columns=["timestamp_ms"]).sort_values("timestamp").reset_index(drop=True)
	return df


@st.cache_data(ttl=300)
def fetch_fear_greed_history(limit_days: int = 365) -> pd.DataFrame:
	"""Fetch Crypto Fear & Greed Index history from alternative.me API."""
	url = f"https://api.alternative.me/fng/?limit=0&format=json"
	resp = requests.get(url, timeout=20)
	resp.raise_for_status()
	data = resp.json()
	values = data.get("data", [])
	if not values:
		return pd.DataFrame(columns=["date", "value"])
	df = pd.DataFrame(values)
	# API provides timestamp (unix), value (string), time_until_update, classification
	df["date"] = pd.to_datetime(df["timestamp"].astype(int), unit="s", utc=True).dt.tz_convert(None)
	df["value"] = pd.to_numeric(df["value"], errors="coerce")
	df = df[["date", "value"]].sort_values("date").reset_index(drop=True)
	# Limit to last N days
	cutoff = datetime.now() - timedelta(days=limit_days)
	df = df[df["date"] >= cutoff].reset_index(drop=True)
	return df


def build_overlay_dataframe(price_df: pd.DataFrame, fgi_df: pd.DataFrame) -> pd.DataFrame:
	"""Align BTC price series with Fear & Greed Index on shared daily timestamps."""
	if price_df.empty or fgi_df.empty:
		return pd.DataFrame(columns=["date", "price", "fgi"])
	# Resample price to daily close
	resampled = (
		price_df.set_index("timestamp")["price"].resample("1D").last().dropna().rename("price")
	)
	fgi_daily = fgi_df.set_index("date")["value"].resample("1D").last().dropna().rename("fgi")
	merged = pd.concat([resampled, fgi_daily], axis=1).dropna().reset_index().rename(columns={"index": "date"})
	return merged


# -----------------------------
# Simple ML Model (Regression)
# -----------------------------
def prepare_features(df: pd.DataFrame, lookback_days: int = 7) -> Tuple[pd.DataFrame, pd.Series]:
	"""Create simple features: past returns and past FGI values to predict next-day FGI."""
	df = df.copy()
	df["return"] = df["price"].pct_change()
	# Lagged features for returns and FGI
	for lag in range(1, lookback_days + 1):
		df[f"ret_lag_{lag}"] = df["return"].shift(lag)
		df[f"fgi_lag_{lag}"] = df["fgi"].shift(lag)
	# Target: tomorrow's FGI
	df["target_fgi_next"] = df["fgi"].shift(-1)
	feature_cols = [c for c in df.columns if c.startswith("ret_lag_") or c.startswith("fgi_lag_")]
	df = df.dropna(subset=feature_cols + ["target_fgi_next"])  # drop rows without full lags
	X = df[feature_cols]
	y = df["target_fgi_next"]
	return X, y


def fit_linear_regression(X: pd.DataFrame, y: pd.Series):
	from sklearn.linear_model import Ridge
	from sklearn.preprocessing import StandardScaler
	from sklearn.pipeline import Pipeline

	model = Pipeline([
		("scaler", StandardScaler()),
		("ridge", Ridge(alpha=1.0, random_state=42)),
	])
	model.fit(X, y)
	return model


def predict_tomorrow_fgi(model, df: pd.DataFrame, lookback_days: int = 7) -> float:
	"""Predict next-day FGI using the last available lags."""
	df = df.copy()
	df["return"] = df["price"].pct_change()
	row = {}
	for lag in range(1, lookback_days + 1):
		row[f"ret_lag_{lag}"] = df["return"].iloc[-lag]
		row[f"fgi_lag_{lag}"] = df["fgi"].iloc[-lag]
	X_pred = pd.DataFrame([row])
	return float(model.predict(X_pred)[0])


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Web3 MarketMind", page_icon="🧠", layout="wide")


def main():
	# Auth
	authenticator, _ = init_authenticator()
	name, auth_status, username = authenticator.login(fields={"Form name": "Login", "Username": "Username", "Password": "Password"})

	if auth_status is False:
		st.error("Username/password is incorrect")
		st.stop()
	elif auth_status is None:
		st.warning("Please enter your username and password")
		st.stop()

	with st.sidebar:
		st.markdown("### Navigation")
		page = st.radio("Go to", options=["Dashboard", "Model", "About"], label_visibility="collapsed")
		st.divider()
		st.caption(f"Logged in as {name} ({username})")
		if st.button("Logout"):
			authenticator.logout(location="sidebar")
			st.experimental_rerun()

	st.title("🧠 Web3 MarketMind")
	st.caption("Overlay crypto sentiment vs BTC prices with a simple predictive model")

	if page == "Dashboard":
		col1, col2 = st.columns([4, 1])
		with col2:
			refresh_sec = st.slider("Auto-refresh (seconds)", 10, 300, 60, step=10)
			st.caption("Data refreshes on rerun")
			st.button("Manual refresh", on_click=lambda: st.cache_data.clear())
			st.write(" ")
			st.metric("Current Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		with col1:
			st.subheader("BTC Price vs Fear & Greed Index")
			with st.spinner("Fetching market and sentiment data..."):
				price_df = fetch_coingecko_btc_market_chart(days=120)
				fgi_df = fetch_fear_greed_history(limit_days=400)
				merged = build_overlay_dataframe(price_df, fgi_df)
			if merged.empty:
				st.warning("No data available.")
			else:
				# Build Altair chart with dual axis
				base = alt.Chart(merged).transform_calculate(
					date="toDate(datum.date)"
				)
				price_line = base.mark_line(color="#1f77b4").encode(
					x=alt.X("date:T", title="Date"),
					y=alt.Y("price:Q", title="BTC Price (USD)", axis=alt.Axis(format="$,.0f")),
					tooltip=[
						alt.Tooltip("date:T", title="Date"),
						alt.Tooltip("price:Q", title="BTC", format=",.2f"),
						alt.Tooltip("fgi:Q", title="FGI")
					],
				).properties(height=420)
				fgi_line = base.mark_line(color="#ff7f0e").encode(
					x="date:T",
					y=alt.Y("fgi:Q", title="Fear & Greed", scale=alt.Scale(domain=[0, 100])),
				)
				chart = alt.layer(price_line, fgi_line).resolve_scale(y="independent")
				st.altair_chart(chart, use_container_width=True)

		st.caption("BTC prices from CoinGecko; sentiment from alternative.me Fear & Greed Index.")
		# Auto refresh
		st.autorefresh = st.experimental_rerun if False else None
		st.experimental_set_query_params(_=int(time.time() // refresh_sec))

	elif page == "Model":
		st.subheader("Predict Tomorrow's Sentiment (FGI)")
		with st.spinner("Preparing features and training model..."):
			price_df = fetch_coingecko_btc_market_chart(days=240)
			fgi_df = fetch_fear_greed_history(limit_days=500)
			merged = build_overlay_dataframe(price_df, fgi_df)
			if len(merged) < 50:
				st.warning("Not enough data to train the model.")
				st.stop()
			X, y = prepare_features(merged, lookback_days=7)
			if X.empty:
				st.warning("Not enough data after feature preparation.")
				st.stop()
			model = fit_linear_regression(X, y)
			pred = predict_tomorrow_fgi(model, merged, lookback_days=7)
			last_fgi = merged["fgi"].iloc[-1]
			st.metric("Predicted FGI (tomorrow)", f"{pred:.1f}", delta=f"{pred - last_fgi:+.1f}")
			st.caption("Simple Ridge regression on lagged returns and FGI.")

			# Show feature importances (coefficients)
			from sklearn.linear_model import Ridge
			from sklearn.pipeline import Pipeline
			if isinstance(model, Pipeline) and isinstance(model[-1], Ridge):
				coefs = model[-1].coef_
				feat_importance = (
					pd.DataFrame({"feature": X.columns, "coef": coefs})
					.sort_values("coef", key=lambda s: s.abs(), ascending=False)
					.head(15)
				)
				st.dataframe(feat_importance, use_container_width=True)

	elif page == "About":
		st.markdown(
			"""
			This app overlays Bitcoin prices with the Crypto Fear & Greed Index and fits a small
			regression model to predict tomorrow's sentiment. Authentication is provided via
			Streamlit Authenticator.
			"""
		)


if __name__ == "__main__":
	main()


