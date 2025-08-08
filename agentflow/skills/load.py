import importlib.util
import os
from .base import Skill

def load_skill(skill_name: str) -> Skill:
    try:
        if os.path.isfile(skill_name):
            spec = importlib.util.spec_from_file_location("skill_module", skill_name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for attr in dir(module):
                skill = getattr(module, attr)
                if isinstance(skill, Skill):
                    return skill
        else:
            module = importlib.import_module(f"agentflow.skills.{skill_name}")
            skill = getattr(module, skill_name)
            return skill
    except Exception as e:
        raise ValueError(f"Failed to load skill {skill_name}: {str(e)}")