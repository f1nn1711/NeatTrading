import unittest


class TestHelpers(unittest.TestCase):
    def testIsSet(self):
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

    def testPluck(self):
        return


if __name__ == '__main__':
    unittest.main()
