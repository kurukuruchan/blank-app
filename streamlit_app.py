import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import date

# ページ設定
st.set_page_config(page_title="日本旅行記 (Supabase版)", layout="wide")

# Supabase 接続
conn = st.connection("supabase", type=SupabaseConnection)

# 都道府県リスト
PREFECTURES = ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
               "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
               "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
               "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
               "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
               "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
               "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"]

st.title("🗾 日本旅行の思い出 DB")

# --- データの読み込み ---
def get_travel_logs():
    return conn.query("*", table="travel_logs", ttl="0s").execute()

response = get_travel_logs()
logs_df = response.data if response.data else []

# --- サイドバー：入力フォーム (書き込み処理) ---
with st.sidebar:
    st.header("✈️ 旅行を記録する")
    with st.form("travel_form", clear_on_submit=True):
        pref = st.selectbox("都道府県", PREFECTURES)
        v_date = st.date_input("日付", date.today())
        comm = st.text_area("思い出メモ")
        # ※画像は本来Storageが必要ですが、課題のシンプル化のため今回はテキスト(URL)のみ対応
        img_url = st.text_input("画像のURL (任意)")
        
        if st.form_submit_button("Supabaseに保存"):
            new_data = {
                "prefecture": pref,
                "visit_date": str(v_date),
                "comment": comm,
                "image_url": img_url
            }
            # データベースへの書き込み
            conn.table("travel_logs").insert(new_data).execute()
            st.success("データベースに書き込みました！")
            st.rerun()

# --- メイン表示 ---
visited_count = len(set([d["prefecture"] for d in logs_df]))
st.metric("制覇した都道府県", f"{visited_count} / 47")

tab1, tab2 = st.tabs(["📍 場所から探す", "📜 タイムライン"])

with tab1:
    target = st.selectbox("都道府県で絞り込む", ["全て"] + PREFECTURES)
    display_logs = logs_df if target == "全て" else [d for d in logs_df if d["prefecture"] == target]
    
    for log in reversed(display_logs):
        with st.container(border=True):
            st.subheader(f"{log['prefecture']} ({log['visit_date']})")
            if log["image_url"]:
                st.image(log["image_url"], use_container_width=True)
            st.write(log["comment"])

with tab2:
    if not logs_df:
        st.info("データがありません。")
    else:
        st.table([{"日付": d["visit_date"], "都道府県": d["prefecture"], "メモ": d["comment"]} for d in logs_df])
