# タスク分析機能

## 急ぎのタスクは？ (Urgent Query)

ユーザーが「急ぎのタスクは？」「優先タスクは？」「何が急ぎ？」「今やるべきことは？」等と聞いた場合、
以下の手順で優先度・期日を分析して報告する。

### 手順

```bash
# Step 1: オープン Issue をラベル付きで取得
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue list --repo banapagg/My-Tasks --state open --json number,title,labels,createdAt

# Step 2: Project アイテム一覧を取得（期日情報含む）
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh project item-list 1 --owner banapagg --format json
```

### 分析ロジック

1. Issue 番号をキーにして、ラベル情報と Project の期日情報をクロス参照する
2. 以下の優先順で並び替え:
   - 期日超過 (overdue) のタスク → 最優先
   - `priority:high` ラベル付き → 高優先
   - 期日が7日以内のタスク → 期限間近
   - `priority:medium` ラベル付き → 中優先
   - それ以外 → 通常

### 表示フォーマット

```
### 🔴 緊急（期日超過）
- #N: タスク名 (期日: YYYY-MM-DD, ⚠️ X日超過)

### 🟠 高優先度（priority:high）
- #N: タスク名 (期日: YYYY-MM-DD / 期日なし)

### ⏰ 期日が近いタスク（7日以内）
- #N: タスク名 (期日: YYYY-MM-DD, 残りX日)

### 🟡 中優先度（priority:medium）
- #N: タスク名

### その他
- #N: タスク名
```

該当タスクがないカテゴリは表示しない。
すべてのタスクが完了済みの場合は「現在オープンなタスクはありません 🎉」と表示する。

---

## マージできるタスクは？ (Merge Analysis)

ユーザーが「マージできるタスクは？」「重複タスクある？」「似たタスクは？」「整理できるタスクは？」等と聞いた場合、
以下の手順で類似タスクを分析して報告する。

### 手順

```bash
# すべてのオープン Issue の詳細を取得
export PATH="/c/Program Files/GitHub CLI:$PATH" && gh issue list --repo banapagg/My-Tasks --state open --json number,title,body,labels
```

### 分析ロジック

Claude が以下の3つの観点で類似性を分析する:

1. **タイトルの類似度**: 同じキーワードや似た表現が含まれているか
2. **ラベルの重複**: 同じ type / priority ラベルを持っているか
3. **本文の内容**: 同じ目的・ゴール・作業内容を含んでいるか

マージ候補の基準:
- 同じ目的を持つが、粒度や表現が異なるタスク
- 一方がもう一方の部分タスクになっているもの
- 重複した作業内容を含むタスク

### 表示フォーマット

```
### マージ候補グループ

**グループ 1**: #X 「タスクA」 と #Y 「タスクB」
- 📝 類似点: （具体的に何が似ているかを説明）
- 💡 提案: #X に統合することを推奨（理由: #X の方が詳細な説明を含むため）

**グループ 2**: #A 「タスクC」 と #B 「タスクD」 と #C 「タスクE」
- 📝 類似点: （説明）
- 💡 提案: （どれに統合するか + 理由）
```

マージ候補がない場合: 「現在マージ可能なタスクの候補はありません。すべてのタスクが独立した内容です。」
