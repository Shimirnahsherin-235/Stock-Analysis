import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import date

# Page config
st.set_page_config(page_title="📈 Stock & Commodity Price Dashboard", layout="wide")

# Title
st.title("📊 Stock & Commodity Price Dashboard")
st.markdown(
    "Visualize historical prices for multiple companies, gold, and silver using data from Yahoo Finance."
)

# Sidebar inputs
st.sidebar.title("Asset Selection")

# Multiselect for multiple symbols including Gold and Silver
tickers = st.sidebar.multiselect(
    "Select Symbols (Stocks / Commodities):",
    [
        # US Stocks
        "AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "META", "NFLX",
        # Indian Stocks
        "TCS.NS", "RELIANCE.NS",
        # Commodities - Spot prices
        "GC=F",    # Gold Spot
        "SI=F",    # Silver Spot
        # ETFs
        "GLD",     # Gold ETF
        "SLV"      # Silver ETF
    ],
    default=["AAPL"]
)

start_date = st.sidebar.date_input("Start Date", date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())

# Fetching stock/commodity data for multiple symbols
@st.cache_data
def get_data(symbols, start, end):
    data = {}
    for symbol in symbols:
        df = yf.download(symbol, start=start, end=end, auto_adjust=True)
        df.reset_index(inplace=True)
        data[symbol] = df
    return data

# Load data
if tickers:
    data = get_data(tickers, start_date, end_date)

    # Show recent data for each selected symbol
    for symbol in tickers:
        st.subheader(f"Data Preview for {symbol}")
        st.dataframe(data[symbol].tail())

    # Plotting
    st.subheader("📉 Closing Price Chart for Selected Symbols")
    fig = go.Figure()

    for symbol in tickers:
        fig.add_trace(go.Scatter(
            x=data[symbol]['Date'],
            y=data[symbol]['Close'],
            mode='lines',
            name=symbol
        ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (USD/INR)",
        template="plotly_dark",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # Optional: Add moving average
    st.sidebar.subheader("Moving Averages")
    if st.sidebar.checkbox("Show 30-Day Moving Average for All Symbols"):
        ma_fig = go.Figure()
        for symbol in tickers:
            data[symbol]['MA30'] = data[symbol]['Close'].rolling(window=30).mean()
            ma_fig.add_trace(go.Scatter(
                x=data[symbol]['Date'],
                y=data[symbol]['MA30'],
                mode='lines',
                name=f"{symbol} 30-Day MA"
            ))
        ma_fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (USD/INR)",
            template="plotly_dark",
            showlegend=True
        )
        st.subheader("📈 30-Day Moving Average Chart")
        st.plotly_chart(ma_fig, use_container_width=True)
else:
    st.warning("Please select at least one symbol from the sidebar.")

