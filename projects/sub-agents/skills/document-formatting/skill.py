#!/usr/bin/env python3
"""
Document Formatting Skill - ドキュメント体裁のベストプラクティス

専門知識: ビジネス文書の体裁、フォーマット、構成
対象: コンサルタント、営業、事務職
"""

from typing import Dict, List, Any


class DocumentFormattingSkill:
    """ドキュメント体裁スキル"""

    def __init__(self):
        """初期化"""
        self.name = "document-formatting"
        self.description = "ビジネス文書の体裁ベストプラクティス"
        self.version = "1.0.0"
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        """体裁ルールをロード"""
        return {
            "structure": {
                "name": "文書構造",
                "rules": [
                    {
                        "id": "STRUCT-001",
                        "rule": "3段階の見出し階層",
                        "description": "見出しは最大3階層まで",
                        "why": "4階層以上は複雑で理解しにくい",
                        "how": "章（レベル1）→節（レベル2）→項（レベル3）"
                    },
                    {
                        "id": "STRUCT-002",
                        "rule": "目次の必須化",
                        "description": "5ページ以上の文書には目次を付ける",
                        "why": "全体像の把握と必要箇所への素早いアクセス",
                        "how": "Wordの目次自動生成機能を使用"
                    },
                    {
                        "id": "STRUCT-003",
                        "rule": "ページ番号の表示",
                        "description": "全ページにページ番号を表示",
                        "why": "参照時の利便性向上",
                        "how": "「1/10」形式（現在/総数）を推奨"
                    }
                ]
            },
            "formatting": {
                "name": "フォーマット",
                "rules": [
                    {
                        "id": "FORMAT-001",
                        "rule": "フォントの統一",
                        "description": "文書内で使用するフォントは2種類まで",
                        "why": "統一感と読みやすさ",
                        "how": "見出し（ゴシック）+ 本文（ゴシックor明朝）"
                    },
                    {
                        "id": "FORMAT-002",
                        "rule": "適切な行間",
                        "description": "行間は1.15-1.5倍",
                        "why": "読みやすさの確保",
                        "how": "Word標準の1.15倍を推奨"
                    },
                    {
                        "id": "FORMAT-003",
                        "rule": "段落間の余白",
                        "description": "段落間は1行分の余白",
                        "why": "視覚的な区切りの明確化",
                        "how": "段落後に6-12ptの余白を設定"
                    }
                ]
            },
            "tables": {
                "name": "表・図表",
                "rules": [
                    {
                        "id": "TABLE-001",
                        "rule": "表番号とタイトル",
                        "description": "すべての表に番号とタイトルを付ける",
                        "why": "参照時の特定が容易",
                        "how": "「表1: 売上推移」の形式"
                    },
                    {
                        "id": "TABLE-002",
                        "rule": "ヘッダー行の強調",
                        "description": "表のヘッダー行は太字または色付け",
                        "why": "項目名の識別を容易にする",
                        "how": "太字 + 背景色（淡いグレー）"
                    },
                    {
                        "id": "TABLE-003",
                        "rule": "出典の明記",
                        "description": "データの出典を必ず記載",
                        "why": "信頼性の担保",
                        "how": "表の下に「出典: ○○調査」"
                    }
                ]
            },
            "business_writing": {
                "name": "ビジネス文書の書き方",
                "rules": [
                    {
                        "id": "WRITING-001",
                        "rule": "結論先行",
                        "description": "重要な結論は最初に書く",
                        "why": "読み手の理解を早める",
                        "how": "概要セクションに要点を凝縮"
                    },
                    {
                        "id": "WRITING-002",
                        "rule": "一文一義",
                        "description": "1つの文には1つの内容のみ",
                        "why": "理解しやすさの向上",
                        "how": "長文は分割、接続詞で明確に"
                    },
                    {
                        "id": "WRITING-003",
                        "rule": "具体的な数値",
                        "description": "抽象的な表現より具体的な数値",
                        "why": "説得力と信頼性の向上",
                        "how": "「多くの」→「80%の」"
                    }
                ]
            }
        }

    def review(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """文書をレビュー"""
        print(f"\n[*] {self.name}: 文書をレビュー中...")

        sections = document_data.get("sections", [])
        findings = []
        suggestions = []
        good_practices = []

        # 構造チェック
        structure_check = self._check_structure(document_data)
        findings.extend(structure_check["findings"])
        suggestions.extend(structure_check["suggestions"])
        good_practices.extend(structure_check["good_practices"])

        # セクションごとのチェック
        for section in sections:
            section_check = self._check_section(section)
            findings.extend(section_check["findings"])
            suggestions.extend(section_check["suggestions"])

        result = {
            "status": "success",
            "skill": self.name,
            "summary": {
                "total_sections": len(sections),
                "findings": len(findings),
                "suggestions": len(suggestions),
                "good_practices": len(good_practices)
            },
            "findings": findings,
            "suggestions": suggestions,
            "good_practices": good_practices,
            "overall_score": self._calculate_score(len(sections), len(findings))
        }

        self._print_result(result)
        return result

    def _check_structure(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """文書構造をチェック"""
        findings = []
        suggestions = []
        good_practices = []

        sections = document_data.get("sections", [])

        # 目次の有無
        has_toc = any(s.get("type") == "toc" for s in sections)
        if len(sections) >= 5 and not has_toc:
            findings.append({
                "rule": "STRUCT-002",
                "severity": "medium",
                "issue": "5セクション以上ありますが目次がありません",
                "suggestion": "目次セクションを追加してください"
            })
        elif has_toc:
            good_practices.append({
                "practice": "目次が含まれています"
            })

        # 見出し階層のチェック（簡易版）
        heading_levels = [s.get("level", 1) for s in sections if "level" in s]
        if heading_levels and max(heading_levels) > 3:
            findings.append({
                "rule": "STRUCT-001",
                "severity": "low",
                "issue": "見出しが4階層以上あります",
                "suggestion": "見出しは3階層までに抑えてください"
            })

        return {
            "findings": findings,
            "suggestions": suggestions,
            "good_practices": good_practices
        }

    def _check_section(self, section: Dict[str, Any]) -> Dict[str, Any]:
        """個別セクションをチェック"""
        findings = []
        suggestions = []

        section_type = section.get("type", "")
        content = section.get("content", "")

        # 表のチェック
        if section_type == "table":
            table_data = section.get("table_data", [])
            if table_data:
                # ヘッダー行の確認（簡易版）
                if len(table_data) > 1:
                    good_practices = [{
                        "practice": "表にデータが含まれています"
                    }]
                else:
                    suggestions.append({
                        "type": "table",
                        "suggestion": "表には最低2行（ヘッダー+データ）必要です"
                    })

                # 出典の確認
                if "source" not in section and "出典" not in str(content):
                    findings.append({
                        "rule": "TABLE-003",
                        "severity": "medium",
                        "issue": "表に出典が記載されていません",
                        "suggestion": "データの出典を明記してください"
                    })

        # コンテンツの長さチェック
        if isinstance(content, str) and len(content) > 500:
            suggestions.append({
                "type": "content",
                "suggestion": "コンテンツが長すぎます。段落に分けることを推奨"
            })

        return {
            "findings": findings,
            "suggestions": suggestions
        }

    def _calculate_score(self, total_sections: int, findings_count: int) -> int:
        """総合スコアを計算"""
        if total_sections == 0:
            return 0

        deduction_per_finding = 5
        score = 100 - (findings_count * deduction_per_finding)
        return max(0, min(100, score))

    def _print_result(self, result: Dict[str, Any]):
        """結果を表示"""
        summary = result["summary"]
        print(f"\n   レビュー結果:")
        print(f"      セクション数: {summary['total_sections']}")
        print(f"      問題点: {summary['findings']}")
        print(f"      提案: {summary['suggestions']}")
        print(f"      良い点: {summary['good_practices']}")
        print(f"      総合スコア: {result['overall_score']}/100")

    def get_guidelines(self, category: str = "all") -> Dict[str, Any]:
        """ガイドラインを取得"""
        if category == "all":
            return self.rules

        return self.rules.get(category, {})


def main():
    """テスト用メイン関数"""
    skill = DocumentFormattingSkill()

    # テストデータ
    test_document = {
        "title": "テスト報告書",
        "sections": [
            {"title": "表紙", "type": "cover"},
            {"title": "目次", "type": "toc"},
            {"title": "概要", "type": "content", "content": "これは概要です。"},
            {
                "title": "データ",
                "type": "table",
                "table_data": [
                    ["項目", "値"],
                    ["売上", "1000万円"]
                ]
            }
        ]
    }

    result = skill.review(test_document)

    print(f"\n総合評価: {result['overall_score']}/100")


if __name__ == "__main__":
    main()
