import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill


class TextSkill(Skill):
    """Skill for reading and summarizing text from files using Gemini AI."""

    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB safety limit
    MAX_CONTENT_CHARS = 5000         # limit for LLM

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")

    @property
    def name(self) -> str:
        return "text_skill"

    # ---------------- TOOL DEFINITIONS ---------------- #

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "summarize_file",
                    "description": "Read a text file and provide a summary",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Absolute or relative path to file"
                            }
                        },
                        "required": ["filepath"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file_content",
                    "description": "Read raw content of a text file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Absolute or relative path to file"
                            }
                        },
                        "required": ["filepath"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "summarize_file": self.summarize_file,
            "read_file_content": self.read_file_content
        }

    # ---------------- FILE READING ---------------- #

    def read_file_content(self, filepath: str) -> str:
        try:
            filepath = os.path.expanduser(filepath)

            # If relative path → check Desktop
            if not os.path.isabs(filepath):
                desktop_candidate = os.path.join(
                    os.path.expanduser("~"),
                    "Desktop",
                    filepath
                )
                if os.path.exists(desktop_candidate):
                    filepath = desktop_candidate

            if not os.path.exists(filepath):
                return json.dumps({
                    "status": "error",
                    "message": f"File not found: {filepath}"
                })

            if not os.path.isfile(filepath):
                return json.dumps({
                    "status": "error",
                    "message": f"Path is not a file: {filepath}"
                })

            # File size protection
            if os.path.getsize(filepath) > self.MAX_FILE_SIZE:
                return json.dumps({
                    "status": "error",
                    "message": "File too large (max 2MB allowed)"
                })

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            return json.dumps({
                "status": "success",
                "filepath": filepath,
                "content": content,
                "length": len(content)
            })

        except UnicodeDecodeError:
            return json.dumps({
                "status": "error",
                "message": "File is not a valid text file"
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error reading file: {str(e)}"
            })

    # ---------------- SUMMARIZATION ---------------- #

    def summarize_file(self, filepath: str) -> str:

        if not self.api_key:
            return json.dumps({
                "status": "error",
                "message": "GEMINI_API_KEY not set in environment variables"
            })

        read_result = json.loads(self.read_file_content(filepath))

        if read_result["status"] == "error":
            return json.dumps(read_result)

        content = read_result["content"]

        if len(content) < 100:
            return json.dumps({
                "status": "success",
                "summary": content
            })

        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)

            truncated_content = content[:self.MAX_CONTENT_CHARS]

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[{
                    "role": "user",
                    "parts": [{
                        "text": f"Summarize the following text clearly and concisely in 2-3 sentences:\n\n{truncated_content}"
                    }]
                }],
                config={"max_output_tokens": 200}
            )

            summary = response.text.strip()

            return json.dumps({
                "status": "success",
                "filepath": filepath,
                "summary": summary
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error generating summary: {str(e)}"
            })
