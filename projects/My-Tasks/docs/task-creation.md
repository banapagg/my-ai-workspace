# タスク作成

ユーザーがタスクに関するテキストを入力したら、以下の手順で **即座に** Issue を作成する。

## キーワード自動検出

ユーザーの入力から以下のキーワードを検出し、自動的にラベルと期日を設定する:

| キーワード | 自動設定 |
|---|---|
| 急ぎ / 至急 / ASAP / 重要 / 緊急 | `priority:high` |
| バグ / 不具合 / エラー / 壊れ | `type:bug` |
| アイデア / 案 / 提案 / 思いつき | `type:idea` |
| 〜までに / 期限 / 締切 / デッドライン | 期日フィールドに日付を設定 |
| 今日中 | 期日=当日 + `priority:high` |

キーワードがない場合のデフォルト: `priority:medium` + `type:task`

## Issue 本文テンプレート

Issue の本文は以下のテンプレートに従い、ユーザーの入力からできるだけ詳しく書く。
短い入力でも、文脈や常識から推測して説明を充実させること。

```markdown
## 概要
（タスクの目的を1〜2文で簡潔に）

## 詳細
（ユーザーの入力を展開した詳細な説明。何をするか、なぜ必要か、どのように進めるかなど）

## 背景・メモ
- 関連する情報やリンクがあれば記載
- 期日がある場合: 期日 YYYY-MM-DD
- その他の補足事項

## 完了条件
- [ ] 具体的に何をもって完了とするか
- [ ] 必要なアクションをチェックリスト形式で
```

## 作成フロー (全ステップを連続実行)

```bash
# Step 1: Issue 作成（リッチな説明文 + ラベル付き）
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue create \
  --title "タスク名" \
  --body "## 概要
タスクの概要

## 詳細
詳細な説明

## 背景・メモ
- 補足情報

## 完了条件
- [ ] 完了条件1" \
  --label "priority:medium,type:task" \
  --repo banapagg/My-Tasks

# Step 2: 作成した Issue を Project に追加（--format json で Item ID を取得）
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh project item-add 1 --owner banapagg --url <Issue URL> --format json

# Step 3: ステータスを "Todo" に設定
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh project item-edit \
  --project-id PVT_kwHOBIcCGs4BOrhY \
  --id <Item ID> \
  --field-id PVTSSF_lAHOBIcCGs4BOrhYzg9T10o \
  --single-select-option-id f75ad846

# Step 4: 期日がある場合、期日を設定
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh project item-edit \
  --project-id PVT_kwHOBIcCGs4BOrhY \
  --id <Item ID> \
  --field-id PVTF_lAHOBIcCGs4BOrhYzg9Vv3k \
  --date "YYYY-MM-DD"
```

**Item ID の取得方法**: Step 2 の `--format json` の出力から `id` フィールドを取得する。

## 作成後の報告

タスク作成後、以下の形式で報告する:

```
✅ タスクを作成しました
- Issue: #N「タスク名」
- ラベル: priority:medium, type:task
- ステータス: Todo
- 期日: YYYY-MM-DD（設定した場合）
- URL: https://github.com/banapagg/My-Tasks/issues/N
```
