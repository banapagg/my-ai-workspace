# my-ai-workspace

AI エージェント開発のための統合ワークスペース

## 構造

```
my-ai-workspace/
├── CLAUDE.md              # グローバルCLAUDE.md（全プロジェクト共通の基本ルール）
├── .gitignore
├── setup.sh               # 環境復元用スクリプト
├── global_mcp/            # 全エージェント共通の自作MCPツール
│   ├── browser-tool/
│   └── file-search/
├── projects/              # プロジェクト（案件）ごとのディレクトリ
│   ├── My-Tasks/          # タスク管理システム
│   │   ├── CLAUDE.md      # プロジェクト固有のルール
│   │   └── docs/          # 詳細ドキュメント
│   ├── project_A/
│   │   ├── .env.example
│   │   └── mcp_config.json
│   └── project_B/
└── templates/             # 設定テンプレート
    └── base_config.json
```

## 使い方

### プロジェクトで作業する場合

```bash
cd my-ai-workspace/projects/My-Tasks
claude
```

→ グローバルCLAUDE.md + My-Tasks/CLAUDE.md が適用される

### 新しいプロジェクトを作成

```bash
cd my-ai-workspace/projects
mkdir new-project
cp ../templates/base_config.json new-project/mcp_config.json
# 必要に応じて CLAUDE.md を作成
```

## ルール

- **グローバルCLAUDE.md**: 全プロジェクト共通の基本ルール（対話スタイル、コーディング規約など）
- **プロジェクト固有のCLAUDE.md**: 各プロジェクトの専用ルール（自動化、特定の手順など）
- グローバルルールは常に適用され、プロジェクト固有ルールはそれに追加される
