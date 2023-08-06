from typing import Callable
import unittest
from Akatosh import Actor, Mundus

class TestActor(unittest.TestCase):

    def test_actor_creation(self):

        actor1 = Actor(lambda: None, at=0)
        self.assertIsInstance(actor1, Actor)
        self.assertIsInstance(actor1.action, Callable)
        self.assertIs(actor1.timeline,Mundus.timeline)
        self.assertEqual(actor1.priority, 0)
        self.assertEqual(actor1.time, 0)
        self.assertIsNone(actor1.step)
        self.assertIsNone(actor1.till)

        actor2 = Actor(lambda: None, after=actor1)
        self.assertEqual(actor2.scheduled, False)



if __name__ == '__main__':
    unittest.main()