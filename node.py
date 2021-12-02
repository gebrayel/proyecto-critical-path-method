class  Node:

    def __init__(self, id: int, description: str, duration: float, predecesores: list) -> None:
        self.id = id
        self.description = description
        self.visitedForward = False
        self.visitedBackward = False
        self.duration = duration
        self.pred = predecesores
        self.suces = []
        self.es = 0 
        self.ef = 0
        self.ls = 0
        self.lf = 0
        self.holgura = 0


    def visitForward (self):
        self.visitedForward = True

    def visitBackward (self):
        self.visitedBackward = True

    def add_predecesor (self, pred: int):
        self.pred.append(pred)

    def add_sucesor (self, suc:int):
        self.suces.append(suc)

    def set_description(self, description: str):
        self.description = description

    def set_es(self, es: float):
        self.es = es

    def set_ef(self, ef: float):
        self.ef = ef

    def set_ls(self, ls: float):
        self.ls = ls

    def set_lf(self, lf: float):
        self.lf = lf


    def set_holgura(self, holgura: int):
        self.holgura = holgura
