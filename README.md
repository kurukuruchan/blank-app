<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Supabase-3EC988?style=for-the-badge&logo=Supabase&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white" />
</p>

<h1 align="center">🗾 日本旅行思い出マップ</h1>

<p align="center">
  <b>都道府県ごとの旅行記録を保存し、自分だけの「日本制覇地図」を作るWebアプリ</b>
</p>

<hr>

## 📝 概要
本アプリケーションは、日本国内の旅行の思い出を都道府県ごとに記録・管理できるツールです。
最大の特徴は、バックエンドに <b>Supabase (PostgreSQL)</b> を採用している点です。これにより、従来の簡易データベース（SQLite3等）とは異なり、サーバーが休止してもデータが失われない<b>完全な永続化</b>を実現しています。


## ✨ 主な機能
<ul>
  <li><b>ビジュアル進捗管理</b>：タイル形式のマップにより、訪問済みの県が一目でわかります。</li>
  <li><b>クラウド保存</b>：Supabase連携により、PCやスマホなど異なるデバイスからでも同じデータにアクセス可能です。</li>
  <li><b>クイックフィルタ</b>：地図上の県名ボタンを押すだけで、特定の地域の思い出を瞬時に抽出できます。</li>
  <li><b>写真ログ</b>：思い出のコメントと共に、WEB上の写真URLを紐づけて保存できます。</li>
</ul>

<br>
<p align="center">
  <a href="https://blank-app-7vq2io2174g.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/🚀%20アプリを今すぐ試す-Open%20App-blue?style=for-the-badge&logo=streamlit" alt="Open App" />
  </a>
</p>

<p align="center">
  <a href="https://blank-app-7vq2io2174g.streamlit.app/">https://blank-app-7vq2io2174g.streamlit.app/#db
</p>

<hr>

## 🚀 使い方
<ol>
  <li><b>思い出を登録する</b>：サイドバーから「都道府県」「日付」「コメント」「画像URL」を入力し保存します。</li>
  <li><b>地図を埋める</b>：訪問した都道府県には自動的に ✅ マークが付き、制覇率がカウントアップされます。</li>
  <li><b>振り返る</b>：都道府県ボタンをクリックして、過去の旅行記を閲覧します。</li>
</ol>

<br>

## 🛠 実行環境・設定

###　使用技術
| カテゴリ | 技術 |
| :--- | :--- |
| **Language** | Python 3.11 |
| **Frontend** | Streamlit |
| **Database** | Supabase (PostgreSQL) |

