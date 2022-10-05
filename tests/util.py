from hooking import H, ChainBreak


def hook1_before(context):
    if context.tag != "calc1":
        raise Exception("tag should be 'calc1'")
    if context.args[0] != 1:
        raise Exception("args[0] should be 1")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if context.target.__qualname__ != "calc1":
        raise Exception("qualname should be 'calc1'")


def hook1_after(context):
    if context.tag != "calc1":
        raise Exception("tag should be 'calc1'")
    if context.args[0] != 1:
        raise Exception("args[0] should be 1")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if context.target.__qualname__ != "calc1":
        raise Exception("qualname should be 'calc1'")
    if context.result != 3:
        raise Exception("result should be 3")


def hook2_before(context):
    if context.tag != "Calculator.calc1":
        raise Exception("tag should be 'Calculator.calc1'")
    if context.args[1] != 1:
        raise Exception("args[1] should be 1")
    if context.args[2] != 2:
        raise Exception("args[2] should be 2")
    if context.kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if context.target.__qualname__ != "Calculator.calc1":
        raise Exception("qualname should be 'Calculator.calc1'")


def hook2_after(context):
    if context.tag != "Calculator.calc1":
        raise Exception("tag should be 'Calculator.calc1'")
    if context.args[1] != 1:
        raise Exception("args[1] should be 1")
    if context.args[2] != 2:
        raise Exception("args[2] should be 2")
    if context.kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if context.target.__qualname__ != "Calculator.calc1":
        raise Exception("qualname should be 'Calculator.calc1'")
    if context.result != 3:
        raise Exception("result should be 3")


def hook3_manip_before(context):
    # manipulation
    context.args = (4, 2)
    context.kwargs = {"op": "*"}


def hook4_manip_before(context):
    # manipulation
    calculator = Calculator()
    context.target = calculator.calc2


def hook5_manip_after(context):
    # manipulation
    context.result = 42


def hook6_breaker(context):
    raise ChainBreak


def hook7_custom_tag_before(context):
    if context.tag != "Calc2":
        raise Exception("tag should be 'Calc2'")
    if context.args[0] != 10:
        raise Exception("args[0] should be 10")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "/":
        raise Exception("op should be '/'")
    if context.target.__qualname__ != "calc2":
        raise Exception("qualname should be 'calc2'")


def hook8_custom_tag_after(context):
    if context.tag != "Calc2":
        raise Exception("tag should be 'Calc2'")
    if context.args[0] != 10:
        raise Exception("args[0] should be 10")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "/":
        raise Exception("op should be '/'")
    if context.target.__qualname__ != "calc2":
        raise Exception("qualname should be 'calc2'")
    if context.result != 5:
        raise Exception("result should be 5")


@H.tag
def calc1(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b


@H.tag("Calc2")
def calc2(a, b, op):
    if op == "*":
        return a + b
    if op == "/":
        return a // b


class Calculator:

    @H.tag
    def calc1(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b

    @H.tag("CalculatorCalc2")
    def calc2(self, a, b, op):
        if op == "*":
            return a * b
        if op == "/":
            return a // b
