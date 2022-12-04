from typing import List

class DimensionIterator:
    def __init__(self, dim_) -> None:
        self._dim = dim_
        self._index = 0

    def __next__(self):
        if self._index < len(self._dim):
            self._index += 1
            return self._dim.x_y_z[self._index - 1]
        raise StopIteration

class MetaFoo(type):
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("__"):
                yield attr

class Dimension(metaclass=MetaFoo):
    def __init__(self, x_y_z: List[int]):
        self.x_y_z = x_y_z
        self.rotation_idx = 0

    def __eq__(self, other):
        if type(other) is type(self):
            if len(self) == len(other):
                for d_1, d_2 in zip(self.x_y_z, other.x_y_z):
                    if d_1 != d_2:
                        return False
                return True
        return False 
    
    def __le__(self, other):
        if type(other) is type(self):
            if len(self) == len(other):
                for d_1, d_2 in zip(self.x_y_z, other.x_y_z):
                    if d_1 > d_2:
                        return False
                return True
        return False
    
    def __len__(self):
        return len(self.x_y_z)
    
    def __str__(self):
        return str(self.x_y_z)
    
    def __add__(self, other, dim_number=None, full=False):
        if type(other) is type(self):
            if len(self) == len(other):
                if full:
                    return Dimension([d_1+ d_2
                    for (d_1, d_2) in zip(self.x_y_z, other.x_y_z)])
                if dim_number is None:
                    return [Dimension(list(self.x_y_z[:i]) + [d_1 + d_2] + list(self.x_y_z[i + 1:])) 
                    for i, (d_1, d_2) in enumerate(zip(self.x_y_z, other.x_y_z))]
                else:
                    if dim_number >= len(self):
                        return None
                    return [Dimension(list(self.x_y_z[:i]) + [d_1 + d_2] + list(self.x_y_z[i + 1:])) 
                    for i, (d_1, d_2) in enumerate(zip(self.x_y_z, other.x_y_z))][dim_number]
        return None
    
    def __iter__(self):
        return DimensionIterator(self)

    def rotate(self, idx_: int = None):
        if idx_ is None:
            tmp_idx = self.rotation_idx % 3
            self.upd_rotation_idx()
        else:
            tmp_idx = idx_
        tmp_el = self.x_y_z[tmp_idx]
        
        self.x_y_z = self.x_y_z[:tmp_idx] + self.x_y_z[tmp_idx + 1:]
        self.x_y_z.reverse()
        self.x_y_z.insert(tmp_idx, tmp_el)
    
    def upd_rotation_idx(self):
        self.rotation_idx = (self.rotation_idx + 1) % 6