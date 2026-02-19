# ネタ収集コマンド

今日のテクノロジートレンドを収集し、`ideas/daily/YYYYMMDD-trend.md` に保存する。

## 手順

### 1. 準備

```bash
mkdir -p ideas/daily
TODAY=$(date +%Y%m%d)
OUTPUT="ideas/daily/${TODAY}-trend.md"
```

### 2. データ収集

以下のソースから並行してデータを取得する。
**JSON解析は必ず `python3` を使うこと（`jq` は使わない）。**
各ソースの取得に失敗しても黙ってスキップし、エラーメッセージは出力しない。

#### はてブ IT ホットエントリ（RSS）

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
  python3 -c "import sys,json; ids=json.load(sys.stdin)[:5]; print(' '.join(map(str,ids)))" 2>/dev/null)

# 各ストーリーの詳細を取得
for id in $HN_IDS; do
  curl -s --max-time 5 "https://hacker-news.firebaseio.com/v0/item/${id}.json" | \
    python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    title=d.get('title','')
    url=d.get('url', f'https://news.ycombinator.com/item?id={d.get(\"id\",\"\")}')
    score=d.get('score',0)
    if title:
        print(f'- [{title}]({url}) ({score}pt)')
except Exception:
    pass
" 2>/dev/null
done
```

#### Reddit プログラミング（old.reddit.com）

```bash
curl -s --max-time 10 -A "Mozilla/5.0" "https://old.reddit.com/r/programming.json?limit=5" | \
  python3 -c "
import sys,json
try:
    data=json.load(sys.stdin)
    for child in data['data']['children'][:5]:
        d=child['data']
        title=d.get('title','')
        url=d.get('url','')
        score=d.get('score',0)
        if title:
            print(f'- [{title}]({url}) ({score}pt)')
except Exception:
    pass
" 2>/dev/null
```

#### セキュリティブログ（RSS）

```bash
for feed_url in \
  "https://www.wiz.io/blog/rss.xml" \
  "https://www.aikido.dev/blog/rss"; do
  curl -s --max-time 10 "$feed_url" | \
    python3 -c "
import sys, xml.etree.ElementTree as ET
try:
    root = ET.fromstring(sys.stdin.read())
    # Atom形式
    ns_atom = '{http://www.w3.org/2005/Atom}'
    entries = root.findall(f'{ns_atom}entry')
    if entries:
        for e in entries[:2]:
            title = e.find(f'{ns_atom}title')
            link = e.find(f'{ns_atom}link')
            if title is not None and link is not None:
                print(f'- [{title.text}]({link.get(\"href\",\"\")})')
    else:
        # RSS 2.0形式
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

収集したデータをまとめて以下の形式で `ideas/daily/YYYYMMDD-trend.md` に保存すること：

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

### 4. 完了報告

保存したファイルパスと、発信候補のサマリーを報告する。

## 注意事項

- `jq` コマンドは使わない（インストール不要な `python3` を使う）
- 各ソースの取得失敗は無視してスキップ（エラーメッセージは出力しない）
- Reddit は `old.reddit.com` の JSON エンドポイントを使用（`www.reddit.com` は403になる）
- User-Agent ヘッダー（`-A "Mozilla/5.0"`）を必ず付与する
