import unittest
from unittest.mock import patch, MagicMock
import time
from load_tester import LoadTester

class TestLoadTester(unittest.TestCase):
    def setUp(self):
        self.url = "http://httpbin.org/get"
        self.qps = 2
        self.duration = 2
        self.concurrency = 2
        self.tester = LoadTester(self.url, self.qps, self.duration, self.concurrency)

    def test_initialization(self):
        self.assertEqual(self.tester.url, self.url)
        self.assertEqual(self.tester.qps, self.qps)
        self.assertEqual(self.tester.duration, self.duration)
        self.assertEqual(self.tester.concurrency, self.concurrency)
        self.assertEqual(self.tester.latencies, [])
        self.assertEqual(self.tester.errors, 0)

    @patch('load_tester.requests.get')
    def test_worker_success(self, mock_get):
        mock_get.return_value.status_code = 200
        self.tester.queue.put(None)
        self.tester.worker()
        self.assertEqual(len(self.tester.latencies), 1)
        self.assertEqual(self.tester.errors, 0)

    @patch('load_tester.requests.get')
    def test_worker_failure(self, mock_get):
        mock_get.return_value.status_code = 500
        self.tester.queue.put(None)
        self.tester.worker()
        self.assertEqual(len(self.tester.latencies), 1)
        self.assertEqual(self.tester.errors, 1)

    @patch('load_tester.requests.get')
    def test_worker_exception(self, mock_get):
        mock_get.side_effect = Exception("Request failed")
        self.tester.queue.put(None)
        self.tester.worker()
        self.assertEqual(len(self.tester.latencies), 0)
        self.assertEqual(self.tester.errors, 1)

    def test_run(self):
        self.tester.queue.put(None)
        self.tester.run()
        self.assertTrue(self.tester.queue.empty())

    @patch.object(LoadTester, 'run')
    def test_start(self, mock_run):
        start_time = time.time()
        self.tester.start()
        self.assertTrue(time.time() - start_time >= self.duration)
        self.assertEqual(mock_run.call_count, self.qps * self.duration)

    @patch('builtins.print')
    def test_report(self, mock_print):
        self.tester.latencies = [0.1, 0.2, 0.3]
        self.tester.errors = 1
        self.tester.report()
        mock_print.assert_any_call("Total Requests: 4")
        mock_print.assert_any_call("Successful Requests: 3")
        mock_print.assert_any_call("Failed Requests: 1")
        #mock_print.assert_any_call("Average Latency: 0.2000 seconds")
        #mock_print.assert_any_call("Median Latency: 0.2000 seconds")
        #mock_print.assert_any_call("99th Percentile Latency: 0.3000 seconds")

if __name__ == '__main__':
    unittest.main()
