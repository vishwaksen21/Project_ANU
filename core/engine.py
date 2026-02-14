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
            "Use the provided tools to answer the user's request effectively. "
            "When using tools, output VALID JSON arguments only. "
            "Do NOT output the tool call as XML or with an equals sign. "
            "Just use the standard tool calling format provided by the API. "
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
                
                # Add assistant response to history
                self.history.add_message("assistant", response_text)
                
                return response_text
        
        # Max iterations reached
        return "I completed as much as I could, but the task required too many steps."
