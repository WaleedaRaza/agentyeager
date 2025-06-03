import os
import shutil
from typing import Optional
from agentflow.memory import Memory

class SkillMarketplace:
    def __init__(self, memory: Memory, marketplace_dir: str = "~/.agentflow/marketplace"):
        self.memory = memory
        self.marketplace_dir = os.path.expanduser(marketplace_dir)
        os.makedirs(self.marketplace_dir, exist_ok=True)

    def pull(self, skill_name: str) -> Optional[str]:
        """Pull a skill from the local marketplace to the project's skills directory."""
        skill_path = os.path.join(self.marketplace_dir, f"{skill_name}.py")
        if not os.path.exists(skill_path):
            return f"Skill {skill_name} not found in marketplace"
        
        project_skills_dir = os.path.join(os.getcwd(), "agentflow", "skills")
        os.makedirs(project_skills_dir, exist_ok=True)
        dest_path = os.path.join(project_skills_dir, f"{skill_name}.py")
        shutil.copy(skill_path, dest_path)
        
        self.memory.store(f"skill_pulled_{skill_name}", dest_path)
        return f"Pulled skill {skill_name} to {dest_path}"

    def push(self, skill_name: str) -> str:
        """Push a skill from the project's skills directory to the local marketplace."""
        project_skill_path = os.path.join(os.getcwd(), "agentflow", "skills", f"{skill_name}.py")
        if not os.path.exists(project_skill_path):
            return f"Skill {skill_name} not found in project"
        
        dest_path = os.path.join(self.marketplace_dir, f"{skill_name}.py")
        shutil.copy(project_skill_path, dest_path)
        
        self.memory.store(f"skill_pushed_{skill_name}", dest_path)
        return f"Pushed skill {skill_name} to marketplace"