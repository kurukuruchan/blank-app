import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import date
from streamlit_japan_map import map_japan # 新しくインポート

# ページ設定
st.set_set_page_config(page_title="日本旅行思い出マップ", layout="wide", page_icon="🗾")

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

st.title("🗾 日本旅行思い出マップ (Supabase永続版)")
st.markdown("Supabaseに保存されるため、アプリが休止しても記録は消えません。")

# --- データの取得 (キャッシュなしで最新を取得) ---
def load_data():
    try:
        response = conn.table("travel_logs").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"データの読み込みに失敗しました。テーブルが作成されているか、Secretsが正しいか確認してください: {e}")
        return []

logs = load_data()
visited_prefs = list(set([log["prefecture"] for log in logs]))

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
col_map, col_detail = st.columns([1.5, 1])

with col_map:
    st.subheader("🗺️ 訪問状況")
    
    # 訪問済みの都道府県に色を付けるための辞書を作成
    # 訪問済みは濃い青、未訪問は薄いグレー
    colors = {pref: "#1f77b4" if pref in visited_prefs else "#cccccc" for pref in PREFECTURES}
    
    # streamlit-japan-map を使って日本地図を描画
    # クリックされた都道府県を受け取る
    clicked_pref = map_japan(colors=colors, width=500) # widthで地図のサイズを調整
    
    st.info(f"現在、**{len(visited_prefs)} / 47** 都道府県を制覇しています！")

with col_detail:
    st.subheader("📸 思い出フィード")

    # 地図がクリックされたら、その都道府県で絞り込む
    # クリックされていない場合は全てのオプションを表示
    current_selection = clicked_pref if clicked_pref else "(全て表示)"
    
    # セレクトボックスのデフォルト値を、クリックされた都道府県に設定
    target_pref_options = ["(全て表示)"] + PREFECTURES
    selected_index = 0
    if current_selection in target_pref_options:
        selected_index = target_pref_options.index(current_selection)

    target_pref_display = st.selectbox(
        "都道府県で絞り込む", 
        options=target_pref_options, 
        index=selected_index,
        key="pref_filter_selectbox" # キーを追加してwidgetの警告を回避
    )
    
    # 絞り込みロジック
    if target_pref_display == "(全て表示)":
        display_logs = logs
        st.caption("全ての旅行記録を表示しています。")
    else:
        display_logs = [l for l in logs if l["prefecture"] == target_pref_display]
        st.caption(f"{target_pref_display} の旅行記録を表示しています。")

    if not display_logs:
        st.warning(f"{target_pref_display} の記録はまだありません。")
    else:
        # 最新の記録から表示
        for log in reversed(display_logs):
            with st.container(border=True):
                st.write(f"**{log['prefecture']}** - 📅 {log['visit_date']}")
                if log["image_url"]:
                    st.image(log["image_url"], caption="思い出の写真", use_container_width=True)
                st.write(log["comment"])
