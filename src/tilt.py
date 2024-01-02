class Tilt:
    def __init__(self) -> None:
        self.prevState = None

    def state(self, accState, log):
        if accState != self.prevState:
            log(accState)
            self.prevState = accState
