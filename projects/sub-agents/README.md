# sub-agents

オーケストレーター・ワーカーパターンとAgent Skillsを使ったサブエージェント環境

## 概要

このプロジェクトは、複雑なタスクを複数の専門化されたエージェントに分割して処理するための基盤を提供します。

**主要コンポーネント:**
- **Orchestrator（オーケストレーター）**: タスクを分析し、適切なワーカーに委譲する中央エージェント
- **Workers（ワーカー）**: 専門タスクを実行するエージェント（コード生成、レビュー、テストなど）
- **Skills（スキル）**: 専門知識をパッケージ化し、動的に注入する仕組み

## 構造

```
sub-agents/
├── CLAUDE.md                      # プロジェクト固有のルール
├── orchestrator/                   # オーケストレーター
│   ├── orchestrator.py            # タスク分割・委譲ロジック
│   ├── config.json                # 設定
│   └── README.md                  # ドキュメント
├── workers/                        # ワーカーエージェント
│   ├── code_writer/               # コード生成
│   ├── code_reviewer/             # コードレビュー
│   └── tester/                    # テスト実行
├── skills/                         # Agent Skills
│   ├── security-review/           # セキュリティレビュー
│   ├── build-test/                # ビルドテスト
│   └── qa-check/                  # QAチェック
├── examples/                       # 使用例
│   └── simple_workflow.py
└── README.md                      # このファイル
```

## 使い方

### 1. ワーカーの追加

新しいワーカーを追加する場合:

```bash
cd workers
mkdir new_worker
cp code_writer/README.template.md new_worker/README.md
# README.mdを編集してワーカーの役割を定義
```

### 2. Skillの追加

新しいSkillを追加する場合:

```bash
cd skills
mkdir new_skill
cp security-review/SKILL.template.md new_skill/SKILL.md
# SKILL.mdを編集してスキルの内容を定義
```

### 3. ワークフローの実行

```bash
cd my-ai-workspace/projects/sub-agents
claude
# オーケストレーターがタスクを分析し、適切なワーカーに委譲します
```

## 設計思想

### オーケストレーター・ワーカーパターン

**利点:**
- タスクの動的な分割が可能
- 各ワーカーが専門化され、品質向上
- 並列処理によるパフォーマンス向上

**適用場面:**
- 予測できないサブタスクが必要な複雑なタスク
- 異なる専門知識が必要なタスク
- 段階的な処理が必要なワークフロー

### Agent Skills

**特徴:**
- Progressive Disclosure（段階的開示）で効率的
- 専門知識を再利用可能な形でパッケージ化
- コンテキストを共有しながら専門性を注入

**構成:**
1. **メタデータ**: 名前と説明（常にロード）
2. **指示**: メイン手順（トリガー時）
3. **リソース**: 追加ファイル（必要時）

## 参考資料

- [Building Effective Agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [Orchestrator-Workers Pattern - Claude Cookbooks](https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/orchestrator_workers.ipynb)
- [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)

## 開発ステータス

- [x] 基本構造の作成
- [ ] オーケストレーターの実装
- [ ] ワーカーの実装
- [ ] Skillsの実装
- [ ] 使用例の作成
