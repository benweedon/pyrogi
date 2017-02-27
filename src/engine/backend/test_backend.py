import unittest
from engine.backend import Screen, Backend
from engine.util.vector import Vec2

class TestScreen(Screen):
    pass

class TestBackend(unittest.TestCase):
    def test_screens(self):
        backend = Backend(Vec2(0, 0), Vec2(0, 0), '', TestScreen())
        self.assertEquals(len(backend.screens), 1)

        backend.set_screen(TestScreen())
        self.assertEquals(len(backend.screens), 2)

        backend.set_screen(TestScreen())
        self.assertEquals(len(backend.screens), 3)

        backend.go_back_n_screens(1)
        self.assertEquals(len(backend.screens), 2)

        backend.set_screen(TestScreen())
        self.assertEquals(len(backend.screens), 3)

        backend.go_back_n_screens(2)
        self.assertEquals(len(backend.screens), 1)

        backend.go_back_n_screens(1)
        self.assertEquals(len(backend.screens), 0)
