from random import choice, randint

def get_response(user_input: str) -> str:
    lowered = str(user_input.lower())
    
    if lowered == "":
        return "Diogo is old!!!!"
    elif "hello" in lowered:
        return "Hello world, bitch!"
    elif "roll dice" in lowered:
        return f"You rolled: {randint(1, 20)}"
    elif "how old is Diogo":
        return "Older then the milky way"
    else:
        return choice(["I don't understand what the hell you are talking about."])