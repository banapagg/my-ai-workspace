#!/usr/bin/env python3
"""
Orchestrator - タスクを分析し、適切なワーカーに委譲する

シンプルな実装例（概念実証）
"""

import json
import sys
import os
import importlib.util
from typing import Dict, List, Any
from pathlib import Path


class Orchestrator:
    """オーケストレーター"""

    def __init__(self, config_path: str = "config.json"):
        """初期化"""
        self.config = self._load_config(config_path)
        self.workers = {}
        self.worker_instances = {}
        self.model_mapping = self._load_model_mapping()
        self.base_path = Path(__file__).parent.parent  # sub-agents/
        self._register_workers()

    def _load_config(self, config_path: str) -> Dict:
        """設定をロード"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # デフォルト設定
            return {
                "workers": {
                    "code_writer": {
                        "enabled": True,
                        "description": "コード生成を担当",
                        "skills": ["coding", "architecture"]
                    },
                    "presentation_builder": {
                        "enabled": True,
                        "description": "プレゼン資料の作成を担当",
                        "skills": ["presentation-design"]
                    },
                    "document_writer": {
                        "enabled": True,
                        "description": "Word/PDF文書の作成を担当",
                        "skills": ["document-formatting", "business-writing"]
                    },
                    "code_reviewer": {
                        "enabled": True,
                        "description": "コードレビューを担当",
                        "skills": ["review", "best-practices"]
                    },
                    "tester": {
                        "enabled": True,
                        "description": "テスト実行を担当",
                        "skills": ["testing", "debugging"]
                    }
                },
                "execution_mode": "auto",
                "parallel_execution": False,
                "default_model": "sonnet"
            }

    def _register_workers(self):
        """ワーカーを登録"""
        for worker_name, worker_config in self.config["workers"].items():
            if worker_config["enabled"]:
                self.workers[worker_name] = worker_config

    def _load_worker(self, worker_name: str):
        """ワーカーモジュールを動的にロード"""
        if worker_name in self.worker_instances:
            return self.worker_instances[worker_name]

        try:
            # workers/worker_name/worker.py を探す
            worker_path = self.base_path / "workers" / worker_name / "worker.py"

            if not worker_path.exists():
                print(f"   [!] ワーカーファイルが見つかりません: {worker_path}")
                return None

            # モジュールを動的にロード
            spec = importlib.util.spec_from_file_location(f"{worker_name}_worker", worker_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # ワーカークラスを探す（慣例: XxxYyyWorker）
            class_name = "".join(word.capitalize() for word in worker_name.split("_")) + "Worker"

            if not hasattr(module, class_name):
                print(f"   [!] ワーカークラスが見つかりません: {class_name}")
                return None

            # インスタンス化
            worker_class = getattr(module, class_name)
            worker_instance = worker_class()

            self.worker_instances[worker_name] = worker_instance
            return worker_instance

        except Exception as e:
            print(f"   [!] ワーカーのロードに失敗: {worker_name}")
            print(f"       エラー: {e}")
            return None

    def _load_model_mapping(self) -> Dict[str, str]:
        """タスクタイプとモデルのマッピングを定義"""
        return {
            # 軽量・高速タスク → haiku
            "suggest_structure": "haiku",
            "format_content": "haiku",
            "quick_review": "haiku",

            # 標準タスク → sonnet (デフォルト)
            "create_document": "sonnet",
            "create_presentation": "sonnet",
            "review": "sonnet",
            "code_writing": "sonnet",
            "code_review": "sonnet",
            "testing": "sonnet",

            # 複雑なタスク → opus
            "complex_analysis": "opus",
            "architectural_design": "opus",
            "comprehensive_review": "opus",

            # デフォルト
            "default": "sonnet"
        }

    def _determine_model(self, task_type: str) -> str:
        """タスクタイプから適切なモデルを判定"""
        return self.model_mapping.get(task_type, self.model_mapping["default"])

    def analyze_task(self, task: str) -> List[Dict[str, Any]]:
        """タスクを分析してサブタスクに分割"""
        print(f"\n[*] タスク分析中: {task}")

        # シンプルなキーワードベースの分析
        subtasks = []

        # レビュー関連（優先度高: 先にチェック）
        if any(keyword in task.lower() for keyword in ["レビュー", "確認", "チェック"]):
            # 複雑なレビューか簡易レビューか判定
            if any(keyword in task.lower() for keyword in ["詳細", "包括", "徹底"]):
                task_type = "comprehensive_review"
            else:
                task_type = "review"

            subtasks.append({
                "type": task_type,
                "worker": "code_reviewer",
                "description": "コードをレビューする",
                "task": task,
                "model": self._determine_model(task_type)
            })

        # プレゼン関連
        elif any(keyword in task.lower() for keyword in ["プレゼン", "スライド", "pptx", "powerpoint"]):
            if any(keyword in task.lower() for keyword in ["構成", "提案", "アイデア"]):
                task_type = "suggest_structure"
                task_data = {
                    "type": task_type,
                    "topic": "プレゼンテーション",
                    "audience": "一般",
                    "duration": 15,
                    "description": "プレゼン構成を提案する"
                }
            else:
                task_type = "create_presentation"
                task_data = {
                    "type": task_type,
                    "topic": "プレゼンテーション",
                    "output_path": "presentation.pptx",
                    "slides": [
                        {"layout": "title", "title": "プレゼンテーション", "subtitle": "サンプル"},
                        {"layout": "content", "title": "内容", "content": "自動生成されたプレゼンです"}
                    ],
                    "description": "プレゼン資料を作成する"
                }

            subtasks.append({
                "type": task_type,
                "worker": "presentation_builder",
                "description": "プレゼン資料を作成する",
                **task_data,
                "model": self._determine_model(task_type)
            })

        # 文書関連
        elif any(keyword in task.lower() for keyword in ["文書", "ドキュメント", "word", "報告書", "議事録", "提案書"]):
            if any(keyword in task.lower() for keyword in ["構成", "提案", "アイデア"]):
                task_type = "suggest_structure"
                task_data = {
                    "type": task_type,
                    "doc_type": "report",
                    "topic": "報告書",
                    "purpose": "情報共有",
                    "description": "文書構成を提案する"
                }
            else:
                task_type = "create_document"
                # 文書タイプを判定
                if "議事録" in task.lower():
                    doc_type = "minutes"
                    title = "議事録"
                elif "提案書" in task.lower():
                    doc_type = "proposal"
                    title = "提案書"
                else:
                    doc_type = "report"
                    title = "報告書"

                task_data = {
                    "type": task_type,
                    "doc_type": doc_type,
                    "title": title,
                    "output_path": f"{title}.docx",
                    "content": {
                        "metadata": {
                            "company": "株式会社サンプル",
                            "author": "システム",
                            "date": "2025年1月"
                        },
                        "sections": [
                            {
                                "title": "概要",
                                "type": "content",
                                "content": "自動生成された文書です。"
                            }
                        ]
                    },
                    "description": "文書を作成する"
                }

            subtasks.append({
                "type": task_type,
                "worker": "document_writer",
                "description": "文書を作成する",
                **task_data,
                "model": self._determine_model(task_type)
            })

        # コード関連
        elif any(keyword in task.lower() for keyword in ["コード", "実装", "作成", "書く"]):
            subtasks.append({
                "type": "code_writing",
                "worker": "code_writer",
                "description": "コードを生成する",
                "task": task,
                "model": self._determine_model("code_writing")
            })

        # テスト関連
        elif any(keyword in task.lower() for keyword in ["テスト", "検証"]):
            subtasks.append({
                "type": "testing",
                "worker": "tester",
                "description": "テストを実行する",
                "task": task,
                "model": self._determine_model("testing")
            })

        # デフォルト
        if not subtasks:
            subtasks.append({
                "type": "default",
                "worker": "code_writer",
                "description": "タスクを実行する",
                "task": task,
                "model": self._determine_model("default")
            })

        # モデル情報を表示
        for subtask in subtasks:
            print(f"   タスク: {subtask['type']} -> モデル: {subtask['model']}")

        return subtasks

    def create_execution_plan(self, subtasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """実行計画を作成"""
        print(f"\n[*] 実行計画を作成中...")

        plan = []
        for i, subtask in enumerate(subtasks):
            worker_name = subtask["worker"]
            model = subtask.get("model", "sonnet")

            if worker_name in self.workers:
                plan.append({
                    "step": i + 1,
                    "worker": worker_name,
                    "model": model,
                    "task": subtask,
                    "status": "pending"
                })
                print(f"   ステップ {i + 1}: {worker_name} ({model}) - {subtask['description']}")
            else:
                print(f"   [!] ワーカー '{worker_name}' が見つかりません（スキップ）")

        return plan

    def execute_plan(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """実行計画を実行"""
        print(f"\n[*] 実行中...")

        results = []
        for step in plan:
            model = step.get('model', 'sonnet')
            worker_name = step['worker']
            print(f"\n   ステップ {step['step']}: {worker_name} ({model}) を実行中...")

            # ワーカーをロード
            worker = self._load_worker(worker_name)

            if worker is None:
                # ワーカーがロードできない場合はスキップ
                result = {
                    "step": step['step'],
                    "worker": worker_name,
                    "model": model,
                    "status": "error",
                    "output": f"[{worker_name}] ワーカーのロードに失敗しました",
                    "details": {
                        "task": step['task'],
                        "model_used": model,
                        "error": "ワーカーがロードできませんでした"
                    }
                }
            else:
                try:
                    # ワーカーを実行
                    # タスク情報をワーカーに渡す
                    task_data = step['task']
                    worker_result = worker.execute(task_data)

                    result = {
                        "step": step['step'],
                        "worker": worker_name,
                        "model": model,
                        "status": worker_result.get("status", "success"),
                        "output": f"[{worker_name}] タスク '{task_data['description']}' を完了しました",
                        "details": {
                            "task": task_data,
                            "model_used": model,
                            "worker_output": worker_result
                        }
                    }

                    print(f"   [+] {worker_name} ({model}) 完了")

                except Exception as e:
                    result = {
                        "step": step['step'],
                        "worker": worker_name,
                        "model": model,
                        "status": "error",
                        "output": f"[{worker_name}] 実行中にエラーが発生しました",
                        "details": {
                            "task": step['task'],
                            "model_used": model,
                            "error": str(e)
                        }
                    }
                    print(f"   [!] {worker_name} エラー: {e}")

            results.append(result)

        return results

    def integrate_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """結果を統合"""
        print(f"\n[*] 結果を統合中...")

        all_success = all(r["status"] == "success" for r in results)

        integrated = {
            "status": "success" if all_success else "partial_success",
            "total_steps": len(results),
            "successful_steps": sum(1 for r in results if r["status"] == "success"),
            "results": results,
            "summary": self._generate_summary(results)
        }

        return integrated

    def _generate_summary(self, results: List[Dict[str, Any]]) -> str:
        """サマリーを生成"""
        lines = ["\n=== 実行結果サマリー ==="]
        for result in results:
            status_icon = "[+]" if result["status"] == "success" else "[!]"
            lines.append(f"{status_icon} ステップ {result['step']}: {result['output']}")
        return "\n".join(lines)

    def process_task(self, task: str) -> Dict[str, Any]:
        """タスクを処理"""
        print(f"\n{'='*60}")
        print(f"[*] オーケストレーター起動")
        print(f"{'='*60}")

        # 1. タスク分析
        subtasks = self.analyze_task(task)

        # 2. 実行計画作成
        plan = self.create_execution_plan(subtasks)

        # 3. 実行
        results = self.execute_plan(plan)

        # 4. 結果統合
        final_result = self.integrate_results(results)

        print(final_result["summary"])
        print(f"\n{'='*60}")
        print(f"[+] 完了")
        print(f"{'='*60}\n")

        return final_result


def main():
    """メイン関数"""
    # オーケストレーターを初期化
    orchestrator = Orchestrator()

    # サンプルタスク（モデル選択のテスト）
    test_tasks = [
        "プレゼンの構成を提案してください",  # haiku
        "報告書の文書を作成してください",    # sonnet
        "詳細なコードレビューをしてください",  # opus (comprehensive_review)
    ]

    for i, task in enumerate(test_tasks, 1):
        print(f"\n{'='*60}")
        print(f"テスト {i}/{len(test_tasks)}")
        print(f"{'='*60}")

        result = orchestrator.process_task(task)

        # 使用されたモデルを確認
        print(f"\n使用モデル:")
        for r in result['results']:
            print(f"  - {r['worker']}: {r['model']}")

    print(f"\n{'='*60}")
    print("全テスト完了")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
