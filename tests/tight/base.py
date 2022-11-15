from hooking import wrap, on_enter, on_leave, override


# =============== HOOKS ===============


def do_before_func(context, *args, **kwargs):
    if context.args[0] != 1:
        raise Exception("args[0] should be 1")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "+" or kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if not context.target.__qualname__.startswith("calc"):
        raise Exception("qualname should start with 'calc'")
    if context.config != {"x": 1, "y": 2}:
        raise Exception("config should be {'x': 1, 'y': 2}")


def do_after_func(context, *args, **kwargs):
    if context.args[0] != 1:
        raise Exception("args[0] should be 1")
    if context.args[1] != 2:
        raise Exception("args[1] should be 2")
    if context.kwargs["op"] != "+" or kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if not context.target.__qualname__.startswith("calc"):
        raise Exception("qualname should start with 'calc'")
    if context.config != {"x": 1, "y": 2}:
        raise Exception("config should be {'x': 1, 'y': 2}")
    if context.result != 3:
        raise Exception("result should be 3")


def do_before_method(context, *args, **kwargs):
    if context.args[1] != 1:
        raise Exception("args[1] should be 1")
    if context.args[2] != 2:
        raise Exception("args[2] should be 2")
    if context.kwargs["op"] != "+" or kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if not context.target.__qualname__.startswith("Calculator.calc"):
        raise Exception("qualname should start with 'Calculator.calc'")
    if context.config != {"x": 1, "y": 2}:
        raise Exception("config should be {'x': 1, 'y': 2}")


def do_after_method(context, *args, **kwargs):
    if context.args[1] != 1:
        raise Exception("args[1] should be 1")
    if context.args[2] != 2:
        raise Exception("args[2] should be 2")
    if context.kwargs["op"] != "+" or kwargs["op"] != "+":
        raise Exception("op should be '+'")
    if not context.target.__qualname__.startswith("Calculator.calc"):
        raise Exception("qualname should start with 'Calculator.calc'")
    if context.config != {"x": 1, "y": 2}:
        raise Exception("config should be {'x': 1, 'y': 2}")
    if context.result != 3:
        raise Exception("result should be 3")


def do_manip_before_func(context, *args, **kwargs):
    context.target = lambda a, b, op: a * b


def do_manip_after_func(context, *args, **kwargs):
    context.result += 40


def do_manip_before_method(context, *args, **kwargs):
    context.target = lambda self, a, b, op: a * b


def do_manip_after_method(context, *args, **kwargs):
    context.result += 40


def do_override(context, *args, **kwargs):
    context.result = context.target(*args, **kwargs)


# =============== TARGETS - TIGHT COUPLING ===============


@wrap(do_before_func, do_after_func, x=1, y=2)
def calc1(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b


@on_enter(do_before_func, x=1, y=2)
def calc2(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b


@on_leave(do_after_func, x=1, y=2)
def calc3(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b


@wrap(do_manip_before_func, do_manip_after_func, x=1, y=2)
def calc4(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b


@override(do_override)
def calc5(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b


class Calculator:

    @wrap(do_before_method, do_after_method, x=1, y=2)
    def calc1(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b

    @on_enter(do_before_method, x=1, y=2)
    def calc2(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b

    @on_leave(do_after_method, x=1, y=2)
    def calc3(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b

    @on_leave(do_after_method, x=1, y=2)
    def calc3(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b

    @wrap(do_manip_before_method, do_manip_after_method, x=1, y=2)
    def calc4(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b        
            
    @override(do_override)
    def calc5(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b
