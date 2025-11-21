import streamlit as st
import pandas as pd

from data_preprocessing import preprocess_retail_data
from rfm import calculate_rfm
from clustering import cluster_rfm
# from visualization import plot_cluster_means  # 使う場合

st.title("Customer Segmentation DSS")
st.write("CSVをアップロードするだけでRFM分析＋クラスタリングを実行します。")

uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file:
    # CSV読み込み
    df = pd.read_csv(uploaded_file)
    st.subheader("① アップロードしたデータ")
    st.dataframe(df.head())

    # 前処理
    df_clean = preprocess_retail_data(df)
    st.subheader("② 前処理後のデータ")
    st.dataframe(df_clean.head())

    # RFM計算
    rfm = calculate_rfm(df_clean)
    st.subheader("③ RFMテーブル")
    st.dataframe(rfm.head())

    # クラスタリング
    k = st.slider("クラスタ数 (k)", 2, 10, 4)
    rfm_clustered, model = cluster_rfm(rfm, k)

    st.subheader("④ クラスタ結果")
    st.dataframe(rfm_clustered.head())

    # クラスタ平均
    st.subheader("⑤ クラスタ別平均")
    cluster_means = rfm_clustered.groupby("Cluster").mean()
    st.dataframe(cluster_means)

    st.success("分析が完了しました！")
