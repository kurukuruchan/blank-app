import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import date

# ページ設定
st.set_page_config(page_title="日本旅行思い出ログ Pro", layout="wide", page_icon="🗾")

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

st.title("🗾 日本旅行思い出ログ Pro")
st.markdown("Supabaseに保存されるため、アプリが休止しても記録は消えません。")

# --- データの取得 (キャッシュなしで最新を取得) ---
def load_data():
    try:
        response = conn.table("travel_logs").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"データの読み込みに失敗しました: {e}")
        return []

logs = load_data()

# --- サイドバー：新規登録 ---
with st.sidebar:
    st.header("✈️ 旅行を記録")
    with st.form("travel_form", clear_on_submit=True):
        pref = st.selectbox("行った都道府県", PREFECTURES)
        travel_date = st.date_input("日付", date.today())
        comment = st.text_area("思い出（食べたもの、行った場所など）")
        img_url = st.text_input("写真のURL (GoogleフォトやWeb上の画像リンク)")
        
        submitted = st.form_submit_button("Supabaseに保存")
        if submitted:
            new_log = {
                "prefecture": pref,
                "visit_date": str(travel_date),
                "comment": comment,
                "image_url": img_url
            }
            conn.table("travel_logs").insert(new_log).execute()
            st.success(f"{pref} の記録を保存しました！")
            st.rerun()

# --- メインエリアの構成 ---
# 1. 統計情報の表示
visited_prefs = list(set([log["prefecture"] for log in logs]))
col1, col2, col3 = st.columns(3)
col1.metric("訪れた都道府県数", f"{len(visited_prefs)} / 47")
col2.metric("総旅行回数", f"{len(logs)} 回")
col3.progress(len(visited_prefs) / 47, text="日本制覇の進捗")

# 2. 地図ライクなリスト表示とフィルタリング
tab_map, tab_history = st.tabs(["📍 場所から振り返る", "📜 全履歴"])

with tab_map:
    target_pref = st.selectbox("表示する都道府県を選択", ["(未選択)"] + PREFECTURES)
    
    if target_pref != "(未選択)":
        filtered_logs = [l for l in logs if l["prefecture"] == target_pref]
        if not filtered_logs:
            st.warning(f"{target_pref} の記録はまだありません。")
        else:
            for log in reversed(filtered_logs):
                with st.container(border=True):
                    st.subheader(f"📅 {log['visit_date']}")
                    if log["image_url"]:
                        st.image(log["image_url"], caption=f"{target_pref}での一枚", use_container_width=True)
                    st.write(log["comment"])

with tab_history:
    if not logs:
        st.info("まだ記録がありません。サイドバーから登録してください。")
    else:
        # 表形式で全データを表示
        st.dataframe(logs, use_container_width=True)

# 3. おまけ：訪問済みの県をテキストで一覧表示
st.divider()
st.subheader("🏁 訪問済みリスト")
st.write(", ".join(visited_prefs) if visited_prefs else "まだありません")
