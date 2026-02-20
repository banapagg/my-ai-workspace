# ネタ収集コマンド

今日のテクノロジートレンドを収集し、`ideas/daily/YYYYMMDD-trend.md` に保存する。

## 手順

### 1. 準備

ファイルが既に存在する場合は連番サフィックスを付与して新規作成する（上書き禁止）。

```bash
mkdir -p ideas/daily
TODAY=$(date +%Y%m%d)
BASE="ideas/daily/${TODAY}-trend"
OUTPUT="${BASE}.md"
n=2
while [ -f "$OUTPUT" ]; do
  OUTPUT="${BASE}-${n}.md"
  n=$((n+1))
done

# JSON 解析ヘルパー（jq 優先、なければ python3 にフォールバック）
parse_json() {
  local jq_filter="$1"
  local py_code="$2"
  if command -v jq >/dev/null 2>&1; then
    jq -r "$jq_filter" 2>/dev/null
  else
    python3 -c "$py_code" 2>/dev/null
  fi
}
```

### 2. データ収集

以下のソースからデータを取得する。
**JSON 解析は `jq` を使う。`jq` がない場合のみ `python3` にフォールバック（メッセージは出力しない）。**
**XML（RSS）の解析は `python3` を使う（jq は XML 非対応）。**
各ソースの取得に失敗しても黙ってスキップし、エラーメッセージは出力しない。

#### はてブ IT ホットエントリ（RSS / XML）

```bash
curl -s --max-time 10 "https://b.hatena.ne.jp/hotentry/it.rss" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
try:
    root = ET.fromstring(sys.stdin.read())
    ns = {'rss': 'http://purl.org/rss/1.0/', 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}
    items = root.findall('rss:item', ns)[:5]
    for i in items:
        title = i.find('rss:title', ns)
        link = i.find('rss:link', ns)
        if title is not None and link is not None:
            print(f'- [{title.text}]({link.text})')
except Exception:
    pass
"
```

#### Hacker News Top（JSON API）

```bash
# Top story IDを5件取得
HN_IDS=$(curl -s --max-time 10 "https://hacker-news.firebaseio.com/v0/topstories.json" | \
  parse_json \
    '.[0:5][]' \
    'import sys,json; [print(i) for i in json.load(sys.stdin)[:5]]')

# 各ストーリーの詳細を取得
for id in $HN_IDS; do
  curl -s --max-time 5 "https://hacker-news.firebaseio.com/v0/item/${id}.json" | \
    parse_json \
      '"- [" + .title + "](" + (.url // ("https://news.ycombinator.com/item?id=" + (.id|tostring))) + ") (" + (.score|tostring) + "pt)"' \
      'import sys,json
try:
    d=json.load(sys.stdin)
    url=d.get("url","https://news.ycombinator.com/item?id="+str(d.get("id","")))
    print(f"- [{d.get(\"title\",\"\")}]({url}) ({d.get(\"score\",0)}pt)")
except Exception: pass'
done
```

#### Reddit プログラミング（old.reddit.com / JSON）

```bash
curl -s --max-time 10 -A "Mozilla/5.0" "https://old.reddit.com/r/programming.json?limit=5" | \
  parse_json \
    '.data.children[:5][].data | "- [" + .title + "](" + .url + ") (" + (.score|tostring) + "pt)"' \
    'import sys,json
try:
    data=json.load(sys.stdin)
    for c in data["data"]["children"][:5]:
        d=c["data"]
        print(f"- [{d.get(\"title\",\"\")}]({d.get(\"url\",\"\")}) ({d.get(\"score\",0)}pt)")
except Exception: pass'
```

#### セキュリティブログ（RSS / XML）

```bash
for feed_url in \
  "https://www.wiz.io/blog/rss.xml" \
  "https://www.aikido.dev/blog/rss"; do
  curl -s --max-time 10 "$feed_url" | \
    python3 -c "
import sys, xml.etree.ElementTree as ET
try:
    root = ET.fromstring(sys.stdin.read())
    ns_atom = '{http://www.w3.org/2005/Atom}'
    entries = root.findall(f'{ns_atom}entry')
    if entries:
        for e in entries[:2]:
            title = e.find(f'{ns_atom}title')
            link = e.find(f'{ns_atom}link')
            if title is not None and link is not None:
                print(f'- [{title.text}]({link.get(\"href\",\"\")})')
    else:
        items = root.findall('.//item')[:2]
        for item in items:
            title = item.find('title')
            link = item.find('link')
            if title is not None and link is not None:
                print(f'- [{title.text}]({link.text})')
except Exception:
    pass
" 2>/dev/null
done
```

### 3. 結果をMarkdownに保存

収集したデータをまとめて以下の形式で保存すること：

```markdown
# トレンドネタ収集 YYYY-MM-DD

## はてブ IT ホットエントリ Top 5
（収集結果）

## Hacker News Top
（収集結果）

## Reddit r/programming
（収集結果）

## セキュリティブログ
（収集結果）

## 発信候補 Top 5

上記から特に注目度・独自性・技術的深さの高いネタを5件選び、以下の形式で整理する：

1. **タイトル案** — 理由（1行）
2. ...
```

### 4. My-Tasks に Issue 登録

収集した MD ファイルの内容をそのまま Issue 本文として `banapagg/My-Tasks` に登録し、Project 1 に追加する。

```bash
ISSUE_URL=$(gh issue create \
  --repo banapagg/My-Tasks \
  --title "$(date +%Y%m%d) のネタ候補" \
  --label "type:idea" \
  --body "$(cat "$OUTPUT")")

gh project item-add 1 --owner banapagg --url "$ISSUE_URL"
```

### 5. 完了報告

保存したファイルパス・作成した Issue URL・発信候補のサマリーを報告する。

## 注意事項

- JSON 解析は `jq` を使う（`jq` がない場合のみ `python3` にフォールバック、メッセージは出力しない）
- XML（RSS）解析は `python3` を使う（jq は XML 非対応）
- 各ソースの取得失敗は無視してスキップ（エラーメッセージは出力しない）
- Reddit は `old.reddit.com` の JSON エンドポイントを使用（`www.reddit.com` は403になる）
- User-Agent ヘッダー（`-A "Mozilla/5.0"`）を必ず付与する
- **既存ファイルは上書きしない**（同日2回目以降は `-2`, `-3` ... と連番を付ける）
