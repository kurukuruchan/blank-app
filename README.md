🗾 日本旅行思い出マップ

日本全国47都道府県の旅行記録を管理・可視化するWebアプリケーションです。

Streamlitをフロントエンド、Supabaseをバックエンドのデータベースとして活用し、アプリを閉じてもデータが永続的に保存される仕組みを構築しています。
🌟 主な機能

    旅行記録の保存（永続化）

        行った都道府県、日付、思い出（コメント）、写真のURLを入力して保存できます。

        データはクラウド上のSupabase（PostgreSQL）に保存されるため、アプリの再起動や休止にかかわらず、あなたの思い出が消えることはありません。

    訪問状況の可視化（タイルマップ）

        47都道府県がボタン形式で並んでおり、訪問済みの県には自動的に「✅」マークが付与されます。

        日本制覇の進捗率をプログレスバーでリアルタイムに確認できます。

    都道府県別の絞り込み表示

        マップ上の各県ボタンをクリックすることで、その都道府県に関連する思い出だけを即座にフィルタリングして表示します。

    写真付きタイムライン

        保存された記録を、写真付きで時系列（最新順）に振り返ることができます。

🛠 使用技術

    Frontend: Streamlit

    Backend/Database: Supabase (PostgreSQL)

    Language: Python 3.x

    Library: st-supabase-connection

🚀 セットアップ方法
1. データベースの準備

SupabaseのSQL Editorで以下のテーブルを作成してください。
SQL

create table travel_logs (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  prefecture text not null,
  visit_date date not null,
  comment text,
  image_url text
);

2. Streamlit Secretsの設定

Streamlit Community Cloudの管理画面で以下の情報を登録してください。
Ini, TOML

SUPABASE_URL = "あなたのSupabase Project URL"
SUPABASE_KEY = "あなたのSupabase Anon Key"

💡 アプリの動作イメージ

    記録する: サイドバーに旅行の情報を入力。

    反映される: 保存ボタンを押すと、即座にメイン画面のマップに✅がつき、リストが更新されます。

    振り返る: 県別のボタンを押して、過去の自分が行った場所の思い出に浸ります。
