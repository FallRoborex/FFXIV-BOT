from random import choice, randint

def get_responce(user_input: str) -> str:
    lowered = str(user_input.lower())
    
    if lowered == "":
        return "Diogo is old!!!!"
    elif "hello" in lowered:
        return "Hello world, bitch!"
    elif "roll dice" in lowered:
        return f"You rolled: {randint(1, 20)}"
    else:
        return choice(["I don't understand what the hell you are talking about."])