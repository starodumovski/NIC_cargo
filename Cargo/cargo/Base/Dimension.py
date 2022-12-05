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
    def __init__(self, x_y_z: List[int], dim_restricted = None):
        self.x_y_z = x_y_z
        self.dim_restricted = dim_restricted if str(dim_restricted).isdigit() else None
        if dim_restricted is None:
            self.rotations_available = [i for i in range(6)]
        else:
            self.rotations_available = [0, self.dim_restricted * 2 + 1]
    
    def rotate(self, rotation_idx: int):
        to_return = self.x_y_z[- (rotation_idx//2):] + self.x_y_z[:- (rotation_idx//2)]
        to_return = to_return[0:1] + to_return[1:][:: -1 if rotation_idx % 2 else 1]
        return Dimension(to_return)
    
    def has_restricted_dim(self):
        if self.dim_restricted is None:
            return False
        return True

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
