# Presentation Builder Worker

## 役割

PPTXファイルの生成、スライド構成の提案、コンテンツの自動配置を担当するワーカー。
コンサルタント業務での提案書・プレゼン資料作成を支援します。

## 責任範囲

### できること
- **スライド構成の提案**: トピック、聴衆、時間に基づいた最適な構成を提案
- **PPTXファイルの生成**: python-pptxを使用した実際のファイル作成
- **レイアウトパターンの適用**: 7種類のレイアウトから適切なものを選択
- **コンテンツの自動配置**: タイトル、本文、箇条書きの自動レイアウト

### できないこと
- 画像の生成・編集（別途画像ファイルが必要）
- 複雑なアニメーション（基本的なスライド遷移のみ）
- デザインテンプレートの完全なカスタマイズ

## 入力

### スライド構成の提案

```json
{
  "type": "suggest_structure",
  "topic": "新規事業提案",
  "audience": "経営陣",
  "duration": 20,
  "context": {
    "company": "株式会社〇〇",
    "purpose": "意思決定"
  }
}
```

### PPTXファイルの作成

```json
{
  "type": "create_presentation",
  "topic": "新規事業提案",
  "output_path": "proposal.pptx",
  "slides": [
    {
      "layout": "title",
      "title": "新規事業提案",
      "content": "株式会社〇〇\n2025年1月"
    },
    {
      "layout": "bullet_points",
      "title": "背景",
      "bullets": [
        "市場の成長率: 年間15%",
        "競合の動向: 参入増加",
        "当社の強み: 技術力"
      ]
    }
  ]
}
```

## 出力

### スライド構成の提案

```json
{
  "status": "success",
  "worker": "presentation_builder",
  "output": {
    "topic": "新規事業提案",
    "audience": "経営陣",
    "duration": 20,
    "estimated_slides": 15,
    "structure": [
      {
        "slide_number": 1,
        "layout": "title",
        "title": "新規事業提案",
        "description": "表紙スライド",
        "notes": "会社名、発表者名、日付を含める"
      },
      ...
    ],
    "recommendations": [
      "1スライド1メッセージを心がける",
      "ビジュアル（図・グラフ）を積極的に使用"
    ]
  }
}
```

## 使用するSkills

- **presentation-design**: プレゼンデザインのベストプラクティス
- **visual-design**: ビジュアル設計の原則
- **storytelling**: ストーリーテリングの技法

## レイアウトパターン

1. **title**: タイトルスライド（表紙）
2. **section**: セクション区切り
3. **content**: 通常のコンテンツ
4. **two_column**: 2カラムレイアウト
5. **bullet_points**: 箇条書き
6. **image_caption**: 画像+説明
7. **conclusion**: まとめスライド

## 実装のポイント

### スライド数の目安
- 1分あたり1スライド（標準的なペース）
- コンサルタント向け: 1分あたり0.5-0.75スライド（詳細説明が多い場合）

### 構成の黄金比
- 導入: 10%（背景、課題）
- 本論: 60%（提案内容、根拠）
- 結論: 20%（まとめ、アクション）
- 付録: 10%（詳細データ、参考資料）

### デザイン原則
- **1スライド1メッセージ**: 伝えたいことを1つに絞る
- **7±2の法則**: 箇条書きは3-7個まで
- **余白の重要性**: 詰め込みすぎない
- **視覚的階層**: サイズ、色、配置で重要度を表現

## 使用例

### 例1: スライド構成の提案

```python
worker = PresentationBuilderWorker()

task = {
    "type": "suggest_structure",
    "topic": "デジタル変革プロジェクト提案",
    "audience": "IT部門マネージャー",
    "duration": 30
}

result = worker.execute(task)

# 提案された構成を確認
for slide in result['output']['structure']:
    print(f"{slide['slide_number']}. {slide['title']}")
```

### 例2: PPTXファイルの作成

```python
worker = PresentationBuilderWorker()

task = {
    "type": "create_presentation",
    "topic": "四半期レポート",
    "output_path": "Q1_report.pptx",
    "slides": [
        {
            "layout": "title",
            "title": "2025年 Q1 業績報告"
        },
        {
            "layout": "bullet_points",
            "title": "主な成果",
            "bullets": [
                "売上: 前年比120%",
                "新規顧客: 50社獲得",
                "顧客満足度: 4.5/5.0"
            ]
        }
    ]
}

result = worker.execute(task)
print(f"作成完了: {result['output']['file_path']}")
```

## エラーハンドリング

### python-pptxが未インストールの場合

```
⚠️  python-pptx がインストールされていません
   インストール: pip install python-pptx
```

→ スライド構成の提案は動作しますが、PPTX生成は失敗します

### ファイル保存エラー

- 出力先のディレクトリが存在するか確認
- ファイルの書き込み権限を確認
- 既存ファイルが開かれていないか確認

## 依存関係

### 必須
- Python 3.7+

### オプション（PPTX生成機能）
- python-pptx: `pip install python-pptx`

### 推奨
- Pillow: 画像処理（`pip install Pillow`）

## 次のステップ

- [ ] テンプレートファイルの追加
- [ ] 画像挿入機能の実装
- [ ] グラフ生成機能の実装
- [ ] マスタースライドのカスタマイズ
- [ ] HTMLプレビュー機能
