from typing import List

# List of crisis-related keywords
CRISIS_KEYWORDS: List[str] = [
    "suicidal", "suicide", "kill myself", "want to die", "hopeless",
    "worthless", "can't go on", "give up", "ending it all", "no reason to live"
]

# Safety message to show if a crisis keyword is detected
SAFETY_MESSAGE = (
    "It sounds like you're going through a really tough time.\n"
    "You're not alone, and there are people who want to help you.\n"
    "Please consider reaching out to a mental health professional or contacting a helpline:\n\n"
    "1926 - National Mental Health Helpline-SriLanka\n"
)

def contains_crisis_keywords(text: str) -> bool:
    """Check if the input text contains any crisis-related keywords."""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in CRISIS_KEYWORDS)