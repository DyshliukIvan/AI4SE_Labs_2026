from mcp.server.fastmcp import FastMCP

server = FastMCP("task7_word_count")


@server.tool()
def count_words(text: str) -> int:
    """Count whitespace-separated words in text."""
    return len(text.split())


if __name__ == "__main__":
    server.run(transport="stdio")
