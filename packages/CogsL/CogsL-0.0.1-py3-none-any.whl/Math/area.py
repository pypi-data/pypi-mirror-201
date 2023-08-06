class Area:
    def __init__(self, height: int):
        self.height = height

    def square(self) -> int:
        out = self.height * self.height
        return out

    def rectangle(self, width: int) -> int:
        out = self.height * width
        return out

    def parallelogram(self, width: int) -> int:
        out = self.height * width
        return out

    def trapezium(self, above: int, under: int) -> int:
        out = self.height * (above + under)
        return out

    def round(self, radius: int) -> float:
        out = radius * radius * 3.14
        return out

    def cuboid(self, length: int, width: int) -> int:
        out = (length * width + length * self.height + width * self.height) * 2
        return out

    def cube(self) -> int:
        out = self.height * self.height * 6
        return out

    def cylinder(self, radius: int) -> float:
        out = self.height * radius * 2 * 3.14 + radius * radius * 3.14 * 2
        return out
