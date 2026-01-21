import streamlit as st
import pandas as pd
from datetime import date

# ページ設定
st.set_page_config(page_title="日本旅行記アプリ", layout="wide")

# セッション状態の初期化
if 'travel_logs' not in st.session_state:
    st.session_state.travel_logs = []

# 都道府県リスト
PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

st.title("🗾 日本旅行の思い出ログ")

# サイドバー：入力フォーム
with st.sidebar:
    st.header("✈️ 新しい旅行を記録")
    with st.form("travel_form", clear_on_submit=True):
        selected_pref = st.selectbox("都道府県を選択", PREFECTURES)
        travel_date = st.date_input("日付", date.today())
        comment = st.text_area("思い出（食事、観光スポットなど）")
        uploaded_file = st.file_uploader("写真", type=['jpg', 'jpeg', 'png'])
        
        if st.form_submit_button("記録を保存"):
            img_data = uploaded_file.getvalue() if uploaded_file else None
            new_log = {
                "prefecture": selected_pref,
                "date": travel_date,
                "comment": comment,
                "image": img_data
            }
            st.session_state.travel_logs.append(new_log)
            st.success(f"{selected_pref}の思い出を保存しました！")
            st.rerun()

# メインエリア
# 訪問済みリストの作成
visited_prefs = list(set([log["prefecture"] for log in st.session_state.travel_logs]))

# 上部にステータス表示
st.write(f"### 🌏 現在の制覇状況: {len(visited_prefs)} / 47 都道府県")
st.progress(len(visited_prefs) / 47)

# 表示切り替え
tab1, tab2 = st.tabs(["📍 場所から探す", "📜 全ての履歴"])

with tab1:
    # 都道府県を選択して表示（地図の代わりにセレクトボックスを使用）
    target_pref = st.selectbox("表示したい都道府県を選んでください", ["未選択"] + PREFECTURES)
    
    if target_pref != "未選択":
        filtered_logs = [log for log in st.session_state.travel_logs if log["prefecture"] == target_pref]
        if not filtered_logs:
            st.info(f"{target_pref} の記録はまだありません。")
        else:
            for log in reversed(filtered_logs):
                with st.container(border=True):
                    st.subheader(f"{log['date']} の思い出")
                    if log["image"]:
                        st.image(log["image"], use_container_width=True)
                    st.write(log["comment"])

with tab2:
    if not st.session_state.travel_logs:
        st.write("まだ記録がありません。")
    else:
        for log in reversed(st.session_state.travel_logs):
            with st.expander(f"{log['date']} - {log['prefecture']}"):
                if log["image"]:
                    st.image(log["image"], use_container_width=True)
                st.write(log["comment"])
