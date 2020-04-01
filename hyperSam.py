import numpy as np
import math as math
class hyperSam:
    def __init__(self,func1,func2):
        self.func1 = func1
        self.func2 = func2
    def getSam(self):
        tmp = self.func1.astype(np.float64)
        self.func2 = self.func2.astype(np.float64)
        print(np.dot(tmp,self.func2))
        print(np.linalg.norm(self.func2))
        errRadians = math.acos(np.dot(tmp,self.func2) / (np.linalg.norm(self.func2)*np.linalg.norm(tmp)))
        return errRadians