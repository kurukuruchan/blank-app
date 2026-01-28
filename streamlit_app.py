import streamlit as st
from st_supabase_connection import SupabaseConnection
import plotly.express as px
import pandas as pd
from datetime import date

# ページ設定
st.set_page_config(page_title="日本旅行思い出マップ", layout="wide")

# Supabase 接続
conn = st.connection("supabase", type=SupabaseConnection)

# 都道府県リスト（JISコード順など、地図データとの紐付け用）
PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

# --- データの取得 ---
def load_data():
    response = conn.table("travel_logs").select("*").execute()
    return response.data

logs = load_data()
visited_prefs = list(set([log["prefecture"] for log in logs]))

# --- タイトル ---
st.title("🗾 日本旅行思い出マップ (Supabase永続版)")

# --- サイドバー：入力 ---
with st.sidebar:
    st.header("✈️ 旅行を記録")
    with st.form("add_form", clear_on_submit=True):
        pref = st.selectbox("都道府県", PREFECTURES)
        v_date = st.date_input("日付", date.today())
        comm = st.text_area("思い出")
        img = st.text_input("画像URL")
        if st.form_submit_button("保存"):
            conn.table("travel_logs").insert({
                "prefecture": pref, "visit_date": str(v_date), "comment": comm, "image_url": img
            }).execute()
            st.rerun()

# --- メインレイアウト ---
col_map, col_detail = st.columns([1.5, 1])

with col_map:
    st.subheader("🗺️ 訪問状況")
    
    # 地図データ用のDataFrame作成
    # 訪問済みは1、未訪問は0として数値化
    df_map = pd.DataFrame({
        "prefecture": PREFECTURES,
        "visited": [1 if p in visited_prefs else 0 for p in PREFECTURES]
    })

    # Plotlyによる簡易日本地図（擬似的なヒートマップ）
    # ※本来はGeoJSONが必要ですが、ここでは訪問数を可視化する簡単なチャートを作成
    fig = px.choropleth(
        df_map,
        geojson="https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/2_bundeslaender/1_sehr_hoch.geo.json", # 日本のGeoJSONが必要
        locations="prefecture",
        color="visited",
        color_continuous_scale=["#eeeeee", "#1f77b4"], # 未訪問はグレー、訪問済みは青
        range_color=[0, 1],
        labels={'visited':'訪問済み'}
    )
    
    # より確実に動く「棒グラフによる進捗確認」を併設
    st.write(f"現在の制覇数: {len(visited_prefs)} / 47")
    st.bar_chart(df_map.set_index("prefecture"))

with col_detail:
    st.subheader("📸 思い出フィード")
    target = st.selectbox("県別フィルタ", ["全て"] + PREFECTURES)
    
    display_logs = logs if target == "全て" else [l for l in logs if l["prefecture"] == target]
    
    for l in reversed(display_logs):
        with st.container(border=True):
            st.write(f"**{l['prefecture']}** ({l['visit_date']})")
            if l.get("image_url"):
                st.image(l["image_url"], use_container_width=True)
            st.write(l["comment"])
