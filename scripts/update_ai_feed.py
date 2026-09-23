"""Collect public release notes and recent AI-tool news leads for the static site."""

from __future__ import annotations

import email.utils
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = [
    "openai/openai-python",
    "anthropics/anthropic-sdk-python",
    "vercel/ai",
    "langchain-ai/langchain",
    "modelcontextprotocol/typescript-sdk",
    "ollama/ollama",
]
NEWS_QUERIES = [
    ("news:zh", "AI 开发工具 发布 更新 when:7d", "zh-CN", "CN", "CN:zh-Hans"),
    ("news:en", "AI developer tools SDK release when:7d", "en-US", "US", "US:en"),
]
NEWS_TITLE_PATTERN = re.compile(
    r"(AI|GPT|Claude|MCP|SDK|API|developer|coding|copilot|agent|model|open.source|"
    r"开发|编程|智能体|模型|工具|发布|上线|升级)",
    re.IGNORECASE,
)
USER_AGENT = "SignalPatch/1.0 (+https://github.com/YoungEWBOK)"


def fetch(url: str, accept: str | None = None) -> bytes:
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    token = os.environ.get("GITHUB_TOKEN", "")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=18) as response:
        return response.read(2_000_000)


def github_releases(repo: str) -> list[dict]:
    url = f"https://api.github.com/repos/{repo}/releases?per_page=8"
    payload = json.loads(fetch(url, "application/vnd.github+json"))
    if not isinstance(payload, list):
        raise ValueError(f"Unexpected GitHub response for {repo}")
    return [
        {
            "source": repo,
            "name": release.get("name") or release.get("tag_name") or "New release",
            "tag_name": release.get("tag_name") or "Release",
            "body": release.get("body") or "",
            "published_at": release["published_at"],
            "html_url": release["html_url"],
            "kind": "release",
        }
        for release in payload
        if release.get("published_at") and release.get("html_url") and not release.get("draft")
    ]


def news_leads(source: str, query: str, hl: str, gl: str, ceid: str) -> list[dict]:
    params = urllib.parse.urlencode({"q": query, "hl": hl, "gl": gl, "ceid": ceid})
    document = ET.fromstring(fetch(f"https://news.google.com/rss/search?{params}", "application/rss+xml"))
    cutoff = datetime.now(timezone.utc) - timedelta(days=8)
    items = []
    for item in document.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        date_text = item.findtext("pubDate") or ""
        publisher = (item.findtext("source") or "新闻来源").strip()
        try:
            published = email.utils.parsedate_to_datetime(date_text).astimezone(timezone.utc)
        except (TypeError, ValueError):
            continue
        if not title or not link or published < cutoff or not NEWS_TITLE_PATTERN.search(title):
            continue
        if not link.startswith("https://news.google.com/"):
            continue
        items.append(
            {
                "source": source,
                "name": title,
                "tag_name": publisher,
                "body": "新闻检索线索；请打开原文核实内容与发布时间。",
                "published_at": published.isoformat().replace("+00:00", "Z"),
                "html_url": link,
                "kind": "news",
            }
        )
    return items[:12]


def write_drafts(items: list[dict], day: str) -> None:
    selected = [item for item in items if item["kind"] == "release"][:6]
    links = "\n".join(
        f"{index}. {item['name']}（{item['source']}）\n   {item['html_url']}"
        for index, item in enumerate(selected, 1)
    )
    text = (
        f"# {day} AI 工具更新发布草稿\n\n"
        "以下根据官方发布标题自动生成，仅供人工核对后发布。请勿直接把版本更新当成产品功能结论。\n\n"
        "## 小红书图文草稿\n\n"
        "标题：今天有哪些 AI 开发工具更新？\n\n"
        f"正文：整理了今天值得查看的官方发布记录：\n\n{links}\n\n"
        "我会持续跟踪这些工具的版本变化。使用前请点击原文查看完整变更。\n\n"
        "#AI工具 #开发者工具 #版本更新\n\n"
        "## 微信公众号草稿\n\n"
        f"标题：AI 工具更新速览｜{day}\n\n"
        "导语：以下内容来自项目官方 GitHub Releases。本文只汇总发布记录，不替代原文说明。\n\n"
        f"{links}\n\n"
        "结语：以上链接可用于逐项核查版本详情。\n"
    )
    target = ROOT / "drafts" / "ai-updates" / f"{day}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def main() -> int:
    now = datetime.now(timezone.utc)
    items: list[dict] = []
    errors = []
    for repo in REPOSITORIES:
        try:
            items.extend(github_releases(repo))
        except Exception as exc:
            errors.append(f"{repo}: {exc}")
    for args in NEWS_QUERIES:
        try:
            items.extend(news_leads(*args))
        except Exception as exc:
            errors.append(f"{args[0]}: {exc}")
    if not items:
        print("No sources returned data; existing feed was preserved.", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1

    # The same story may appear in both language queries or more than one source.
    unique = {}
    for item in items:
        key = re.sub(r"\W+", " ", item["name"].casefold()).strip()
        unique.setdefault((item["kind"], key), item)
    items = sorted(unique.values(), key=lambda x: x["published_at"], reverse=True)
    payload = {
        "generated_at": now.isoformat().replace("+00:00", "Z"),
        "source_count": len(REPOSITORIES) + len(NEWS_QUERIES) - len(errors),
        "items": items,
    }
    output = ROOT / "static" / "ai-updates" / "data" / "updates.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_drafts(items, now.date().isoformat())
    print(f"Collected {len(items)} records from {payload['source_count']} sources")
    if errors:
        print("Partial source failures: " + "; ".join(errors), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

