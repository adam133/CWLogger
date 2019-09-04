import unittest
import mylogger


class MyTestCase(unittest.TestCase):
    def test_something(self):
        log = mylogger.CWLog()
        log.log("Successfully Executed...")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
