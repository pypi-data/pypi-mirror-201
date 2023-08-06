from yitizi import map

from .utils import BaseTestCase


class TestYitizi(BaseTestCase):
    def test_get(self):
        self.assertSetEqual(map.get("你"), {"伱", "奶", "妳", "嬭"})
        self.assertSetEqual(map.get("好"), set())
        self.assertSetEqual(map.get("a"), set())
        with self.assertRaises(TypeError):
            map.get("")
        with self.assertRaises(TypeError):
            map.get("兩字")
