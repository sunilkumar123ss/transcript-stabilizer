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

    def test_final_flush(self):
        s = Stabilizer()
        self.assertEqual(s.update(' hi   there ', True)['committed'], 'hi there')
        with self.assertRaises(ValueError):
            s.update('hi there')

    def test_committed_revision_rejected(self):
        s = Stabilizer(2)
        s.update('hello')
        s.update('hello world')
        with self.assertRaises(ValueError):
            s.update('goodbye')
        self.assertEqual(s.update('hello again', True)['committed'], 'hello again')
