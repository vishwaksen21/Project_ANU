import os
import json
import re
from groq import Groq
from core.registry import SkillRegistry
from core.conversation_history import ConversationHistory

class AnuEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = "llama-3.3-70b-versatile"
        self.history = ConversationHistory()  # Add conversation history
        
        self.system_instruction = (
            "You are ANU, a helpful, friendly, and intelligent AI assistant with a warm, caring personality. "
            "You have a sweet, gentle voice and communicate with warmth and empathy. "
            "You are like a supportive friend who is always ready to help with a positive attitude. "
            "Use the provided tools to help the user effectively. "
            "IMPORTANT: You MUST use the tool calling system - do NOT write JSON in your response text. "
            "When you need to use a tool, let the system handle it automatically. "
            "After tools execute, provide a warm, natural response about what you did. "
            "Speak naturally and warmly, as if you're a caring companion who genuinely wants to help. "
            "Use encouraging phrases and be supportive in your responses. "
            "Always be polite, patient, and understanding. "
            "Remember previous conversations to provide context-aware responses."
        )

    def run_conversation(self, user_prompt: str) -> str:
        # Add user message to history
        self.history.add_message("user", user_prompt)
        
        # Get recent context from history
        recent_context = self.history.get_recent_context(num_messages=6)  # Last 3 exchanges
        
        # Build messages with context
        messages = [{"role": "system", "content": self.system_instruction}]
        
        # Add recent context for continuity
        for msg in recent_context[:-1]:  # Exclude the last one (current message)
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_prompt})
        
        try:
            tools_schema = self.registry.get_tools_schema()
            
            completion_kwargs = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": 200
            }
            
            if tools_schema:
                completion_kwargs["tools"] = tools_schema
                completion_kwargs["tool_choice"] = "auto"
            
            response = self.client.chat.completions.create(**completion_kwargs)
        except Exception as e:
            # Handle tool_use_failed error from Groq
            error_str = str(e)
            if "tool_use_failed" in error_str and "failed_generation" in error_str:
                try:
                    match = re.search(r"<function=(\w+)(?:.*?)(?=\{)(\{.*?\})<\/function>", error_str)
                    if match:
                        func_name = match.group(1)
                        func_args_str = match.group(2)
                        print(f"DEBUG: Recovered failed tool call: {func_name} with {func_args_str}")
                        
                        function_to_call = self.registry.get_function(func_name)
                        if function_to_call:
                            try:
                                args = json.loads(func_args_str)
                                res = function_to_call(**args)
                                return str(res)
                            except Exception as exec_e:
                                return f"Error executing recovered tool: {exec_e}"
                except Exception as parse_e:
                    print(f"Failed to recover tool call: {parse_e}")

            print(f"Groq API Error: {e}")
            return "I am having trouble connecting to the brain, sir."

        # 🔥 PROPER AGENT LOOP: Keep processing until no more tool calls
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # CASE 1: AI wants to use tools
            if tool_calls:
                print(f"DEBUG: Tool Execution (Iteration {iteration})...")
                messages.append(response_message)

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    print(f"DEBUG: AI calling: {function_name}")
                    
                    function_to_call = self.registry.get_function(function_name)
                    
                    if not function_to_call:
                        res = "Error: Tool not found."
                        print(f"DEBUG: Tool {function_name} not found in registry.")
                    else:
                        try:
                            function_args = json.loads(tool_call.function.arguments)
                            print(f"DEBUG: Tool arguments: {function_args}")
                            
                            if function_args is None:
                                function_args = {}
                                
                            res = function_to_call(**function_args)
                            print(f"DEBUG: Tool Output: {str(res)[:100]}...")
                        except Exception as e:
                            res = f"Error executing tool: {e}"
                            print(f"DEBUG: Tool Execution Error: {e}")

                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": str(res),
                        }
                    )
                
                # Get next response - might have more tool calls!
                try:
                    completion_kwargs = {
                        "model": self.model_name,
                        "messages": messages,
                        "max_tokens": 200
                    }
                    
                    if tools_schema:
                        completion_kwargs["tools"] = tools_schema
                        completion_kwargs["tool_choice"] = "auto"
                    
                    response = self.client.chat.completions.create(**completion_kwargs)
                except Exception as e:
                    print(f"Error in tool continuation: {e}")
                    return "I had trouble continuing the task."
                    
                # Loop continues to check if new response has more tool calls
        
            # CASE 2: AI wants to chat (no more tool calls)
            else:
                response_text = response_message.content
                
                # 🔥 FALLBACK: Check if model output JSON tool calls as text
                if response_text and '{"type": "function"' in response_text:
                    print("⚠️  WARNING: Model output tool calls as text instead of using API")
                    print(f"Raw response: {response_text[:200]}")
                    
                    # Try to parse and execute manually
                    try:
                        # Extract JSON objects from text
                        import re
                        json_pattern = r'\{"type":\s*"function"[^}]*"name":\s*"([^"]+)"[^}]*"parameters":\s*(\{[^}]*\})\}'
                        matches = re.findall(json_pattern, response_text)
                        
                        if matches:
                            print(f"Found {len(matches)} tool calls in text, executing manually...")
                            
                            for func_name, params_str in matches:
                                function_to_call = self.registry.get_function(func_name)
                                
                                if function_to_call:
                                    try:
                                        params = json.loads(params_str) if params_str != '{}' else {}
                                        print(f"Manually executing: {func_name}({params})")
                                        res = function_to_call(**params)
                                        print(f"Result: {str(res)[:100]}")
                                        
                                        # Update response_text with result
                                        response_text = str(res)
                                    except Exception as e:
                                        print(f"Error executing manual tool call: {e}")
                                        response_text = f"I tried to {func_name} but encountered an error."
                        
                    except Exception as e:
                        print(f"Failed to parse manual tool calls: {e}")
                
                # Add assistant response to history
                self.history.add_message("assistant", response_text)
                
                return response_text
        
        # Max iterations reached
        return "I completed as much as I could, but the task required too many steps."
