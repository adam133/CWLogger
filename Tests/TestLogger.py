import unittest
import mylogger


class MyTestCase(unittest.TestCase):
    def test_basicLog(self):
        log = mylogger.CWLog()
        text = "Success"
        log.log(text)

        rspText = log.response['logged-value']

        self.assertEqual(text, rspText)

    def test_specify_group(self):
        group = 'MyTestLogGroup'
        log = mylogger.CWLog(logGroup=group)
        text = "Success"
        log.log(text)
        rspGroup = log.logGroup

        self.assertEqual(group, rspGroup)

    def test_specify_stream(self):
        stream = 'MyTestStream'

        log = mylogger.CWLog(logStreamName=stream)
        text = "Success"
        log.log(text)
        rspStream = log.logStreamName

        self.assertEqual(rspStream.startswith(stream), True)

    def test_specify_group_and_stream(self):
        stream = 'MyTestStream'
        group = 'MyTestLogGroup'

        log = mylogger.CWLog(logStreamName=stream, logGroup=group)

        text = "Success"

        log.log(text)

        rspStream = log.logStreamName
        rspGroup = log.logGroup
        rspText = log.response['logged-value']

        self.assertEqual(rspStream.startswith(stream), True)
        self.assertEqual(group, rspGroup)
        self.assertEqual(text, rspText)

if __name__ == '__main__':
    unittest.main()
