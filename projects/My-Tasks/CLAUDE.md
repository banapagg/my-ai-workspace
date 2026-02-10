# My-Tasks タスク管理システム

このリポジトリは Claude Code からタスクを管理するためのシステムです。
GitHub Issues + GitHub Projects (カンバンボード) を使い、自然言語でタスクの作成・管理・分析を行います。

---

## 基本方針

### 確認不要・即時実行

**ユーザーがタスクに関する指示を出した場合、確認を求めずに即座に実行すること。**

- 「追加しますか?」「よろしいですか?」などの確認は **一切不要**
- 指示を受けたら即座に gh コマンドを実行し、結果を報告する
- タスクのタイトルや本文はユーザーの入力から推測・展開して充実させる
- 迷ったらデフォルト値で作成する (優先度なし → `priority:medium`、タイプなし → `type:task`)

---

## ドキュメント一覧

My-Tasks の詳細な操作方法は、以下のドキュメントを参照してください:

### 📋 [metadata.md](./docs/metadata.md)
- リポジトリ情報、Project ID
- Status フィールド、期日フィールド
- ラベル体系
- gh コマンド実行ルール

### ➕ [task-creation.md](./docs/task-creation.md)
- タスク作成の詳細手順
- キーワード自動検出
- Issue 本文テンプレート
- 作成フロー

### 🔧 [task-management.md](./docs/task-management.md)
- タスク一覧表示
- ボード表示 (カンバン)
- ステータス変更
- 期日の設定・変更
- ラベル変更

### 📊 [task-analysis.md](./docs/task-analysis.md)
- 急ぎのタスク分析
- マージできるタスクの分析

### 🔀 [task-merge.md](./docs/task-merge.md)
- タスクのマージ (統合) 手順
- 統合後の本文テンプレート

### 💬 [natural-language.md](./docs/natural-language.md)
- 日付の解釈ルール
- 自然言語マッピング一覧

---

## クイックリファレンス

### よく使うコマンド

| 操作 | コマンド |
|---|---|
| タスク作成 | ユーザーの入力から自動的に Issue 作成 + Project 追加 |
| タスク一覧 | `gh issue list --repo banapagg/My-Tasks --state open` |
| ボード表示 | `gh project item-list 1 --owner banapagg --format json` |
| ステータス変更 | Project アイテムのステータスフィールドを更新 |
| 急ぎ分析 | ラベルと期日から優先タスクを分析 |
| マージ分析 | タイトル・ラベル・本文から類似タスクを検出 |

詳細は各ドキュメントを参照してください。
