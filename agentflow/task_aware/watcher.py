import os
import time
import tkinter as tk
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from agentflow.memory import Memory
from agentflow.core.llm import LLM
import json
import asyncio

class AgentWatcher(FileSystemEventHandler):
    def __init__(self, memory: Memory, timeout: float = float('inf')):
        self.memory = memory
        self.timeout = timeout
        self.start_time = time.time()
        self.last_suggestion = 0
        self.cooldown = 5
        self.event_count = 0
        self.action_times = []
        self.llm = LLM(provider="ollama")
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window

    async def reason_suggestion(self, file_path: str) -> str:
        """Generate natural language suggestion using LLM."""
        file_type = os.path.splitext(file_path)[1]
        prompt = f"A developer modified a {file_type} file at {file_path}. Suggest an action in natural language, considering file type and context."
        try:
            return await self.llm.generate(prompt)
        except Exception as e:
            return f"Based on the {file_type} file, consider optimizing or debugging."

    def estimate_remaining_time(self) -> str:
        elapsed = time.time() - self.start_time
        remaining = self.timeout - elapsed if self.timeout != float('inf') else float('inf')
        history = self.memory.retrieve_json("watch_history")
        if history:
            avg_interval = sum(history["intervals"]) / len(history["intervals"]) if history["intervals"] else 60
            avg_action_time = sum(self.action_times) / len(self.action_times) if self.action_times else 10
            expected_events = remaining / avg_interval if remaining != float('inf') else 10
            estimated_time = expected_events * avg_action_time
            return f"Estimated time for {int(expected_events)} events: ~{int(estimated_time)} seconds"
        return f"Timeout in {int(remaining)} seconds" if remaining != float('inf') else "No timeout set"

    def on_modified(self, event):
        if time.time() - self.last_suggestion < self.cooldown or not event.src_path.endswith((".py", ".md", ".txt")):
            return
        
        self.event_count += 1
        file_type = os.path.splitext(event.src_path)[1]
        suggestions = {
            ".py": [
                ("optimize_agent", "Deploy code optimization agent"),
                ("debug_agent", "Deploy debug agent")
            ],
            ".md": [
                ("doc_agent", "Deploy documentation agent"),
                ("summarize_agent", "Deploy summarization agent")
            ],
            ".txt": [
                ("summarize_agent", "Deploy summarization agent")
            ]
        }.get(file_type, [])

        if not suggestions:
            return

        # Generate natural language suggestion
        suggestion_text = asyncio.run(self.reason_suggestion(event.src_path))
        response = messagebox.askyesno(
            "AgentFlow Suggestion",
            f"{suggestion_text}\n\nProceed with one of these actions?\n" + "\n".join(f"{i}. {desc}" for i, (_, desc) in enumerate(suggestions, 1)),
            parent=self.root
        )

        if response:
            choice = messagebox.askinteger("Select Action", f"Enter action number (1-{len(suggestions)}):", minvalue=1, maxvalue=len(suggestions))
            if choice and 1 <= choice <= len(suggestions):
                agent_name, _ = suggestions[choice - 1]
                start_action = time.time()
                os.system(f"python -m agentflow.cli deploy {agent_name} {event.src_path}")
                action_time = time.time() - start_action
                self.action_times.append(action_time)
                self.memory.store(f"last_task_{event.src_path}", agent_name)

                # Update watch history
                history = self.memory.retrieve_json("watch_history") or {"intervals": [], "events": 0}
                history["intervals"].append(time.time() - self.last_suggestion)
                history["events"] += 1
                self.memory.store_json("watch_history", history)
        
        self.last_suggestion = time.time()

def run_watcher(directory: str, timeout: float):
    """Run the watcher in a separate process."""
    memory = Memory()
    watcher = AgentWatcher(memory, timeout)
    observer = Observer()
    observer.schedule(watcher, directory, recursive=True)
    observer.start()
    print("[AgentFlow] Watching your workflow in background...")
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("[AgentFlow] Background watcher stopped.")