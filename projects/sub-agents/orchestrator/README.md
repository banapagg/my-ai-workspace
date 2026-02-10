# Orchestrator（オーケストレーター）

## 役割

複雑なタスクを分析し、適切なワーカーエージェントに委譲する中央エージェント。

## 責任

- **タスク分析**: ユーザーのタスクを理解し、必要なサブタスクに分割
- **ワーカー選択**: 各サブタスクに最適なワーカーを選択
- **モデル選択**: タスクの複雑さに応じて適切なモデル（haiku/sonnet/opus）を選択
- **実行調整**: ワーカーの実行順序を決定（並列 or 順次）
- **結果統合**: 各ワーカーの結果を統合し、最終結果を生成

## 動作フロー

```
1. タスク受信
   - ユーザーからのタスク要求を受け取る
   - タスクの複雑度を評価

2. タスク分析
   - 必要なサブタスクを洗い出す
   - 各サブタスクの依存関係を特定

3. ワーカー選択
   - 利用可能なワーカーを確認
   - 各サブタスクに最適なワーカーを割り当て

4. 実行計画
   - 実行順序を決定（並列処理可能なものは並列化）
   - 各ワーカーへの入力を準備

5. 実行
   - ワーカーにタスクを委譲
   - 進捗を監視

6. 結果統合
   - 各ワーカーの結果を収集
   - 必要に応じて追加のワーカーを起動（例: レビュー結果に基づく修正）
   - 最終結果を生成

7. 報告
   - ユーザーに結果を報告
   - 実行ログを記録
```

## 設定（config.json）

```json
{
  "workers": {
    "code_writer": {
      "enabled": true,
      "description": "コード生成を担当",
      "skills": ["coding", "architecture"]
    },
    "presentation_builder": {
      "enabled": true,
      "description": "プレゼン資料の作成を担当",
      "skills": ["presentation-design"]
    },
    "document_writer": {
      "enabled": true,
      "description": "Word/PDF文書の作成を担当",
      "skills": ["document-formatting", "business-writing"]
    },
    "code_reviewer": {
      "enabled": true,
      "description": "コードレビューを担当",
      "skills": ["review", "best-practices"]
    },
    "tester": {
      "enabled": true,
      "description": "テスト実行を担当",
      "skills": ["testing", "debugging"]
    }
  },
  "execution_mode": "auto",
  "parallel_execution": true,
  "max_workers": 3,
  "default_model": "sonnet"
}
```

## モデル選択

オーケストレーターは、タスクの複雑さに応じて適切なモデルを自動選択します。

### モデルの種類

| モデル | 特徴 | 用途 |
|---|---|---|
| **haiku** | 最速・最安 | 軽量タスク |
| **sonnet** | バランス型 | 標準タスク |
| **opus** | 最高性能 | 複雑なタスク |

### タスクタイプとモデルのマッピング

```python
# 軽量・高速タスク → haiku
"suggest_structure"  # 構成提案
"format_content"     # フォーマット提案
"quick_review"       # 簡易レビュー

# 標準タスク → sonnet (デフォルト)
"create_document"       # 文書生成
"create_presentation"   # プレゼン生成
"review"               # レビュー
"code_writing"         # コード生成
"code_review"          # コードレビュー
"testing"              # テスト実行

# 複雑なタスク → opus
"complex_analysis"        # 複雑な分析
"architectural_design"    # アーキテクチャ設計
"comprehensive_review"    # 包括的レビュー
```

### 判断基準

オーケストレーターは以下のキーワードからタスクの複雑さを判断します:

- **haiku**: 「構成」「提案」「アイデア」（準備段階の軽量タスク）
- **sonnet**: 「作成」「実装」「レビュー」（標準的な実行タスク）
- **opus**: 「詳細」「包括」「徹底」（高度な分析・設計タスク）

デフォルトは **sonnet** です。

## 実装のポイント

### タスク分割の判断
- タスクが単純 → 直接実行
- タスクが複雑 → ワーカーに委譲
- 基準: 複数の専門知識が必要か、独立したサブタスクに分割可能か

### エラーハンドリング
- ワーカーが失敗した場合の再試行ロジック
- 依存関係のあるタスクの中断処理
- エラーメッセージの集約と報告

### 最適化
- 並列実行可能なタスクの検出
- ワーカーの負荷分散
- キャッシュの活用（同じタスクの重複実行を避ける）

## 使用例

### 基本的な使い方

```python
from orchestrator import Orchestrator

# オーケストレーターを初期化
orchestrator = Orchestrator()

# タスクを実行
result = orchestrator.process_task("プレゼンの構成を提案してください")

# 結果を確認
print(result['summary'])
```

### モデル選択の例

```python
# 軽量タスク（haiku使用）
task1 = "プレゼンの構成を提案してください"
result1 = orchestrator.process_task(task1)
# → presentation_builder (haiku)

# 標準タスク（sonnet使用）
task2 = "報告書を作成してください"
result2 = orchestrator.process_task(task2)
# → document_writer (sonnet)

# 複雑なタスク（opus使用）
task3 = "詳細なコードレビューをしてください"
result3 = orchestrator.process_task(task3)
# → code_reviewer (opus)
```

### 実行ログの例

```
============================================================
🎯 オーケストレーター起動
============================================================

📋 タスク分析中: プレゼンの構成を提案してください
   タスク: suggest_structure -> モデル: haiku

📝 実行計画を作成中...
   ステップ 1: presentation_builder (haiku) - プレゼン資料を作成する

🚀 実行中...
   ステップ 1: presentation_builder (haiku) を実行中...
   ✅ presentation_builder (haiku) 完了

📊 結果を統合中...

=== 実行結果サマリー ===
✅ ステップ 1: [presentation_builder] タスク 'プレゼン資料を作成する' を完了しました

============================================================
✨ 完了
============================================================
```

## 実装済み機能

- [x] `orchestrator.py` の基本実装
- [x] モデル選択ロジック（haiku/sonnet/opus）
- [x] タスクタイプの自動判定
- [x] ワーカー設定のデフォルト値
- [x] 実行ログの表示

## 次のステップ

- [ ] 実際のワーカーとの連携実装
- [ ] `config.json` の作成（現在はデフォルト値使用）
- [ ] エラーハンドリングの強化
- [ ] 並列処理の最適化
- [ ] モデル選択ロジックの動的調整（コンテキスト量ベース）
