class Tilt:
    def __init__(self) -> None:
        pass

    def state(self, accState):
        x, y, z = accState
        if x <= 100: return ["tilt", ["left"]]
        elif x >= 140: return ["tilt", ["right"]]
        if y <= 100: return ["tilt", ["up"]]
        elif y >= 135: return ["tilt", ["down"]]
        return ["", [""]]
