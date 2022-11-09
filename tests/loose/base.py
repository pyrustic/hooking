from hooking import H, ChainBreak


# =============== HOOKS ===============


def do_before_func(context, *args, **kwargs):
    if context.tag != "calc1":
        raise Exception("tag should be 'calc1'")
    if context.args[0] != 1:
        raise Exception("args[0] should be 1")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "+" or kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if context.target.__qualname__ != "calc1":
        raise Exception("qualname should be 'calc1'")


def do_after_func(context, *args, **kwargs):
    if context.tag != "calc1":
        raise Exception("tag should be 'calc1'")
    if context.args[0] != 1:
        raise Exception("args[0] should be 1")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "+" or kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if context.target.__qualname__ != "calc1":
        raise Exception("qualname should be 'calc1'")
    if context.result != 3:
        raise Exception("result should be 3")


def do_before_method(context, *args, **kwargs):
    if context.tag != "Calculator.calc1":
        raise Exception("tag should be 'Calculator.calc1'")
    if context.args[1] != 1:
        raise Exception("args[1] should be 1")
    if context.args[2] != 2:
        raise Exception("args[2] should be 2")
    if context.kwargs["op"] != "+" or kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if context.target.__qualname__ != "Calculator.calc1":
        raise Exception("qualname should be 'Calculator.calc1'")


def do_after_method(context, *args, **kwargs):
    if context.tag != "Calculator.calc1":
        raise Exception("tag should be 'Calculator.calc1'")
    if context.args[1] != 1:
        raise Exception("args[1] should be 1")
    if context.args[2] != 2:
        raise Exception("args[2] should be 2")
    if context.kwargs["op"] != "+" or kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if context.target.__qualname__ != "Calculator.calc1":
        raise Exception("qualname should be 'Calculator.calc1'")
    if context.result != 3:
        raise Exception("result should be 3")


def do_manip_before_1(context, *args, **kwargs):
    # manipulation
    context.args = (4, 2)
    context.kwargs = {"op": "*"}


def do_manip_before_2(context, *args, **kwargs):
    # manipulation
    calculator = Calculator()
    context.target = calculator.calc2


def do_manip_after(context, *args, **kwargs):
    # manipulation
    context.result = 42


def do_chain_break(context, *args, **kwargs):
    raise ChainBreak


def do_check_custom_tag_before(context, *args, **kwargs):
    if context.tag != "Calc2":
        raise Exception("tag should be 'Calc2'")
    if context.args[0] != 10:
        raise Exception("args[0] should be 10")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "/" or kwargs["op"] != "/":
        raise Exception("op should be '/'")
    if context.target.__qualname__ != "calc2":
        raise Exception("qualname should be 'calc2'")


def do_check_custom_tag_after(context, *args, **kwargs):
    if context.tag != "Calc2":
        raise Exception("tag should be 'Calc2'")
    if context.args[0] != 10:
        raise Exception("args[0] should be 10")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "/" or kwargs["op"] != "/":
        raise Exception("op should be '/'")
    if context.target.__qualname__ != "calc2":
        raise Exception("qualname should be 'calc2'")
    if context.result != 5:
        raise Exception("result should be 5")


def do_check_config_before(context, *args, **kwargs):
    if context.config != {"x": 1, "y": 2}:
        raise Exception("config should be {'x': 1, 'y': 2}")


def do_check_config_after(context, *args, **kwargs):
    if context.config != {"x": 1, "y": 2}:
        raise Exception("config should be {'x': 1, 'y': 2}")


# =============== TARGETS - LOOSE COUPLING ===============

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


@H.tag("Calc3", x=1, y=2)
def calc3(a, b, op):
    if op == "%":
        return a % b


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

    @H.tag("CalculatorCalc3", x=1, y=2)
    def calc3(self, a, b, op):
        if op == "%":
            return a % b


# ===== Subclassing H =====

CustomHookingClass = H.subclass("CustomHookingClass")


def do_something(context, name):
    pass


@CustomHookingClass.tag
def greet(name):
    return "Hello {}".format(name)
