from __future__ import annotations
import math

class Complex(object):
    def __init__(self, real: float, imaginary: float):
        self.real = float(real)
        self.imaginary = float(imaginary)

    def __add__(self, no: "Complex") -> "Complex":
        return Complex(self.real + no.real, self.imaginary + no.imaginary)

    def __sub__(self, no: "Complex") -> "Complex":
        return Complex(self.real - no.real, self.imaginary - no.imaginary)

    def __mul__(self, no: "Complex") -> "Complex":
        a, b = self.real, self.imaginary
        c, d = no.real, no.imaginary
        return Complex(a * c - b * d, a * d + b * c)

    def __truediv__(self, no: "Complex") -> "Complex":
        a, b = self.real, self.imaginary
        c, d = no.real, no.imaginary
        denom = c * c + d * d
        if denom == 0:
            raise ZeroDivisionError("complex division by zero")
        return Complex((a * c + b * d) / denom, (b * c - a * d) / denom)

    def mod(self) -> "Complex":
        return Complex(math.sqrt(self.real ** 2 + self.imaginary ** 2), 0.0)

    def __str__(self) -> str:
        a = self.real
        b = self.imaginary
        sign = "+" if b >= 0 else "-"
        return f"{a:.2f}{sign}{abs(b):.2f}i"

if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    if len(data) != 4:
        raise SystemExit("Expected 4 numbers (two complex numbers)")
    a, b, c, d = map(float, data)
    C = Complex(a, b)
    D = Complex(c, d)
    print(C + D)
    print(C - D)
    print(C * D)
    print(C / D)
    print(C.mod())
    print(D.mod())
