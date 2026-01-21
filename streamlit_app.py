import streamlit as st
from streamlit_japan_map import map_japan
from datetime import date
import io

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

st.title("🗾 日本旅行の思い出マップ")

# サイドバー：入力フォーム
with st.sidebar:
    st.header("✈️ 新しい旅行を記録")
    with st.form("travel_form", clear_on_submit=True):
        selected_pref = st.selectbox("都道府県", PREFECTURES)
        travel_date = st.date_input("日付", date.today())
        comment = st.text_area("思い出（食事、観光スポットなど）")
        uploaded_file = st.file_uploader("写真", type=['jpg', 'jpeg', 'png'])
        
        submitted = st.form_submit_button("記録を保存")
        if submitted:
            # 画像の処理（BytesIOを使ってメモリ上に保持）
            img_display = None
            if uploaded_file is not None:
                img_display = uploaded_file.getvalue()

            new_log = {
                "prefecture": selected_pref,
                "date": travel_date,
                "comment": comment,
                "image": img_display
            }
            st.session_state.travel_logs.append(new_log)
            st.rerun()

# メインレイアウト
col_map, col_info = st.columns([1.2, 1])

with col_map:
    st.subheader("🗺️ 日本地図")
    # 訪問済みの都道府県を抽出
    visited_prefs = list(set([log["prefecture"] for log in st.session_state.travel_logs]))
    # 訪問済みは青(#1f77b4)、未訪問は薄いグレー
    colors = {pref: "#1f77b4" for pref in visited_prefs}
    
    # 地図を表示し、クリックされた都道府県を取得
    clicked_pref = map_japan(colors=colors)

with col_info:
    # フィルタリング
    if clicked_pref:
        st.subheader(f"📍 {clicked_pref} の思い出")
        filtered_logs = [log for log in st.session_state.travel_logs if log["prefecture"] == clicked_pref]
        
        if not filtered_logs:
            st.info(f"{clicked_pref} の記録はまだありません。")
        else:
            for log in reversed(filtered_logs):
                with st.container(border=True):
                    st.caption(f"📅 {log['date']}")
                    if log["image"]:
                        st.image(log["image"], use_container_width=True)
                    st.write(log["comment"])
    else:
        st.subheader("📸 最近の思い出")
        if not st.session_state.travel_logs:
            st.info("左のサイドバーから最初の旅行を記録しましょう！")
        else:
            st.write("地図をクリックすると、その場所の思い出に絞り込めます。")
            # 直近3件を表示
            for log in reversed(st.session_state.travel_logs[-3:]):
                st.text(f"📍 {log['prefecture']} ({log['date']})")
