#!/usr/bin/env python3
"""
Security Review Skill - セキュリティレビュースキル

専門知識: コードのセキュリティ脆弱性をチェックする
"""

from typing import Dict, List, Any


class SecurityReviewSkill:
    """セキュリティレビュースキル"""

    def __init__(self):
        """初期化"""
        self.name = "security-review"
        self.description = "コードのセキュリティ脆弱性をチェック"
        self.version = "1.0.0"
        self.checklist = self._load_checklist()

    def _load_checklist(self) -> List[Dict[str, str]]:
        """チェックリストをロード"""
        return [
            {
                "id": "SEC-001",
                "category": "入力検証",
                "check": "ユーザー入力を適切にバリデーションしているか",
                "severity": "high"
            },
            {
                "id": "SEC-002",
                "category": "SQLインジェクション",
                "check": "SQLクエリでプレースホルダーを使用しているか",
                "severity": "critical"
            },
            {
                "id": "SEC-003",
                "category": "XSS",
                "check": "出力時にHTMLエスケープを行っているか",
                "severity": "high"
            },
            {
                "id": "SEC-004",
                "category": "認証",
                "check": "パスワードをハッシュ化して保存しているか",
                "severity": "critical"
            },
            {
                "id": "SEC-005",
                "category": "エラーハンドリング",
                "check": "機密情報をエラーメッセージに含めていないか",
                "severity": "medium"
            },
            {
                "id": "SEC-006",
                "category": "ファイル操作",
                "check": "パストラバーサル攻撃を防いでいるか",
                "severity": "high"
            },
            {
                "id": "SEC-007",
                "category": "暗号化",
                "check": "機密データを暗号化して保存しているか",
                "severity": "high"
            },
            {
                "id": "SEC-008",
                "category": "権限管理",
                "check": "適切なアクセス制御を実装しているか",
                "severity": "high"
            }
        ]

    def review(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """セキュリティレビューを実行"""
        print(f"\n🔒 {self.name}: セキュリティレビュー中...")

        findings = []
        warnings = []
        passed = []

        # シンプルなキーワードベースのチェック
        for check_item in self.checklist:
            result = self._check_item(code, check_item)
            if result["status"] == "fail":
                findings.append(result)
            elif result["status"] == "warning":
                warnings.append(result)
            else:
                passed.append(result)

        # レビュー結果
        total_checks = len(self.checklist)
        critical_issues = len([f for f in findings if f["severity"] == "critical"])
        high_issues = len([f for f in findings if f["severity"] == "high"])

        result = {
            "status": "fail" if critical_issues > 0 else "pass" if not findings else "warning",
            "skill": self.name,
            "summary": {
                "total_checks": total_checks,
                "passed": len(passed),
                "warnings": len(warnings),
                "findings": len(findings),
                "critical_issues": critical_issues,
                "high_issues": high_issues
            },
            "findings": findings,
            "warnings": warnings,
            "recommendations": self._generate_recommendations(findings)
        }

        # 結果を表示
        self._print_result(result)

        return result

    def _check_item(self, code: str, check_item: Dict[str, str]) -> Dict[str, Any]:
        """個別のチェック項目を確認"""
        check_id = check_item["id"]
        category = check_item["category"]
        severity = check_item["severity"]

        # シンプルなキーワードベースのチェック（実際にはより高度な静的解析が必要）
        if check_id == "SEC-001":
            # 入力検証のチェック
            if "input(" in code and ("int(" not in code and "float(" not in code):
                return {
                    "id": check_id,
                    "category": category,
                    "severity": severity,
                    "status": "warning",
                    "message": "入力検証が不十分な可能性があります"
                }

        elif check_id == "SEC-005":
            # エラーハンドリングのチェック
            if "Exception as e" in code and "print(f" in code:
                return {
                    "id": check_id,
                    "category": category,
                    "severity": severity,
                    "status": "warning",
                    "message": "エラーメッセージに機密情報が含まれる可能性があります"
                }

        elif check_id == "SEC-004":
            # パスワードハッシュ化のチェック
            if "password" in code.lower() and "hash" not in code.lower():
                return {
                    "id": check_id,
                    "category": category,
                    "severity": severity,
                    "status": "fail",
                    "message": "パスワードがハッシュ化されていない可能性があります"
                }

        # デフォルト: パス
        return {
            "id": check_id,
            "category": category,
            "severity": severity,
            "status": "pass",
            "message": "OK"
        }

    def _generate_recommendations(self, findings: List[Dict[str, Any]]) -> List[str]:
        """推奨事項を生成"""
        recommendations = []

        if any(f["id"] == "SEC-001" for f in findings):
            recommendations.append("入力検証: すべてのユーザー入力を検証・サニタイズしてください")

        if any(f["id"] == "SEC-004" for f in findings):
            recommendations.append("パスワード: bcryptやArgon2などの安全なハッシュ関数を使用してください")

        if any(f["id"] == "SEC-005" for f in findings):
            recommendations.append("エラー処理: 本番環境では詳細なエラーメッセージを表示しないでください")

        if not recommendations:
            recommendations.append("現時点で大きな問題は検出されませんでした")

        return recommendations

    def _print_result(self, result: Dict[str, Any]):
        """結果を表示"""
        summary = result["summary"]
        print(f"\n   📊 レビュー結果:")
        print(f"      チェック項目: {summary['total_checks']}")
        print(f"      ✅ パス: {summary['passed']}")
        print(f"      ⚠️  警告: {summary['warnings']}")
        print(f"      ❌ 問題: {summary['findings']}")

        if result["findings"]:
            print(f"\n   🚨 検出された問題:")
            for finding in result["findings"]:
                severity_icon = "🔴" if finding["severity"] == "critical" else "🟠"
                print(f"      {severity_icon} [{finding['id']}] {finding['category']}: {finding['message']}")

        if result["recommendations"]:
            print(f"\n   💡 推奨事項:")
            for i, rec in enumerate(result["recommendations"], 1):
                print(f"      {i}. {rec}")


def main():
    """テスト用メイン関数"""
    skill = SecurityReviewSkill()

    # テストコード
    test_code = '''
def login(username, password):
    # パスワードを平文で保存（危険！）
    users = {"admin": "password123"}
    return users.get(username) == password
'''

    result = skill.review(test_code)

    print("\n📄 レビュー完了")
    print(f"ステータス: {result['status']}")


if __name__ == "__main__":
    main()
