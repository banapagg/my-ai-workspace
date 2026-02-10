# タスク管理の基本操作

## タスク一覧表示
```bash
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue list --repo banapagg/My-Tasks --state open
```

## ボード表示（カンバン）
```bash
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh project item-list 1 --owner banapagg --format json
```
→ JSON の結果を、ステータスごとにグループ化して見やすく表示する:
```
📋 Todo:
  - #N: タスク名 (期日: YYYY-MM-DD)

🔄 In Progress:
  - #N: タスク名

⏸️ Pending:
  - #N: タスク名

✅ Done:
  - #N: タスク名
```

## ステータス変更

```bash
# まず Item ID を取得
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh project item-list 1 --owner banapagg --format json

# ステータスを変更（オプション ID を対応するものに変更）
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh project item-edit \
  --project-id PVT_kwHOBIcCGs4BOrhY \
  --id <Item ID> \
  --field-id PVTSSF_lAHOBIcCGs4BOrhYzg9T10o \
  --single-select-option-id <Option ID>
```

- 「#N を進行中に」→ Option ID: `47fc9ee4`
- 「#N を保留に」→ Option ID: `1ea3cfe9`
- 「#N を完了」→ Issue をクローズ + Option ID: `98236657`

```bash
# 完了の場合は Issue もクローズ
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue close <N> --repo banapagg/My-Tasks
```

## 期日の設定・変更

```bash
# まず Item ID を取得してから
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh project item-edit \
  --project-id PVT_kwHOBIcCGs4BOrhY \
  --id <Item ID> \
  --field-id PVTF_lAHOBIcCGs4BOrhYzg9Vv3k \
  --date "YYYY-MM-DD"
```

## ラベル変更

```bash
# ラベル追加
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue edit <N> --add-label "priority:high" --repo banapagg/My-Tasks

# ラベル削除
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue edit <N> --remove-label "priority:medium" --repo banapagg/My-Tasks
```
