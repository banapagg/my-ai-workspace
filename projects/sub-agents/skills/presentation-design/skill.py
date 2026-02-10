#!/usr/bin/env python3
"""
Presentation Design Skill - プレゼンデザインのベストプラクティス

専門知識: 効果的なプレゼン資料のデザイン原則
対象: コンサルタント、営業、事務職
"""

from typing import Dict, List, Any


class PresentationDesignSkill:
    """プレゼンデザインスキル"""

    def __init__(self):
        """初期化"""
        self.name = "presentation-design"
        self.description = "効果的なプレゼン資料のデザイン原則"
        self.version = "1.0.0"
        self.principles = self._load_principles()

    def _load_principles(self) -> Dict[str, Any]:
        """デザイン原則をロード"""
        return {
            "content": {
                "name": "コンテンツ設計",
                "rules": [
                    {
                        "id": "CONTENT-001",
                        "principle": "1スライド1メッセージ",
                        "description": "1枚のスライドで伝えることは1つに絞る",
                        "why": "複数のメッセージは聴衆の理解を妨げる",
                        "how": "スライドのタイトルでメッセージを明示する"
                    },
                    {
                        "id": "CONTENT-002",
                        "principle": "7±2の法則",
                        "description": "箇条書きは3-7個まで",
                        "why": "人間の短期記憶の限界",
                        "how": "7個を超える場合はカテゴリに分ける"
                    },
                    {
                        "id": "CONTENT-003",
                        "principle": "40文字ルール",
                        "description": "1スライドの文字数は40文字以内",
                        "why": "読むスライドではなく見るスライドを作る",
                        "how": "キーワードのみを残し、詳細は口頭で補足"
                    }
                ]
            },
            "layout": {
                "name": "レイアウト設計",
                "rules": [
                    {
                        "id": "LAYOUT-001",
                        "principle": "Zの法則",
                        "description": "視線は左上→右上→左下→右下の順に動く",
                        "why": "自然な視線の流れに沿った配置が理解しやすい",
                        "how": "重要な情報を左上に配置"
                    },
                    {
                        "id": "LAYOUT-002",
                        "principle": "余白の重要性",
                        "description": "スライドの30-40%は余白にする",
                        "why": "詰め込みすぎは読みにくい",
                        "how": "要素間のスペースを十分に取る"
                    },
                    {
                        "id": "LAYOUT-003",
                        "principle": "グリッドシステム",
                        "description": "要素を整列させる",
                        "why": "整列は視覚的な美しさと理解しやすさを生む",
                        "how": "ガイド線を使って要素を揃える"
                    }
                ]
            },
            "visual": {
                "name": "ビジュアル設計",
                "rules": [
                    {
                        "id": "VISUAL-001",
                        "principle": "図>表>文字",
                        "description": "図で表現できるなら図を使う",
                        "why": "ビジュアルは理解を早める",
                        "how": "プロセスはフロー図、比較は表、データはグラフ"
                    },
                    {
                        "id": "VISUAL-002",
                        "principle": "色の使用は3色まで",
                        "description": "ベース色+メイン色+アクセント色",
                        "why": "色が多すぎると焦点がぼやける",
                        "how": "重要な部分のみアクセント色を使用"
                    },
                    {
                        "id": "VISUAL-003",
                        "principle": "フォントは2種類まで",
                        "description": "見出し用と本文用",
                        "why": "統一感が生まれる",
                        "how": "ゴシック体（見出し）+ 明朝体（本文）"
                    }
                ]
            },
            "storytelling": {
                "name": "ストーリーテリング",
                "rules": [
                    {
                        "id": "STORY-001",
                        "principle": "問題→解決の流れ",
                        "description": "課題を提示してから解決策を示す",
                        "why": "聴衆の関心を引き、提案の価値を高める",
                        "how": "現状の問題点→影響→解決策→効果の順"
                    },
                    {
                        "id": "STORY-002",
                        "principle": "3の法則",
                        "description": "重要ポイントは3つに絞る",
                        "why": "3つは記憶しやすく、説得力がある",
                        "how": "最重要な3点を選び、それぞれ詳しく説明"
                    },
                    {
                        "id": "STORY-003",
                        "principle": "データで裏付ける",
                        "description": "主張には必ず根拠を示す",
                        "why": "信頼性と説得力が増す",
                        "how": "統計データ、事例、専門家の意見を引用"
                    }
                ]
            }
        }

    def review(self, presentation_data: Dict[str, Any]) -> Dict[str, Any]:
        """プレゼンをレビュー"""
        print(f"\n[*] {self.name}: プレゼンをレビュー中...")

        slides = presentation_data.get("slides", [])
        findings = []
        suggestions = []
        good_practices = []

        for i, slide in enumerate(slides, 1):
            slide_findings = self._review_slide(slide, i)
            findings.extend(slide_findings["findings"])
            suggestions.extend(slide_findings["suggestions"])
            good_practices.extend(slide_findings["good_practices"])

        result = {
            "status": "success",
            "skill": self.name,
            "summary": {
                "total_slides": len(slides),
                "findings": len(findings),
                "suggestions": len(suggestions),
                "good_practices": len(good_practices)
            },
            "findings": findings,
            "suggestions": suggestions,
            "good_practices": good_practices,
            "overall_score": self._calculate_score(len(slides), len(findings))
        }

        self._print_result(result)
        return result

    def _review_slide(self, slide: Dict[str, Any], slide_number: int) -> Dict[str, Any]:
        """個別スライドをレビュー"""
        findings = []
        suggestions = []
        good_practices = []

        # コンテンツチェック
        if "content" in slide:
            content = slide["content"]
            word_count = len(content)

            if word_count > 40:
                findings.append({
                    "slide": slide_number,
                    "type": "content",
                    "severity": "medium",
                    "issue": f"文字数が多すぎます ({word_count}文字)",
                    "rule": "CONTENT-003",
                    "suggestion": "40文字以内に削減してください"
                })

        # 箇条書きチェック
        if "bullets" in slide:
            bullets = slide["bullets"]
            bullet_count = len(bullets)

            if bullet_count > 7:
                findings.append({
                    "slide": slide_number,
                    "type": "content",
                    "severity": "high",
                    "issue": f"箇条書きが多すぎます ({bullet_count}個)",
                    "rule": "CONTENT-002",
                    "suggestion": "7個以内に絞るか、スライドを分割してください"
                })
            elif 3 <= bullet_count <= 7:
                good_practices.append({
                    "slide": slide_number,
                    "practice": "箇条書きの数が適切（7±2の法則）"
                })

        # タイトルチェック
        if "title" in slide:
            title = slide["title"]
            if len(title) > 20:
                suggestions.append({
                    "slide": slide_number,
                    "type": "content",
                    "suggestion": "タイトルは簡潔に（20文字以内が理想）"
                })
            elif len(title) <= 15:
                good_practices.append({
                    "slide": slide_number,
                    "practice": "タイトルが簡潔"
                })

        return {
            "findings": findings,
            "suggestions": suggestions,
            "good_practices": good_practices
        }

    def _calculate_score(self, total_slides: int, findings_count: int) -> int:
        """総合スコアを計算（100点満点）"""
        if total_slides == 0:
            return 0

        deduction_per_finding = 5
        score = 100 - (findings_count * deduction_per_finding)
        return max(0, min(100, score))

    def _print_result(self, result: Dict[str, Any]):
        """結果を表示"""
        summary = result["summary"]
        print(f"\n   レビュー結果:")
        print(f"      スライド数: {summary['total_slides']}")
        print(f"      問題点: {summary['findings']}")
        print(f"      提案: {summary['suggestions']}")
        print(f"      良い点: {summary['good_practices']}")
        print(f"      総合スコア: {result['overall_score']}/100")

        if result["findings"]:
            print(f"\n   主な問題点:")
            for finding in result["findings"][:3]:  # 最初の3つを表示
                print(f"      - スライド{finding['slide']}: {finding['issue']}")

    def get_guidelines(self, category: str = "all") -> Dict[str, Any]:
        """ガイドラインを取得"""
        if category == "all":
            return self.principles

        return self.principles.get(category, {})


def main():
    """テスト用メイン関数"""
    skill = PresentationDesignSkill()

    # テストデータ
    test_presentation = {
        "topic": "新規事業提案",
        "slides": [
            {
                "title": "新規事業提案",
                "layout": "title"
            },
            {
                "title": "背景と課題",
                "content": "市場は急速に成長しており、競合他社も次々と参入しています。当社も早急に対応する必要があります。",
                "layout": "content"
            },
            {
                "title": "提案内容",
                "bullets": [
                    "新製品の開発",
                    "販路の拡大",
                    "マーケティング強化",
                    "人材の採用",
                    "設備投資",
                    "パートナーシップ",
                    "ブランド強化",
                    "顧客サポート体制の構築"
                ],
                "layout": "bullet_points"
            }
        ]
    }

    result = skill.review(test_presentation)

    print(f"\n総合評価: {result['overall_score']}/100")


if __name__ == "__main__":
    main()
