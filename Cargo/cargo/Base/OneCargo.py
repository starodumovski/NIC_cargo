
class OneCargo:
    def __init__(self, dim_1:float, dim_2:float, dim_3:float, weight:float, dim_restricted = None) -> None:
        try:
            self.measure = list(map(float, [dim_1, dim_2, dim_3]))
        except ValueError as e:
            print(e, "dimensions")
            exit()
        try:
            self.weight = float(weight)
        except ValueError as e:
            print(e, "weight")
            exit()
        self.dim_restricted = dim_restricted if str(dim_restricted).isdigit() else None

        self.rotation_idx = 0

    def rotate(self):
        if self.dim_restricted is None:
            self.rotate_cont()
        else:
            self.rotate_cont(self.dim_restricted)
    
    def rotate_cont(self, idx_: int = None):
        if idx_ is None:
            tmp_idx = self.rotation_idx % 3
            self.upd_rotation_idx()
        else:
            tmp_idx = idx_
        tmp_el = self.measure[tmp_idx]
        
        self.measure = self.measure[:tmp_idx] + self.measure[tmp_idx + 1:]
        self.measure.reverse()
        self.measure.insert(tmp_idx, tmp_el)

    def upd_rotation_idx(self):
        self.rotation_idx = (self.rotation_idx + 1) % 6

    