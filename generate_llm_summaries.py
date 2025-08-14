#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_llm_summaries.py

This script demonstrates how to use the OpenAI API to generate structured
summaries for a handful of news articles. Each summary is broken down
into three key sections: 問題設定 (problem setup), 手法 (methodology), and
結果 (results). The goal is to provide engineers with concise, high-level
insights that capture the essence of each article.

Requirements:
  - Python 3.8+
  - openai (pip install openai)
  - feedparser (optional, pip install feedparser) if you wish to pull
    articles from RSS feeds defined in feeds.yml.

Before running this script, set your OpenAI API key via the environment
variable OPENAI_API_KEY. You can obtain a key from https://platform.openai.com/.

Usage examples:

  # Summarise the latest 5 business articles defined in feeds.yml
  python3 generate_llm_summaries.py --feeds feeds.yml --category Business --count 5

  # Summarise arbitrary text snippets defined inline
  python3 generate_llm_summaries.py --text "Title1|This is the body of article 1" \
                                      --text "Title2|Another article body"

The script will print the structured summaries to stdout in a readable
format. None of the operations here modify your existing project files.
"""
import argparse
import os
import sys
import json
from typing import List, Tuple, Dict

# We defer importing openai until it is actually needed to avoid hard
# dependency when using the Gemini provider. If the import fails inside
# summarise_article_via_openai, a helpful error will be raised.
openai = None

# Optional: feedparser for RSS parsing
try:
    import feedparser  # type: ignore
except ImportError:
    feedparser = None


def load_articles_from_feed(feeds_file: str, category: str, count: int) -> List[Tuple[str, str]]:
    """Load articles from the specified category in feeds.yml using feedparser.

    Args:
        feeds_file: Path to the YAML file defining RSS feeds.
        category: Which category to pull (case-insensitive).
        count: Maximum number of articles to return.

    Returns:
        A list of tuples (title, summary) for the latest articles.
    """
    if feedparser is None:
        raise RuntimeError("feedparser is not installed. Install it via 'pip install feedparser'.")
    try:
        import yaml  # type: ignore
    except ImportError:
        raise RuntimeError("Missing dependency: PyYAML. Install it via 'pip install pyyaml'.")

    with open(feeds_file, "r", encoding="utf-8") as f:
        feeds = yaml.safe_load(f)
    if not isinstance(feeds, dict):
        raise ValueError(f"Invalid feeds file: {feeds_file}")

    # Gather URLs for the chosen category
    urls: List[str] = []
    for cat, entries in feeds.items():
        if cat.lower() == category.lower():
            for e in entries:
                url = e.get("url")
                if url:
                    urls.append(url)
            break

    articles: List[Tuple[str, str]] = []
    for url in urls:
        parsed = feedparser.parse(url)
        for entry in parsed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "") or entry.get("description", "")
            if title and summary:
                articles.append((title, summary))
                if len(articles) >= count:
                    return articles
    return articles


def summarise_article_via_openai(title: str, body: str, model: str = "gpt-3.5-turbo") -> Dict[str, str]:
    """Call the OpenAI Chat API to summarise a single article.

    Args:
        title: Article title.
        body: Article body (or summary) text.
        model: Which OpenAI model to use (e.g., 'gpt-3.5-turbo' or 'gpt-4').

    Returns:
        A dict with keys '問題設定', '手法', '結果', each containing a short Japanese summary.
    """
    # Lazy import of openai to avoid hard dependency when using Gemini provider
    global openai
    if openai is None:
        try:
            import openai as _openai  # type: ignore
            openai = _openai
        except ImportError:
            raise ImportError("Missing dependency: openai. Install it via 'pip install openai'.")

    system_prompt = (
        "あなたは技術ニュースの編集者です。入力された記事に対し、問題設定、手法、結果の3点に分けて"
        "日本語で簡潔にまとめてください。専門用語は適宜補足し、各項目は2〜3文程度に収めます。"
    )
    user_content = f"タイトル: {title}\n本文: {body}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    # API key must be set via OPENAI_API_KEY environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=512,
        )
        content = response.choices[0].message["content"].strip()
        # Expecting output in the form of separate sections labeled appropriately
        summary: Dict[str, str] = {}
        for line in content.splitlines():
            if line.startswith("問題設定"):
                summary["問題設定"] = line.split("：", 1)[-1].strip()
            elif line.startswith("手法"):
                summary["手法"] = line.split("：", 1)[-1].strip()
            elif line.startswith("結果"):
                summary["結果"] = line.split("：", 1)[-1].strip()
        return summary
    except Exception as e:
        print(f"[ERROR] Failed to summarise article '{title}': {e}", file=sys.stderr)
        return {}


def summarise_article_via_gemini(title: str, body: str, model: str = "gemini-pro") -> Dict[str, str]:
    """Use Google's Generative AI (Gemini) to summarise an article.

    This function requires the `google-generativeai` library (or the newer
    `google-genai` SDK) to be installed. You must set the `GOOGLE_API_KEY`
    environment variable with your Gemini Developer API key. Refer to the
    official documentation for details:
    https://googleapis.github.io/python-genai/

    Args:
        title: Article title.
        body: Article body or summary text.
        model: Name of the Gemini model to use (e.g., 'gemini-pro' or
            'gemini-2.0-flash-001').

    Returns:
        A dict with keys '問題設定', '手法', '結果'. Empty dict on failure.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY environment variable is not set.")
    # Attempt to import either google.generativeai or google_genai SDK
    try:
        # The official SDK prior to 2024 was named google.generativeai
        import google.generativeai as genai  # type: ignore
        use_genai = True
    except ImportError:
        try:
            # google-genai SDK uses google.genai
            from google import genai  # type: ignore
            use_genai = False
        except ImportError:
            raise ImportError(
                "Neither 'google-generativeai' nor 'google-genai' is installed. "
                "Install one of them via 'pip install google-generativeai' or 'pip install google-genai'."
            )

    # Configure client with API key
    if use_genai:
        # google.generativeai style
        genai.configure(api_key=api_key)
        # Create a generative model instance
        model_name = model or "gemini-pro"
        gmodel = genai.GenerativeModel(model_name)
        # Compose conversation: similar to system/user messages in OpenAI API
        system_prompt = (
            "あなたは技術ニュースの編集者です。入力された記事に対し、問題設定、手法、結果の3点に分けて"
            "日本語で簡潔にまとめてください。専門用語は適宜補足し、各項目は2〜3文程度に収めます。"
        )
        user_prompt = f"タイトル: {title}\n本文: {body}"
        try:
            response = gmodel.generate_content([
                system_prompt,
                user_prompt,
            ])
            content = response.text.strip()
        except Exception as e:
            print(f"[ERROR] Gemini summarisation failed for '{title}': {e}", file=sys.stderr)
            return {}
    else:
        # google-genai style using genai.Client
        client = genai.Client(api_key=api_key)
        model_name = model or "gemini-pro"
        # Build message string by combining system and user instructions
        system_prompt = (
            "あなたは技術ニュースの編集者です。入力された記事に対し、問題設定、手法、結果の3点に分けて"
            "日本語で簡潔にまとめてください。専門用語は適宜補足し、各項目は2〜3文程度に収めます。"
        )
        user_prompt = f"タイトル: {title}\n本文: {body}"
        try:
            # The generate_content API accepts a list of message segments
            resp = client.models.generate_content(
                model=model_name,
                contents=[system_prompt, user_prompt],
            )
            # Access text depending on library version
            content = getattr(resp, "text", None) or getattr(resp, "result", "")
            content = content.strip()
        except Exception as e:
            print(f"[ERROR] Gemini summarisation failed for '{title}': {e}", file=sys.stderr)
            return {}

    # Parse the response into our structured fields
    summary: Dict[str, str] = {}
    for line in content.splitlines():
        if line.startswith("問題設定"):
            summary["問題設定"] = line.split("：", 1)[-1].strip()
        elif line.startswith("手法"):
            summary["手法"] = line.split("：", 1)[-1].strip()
        elif line.startswith("結果"):
            summary["結果"] = line.split("：", 1)[-1].strip()
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate structured LLM summaries for news articles.")
    parser.add_argument("--feeds", type=str, help="Path to feeds.yml to fetch articles from")
    parser.add_argument("--category", type=str, default="Business", help="Category name in feeds.yml (Business, Tools, Posts)")
    parser.add_argument("--count", type=int, default=5, help="Number of articles to summarise (default: 5)")
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "gemini"],
        default="openai",
        help="LLM provider to use: 'openai' or 'gemini' (default: openai)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help=(
            "Model name to use. For OpenAI, specify gpt-3.5-turbo or gpt-4. "
            "For Gemini, specify gemini-pro or gemini-2.0-flash-001. If omitted, a reasonable default is used."
        ),
    )
    parser.add_argument("--text", action="append", help="Inline article as 'Title|Body'. Can be specified multiple times.")
    args = parser.parse_args()

    articles: List[Tuple[str, str]] = []

    # If inline text is provided, use it; else load from feeds
    if args.text:
        for item in args.text:
            if "|" not in item:
                print(f"Ignoring invalid text input: {item}", file=sys.stderr)
                continue
            title, body = item.split("|", 1)
            articles.append((title.strip(), body.strip()))
    elif args.feeds:
        articles = load_articles_from_feed(args.feeds, args.category, args.count)
    else:
        parser.error("Either --text or --feeds must be provided.")

    if not articles:
        print("No articles to summarise.", file=sys.stderr)
        return

    summaries: List[Dict[str, str]] = []
    for title, body in articles[: args.count]:
        if args.provider == "openai":
            model_name = args.model or "gpt-3.5-turbo"
            summary = summarise_article_via_openai(title, body, model=model_name)
        else:  # gemini
            model_name = args.model or "gemini-pro"
            summary = summarise_article_via_gemini(title, body, model=model_name)
        summaries.append({"title": title, **summary})

    # Print results as JSON for easy parsing
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()