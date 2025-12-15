import streamlit as st
import pandas as pd
import numpy as np

def simulate_product_forecast(product_summary: pd.DataFrame) -> pd.DataFrame:
    """
    Adds dummy metrics for sales forecast accuracy based on the aggregated results.
    A machine learning model would be integrated here in a real application.
    """
    
    # Generate dummy accuracy metrics
    # Assume higher accuracy for products with more sales (likely more important products)
    
    def get_dummy_metrics(count):
        # MAE (Mean Absolute Error), RMSE (Root Mean Square Error), R² (R-squared)
        if count > 500:
            return 15.0, 25.0, 0.85
        elif count > 100:
            return 25.0, 40.0, 0.75
        else:
            return 35.0, 50.0, 0.65
            
    # Calculate and add new columns
    metrics = product_summary['SalesCount'].apply(
        lambda x: pd.Series(get_dummy_metrics(x))
    )
    metrics.columns = ['MAE', 'RMSE', 'R²']
    
    forecast_summary = pd.concat([product_summary, metrics], axis=1)
    
    return forecast_summary.sort_values(by='SalesCount', ascending=False)

def run_forecast_tab():
    st.header("📦 Product Sales Forecasting (Trial Implementation)")
    st.write("Performs simple sales trend analysis from data including date and product name (+ quantity), and creates a summary for reporting.")

    uploaded_file = st.file_uploader("Upload Sales Data CSV", type="csv", key="forecast")

    if not uploaded_file:
        # Clear session state if no file is present
        st.session_state.pop("product_summary", None)
        st.session_state["product_ready"] = False
        return
    try:
        uploaded_file.seek(0) # Reset pointer just in case
        df = pd.read_csv(uploaded_file, encoding='utf_8_sig') 
        st.success(f"File `{uploaded_file.name}` loaded successfully (UTF-8 SIG).")
    
    except UnicodeDecodeError:
        # 2. Retry with Shift-JIS on failure
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='shift_jis')
            st.warning("⚠️ File was loaded as Shift-JIS.")
        except Exception as e_sjis:
            # 3. Last resort: Load with Shift-JIS, ignoring errors
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='shift_jis', errors='ignore')
                st.error("🚨 Critical encoding error. Loaded by ignoring invalid characters. Please check your data.")
            except Exception as e_ignore:
                st.error(f"Failed to load file. Please check encoding: {e_ignore}")
                st.session_state.pop("product_summary", None)
                st.session_state["product_ready"] = False
                return
    
    except Exception as e:
        # Other general loading errors
        st.error(f"An unexpected error occurred while loading the file: {e}")
        st.session_state.pop("product_summary", None)
        st.session_state["product_ready"] = False
        return
    
    # --- Processing after file upload ---
    
    st.subheader("① Uploaded Data")
    st.dataframe(df.head())

    # Date format conversion
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        # Warning if dates are missing
        if df["Date"].isna().sum() > 0:
            st.warning("⚠️ Some dates in the 'Date' column are invalid.")

    # Aggregation example: Sales count per product
    st.subheader("② Product Sales Aggregation (Simple)")
    if "Product" not in df.columns:
        st.error("❌ The 'Product' column does not exist. Please check the column names in your CSV.")
        st.session_state.pop("product_summary", None)
        st.session_state["product_ready"] = False
        return
        
    # Perform product aggregation
    product_summary = df.groupby("Product").size().reset_index(name="SalesCount")
    st.dataframe(product_summary.sort_values("SalesCount", ascending=False))

    # Daily trend (optional)
    if "Date" in df.columns:
        st.subheader("③ Daily Sales Trend")
        daily_sales = df.groupby("Date").size().reset_index(name="SalesCount")
        st.line_chart(daily_sales.set_index("Date")["SalesCount"])
        
    st.success("Simple sales analysis completed. Creating summary for report.")
    
    # 1. Execute Forecast Simulation (immediate execution)
    forecast_summary_df = simulate_product_forecast(product_summary)

    # 2. Display Results
    st.subheader("④ Forecast Summary (For Report Integration)")
    st.info("Forecast accuracy metrics are simulated based on sales count.")
    st.dataframe(forecast_summary_df)
        
    # 3. Save to session state for report integration
    st.session_state["product_summary"] = forecast_summary_df
        
    # Set flag to enable report generation checkbox
    st.session_state["product_ready"] = True 

    st.success("All analysis and summary creation are complete. You can select this result in the Report Generation Settings on the left.")
    st.session_state["forecast_done"] = True

    # Keep this line!
    if not st.session_state.get("rerun_triggered", False):
        st.session_state["rerun_triggered"] = True
        st.rerun()