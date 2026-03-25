from __future__ import annotations

import logging
import sys
from typing import Any

import wikipedia
from mcp.server.fastmcp import FastMCP

# IMPORTANT: never print to stdout in stdio mode
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

mcp = FastMCP(
    "wikipedia-research",
    stateless_http=True,
    json_response=True
)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

# Wikipedia config
wikipedia.set_lang("en")
wikipedia.set_rate_limiting(True)


def _load_page(title: str):
    return wikipedia.page(title=title, auto_suggest=True, redirect=True, preload=True)


@mcp.tool()
def search_wikipedia(query: str, limit: int = 5) -> dict[str, Any]:
    """Search Wikipedia article titles."""
    try:
        results, suggestion = wikipedia.search(query, results=limit, suggestion=True)
        return {
            "query": query,
            "suggestion": suggestion,
            "results": results,
        }
    except wikipedia.exceptions.WikipediaException as e:
        return {"error": str(e)}


@mcp.tool()
def get_article_summary(query: str, sentences: int = 3) -> dict[str, Any]:
    """Get a short summary of a topic."""
    try:
        page = wikipedia.page(query, auto_suggest=True, redirect=True)
        summary = wikipedia.summary(query, sentences=sentences)

        return {
            "title": page.title,
            "url": page.url,
            "summary": summary,
        }

    except wikipedia.exceptions.DisambiguationError as e:
        return {
            "error": "disambiguation",
            "options": e.options[:10],
        }

    except wikipedia.exceptions.PageError:
        return {
            "error": "not_found",
            "suggestion": wikipedia.suggest(query),
        }


@mcp.tool()
def list_sections(title: str) -> dict[str, Any]:
    """List top-level sections of an article."""
    try:
        page = _load_page(title)
        return {
            "title": page.title,
            "sections": page.sections,
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_section_content(title: str, section: str) -> dict[str, Any]:
    """Get content of a specific section."""
    try:
        page = _load_page(title)
        content = page.section(section)

        if not content:
            return {
                "error": "section_not_found",
                "available_sections": page.sections,
            }

        return {
            "title": page.title,
            "section": section,
            "content": content,
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
