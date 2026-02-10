; GitHub Tasks - Hotkey Script
; Ctrl+Shift+X で選択中のテキストをGitHub Projectsのタスクとして追加

#Requires AutoHotkey v2.0

; Ctrl+Shift+X のホットキー
^+x:: {
    ; 選択中のテキストをコピー
    A_Clipboard := ""  ; クリップボードをクリア
    Send("^c")  ; Ctrl+C でコピー

    ; クリップボードにデータが入るまで待機（最大1秒）
    if !ClipWait(1) {
        MsgBox("テキストが選択されていません。", "エラー", "Icon!")
        return
    }

    ; PowerShellスクリプトを実行
    ScriptPath := A_ScriptDir . "\Add-GitHubTask.ps1"

    ; PowerShellを非表示で実行
    Run('powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "' . ScriptPath . '"', , "Hide")

    ; 実行中の通知（オプション）
    ToolTip("タスクを作成中...")
    SetTimer(() => ToolTip(), -3000)  ; 3秒後にツールチップを消す
}
