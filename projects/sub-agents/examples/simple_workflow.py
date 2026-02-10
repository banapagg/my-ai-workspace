#!/usr/bin/env python3
"""
Simple Workflow Example - サブエージェント環境の使用例

このスクリプトは、オーケストレーター、ワーカー、Skillsを統合した
簡単なワークフローのデモンストレーションです。
"""

import sys
import os

# パスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# パスを直接インポート（ハイフン付きディレクトリ名のため）
import importlib.util

# Orchestratorをインポート
spec = importlib.util.spec_from_file_location("orchestrator", "../orchestrator/orchestrator.py")
orchestrator_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orchestrator_module)
Orchestrator = orchestrator_module.Orchestrator

# CodeWriterWorkerをインポート
spec = importlib.util.spec_from_file_location("worker", "../workers/code_writer/worker.py")
worker_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker_module)
CodeWriterWorker = worker_module.CodeWriterWorker

# SecurityReviewSkillをインポート
spec = importlib.util.spec_from_file_location("skill", "../skills/security-review/skill.py")
skill_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skill_module)
SecurityReviewSkill = skill_module.SecurityReviewSkill


def demo_orchestrator_only():
    """オーケストレーターのみのデモ"""
    print("\n" + "="*70)
    print("デモ1: オーケストレーター単体")
    print("="*70)

    orchestrator = Orchestrator()
    task = "Pythonで簡単な電卓プログラムを作成してください"
    result = orchestrator.process_task(task)

    print(f"\nステータス: {result['status']}")
    print(f"実行ステップ数: {result['total_steps']}")


def demo_worker_only():
    """ワーカー単体のデモ"""
    print("\n" + "="*70)
    print("デモ2: Code Writer ワーカー単体")
    print("="*70)

    worker = CodeWriterWorker()

    task = {
        "type": "code_writing",
        "description": "電卓プログラムを生成",
        "task": "Pythonで簡単な電卓プログラムを作成してください"
    }

    result = worker.execute(task)

    print(f"\nステータス: {result['status']}")
    print(f"言語: {result['output']['language']}")
    print(f"\n生成されたコード:\n")
    print(result['output']['code'][:500] + "..." if len(result['output']['code']) > 500 else result['output']['code'])


def demo_skill_only():
    """Skill単体のデモ"""
    print("\n" + "="*70)
    print("デモ3: Security Review Skill単体")
    print("="*70)

    skill = SecurityReviewSkill()

    # 脆弱性のあるコード例
    vulnerable_code = '''
def login(username, password):
    # パスワードを平文で保存（危険！）
    users = {"admin": "password123"}

    if users.get(username) == password:
        print(f"ログイン成功: {username}")
        return True
    return False
'''

    print("\nレビュー対象コード:")
    print(vulnerable_code)

    result = skill.review(vulnerable_code)

    print(f"\n総合ステータス: {result['status']}")


def demo_integrated_workflow():
    """統合ワークフローのデモ"""
    print("\n" + "="*70)
    print("デモ4: 統合ワークフロー（オーケストレーター + ワーカー + Skill）")
    print("="*70)

    # 1. オーケストレーターでコード生成
    print("\n【フェーズ1】コード生成")
    orchestrator = Orchestrator()
    task = "Pythonで簡単な電卓プログラムを作成してください"
    orchestrator_result = orchestrator.process_task(task)

    # 2. ワーカーで実際にコードを生成
    print("\n【フェーズ2】コード生成の実行")
    worker = CodeWriterWorker()
    worker_task = {
        "type": "code_writing",
        "description": "電卓プログラムを生成",
        "task": task
    }
    worker_result = worker.execute(worker_task)
    generated_code = worker_result['output']['code']

    # 3. Skillでセキュリティレビュー
    print("\n【フェーズ3】セキュリティレビュー")
    skill = SecurityReviewSkill()
    review_result = skill.review(generated_code)

    # 4. 最終レポート
    print("\n" + "="*70)
    print("📊 最終レポート")
    print("="*70)
    print(f"\n✅ コード生成: {worker_result['status']}")
    print(f"   言語: {worker_result['output']['language']}")
    print(f"   行数: {len(generated_code.split(chr(10)))}")

    print(f"\n🔒 セキュリティレビュー: {review_result['status']}")
    print(f"   チェック項目: {review_result['summary']['total_checks']}")
    print(f"   パス: {review_result['summary']['passed']}")
    print(f"   警告: {review_result['summary']['warnings']}")
    print(f"   問題: {review_result['summary']['findings']}")

    if review_result['recommendations']:
        print(f"\n💡 推奨事項:")
        for i, rec in enumerate(review_result['recommendations'], 1):
            print(f"   {i}. {rec}")

    print("\n" + "="*70)
    print("✨ ワークフロー完了")
    print("="*70)


def main():
    """メイン関数"""
    print("\n" + "="*70)
    print("[*] Sub-Agents Workflow Demo")
    print("="*70)
    print("\nこのデモでは、オーケストレーター・ワーカーパターンと")
    print("Agent Skillsを使ったサブエージェント環境を実演します。")

    demos = [
        ("1", "オーケストレーター単体", demo_orchestrator_only),
        ("2", "ワーカー単体", demo_worker_only),
        ("3", "Skill単体", demo_skill_only),
        ("4", "統合ワークフロー", demo_integrated_workflow),
        ("a", "全て実行", None)
    ]

    print("\n実行するデモを選択してください:")
    for code, name, _ in demos:
        print(f"  {code}. {name}")

    choice = input("\n選択 (1-4, a): ").strip().lower()

    if choice == "a":
        for code, name, demo_func in demos:
            if demo_func:
                demo_func()
                input("\n[Enter キーで次のデモへ]")
    else:
        for code, name, demo_func in demos:
            if code == choice and demo_func:
                demo_func()
                break
        else:
            print("無効な選択です")

    print("\n[*] デモ終了")


if __name__ == "__main__":
    main()
