from ..lib._eptlsoot import CTempFlameSolver, CTempFlameSolverVector

class TempFlameSolver(CTempFlameSolver):
    def __init__(self, soot_gas, flame, grid, soot_model):
        super().__init__(soot_gas, flame, grid, soot_model)


class TempFlameSolverVector(CTempFlameSolverVector):
    def __init__(self, soot_gas, flame, grid, soot_model):
        super().__init__(soot_gas, flame, grid, soot_model)