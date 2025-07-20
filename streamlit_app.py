import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Mini TraderSync", layout="wide")

st.title("📈 Mini TraderSync - IBKR Trade Journal")

uploaded_file = st.file_uploader("Upload your IBKR Trade CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Try to standardize column names if needed
        df.columns = [col.strip() for col in df.columns]

        # Sample mappings (customize based on actual IBKR format)
        df['Date'] = pd.to_datetime(df['Date'])
        df['RealizedPNL'] = df['Proceeds'] - df['CostBasis']

        df = df.sort_values("Date")
        df['CumulativePNL'] = df['RealizedPNL'].cumsum()

        # Metrics
        total_pnl = df['RealizedPNL'].sum()
        win_rate = (df['RealizedPNL'] > 0).mean()
        avg_win = df[df['RealizedPNL'] > 0]['RealizedPNL'].mean()
        avg_loss = df[df['RealizedPNL'] < 0]['RealizedPNL'].mean()

        # Layout
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total P&L", f"${total_pnl:.2f}")
        col2.metric("Win Rate", f"{win_rate * 100:.2f}%")
        col3.metric("Avg Win", f"${avg_win:.2f}" if not pd.isna(avg_win) else "N/A")
        col4.metric("Avg Loss", f"${avg_loss:.2f}" if not pd.isna(avg_loss) else "N/A")

        # Charts
        st.subheader("📊 Equity Curve")
        st.line_chart(df.set_index("Date")["CumulativePNL"])

        st.subheader("📄 Raw Trades Table")
        st.dataframe(df)

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
else:
    st.info("Upload an IBKR CSV trade report to get started.")

