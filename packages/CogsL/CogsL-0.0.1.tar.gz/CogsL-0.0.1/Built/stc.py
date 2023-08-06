def stc(data: str) -> str:
    try:
        out = str(eval(data))
        return out
    except TypeError:
        print("[Interpreter/ERROR]:The parameter type is wrong, the parameter should be of type str")
