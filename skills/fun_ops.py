"""
Jokes and Fun Skill - Tell jokes and fun facts
"""
import random

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

def tell_joke() -> dict:
    """
    Tell a random joke.
    
    Returns:
        A funny joke
    """
    joke = random.choice(JOKES)
    return {"status": "success", "message": joke}

def fun_fact() -> dict:
    """
    Share a random fun fact.
    
    Returns:
        An interesting fun fact
    """
    fact = random.choice(FUN_FACTS)
    return {"status": "success", "message": f"Here's a fun fact: {fact}"}

def motivate() -> dict:
    """
    Share a motivational quote.
    
    Returns:
        A motivational message
    """
    quote = random.choice(MOTIVATIONAL_QUOTES)
    return {"status": "success", "message": quote}

def compliment() -> dict:
    """
    Give a nice compliment to brighten someone's day.
    
    Returns:
        A sweet compliment
    """
    compliments = [
        "You're doing an amazing job today!",
        "Your smile is contagious!",
        "You light up the room!",
        "You're incredibly thoughtful and kind!",
        "You have excellent taste!",
        "You're more helpful than you realize!",
        "You're a great friend!",
        "Your positive attitude is inspiring!",
    ]
    compliment_msg = random.choice(compliments)
    return {"status": "success", "message": compliment_msg}

def register():
    """Register fun skills"""
    from core.skill import Skill
    skill = Skill("fun")
    skill.register(
        name="tell_joke",
        func=tell_joke,
        description="Tell a funny joke to make you laugh",
        parameters={},
        required=[]
    )
    
    skill.register(
        name="fun_fact",
        func=fun_fact,
        description="Share an interesting fun fact",
        parameters={},
        required=[]
    )
    
    skill.register(
        name="motivate",
        func=motivate,
        description="Share a motivational quote to inspire",
        parameters={},
        required=[]
    )
    
    skill.register(
        name="compliment",
        func=compliment,
        description="Give a nice compliment",
        parameters={},
        required=[]
    )

    print("Loaded skill: fun_skill")
    return skill
