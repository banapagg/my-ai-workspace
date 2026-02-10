# GitHub Tasks ホットキー セットアップガイド

このガイドでは、選択したテキストを **Ctrl+Shift+X** 一発でGitHub Projectsのタスクとして追加する機能をセットアップします。

---

## 前提条件

以下がインストール済みであることを確認してください：

1. **GitHub CLI (gh)**
   - インストール場所: `C:\Program Files\GitHub CLI\gh.exe`
   - インストール確認: `gh --version`
   - 認証確認: `gh auth status`

2. **AutoHotkey v2.0**
   - ダウンロード: https://www.autohotkey.com/
   - v2.0 以降が必要です

3. **PowerShell**
   - Windows に標準搭載

---

## セットアップ手順

### Step 1: ファイル配置確認

以下のファイルが `C:\Users\stkn1\My-Tasks\` に配置されていることを確認：

- `Add-GitHubTask.ps1` - PowerShellスクリプト
- `GitHubTaskHotkey.ahk` - AutoHotkeyスクリプト
- `CLAUDE.md` - タスク処理の設定ファイル

### Step 2: PowerShell実行ポリシーの設定

PowerShellスクリプトを実行できるようにするため、管理者権限でPowerShellを開き、以下を実行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

確認メッセージが表示されたら `Y` を入力して Enter。

### Step 3: 手動テスト

1. 適当なテキストをコピー（Ctrl+C）
2. PowerShellで以下を実行：

```powershell
cd C:\Users\stkn1\My-Tasks
.\Add-GitHubTask.ps1
```

3. タスクが正常に作成されることを確認

### Step 4: AutoHotkeyスクリプトの起動

1. `GitHubTaskHotkey.ahk` をダブルクリックして起動
2. タスクトレイに AutoHotkey のアイコンが表示されることを確認

### Step 5: ホットキーのテスト

1. 任意のアプリケーション（ブラウザ、メモ帳など）でテキストを選択
2. **Ctrl+Shift+X** を押す
3. 「タスクを作成中...」のツールチップが表示される
4. 数秒後、成功メッセージが表示される
5. GitHub Projects (https://github.com/users/banapagg/projects/1) を開いてタスクが追加されていることを確認

---

## 自動起動の設定

Windowsログイン時に自動的にAutoHotkeyスクリプトを起動する方法：

### 方法1: スタートアップフォルダに配置

1. `Win + R` を押して「ファイル名を指定して実行」を開く
2. `shell:startup` と入力してEnter
3. 開いたフォルダに `GitHubTaskHotkey.ahk` のショートカットを作成

### 方法2: タスクスケジューラを使用

1. タスクスケジューラを開く
2. 「基本タスクの作成」を選択
3. トリガー: 「ログオン時」
4. 操作: 「プログラムの開始」
5. プログラム: `C:\Users\stkn1\My-Tasks\GitHubTaskHotkey.ahk`

---

## 使い方

1. **任意のアプリでテキストを選択**
   - ブラウザ、エディタ、PDF、Officeドキュメントなど

2. **Ctrl+Shift+X を押す**
   - 自動でコピー → GitHub Issue作成 → Project追加 → ステータス設定

3. **キーワードによる自動設定**
   - 「急ぎ」「至急」「ASAP」 → `priority:high`
   - 「バグ」「不具合」「エラー」 → `type:bug`
   - 「アイデア」「提案」 → `type:idea`
   - 「今日中」 → 期日が当日 + `priority:high`
   - 「明日」 → 期日が翌日
   - 「3日後」 → 期日が3日後

---

## トラブルシューティング

### エラー: 「gh: command not found」

GitHub CLI のパスが正しくない可能性があります。

1. `gh.exe` の実際の場所を確認：
   ```powershell
   Get-Command gh
   ```

2. `Add-GitHubTask.ps1` の5行目を修正：
   ```powershell
   $env:PATH = "実際のパス;$env:PATH"
   ```

### エラー: 「認証エラー」

GitHub CLI で認証されていません。

```bash
gh auth login
```

### ホットキーが動作しない

1. AutoHotkeyスクリプトが起動しているか確認（タスクトレイを確認）
2. 他のアプリケーションが同じホットキーを使用していないか確認
3. AutoHotkey v2.0 がインストールされているか確認

### PowerShell実行ポリシーエラー

管理者権限でPowerShellを開き、再度実行ポリシーを設定：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## カスタマイズ

### ホットキーを変更する

`GitHubTaskHotkey.ahk` の3行目を編集：

```autohotkey
^+x::  ; Ctrl+Shift+X
```

変更例：
- `^!t` → Ctrl+Alt+T
- `#t` → Win+T
- `^+!t` → Ctrl+Shift+Alt+T

参考: https://www.autohotkey.com/docs/v2/Hotkeys.htm

### 本文のテンプレートを変更する

`Add-GitHubTask.ps1` の48行目以降の `$Body` 変数を編集。

---

## ファイル構成

```
C:\Users\stkn1\My-Tasks\
├── CLAUDE.md                  # タスク処理の設定・ルール
├── Add-GitHubTask.ps1         # PowerShellスクリプト
├── GitHubTaskHotkey.ahk       # AutoHotkeyスクリプト
└── SETUP.md                   # このファイル
```

---

## 完成！

これで、どんなアプリでもテキストを選択して **Ctrl+Shift+X** を押すだけで、GitHub Projectsにタスクが追加されます。

お疲れ様でした！
