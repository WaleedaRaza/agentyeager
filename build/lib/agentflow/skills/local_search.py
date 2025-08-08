from .base import skill
import os

@skill
async def local_search(query: str) -> str:
    """Search local files for a query."""
    try:
        results = []
        for root, _, files in os.walk("."):
            for file in files:
                if query.lower() in file.lower():
                    results.append(os.path.join(root, file))
        return f"Found {len(results)} files: {', '.join(results[:3])}" if results else "No files found"
    except Exception as e:
        return f"Search error: {str(e)}"