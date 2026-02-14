"""
Conversation History Management for ANU
Saves and loads chat history for context-aware responses
"""

import json
import os
from datetime import datetime
from typing import List, Dict

class ConversationHistory:
    def __init__(self, history_file="conversation_history.json", max_messages=100):
        self.history_file = history_file
        self.max_messages = max_messages
        self.messages = []
        self.load_history()
    
    def add_message(self, role: str, content: str):
        """Add a message to history (role: 'user' or 'assistant')"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        
        # Keep only last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        
        self.save_history()
    
    def get_recent_context(self, num_messages=10) -> List[Dict]:
        """Get recent messages for context"""
        return self.messages[-num_messages:] if self.messages else []
    
    def get_all_messages(self) -> List[Dict]:
        """Get all messages"""
        return self.messages
    
    def clear_history(self):
        """Clear all conversation history"""
        self.messages = []
        self.save_history()
    
    def save_history(self):
        """Save history to JSON file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.messages, f, indent=2)
        except Exception as e:
            print(f"Error saving conversation history: {e}")
    
    def load_history(self):
        """Load history from JSON file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.messages = json.load(f)
                print(f"Loaded {len(self.messages)} messages from history")
        except Exception as e:
            print(f"Error loading conversation history: {e}")
            self.messages = []
    
    def get_summary(self) -> str:
        """Get a summary of conversation history"""
        if not self.messages:
            return "No conversation history"
        
        user_messages = len([m for m in self.messages if m['role'] == 'user'])
        assistant_messages = len([m for m in self.messages if m['role'] == 'assistant'])
        
        if self.messages:
            first_msg = datetime.fromisoformat(self.messages[0]['timestamp'])
            last_msg = datetime.fromisoformat(self.messages[-1]['timestamp'])
            return f"History: {user_messages} user messages, {assistant_messages} assistant messages. From {first_msg.strftime('%Y-%m-%d %H:%M')} to {last_msg.strftime('%Y-%m-%d %H:%M')}"
        
        return "No history available"
