from yitizi import get, yitizi_map

from .utils import BaseTestCase


class TestYitizi(BaseTestCase):
    def test_get(self):
        self.assertSetEqual(yitizi_map.get("你"), {"伱", "奶", "妳", "嬭"})
        self.assertSetEqual(get("你"), {"伱", "奶", "妳", "嬭"})
        self.assertSetEqual(get("好"), set())
        self.assertSetEqual(get("a"), set())
        with self.assertRaises(TypeError):
            yitizi_map.get("")
        with self.assertRaises(TypeError):
            yitizi_map.get("兩字")
