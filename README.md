旅行思い出マップ

都道府県ごとに旅行の思い出を記録し、日本地図（タイル形式）で訪問状況を可視化するアプリケーションです。
概要

このアプリは、ユーザーが訪れた都道府県を記録し、その思い出（コメントや写真）を保存・閲覧できるツールです。データベースに Supabase を利用しているため、Streamlit Cloudのアプリが休止しても、記録したデータは永続的に保持されます。
デモ

(※GitHubに画像をアップロードして、このパスを書き換えることで実際の画像を表示できます)
特徴

    訪問状況の可視化: 47都道府県がタイル形式で並び、訪問済みの県には自動的に ✅ マークが付きます。

    データの永続化: クラウドDB（Supabase）との連携により、ブラウザを閉じてもデータが消えません。

    写真付きログ: 旅行の思い出をテキストだけでなく、画像URLを指定して保存できます。

    フィルタリング機能: マップ上のボタンをクリックすることで、特定の都道府県の思い出だけを抽出して表示できます。

使い方

    記録の追加: サイドバーの入力フォームから、「都道府県」「日付」「思い出」「画像URL」を入力し、「データベースに保存」ボタンを押します。

    状況の確認: メイン画面の「訪問状況」セクションで、現在の制覇率と訪問済み都道府県を確認します。

    思い出の表示: 都道府県ボタンをクリックすると、その県の過去の記録が右側のフィードに表示されます。

実行方法
必要なライブラリ

以下のライブラリを requirements.txt に記述してインストールしてください。

    streamlit

    st-supabase-connection

設定（Secrets）

Streamlit Cloudの Secrets またはローカルの .streamlit/secrets.toml に以下の情報を設定してください。
Ini, TOML

SUPABASE_URL = "あなたのSupabase Project URL"
SUPABASE_KEY = "あなたのSupabase Anon Key"

データベース構築

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

開発環境

    Python 3.11

    Streamlit

    Supabase (PostgreSQL)
