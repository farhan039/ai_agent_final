import random

SCHEDULE_TEMPLATES = [
    "Sure, we can get that done by {day}. Should I confirm?",
    "Yes, that can be scheduled for {day}. Want me to lock it in?",
    "Absolutely, we can aim for {day}. Can I go ahead and confirm?"
]

REFUND_TEMPLATES = [
    "It looks like you may need help with a refund. I'm escalating this to a human operator.",
    "Refund requests need special handling. Passing this to our support team now.",
    "Let me connect you to a human operator to process this refund."
]

GENERIC_TEMPLATES = [
    "Could you share a bit more detail so I can help?",
    "I want to make sure I understand. Can you clarify?",
    "Thanks for reaching out. Could you tell me more about this?"
]

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def local_ai_generate(history, user_input):
    text = user_input.lower()

    # Intent detection
    if "refund" in text or "money back" in text or "return" in text:
        return random.choice(REFUND_TEMPLATES), True  # escalate = True

    for day in DAYS:
        if day in text:
            return random.choice(SCHEDULE_TEMPLATES).format(day=day.title()), False

    if "schedule" in text or "finish by" in text or "deadline" in text:
        return random.choice(SCHEDULE_TEMPLATES).format(day="the requested day"), False

    return random.choice(GENERIC_TEMPLATES), False
