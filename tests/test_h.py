import unittest
from tests import util
from hooking import H, BEFORE, AFTER


class BindBeforeCase(unittest.TestCase):

    def setUp(self):
        H.bind("calc1", util.hook1_before, spec=BEFORE)
        H.bind("Calculator.calc1", util.hook2_before, spec=BEFORE)

    def tearDown(self):
        H.clear()

    def test_hook1(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(3, result)

    def test_hook2(self):
        calculator = util.Calculator()
        result = calculator.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class BindAfterCase(unittest.TestCase):

    def setUp(self):
        H.bind("calc1", util.hook1_after, spec=AFTER)
        H.bind("Calculator.calc1", util.hook2_after, spec=AFTER)

    def tearDown(self):
        H.clear()

    def test_hook1(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(3, result)

    def test_hook2(self):
        calculator = util.Calculator()
        result = calculator.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class HookManipulationBeforeCase(unittest.TestCase):
    def setUp(self):
        H.bind("calc1", util.hook3_manip_before, spec=BEFORE)
        H.bind("calc1", util.hook4_manip_before, spec=BEFORE)

    def tearDown(self):
        H.clear()

    def test_hook(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(8, result)


class HookManipulationAfterCase(unittest.TestCase):
    def setUp(self):
        H.bind("calc1", util.hook5_manip_after, spec=AFTER)

    def tearDown(self):
        H.clear()

    def test_hook(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(42, result)


class UnbindCase(unittest.TestCase):
    def setUp(self):
        hid1 = H.bind("calc1", util.hook3_manip_before, spec=BEFORE)
        H.bind("calc1", util.hook4_manip_before, spec=BEFORE)
        H.unbind(hid1)

    def tearDown(self):
        H.clear()

    def test_calc(self):
        result = util.calc1(1, 2, op="*")
        self.assertEqual(2, result)


class UnbindAllCase(unittest.TestCase):
    def setUp(self):
        H.bind("calc1", util.hook3_manip_before, spec=BEFORE)
        H.bind("calc1", util.hook4_manip_before, spec=BEFORE)
        H.unbind()

    def tearDown(self):
        H.clear()

    def test_calc(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class ClearCase(unittest.TestCase):
    def setUp(self):
        H.bind("calc1", util.hook3_manip_before, spec=BEFORE)
        H.bind("calc1", util.hook4_manip_before, spec=BEFORE)
        H.clear()

    def tearDown(self):
        pass

    def test_calc(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class ChainBreakingCase(unittest.TestCase):
    def setUp(self):
        H.bind("calc1", util.hook6_breaker, spec=BEFORE)
        H.bind("calc1", util.hook3_manip_before, spec=BEFORE)
        H.bind("calc1", util.hook4_manip_before, spec=BEFORE)

    def tearDown(self):
        H.clear()

    def test_hook(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class FreezeCase(unittest.TestCase):
    def setUp(self):
        H.freeze("calc1")
        H.bind("calc1", util.hook3_manip_before, spec=BEFORE)
        H.bind("calc1", util.hook4_manip_before, spec=BEFORE)

    def tearDown(self):
        H.clear()

    def test_calc(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class FreezeAllCase(unittest.TestCase):
    def setUp(self):
        H.bind("calc1", util.hook3_manip_before, spec=BEFORE)
        H.bind("calc1", util.hook4_manip_before, spec=BEFORE)
        H.freeze()

    def tearDown(self):
        H.clear()

    def test_calc(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class UnfreezeCase(unittest.TestCase):
    def setUp(self):
        H.freeze("calc1")
        H.bind("calc1", util.hook3_manip_before, spec=BEFORE)
        H.bind("calc1", util.hook4_manip_before, spec=BEFORE)
        H.unfreeze("calc1")

    def tearDown(self):
        H.clear()

    def test_calc(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(8, result)


class UnfreezeAllCase(unittest.TestCase):
    def setUp(self):
        H.freeze()
        H.bind("calc1", util.hook3_manip_before, spec=BEFORE)
        H.bind("calc1", util.hook4_manip_before, spec=BEFORE)
        H.unfreeze()

    def tearDown(self):
        H.clear()

    def test_calc(self):
        result = util.calc1(1, 2, op="+")
        self.assertEqual(8, result)


class CustomTagCaseBefore(unittest.TestCase):
    def setUp(self):
        H.bind("Calc2", util.hook7_custom_tag_before, spec=BEFORE)

    def tearDown(self):
        H.clear()

    def test_hook(self):
        result = util.calc2(10, 2, op="/")
        self.assertEqual(5, result)


class CustomTagCaseAfter(unittest.TestCase):
    def setUp(self):
        H.bind("Calc2", util.hook8_custom_tag_after, spec=AFTER)

    def tearDown(self):
        H.clear()

    def test_hook(self):
        result = util.calc2(10, 2, op="/")
        self.assertEqual(5, result)


if __name__ == '__main__':
    unittest.main()
