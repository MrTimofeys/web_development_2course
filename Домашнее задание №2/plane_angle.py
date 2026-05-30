from __future__ import annotations
import math

class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __sub__(self, no: "Point") -> "Point":
        return Point(self.x - no.x, self.y - no.y, self.z - no.z)

    def dot(self, no: "Point") -> float:
        return self.x * no.x + self.y * no.y + self.z * no.z

    def cross(self, no: "Point") -> "Point":
        return Point(
            self.y * no.z - self.z * no.y,
            self.z * no.x - self.x * no.z,
            self.x * no.y - self.y * no.x
        )

    def absolute(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def plane_angle(A: Point, B: Point, C: Point, D: Point) -> float:
    """Угол между плоскостями ABC и BCD в градусах."""
    BA = A - B
    BC = C - B
    CD = D - C
    X = BA.cross(BC)
    Y = BC.cross(CD)
    denom = X.absolute() * Y.absolute()
    if denom == 0:
        raise ValueError("Degenerate plane(s): normal vector has zero length")
    cos_phi = X.dot(Y) / denom
    # числовая устойчивость
    cos_phi = max(-1.0, min(1.0, cos_phi))
    return math.degrees(math.acos(cos_phi))

if __name__ == "__main__":
    # ввода в задании нет, оставляем как библиотечный модуль
    pass
