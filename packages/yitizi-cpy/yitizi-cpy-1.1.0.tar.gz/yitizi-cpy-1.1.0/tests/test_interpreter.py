from yitizi import get

from .utils import BaseTestCase


class TestYitizi(BaseTestCase):
    def test_get(self):
        self.assertSetEqual(get(字="你"), {"伱", "奶", "妳", "嬭"})
        self.assertSetEqual(get("你"), {"伱", "奶", "妳", "嬭"})
        self.assertSetEqual(get("好"), set())
        self.assertSetEqual(get("a"), set())
        with self.assertRaises(ValueError):
            get("")
        with self.assertRaises(ValueError):
            get("兩字")
