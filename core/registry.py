import os
import importlib.util
import inspect
from typing import Dict, List, Any, Callable
from .skill import Skill

class SkillRegistry:
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.tools_schema: List[Dict[str, Any]] = []
        self.functions: Dict[str, Callable] = {}

    def load_skills(self, skills_dir: str, context: Dict[str, Any] = None):
        """Dynamically load skills from the specified directory."""
        if not os.path.exists(skills_dir):
            print(f"Skills directory not found: {skills_dir}")
            return

        for filename in os.listdir(skills_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                file_path = os.path.join(skills_dir, filename)
                self._load_skill_from_file(module_name, file_path, context)

    def _load_skill_from_file(self, module_name: str, file_path: str, context: Dict[str, Any] = None):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # First try to find register() function (new simpler pattern)
            if hasattr(module, 'register'):
                try:
                    skill_instance = module.register()  # Call without self
                    if skill_instance:
                        self.register_skill(skill_instance)
                        print(f"Loaded skill: {skill_instance.name}")
                    return  # Successfully registered using function pattern
                except Exception as e:
                    print(f"Failed to register skill {module_name}: {e}")
            
            # Fall back to class-based skills
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Skill) and obj is not Skill:
                    try:
                        skill_instance = obj()
                        if context:
                            skill_instance.initialize(context)
                        self.register_skill(skill_instance)
                        print(f"Loaded skill: {skill_instance.name}")
                    except Exception as e:
                        print(f"Failed to load skill {name}: {e}")

    def register_skill(self, skill: Skill):
        self.skills[skill.name] = skill
        self.tools_schema.extend(skill.get_tools())
        self.functions.update(skill.get_functions())
    
    def register(self, name: str, func: Callable, description: str, 
                 parameters: Dict[str, Any], required: List[str]):
        """Simple function registration for new-style skills"""
        # Add to functions dict
        self.functions[name] = func
        
        # Create tool schema
        tool_schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": required
                }
            }
        }
        self.tools_schema.append(tool_schema)

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        return self.tools_schema

    def get_function(self, name: str) -> Callable:
        return self.functions.get(name)
