#!/bin/bash

# my-ai-workspace セットアップスクリプト

echo "🚀 my-ai-workspace のセットアップを開始します..."

# 1. 環境変数の確認
echo "📋 環境変数をチェック中..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env ファイルが見つかりません"
    echo "   必要に応じて .env ファイルを作成してください"
fi

# 2. プロジェクトごとの .env.example を確認
echo "📂 プロジェクトの環境変数テンプレートを確認中..."
for project in projects/*/; do
    if [ -f "$project.env.example" ]; then
        project_name=$(basename "$project")
        echo "   ✓ $project_name: .env.example が存在します"
        if [ ! -f "$project.env" ]; then
            echo "     → $project.env を作成することを推奨します"
        fi
    fi
done

# 3. Git の初期化確認
if [ ! -d ".git" ]; then
    echo "📦 Git リポジトリを初期化中..."
    git init
    echo "   ✓ Git リポジトリを初期化しました"
else
    echo "✓ Git リポジトリは既に初期化されています"
fi

# 4. リモートリポジトリの設定確認
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  Git リモートリポジトリが設定されていません"
    echo "   以下のコマンドでリモートを追加してください:"
    echo "   git remote add origin <リポジトリURL>"
else
    echo "✓ Git リモートリポジトリ: $(git remote get-url origin)"
fi

echo ""
echo "✅ セットアップが完了しました！"
echo ""
echo "📖 使い方:"
echo "   プロジェクトで作業: cd projects/<プロジェクト名> && claude"
echo "   Git同期: git add . && git commit -m \"message\" && git push"
