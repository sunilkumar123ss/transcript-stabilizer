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

    def test_empty_hypothesis_does_not_invent_tokens(self):
        self.assertEqual(stabilize([{'text': ''}, {'text': 'a'}, {'text': 'a'}])[-1]['committed'], '')

    def test_invalid(self):
        with self.assertRaises(ValueError):
            Stabilizer(1)
        with self.assertRaises(ValueError):
            stabilize([{'final': True}])
        with self.assertRaises(ValueError):
            Stabilizer().update('x', 1)
if __name__ == '__main__':
    unittest.main()
