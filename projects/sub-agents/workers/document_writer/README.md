# Document Writer Worker

## 役割

Word/PDF文書の生成、体裁の良いフォーマット適用を担当するワーカー。
お客様向けの提案書、報告書、議事録などの作成を支援します。

## 責任範囲

### できること
- **文書構成の提案**: 文書タイプに応じた最適な構成
- **Word文書の生成**: python-docxを使用したdocxファイル作成
- **3種類のテンプレート**: 提案書、報告書、議事録
- **表・図表の挿入**: データの視覚化
- **目次の自動生成**: セクション構造に基づく目次
- **体裁の統一**: 見出し、本文、箇条書きのスタイル適用

### できないこと
- 複雑なレイアウトデザイン（テンプレートに準拠）
- 画像の編集・加工（別途画像ファイルが必要）
- PDFへの直接エクスポート（Wordで手動保存が必要）

## 入力

### 文書構成の提案

```json
{
  "type": "suggest_structure",
  "doc_type": "report",
  "topic": "市場調査報告",
  "purpose": "経営陣への報告"
}
```

### Word文書の作成

```json
{
  "type": "create_document",
  "doc_type": "report",
  "title": "2025年第1四半期 市場調査報告書",
  "output_path": "market_report_Q1.docx",
  "content": {
    "metadata": {
      "company": "株式会社〇〇",
      "author": "山田太郎",
      "date": "2025年1月15日"
    },
    "sections": [
      {
        "title": "概要",
        "type": "content",
        "content": "本報告書は2025年第1四半期の市場動向をまとめたものです。"
      },
      {
        "title": "調査結果",
        "type": "table",
        "table_data": [
          ["項目", "2024年", "2025年", "成長率"],
          ["市場規模", "1,000億円", "1,150億円", "15%"],
          ["当社シェア", "15%", "18%", "20%"]
        ]
      }
    ]
  }
}
```

## 出力

### 文書構成の提案

```json
{
  "status": "success",
  "worker": "document_writer",
  "output": {
    "doc_type": "report",
    "template_name": "報告書・レポート",
    "sections": [
      {"title": "表紙", "type": "cover"},
      {"title": "目次", "type": "toc"},
      {"title": "概要", "type": "content"},
      ...
    ],
    "recommendations": [
      "概要（エグゼクティブサマリー）は1ページ以内",
      "データは図表で視覚化"
    ]
  }
}
```

## 使用するSkills

- **document-formatting**: ドキュメント体裁のベストプラクティス
- **business-writing**: ビジネス文書の書き方

## 文書テンプレート

### 1. 提案書・企画書

**構成**:
1. 表紙
2. 目次
3. 背景・課題
4. 提案内容
5. 実施計画
6. 期待効果
7. 費用見積（表形式）
8. 付録

**用途**: 新規提案、企画書、RFP対応

### 2. 報告書・レポート

**構成**:
1. 表紙
2. 目次
3. 概要（エグゼクティブサマリー）
4. 調査結果
5. 分析
6. 結論・提言
7. 付録

**用途**: 調査レポート、プロジェクト報告、分析レポート

### 3. 議事録

**構成**:
1. 会議情報（日時、場所、議題）
2. 出席者リスト
3. 議題と討議内容
4. 決定事項
5. アクション項目（表形式：担当者、期限）
6. 次回予定

**用途**: 定例会議、プロジェクト会議、打ち合わせ

## 体裁のベストプラクティス

### 見出し階層

- **レベル1（見出し1）**: 章タイトル（18pt、太字）
- **レベル2（見出し2）**: 節タイトル（16pt、太字）
- **レベル3（見出し3）**: 小見出し（14pt、太字）

### フォント

- **日本語**: 游ゴシック、メイリオ（読みやすさ重視）
- **英数字**: Arial、Calibri
- **本文サイズ**: 10.5-11pt

### 余白

- **上下**: 25mm
- **左右**: 30mm（綴じ代を考慮）

### ページ番号

- **位置**: 下部中央または右下
- **形式**: 「1/10」形式（現在ページ/総ページ数）

### 表・図表

- **番号**: 「表1」「図1」と連番
- **タイトル**: 表は上、図は下に配置
- **出典**: 必ず記載

## 使用例

### 例1: 報告書の構成提案

```python
worker = DocumentWriterWorker()

task = {
    "type": "suggest_structure",
    "doc_type": "report",
    "topic": "競合分析レポート",
    "purpose": "戦略会議資料"
}

result = worker.execute(task)

# 提案されたセクション
for section in result['output']['sections']:
    print(f"{section['title']} ({section['type']})")
```

### 例2: 議事録の作成

```python
worker = DocumentWriterWorker()

task = {
    "type": "create_document",
    "doc_type": "minutes",
    "title": "2025年1月 週次定例会議 議事録",
    "output_path": "minutes_20250115.docx",
    "content": {
        "metadata": {
            "company": "株式会社〇〇",
            "date": "2025年1月15日"
        },
        "sections": [
            {
                "title": "会議情報",
                "type": "content",
                "content": "日時: 2025年1月15日 10:00-11:00\\n場所: 会議室A"
            },
            {
                "title": "決定事項",
                "type": "list",
                "content": [
                    "新製品の発売日を3月1日に決定",
                    "マーケティング予算を20%増額",
                    "追加人員の採用を承認"
                ]
            },
            {
                "title": "アクション項目",
                "type": "table",
                "table_data": [
                    ["項目", "担当者", "期限"],
                    ["製品仕様確定", "山田", "1/20"],
                    ["広告代理店選定", "佐藤", "1/25"]
                ]
            }
        ]
    }
}

result = worker.execute(task)
print(f"作成完了: {result['output']['file_path']}")
```

## エラーハンドリング

### python-docxが未インストールの場合

```
[!] python-docx がインストールされていません
    インストール: pip install python-docx
```

→ 文書構成の提案は動作しますが、Word生成は失敗します

## 依存関係

### 必須
- Python 3.7+

### オプション（Word生成機能）
- python-docx: `pip install python-docx`

### 推奨（PDF変換）
- python-docx2pdf: `pip install docx2pdf`（Windows）
- LibreOffice: コマンドライン変換（Linux/Mac）

## 次のステップ

- [ ] PDFエクスポート機能
- [ ] カスタムテンプレートの追加
- [ ] 画像挿入機能の強化
- [ ] 自動校正機能（誤字脱字チェック）
- [ ] 契約書テンプレートの追加
