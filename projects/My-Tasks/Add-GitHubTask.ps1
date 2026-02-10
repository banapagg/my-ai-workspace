# GitHub Tasks - Quick Add Script
# クリップボードのテキストをGitHub Projectsのタスクとして追加

param(
    [string]$Text = ""
)

# クリップボードからテキスト取得
if ([string]::IsNullOrWhiteSpace($Text)) {
    Add-Type -AssemblyName System.Windows.Forms
    $Text = [System.Windows.Forms.Clipboard]::GetText()
}

if ([string]::IsNullOrWhiteSpace($Text)) {
    [System.Windows.Forms.MessageBox]::Show("テキストが選択されていません。", "エラー", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
    exit 1
}

# GitHub CLI のパスを設定
$env:PATH = "C:\Program Files\GitHub CLI;$env:PATH"

# タイトル（テキスト全体）
$Title = $Text.Trim()

# キーワード検出
$Priority = "medium"
$Type = "task"
$DueDate = $null

# 優先度検出
if ($Text -match "(急ぎ|至急|ASAP|重要|緊急|今日中)") {
    $Priority = "high"
}

# タイプ検出
if ($Text -match "(バグ|不具合|エラー|壊れ)") {
    $Type = "bug"
} elseif ($Text -match "(アイデア|案|提案|思いつき)") {
    $Type = "idea"
}

# 期日検出（簡易版）
$Today = Get-Date
if ($Text -match "今日中") {
    $DueDate = $Today.ToString("yyyy-MM-dd")
    $Priority = "high"
} elseif ($Text -match "明日") {
    $DueDate = $Today.AddDays(1).ToString("yyyy-MM-dd")
} elseif ($Text -match "(\d+)日後") {
    $Days = [int]$Matches[1]
    $DueDate = $Today.AddDays($Days).ToString("yyyy-MM-dd")
}

# 本文生成（CLAUDE.mdのテンプレートに従う）
$Body = @"
## 概要
$Title

## 詳細
このタスクの詳細な説明や実施内容を記載してください。

## 背景・メモ
- 追加日時: $(Get-Date -Format "yyyy-MM-dd HH:mm")
$(if ($DueDate) { "- 期日: $DueDate" } else { "" })

## 完了条件
- [ ] タスクの完了条件を記載
"@

# ラベル
$Labels = "priority:$Priority,type:$Type"

Write-Host "タスクを作成中..." -ForegroundColor Cyan
Write-Host "タイトル: $Title" -ForegroundColor Yellow
Write-Host "ラベル: $Labels" -ForegroundColor Yellow
if ($DueDate) {
    Write-Host "期日: $DueDate" -ForegroundColor Yellow
}

try {
    # Step 1: Issue 作成
    Write-Host "`n[Step 1/4] Issue を作成中..." -ForegroundColor Cyan
    $IssueJson = gh issue create `
        --title $Title `
        --body $Body `
        --label $Labels `
        --repo banapagg/My-Tasks `
        --json number,url 2>&1

    if ($LASTEXITCODE -ne 0) {
        throw "Issue 作成に失敗しました: $IssueJson"
    }

    $Issue = $IssueJson | ConvertFrom-Json
    $IssueNumber = $Issue.number
    $IssueUrl = $Issue.url

    Write-Host "✅ Issue #$IssueNumber を作成しました" -ForegroundColor Green

    # Step 2: Project に追加
    Write-Host "`n[Step 2/4] Project に追加中..." -ForegroundColor Cyan
    $ItemJson = gh project item-add 1 `
        --owner banapagg `
        --url $IssueUrl `
        --format json 2>&1

    if ($LASTEXITCODE -ne 0) {
        throw "Project への追加に失敗しました: $ItemJson"
    }

    $Item = $ItemJson | ConvertFrom-Json
    $ItemId = $Item.id

    Write-Host "✅ Project に追加しました (Item ID: $ItemId)" -ForegroundColor Green

    # Step 3: ステータスを Todo に設定
    Write-Host "`n[Step 3/4] ステータスを設定中..." -ForegroundColor Cyan
    gh project item-edit `
        --project-id PVT_kwHOBIcCGs4BOrhY `
        --id $ItemId `
        --field-id PVTSSF_lAHOBIcCGs4BOrhYzg9T10o `
        --single-select-option-id f75ad846 2>&1 | Out-Null

    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ ステータス設定に失敗しました（タスクは作成済み）" -ForegroundColor Yellow
    } else {
        Write-Host "✅ ステータスを Todo に設定しました" -ForegroundColor Green
    }

    # Step 4: 期日設定（必要な場合）
    if ($DueDate) {
        Write-Host "`n[Step 4/4] 期日を設定中..." -ForegroundColor Cyan
        gh project item-edit `
            --project-id PVT_kwHOBIcCGs4BOrhY `
            --id $ItemId `
            --field-id PVTF_lAHOBIcCGs4BOrhYzg9Vv3k `
            --date $DueDate 2>&1 | Out-Null

        if ($LASTEXITCODE -ne 0) {
            Write-Host "⚠️ 期日設定に失敗しました（タスクは作成済み）" -ForegroundColor Yellow
        } else {
            Write-Host "✅ 期日を設定しました: $DueDate" -ForegroundColor Green
        }
    } else {
        Write-Host "`n[Step 4/4] 期日の設定はスキップしました" -ForegroundColor Gray
    }

    # 成功通知
    $Message = @"
✅ タスクを作成しました

Issue: #$IssueNumber 「$Title」
ラベル: $Labels
ステータス: Todo
$(if ($DueDate) { "期日: $DueDate" } else { "" })
URL: $IssueUrl
"@

    Write-Host "`n" -NoNewline
    Write-Host $Message -ForegroundColor Green

    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show($Message, "タスク作成完了", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)

} catch {
    $ErrorMessage = "❌ タスク作成に失敗しました`n`n$($_.Exception.Message)"
    Write-Host "`n$ErrorMessage" -ForegroundColor Red

    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show($ErrorMessage, "エラー", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)

    exit 1
}
