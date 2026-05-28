class UDSFSystem:
    def __init__(self):
        self.layers = ["system", "state", "dynamics", "equilibrium"]

    def get_framework(self):
        return self.layers