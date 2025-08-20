@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 🔧 Gemini API環境設定セットアップ

echo.
echo 📝 .envファイル作成中...

if exist ".env" (
    echo ⚠️ .envファイルが既に存在します
    echo 💾 バックアップを作成します...
    copy ".env" ".env.backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
)

echo # Gemini API設定> .env
echo GEMINI_API_KEY=>> .env
echo GEMINI_MODEL=gemini-2.5-flash>> .env
echo.>> .env
echo # Vertex AI使用時（オプション）>> .env
echo # GOOGLE_GENAI_USE_VERTEXAI=false>> .env
echo.>> .env
echo # Google Search併用（オプション）>> .env
echo # ENABLE_GOOGLE_SEARCH=false>> .env
echo.>> .env
echo # 翻訳設定>> .env
echo TRANSLATE_TO_JA=1>> .env
echo TRANSLATE_ENGINE=google>> .env
echo HOURS_LOOKBACK=24>> .env
echo MAX_ITEMS_PER_CATEGORY=8>> .env
echo.>> .env
echo # X投稿CSV（既存設定）>> .env
echo X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv^&gid=0>> .env

echo.
echo ✅ .envファイル作成完了
echo.
echo 🔑 重要: GEMINI_API_KEYを設定してください
echo.
echo 📋 GEMINI_API_KEYの取得方法:
echo 1. https://ai.google.dev/ にアクセス
echo 2. "Get API Key" をクリック  
echo 3. Google アカウントでログイン
echo 4. "Create API Key" で新しいキーを生成
echo 5. 生成されたキーを.envファイルのGEMINI_API_KEY=の後に追加
echo.
echo 📄 設定例:
echo GEMINI_API_KEY=AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q
echo.
echo 🚀 設定後は python test_integration.py でテスト実行

pause