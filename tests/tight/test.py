# test the loose coupling paradigm
import unittest
from tests.tight import base


class WrapCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_func(self):
        result = base.calc1(1, 2, op="+")
        self.assertEqual(3, result)

    def test_method(self):
        calculator = base.Calculator()
        result = calculator.calc1(1, 2, op="+")
        self.assertEqual(3, result)


class OnEnterCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_func(self):
        result = base.calc2(1, 2, op="+")
        self.assertEqual(3, result)

    def test_method(self):
        calculator = base.Calculator()
        result = calculator.calc2(1, 2, op="+")
        self.assertEqual(3, result)


class OnLeaveCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_func(self):
        result = base.calc3(1, 2, op="+")
        self.assertEqual(3, result)

    def test_method(self):
        calculator = base.Calculator()
        result = calculator.calc3(1, 2, op="+")
        self.assertEqual(3, result)


class HookManipulationCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_func(self):
        result = base.calc4(1, 2, op="+")
        self.assertEqual(42, result)

    def test_method(self):
        calculator = base.Calculator()
        result = calculator.calc4(1, 2, op="+")
        self.assertEqual(42, result)


class TargetOverrideCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_func(self):
        result = base.calc5(1, 2, op="+")
        self.assertEqual(3, result)

    def test_method(self):
        calculator = base.Calculator()
        result = calculator.calc5(1, 2, op="+")
        self.assertEqual(3, result)


if __name__ == '__main__':
    unittest.main()
