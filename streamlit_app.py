import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import date

# ページ設定
st.set_page_config(page_title="日本旅行思い出マップ", layout="wide")

# Supabase 接続
conn = st.connection("supabase", type=SupabaseConnection)

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

# --- データの取得 ---
def load_data():
    try:
        response = conn.table("travel_logs").select("*").execute()
        return response.data
    except:
        return []

logs = load_data()
visited_prefs = list(set([log["prefecture"] for log in logs]))

st.title("🗾 日本旅行思い出マップ")

# --- サイドバー：入力 ---
with st.sidebar:
    st.header("✈️ 旅行を記録")
    with st.form("add_form", clear_on_submit=True):
        pref = st.selectbox("都道府県", PREFECTURES)
        v_date = st.date_input("日付", date.today())
        comm = st.text_area("思い出（食べたものなど）")
        img_url = st.text_input("画像URL (任意)")
        if st.form_submit_button("保存"):
            conn.table("travel_logs").insert({
                "prefecture": pref, "visit_date": str(v_date), "comment": comm, "image_url": img_url
            }).execute()
            st.rerun()

# --- メインレイアウト ---
col_map, col_info = st.columns([1, 1])

with col_map:
    st.subheader("🗺️ 訪問状況")
    
    # 簡易的なタイルマップ形式（地図の代わり）
    # 都道府県をボタンや色付きボックスで表示
    cols = st.columns(6) # 6列で並べる
    for i, p in enumerate(PREFECTURES):
        color = "blue" if p in visited_prefs else "gray"
        icon = "✅" if p in visited_prefs else "⬜"
        with cols[i % 6]:
            if st.button(f"{icon} {p}", key=f"btn_{p}"):
                st.session_state.selected_pref = p

    st.info(f"制覇状況: {len(visited_prefs)} / 47")

with col_info:
    # 絞り込み表示
    selected = st.session_state.get("selected_pref", "(全て表示)")
    st.subheader(f"📸 {selected} の思い出")
    
    if st.button("絞り込みを解除"):
        st.session_state.selected_pref = "(全て表示)"
        st.rerun()

    display_logs = logs if selected == "(全て表示)" else [l for l in logs if l["prefecture"] == selected]
    
    if not display_logs:
        st.write("記録がありません。")
    else:
        for l in reversed(display_logs):
            with st.container(border=True):
                st.write(f"**{l['prefecture']}** ({l['visit_date']})")
                if l.get("image_url"):
                    st.image(l["image_url"], use_container_width=True)
                st.write(l["comment"])
