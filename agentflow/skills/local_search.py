from agentflow.skills import skill
import os
import glob

@skill
async def local_search(query: str) -> str:
    """Search for files locally matching the query."""
    try:
        # Simple file search in current directory
        search_path = os.getcwd()
        matches = []
        for file in glob.glob(os.path.join(search_path, f"*{query}*")):
            matches.append(os.path.basename(file))
        if matches:
            return f"Found files: {', '.join(matches)}"
        return "No matching files found."
    except Exception as e:
        return f"Local search error: {str(e)}"