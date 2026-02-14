import os
import json
import re
from google import genai
from google.genai import types
from core.registry import SkillRegistry
from core.conversation_history import ConversationHistory


class AnuEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model_name = "gemini-2.5-flash"  # Latest and fastest Gemini model
        self.history = ConversationHistory()

        self.system_instruction = (
            "You are ANU, a warm, caring, and intelligent AI assistant. "
            "You must use structured tool_calls whenever a tool is required. "
            "Never output tool calls as text or JSON. Use the function calling system. "
            "After tools execute, respond naturally and warmly. "
            "Be supportive, friendly, and empathetic."
        )

    # ============================================================
    # MAIN AGENT LOOP
    # ============================================================

    def run_conversation(self, user_prompt: str) -> str:

        self.history.add_message("user", user_prompt)

        recent_context = self.history.get_recent_context(num_messages=6)

        # Build Gemini-style messages
        messages = []
        
        for msg in recent_context:
            role = "user" if msg["role"] == "user" else "model"
            messages.append({"role": role, "parts": [{"text": msg["content"]}]})

        # Get tools schema and convert to Gemini format
        tools_schema = self.registry.get_tools_schema()
        
        # Convert OpenAI-style tools to Gemini format
        gemini_tools = None
        if tools_schema:
            function_declarations = []
            for tool in tools_schema:
                if tool.get("type") == "function":
                    func_def = tool.get("function", {})
                    function_declarations.append({
                        "name": func_def.get("name"),
                        "description": func_def.get("description", ""),
                        "parameters": func_def.get("parameters", {})
                    })
            
            if function_declarations:
                gemini_tools = [{"function_declarations": function_declarations}]

        generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 200
        }

        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            try:
                # Call Gemini API
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=messages,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        tools=gemini_tools if gemini_tools else None,
                        temperature=generation_config["temperature"],
                        max_output_tokens=generation_config["max_output_tokens"]
                    )
                )

            except Exception as e:
                print(f"Gemini API Error: {e}")
                import traceback
                traceback.print_exc()
                return "I'm having trouble thinking right now."

            if not response.candidates:
                return "I couldn't generate a response."
            
            candidate = response.candidates[0]
            
            if not candidate.content or not candidate.content.parts:
                return "I received an empty response."

            parts = candidate.content.parts

            # Check for function calls
            function_calls = []
            text_response = ""
            
            for part in parts:
                if hasattr(part, "function_call") and part.function_call:
                    function_calls.append(part.function_call)
                elif hasattr(part, "text") and part.text:
                    text_response += part.text

            # ============================================================
            # CASE 1: STRUCTURED TOOL CALLS
            # ============================================================

            if function_calls:
                print(f"\n🔧 Tool Execution (Iteration {iteration})")

                # Add model response to messages
                messages.append({"role": "model", "parts": parts})

                # Execute each function call
                function_responses = []
                
                for func_call in function_calls:
                    function_name = func_call.name
                    print(f"   Calling: {function_name}")
                    
                    function_to_call = self.registry.get_function(function_name)

                    if not function_to_call:
                        tool_result = {"error": f"Tool '{function_name}' not found."}
                    else:
                        try:
                            # Gemini provides args as a dict already
                            function_args = dict(func_call.args) if func_call.args else {}
                            tool_result = function_to_call(**function_args)
                            print(f"   Result: {str(tool_result)[:100]}")
                        except Exception as e:
                            tool_result = {"error": f"Tool execution error: {str(e)}"}
                            print(f"   Error: {e}")
                    
                    function_responses.append({
                        "function_response": {
                            "name": function_name,
                            "response": tool_result
                        }
                    })

                # Add function responses to messages
                messages.append({
                    "role": "user",
                    "parts": function_responses
                })

                continue  # Loop again to get final response

            # ============================================================
            # CASE 2: NORMAL TEXT RESPONSE
            # ============================================================

            if text_response:
                self.history.add_message("assistant", text_response)
                return text_response
            
            # If we get here with no text and no function calls, something's wrong
            return "I'm not sure how to respond to that."

        return "I completed as much as I could, but the task required too many steps."
