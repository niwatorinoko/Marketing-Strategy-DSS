# Customer Behavior Analytics DSS

顧客の購買履歴をアップロードすると、RFM 分析と KMeans によるクラスタリングを一括で実行する Streamlit アプリです。クレンジング済みの RFM テーブルとクラスタ別統計を素早く確認できます。

## セットアップ
- Python 3.10 以上を推奨
- 仮想環境を作成する場合（任意）
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- 依存関係をインストール
  ```bash
  pip install -r requirements.txt
  ```

## 実行方法
```bash
streamlit run app.py
```
ブラウザが開いたら CSV をアップロードし、スライダーでクラスタ数 `k` を設定すると結果が表示されます。

### Docker Compose で動かす場合
Dockerfile があるため `docker-compose.yml` から起動できます。
```bash
docker compose build
docker compose up
```
ブラウザで `http://localhost:8501` にアクセスしてください。コードを編集するとコンテナ内にも反映されるよう、リポジトリ全体をコンテナにマウントしています。

## 入力データ要件
- 必須列: `CustomerID`（または `Customer ID`）、`InvoiceNo`（または `Invoice`）、`InvoiceDate`、`Quantity`、`Price`
- `InvoiceDate` は日時形式に変換可能であること
- `Quantity` と `Price` は正の数を想定
- 欠損行は `CustomerID` と `InvoiceDate` が揃っている必要があります

## 処理の流れ
- 前処理 (`data_preprocessing.py`): 列名の標準化、日付・型変換、不正値除外、`TotalPrice` 作成
- RFM 計算 (`rfm.py`): 最新日付を基準に `Recency` `Frequency` `Monetary` を算出
- クラスタリング (`clustering.py`): 標準化後に KMeans でクラスタ付与、クラスタ平均を表示

## 主なファイル
- `app.py`: Streamlit フロントエンドと分析実行フロー
- `data_preprocessing.py` / `preprocess_data.py`: データ前処理関数
- `rfm.py`: RFM 指標の算出
- `clustering.py`: KMeans クラスタリング
- `data/`: サンプル CSV（`online_retail_II.csv` など）

## 備考
- データ列名が異なる場合は前処理部を適宜調整してください。
- 追加の可視化を行う場合は `visualization.py` を拡張できます。
