class X:
    def __init__(self):
        pass

    def __repr__(self):
        return "X"

    def evaluate(self, x_value):
        # X evaluates to the provided x_value (wrapped as Int)
        return Int(x_value)

    def simplify(self):
        # X cannot be simplified further
        return self


class Int:
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return str(self.i)

    def evaluate(self, x_value):
        # Integer constants evaluate to themselves
        return Int(self.i)

    def simplify(self):
        # Int cannot be simplified further
        return self


class Add:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return repr(self.p1) + " + " + repr(self.p2)

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value)
        v2 = self.p2.evaluate(x_value)
        return Int(v1.i + v2.i)

    def simplify(self):
        s1 = self.p1.simplify()
        s2 = self.p2.simplify()

        # 0 + X -> X ; X + 0 -> X
        if isinstance(s1, Int) and s1.i == 0:
            return s2
        if isinstance(s2, Int) and s2.i == 0:
            return s1

        # 3 + 5 -> 8
        if isinstance(s1, Int) and isinstance(s2, Int):
            return Int(s1.i + s2.i)

        return Add(s1, s2)


class Mul:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        # Parenthesize additive/subtractive operands to preserve precedence
        def fmt(p):
            return "( " + repr(p) + " )" if isinstance(p, (Add, Sub)) else repr(p)

        return f"{fmt(self.p1)} * {fmt(self.p2)}"

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value)
        v2 = self.p2.evaluate(x_value)
        return Int(v1.i * v2.i)

    def simplify(self):
        s1 = self.p1.simplify()
        s2 = self.p2.simplify()

        # X * 0 -> 0 ; 0 * X -> 0
        if (isinstance(s1, Int) and s1.i == 0) or (isinstance(s2, Int) and s2.i == 0):
            return Int(0)

        # X * 1 -> X ; 1 * X -> X
        if isinstance(s1, Int) and s1.i == 1:
            return s2
        if isinstance(s2, Int) and s2.i == 1:
            return s1

        # 3 * 5 -> 15
        if isinstance(s1, Int) and isinstance(s2, Int):
            return Int(s1.i * s2.i)

        return Mul(s1, s2)


class Sub:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        # Parenthesize additive on the left; add/sub on the right (to avoid "a - (b - c)" ambiguity)
        left = f"( {repr(self.p1)} )" if isinstance(self.p1, Add) else repr(self.p1)
        right = (
            f"( {repr(self.p2)} )" if isinstance(self.p2, (Add, Sub)) else repr(self.p2)
        )
        return f"{left} - {right}"

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value)
        v2 = self.p2.evaluate(x_value)
        return Int(v1.i - v2.i)

    def simplify(self):
        s1 = self.p1.simplify()
        s2 = self.p2.simplify()

        # X - 0 -> X
        if isinstance(s2, Int) and s2.i == 0:
            return s1

        # 5 - 3 -> 2
        if isinstance(s1, Int) and isinstance(s2, Int):
            return Int(s1.i - s2.i)

        return Sub(s1, s2)


class Div:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        # Parenthesize if operand is Add or Sub to preserve precedence:
        # e.g., ( 10 - 2 ) / 4  not  10 - 2 / 4
        def fmt(p):
            return f"( {repr(p)} )" if isinstance(p, (Add, Sub)) else repr(p)

        return f"{fmt(self.p1)} / {fmt(self.p2)}"

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value)
        v2 = self.p2.evaluate(x_value)
        if v2.i == 0:
            raise ZeroDivisionError("division by zero")
        return Int(v1.i // v2.i)

    def simplify(self):
        s1 = self.p1.simplify()
        s2 = self.p2.simplify()

        # 0 / X -> 0 (if denominator nonzero at evaluation time; keep form if 0 to allow eval to raise)
        if isinstance(s1, Int) and s1.i == 0:
            if isinstance(s2, Int) and s2.i == 0:
                return Div(s1, s2)  # keep; evaluate() will raise if attempted
            return Int(0)

        # X / 1 -> X
        if isinstance(s2, Int) and s2.i == 1:
            return s1

        # 6 / 2 -> 3 (integer division)
        if isinstance(s1, Int) and isinstance(s2, Int):
            if s2.i == 0:
                return Div(s1, s2)  # keep; evaluate() will raise
            return Int(s1.i // s2.i)

        return Div(s1, s2)


# Original polynomial example
poly = Add(Add(Int(4), Int(3)), Add(X(), Mul(Int(1), Add(Mul(X(), X()), Int(1)))))
print("Original polynomial:", poly)

# Test new Sub and Div classes (will fail until implemented)
print("\n--- Testing Sub and Div classes ---")
try:
    sub_poly = Sub(Int(10), Int(3))
    print("Subtraction:", sub_poly)
except Exception as e:
    print("❌ Subtraction test failed - Sub class not implemented yet")

try:
    div_poly = Div(Int(15), Int(3))
    print("Division:", div_poly)
except Exception as e:
    print("❌ Division test failed - Div class not implemented yet")

# Test evaluation (will fail until implemented)
print("\n--- Testing evaluation ---")
try:
    simple_poly = Add(Sub(Mul(Int(2), X()), Int(1)), Div(Int(6), Int(2)))
    print("Test polynomial:", simple_poly)
    result = simple_poly.evaluate(4)
    print(f"Evaluation for X=4: {result}")
except Exception as e:
    print("❌ Evaluation test failed - evaluate methods not implemented yet")

try:
    original_result = poly.evaluate(2)
    print(f"Original polynomial evaluation for X=2: {original_result}")
except Exception as e:
    print(
        "❌ Original polynomial evaluation failed - evaluate methods not implemented yet"
    )

# Option to run comprehensive tests
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("\n" + "=" * 60)
        print("Running comprehensive test suite...")
        print("=" * 60)
        from test_polynomial import run_all_tests

        run_all_tests()
    else:
        print("\n💡 To run comprehensive tests, use: python polynomial.py --test")
        print("💡 Or run directly: python test_polynomial.py")
