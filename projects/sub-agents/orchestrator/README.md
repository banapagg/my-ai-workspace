# Orchestrator（オーケストレーター）

## 役割

複雑なタスクを分析し、適切なワーカーエージェントに委譲する中央エージェント。

## 責任

- **タスク分析**: ユーザーのタスクを理解し、必要なサブタスクに分割
- **ワーカー選択**: 各サブタスクに最適なワーカーを選択
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
  "max_workers": 3
}
```

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

```python
# orchestrator.py の実装例（疑似コード）

class Orchestrator:
    def __init__(self, config):
        self.config = config
        self.workers = self.load_workers()

    def process_task(self, task):
        # 1. タスク分析
        subtasks = self.analyze_task(task)

        # 2. 実行計画
        plan = self.create_execution_plan(subtasks)

        # 3. 実行
        results = self.execute_plan(plan)

        # 4. 統合
        final_result = self.integrate_results(results)

        return final_result

    def analyze_task(self, task):
        # タスクをサブタスクに分割
        pass

    def create_execution_plan(self, subtasks):
        # 実行順序を決定
        pass

    def execute_plan(self, plan):
        # ワーカーにタスクを委譲
        pass

    def integrate_results(self, results):
        # 結果を統合
        pass
```

## 次のステップ

- [ ] `orchestrator.py` の実装
- [ ] `config.json` の作成
- [ ] ワーカーとの連携テスト
- [ ] エラーハンドリングの追加
- [ ] 並列処理の最適化
