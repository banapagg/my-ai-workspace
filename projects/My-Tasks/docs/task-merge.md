# タスクのマージ (統合)

## これとこれマージして (Merge Execution)

ユーザーが「#X と #Y をマージして」「#X と #Y を統合して」「#X と #Y をまとめて」等と指示した場合、
以下の手順でタスクを統合する。**確認不要で即時実行する。**

## 手順

```bash
# Step 1: 各 Issue の詳細を取得
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue view <N> --repo banapagg/My-Tasks --json number,title,body,labels

# Step 2: 統合先 Issue を決定
# - デフォルト: 最も番号が小さい Issue
# - ユーザーが指定した場合はその Issue

# Step 3: 統合先 Issue の本文を更新
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue edit <SURVIVING_N> \
  --title "統合後のタイトル" \
  --body "統合後の本文" \
  --repo banapagg/My-Tasks

# Step 4: 全ラベルを統合先に集約
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue edit <SURVIVING_N> \
  --add-label "label1,label2" \
  --repo banapagg/My-Tasks

# Step 5: 重複 Issue にコメントを追加してクローズ
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue comment <DUP_N> \
  --body "🔀 このタスクは #<SURVIVING_N> に統合されました。" \
  --repo banapagg/My-Tasks

export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue close <DUP_N> --repo banapagg/My-Tasks
```

## 統合後の本文テンプレート

```markdown
## 概要
（統合されたタスクの概要を新たに書く）

## 統合元タスク
- #X: 元のタイトル
- #Y: 元のタイトル

## 詳細
（各タスクの内容を整理・統合して記述する。単純なコピペではなく、重複を排除して整理する）

### 元 #X の内容
（元の本文を要約して保持）

### 元 #Y の内容
（元の本文を要約して保持）

## 完了条件
- [ ] （両方のタスクの完了条件を統合）
```

## マージ後の報告

```
🔀 タスクを統合しました
- 統合先: #X「統合後タイトル」
- 統合元: #Y「元タイトル」（クローズ済み）
- ラベル: （統合後のラベル一覧）
- URL: https://github.com/banapagg/My-Tasks/issues/X
```
