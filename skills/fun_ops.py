"""
Fun and Entertainment Skill - Jokes, facts, quotes, compliments
"""
import random
from typing import List, Dict, Any, Callable
from core.skill import Skill


JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "What do you call a fake noodle? An impasta!",
    "Why did the bicycle fall over? Because it was two-tired!",
    "What do you call a can opener that doesn't work? A can't opener!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
]

FUN_FACTS = [
    "Honey never spoils! Archaeologists have found 3,000-year-old honey in Egyptian tombs that's still edible.",
    "Octopuses have three hearts and blue blood!",
    "Bananas are berries, but strawberries aren't!",
    "A group of flamingos is called a 'flamboyance'!",
    "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion!",
    "Dolphins have names for each other!",
    "The shortest war in history lasted only 38 to 45 minutes!",
    "A day on Venus is longer than a year on Venus!",
    "The world's largest desert is Antarctica, not the Sahara!",
    "Butterflies can taste with their feet!",
]

MOTIVATIONAL_QUOTES = [
    "Believe you can and you're halfway there!",
    "The only way to do great work is to love what you do!",
    "Don't watch the clock; do what it does. Keep going!",
    "Success is not final, failure is not fatal: it is the courage to continue that counts!",
    "You are stronger than you think!",
    "Every day is a new beginning!",
    "Dream big, work hard, stay focused!",
    "You've got this! I believe in you!",
]

COMPLIMENTS = [
    "You're absolutely amazing!",
    "You light up every room you enter!",
    "You have the best laugh!",
    "Your smile is contagious!",
    "You're incredibly smart!",
    "You're so creative and talented!",
    "You make the world a better place!",
]


class FunSkill(Skill):
    
    @property
    def name(self) -> str:
        return "fun_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "tell_joke",
                    "description": "Tell a funny joke",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fun_fact",
                    "description": "Share an interesting fun fact",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "motivate",
                    "description": "Share a motivational quote",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "compliment",
                    "description": "Give a nice compliment",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "tell_joke": self.tell_joke,
            "fun_fact": self.fun_fact,
            "motivate": self.motivate,
            "compliment": self.compliment
        }

    def tell_joke(self) -> dict:
        """Tell a random joke"""
        joke = random.choice(JOKES)
        return {"status": "success", "message": f"😄 {joke}"}

    def fun_fact(self) -> dict:
        """Share a fun fact"""
        fact = random.choice(FUN_FACTS)
        return {"status": "success", "message": f"🤓 {fact}"}

    def motivate(self) -> dict:
        """Share motivational quote"""
        quote = random.choice(MOTIVATIONAL_QUOTES)
        return {"status": "success", "message": f"💪 {quote}"}

    def compliment(self) -> dict:
        """Give a compliment"""
        compliment_msg = random.choice(COMPLIMENTS)
        return {"status": "success", "message": f"✨ {compliment_msg}"}


def register():
    """Register the Fun skill"""
    return FunSkill()
