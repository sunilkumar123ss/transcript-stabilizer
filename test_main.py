import unittest
try:
    from .main import Stabilizer, stabilize
except ImportError:
    from main import Stabilizer, stabilize

class StabilizerTests(unittest.TestCase):

    def test_wait_then_commit_common_prefix(self):
        s = Stabilizer(3)
        self.assertEqual(s.update('hello there')['committed'], '')
        s.update('hello world')
        self.assertEqual(s.update('hello friend'), {'committed': 'hello', 'provisional': 'friend', 'final': False})
