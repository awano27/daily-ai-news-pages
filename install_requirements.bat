@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 📦 Gemini URL Context システム用パッケージインストール中...

echo.
echo 🔧 既存の問題のあるパッケージをクリーンアップ...
pip uninstall -y google-generativeai google-genai deep-translator

echo.
echo 📥 必要なパッケージを順次インストール...
pip install --upgrade pip

echo 🤖 Gemini関連パッケージ...
pip install google-genai

echo 🌐 翻訳・テキスト処理パッケージ...
pip install "deep-translator>=1.11.4"
pip install feedparser
pip install "requests>=2.31.0"
pip install pyyaml
pip install "python-dotenv>=1.0.0"

echo 🔍 スクレイピング・解析パッケージ...
pip install "beautifulsoup4>=4.12.0"
pip install "lxml>=4.9.0" 
pip install "html2text>=2020.1.16"

echo 🧪 テスト・開発パッケージ...
pip install "pytest>=7.4.0"
pip install "jsonschema>=4.17.0"

echo 📊 その他のオプションパッケージ...
pip install "redis>=5.0.0"
pip install "selenium>=4.15.0"
pip install "playwright>=1.40.0"

echo.
echo ✅ パッケージインストール完了！
echo.
echo 📋 次のステップ:
echo 1. .envファイルを作成し、GEMINI_API_KEYを設定
echo 2. python test_integration.py でテスト実行
echo 3. python enhanced_build.py で強化版ビルド実行

pause