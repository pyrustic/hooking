# test the loose coupling paradigm
import unittest
from tests.loose import base
from hooking import H


class WrapCase(unittest.TestCase):

    def setUp(self):
        H.wrap("calc1", base.do_before_func, base.do_after_func)
        H.wrap("Calculator.calc1", base.do_before_method, base.do_after_method)

    def tearDown(self):
        H.reset()

    def test_func(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(3, result)

    def test_method(self):
        calculator = base.Calculator()
        result = calculator.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class OnEnterCase(unittest.TestCase):

    def setUp(self):
        H.on_enter("calc1", base.do_before_func)
        H.on_enter("Calculator.calc1", base.do_before_method)

    def tearDown(self):
        H.reset()

    def test_func(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(3, result)

    def test_method(self):
        calculator = base.Calculator()
        result = calculator.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class OnLeaveCase(unittest.TestCase):

    def setUp(self):
        H.on_leave("calc1", base.do_after_func)
        H.on_leave("Calculator.calc1", base.do_after_method)

    def tearDown(self):
        H.reset()

    def test_func(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(3, result)

    def test_method(self):
        calculator = base.Calculator()
        result = calculator.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class UnbindCase(unittest.TestCase):
    def setUp(self):
        hid1 = H.on_enter("calc1", base.do_manip_before_1)
        hid2, hid3 = H.wrap("calc1", base.do_manip_before_2, base.do_manip_after)
        H.unbind(hid1, hid3)

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc1(1, 2, op="*")
        self.assertEqual(2, result)


class HookManipulationBeforeCase(unittest.TestCase):
    def setUp(self):
        H.on_enter("calc1", base.do_manip_before_1)
        H.on_enter("calc1", base.do_manip_before_2)

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(8, result)


class HookManipulationAfterCase(unittest.TestCase):
    def setUp(self):
        H.on_leave("calc1", base.do_manip_after)

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(42, result)


class ChainBreakingCase(unittest.TestCase):
    def setUp(self):
        H.on_enter("calc1", base.do_chain_break)
        H.on_enter("calc1", base.do_manip_before_1)
        H.on_enter("calc1", base.do_manip_before_2)

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class FreezeCase(unittest.TestCase):
    def setUp(self):
        H.on_enter("calc1", base.do_manip_before_1)
        H.on_enter("calc1", base.do_manip_before_2)
        H.freeze()

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class UnfreezeCase(unittest.TestCase):
    def setUp(self):
        H.freeze()
        H.on_enter("calc1", base.do_manip_before_1)
        H.on_enter("calc1", base.do_manip_before_2)
        H.unfreeze()

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(8, result)


class CustomTagBeforeCase(unittest.TestCase):
    def setUp(self):
        H.on_enter("Calc2", base.do_check_custom_tag_before)

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc2(10, 2, op="/")
        self.assertEqual(5, result)


class CustomTagAfterCase(unittest.TestCase):
    def setUp(self):
        H.on_leave("Calc2", base.do_check_custom_tag_after)

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc2(10, 2, op="/")
        self.assertEqual(5, result)


class TagDataBeforeCase(unittest.TestCase):
    def setUp(self):
        H.on_enter("Calc3", base.do_check_config_before)

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc3(10, 2, op="%")
        self.assertEqual(0, result)


class TagDataAfterCase(unittest.TestCase):
    def setUp(self):
        H.on_leave("Calc3", base.do_check_config_after)

    def tearDown(self):
        H.reset()

    def test(self):
        result = base.calc3(10, 2, op="%")
        self.assertEqual(0, result)


class ClearCase(unittest.TestCase):
    def setUp(self):
        H.on_enter("calc1", base.do_manip_before_1)
        H.on_enter("calc1", base.do_manip_before_2)
        H.clear("calc1")

    def tearDown(self):
        pass

    def test(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class ResetCase(unittest.TestCase):
    def setUp(self):
        H.on_enter("calc1", base.do_manip_before_1)
        H.on_enter("calc1", base.do_manip_before_2)
        H.reset()

    def tearDown(self):
        pass

    def test(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class SubclassCase(unittest.TestCase):
    def setUp(self):
        H.on_enter("greet", base.do_something)
        H.freeze()
        base.CustomHookingClass.on_enter("greet", base.do_something)

    def tearDown(self):
        H.reset()
        base.CustomHookingClass.reset()

    def test_greet(self):
        result = base.greet("Alex")
        self.assertEqual("Hello Alex", result)

    def test_inheritance(self):
        self.assertTrue(issubclass(base.CustomHookingClass, H))

    def test_vars(self):
        self.assertTrue(H.frozen)
        self.assertFalse(base.CustomHookingClass.frozen)
        self.assertEqual(6, len(H.tags))
        self.assertEqual(1, len(base.CustomHookingClass.tags))
        self.assertEqual(1, len(H.hooks))
        self.assertEqual(1, len(base.CustomHookingClass.hooks))
        self.assertEqual(6, len(H.targets))
        self.assertEqual(1, len(base.CustomHookingClass.targets))


if __name__ == '__main__':
    unittest.main()
