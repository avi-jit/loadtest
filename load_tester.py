import argparse
import time
import requests
import threading
import statistics
from queue import Queue, Empty

class LoadTester:
    """
    A class to perform HTTP load testing and benchmarking.

    Attributes:
        url (str): The URL to test.
        qps (int): Queries per second.
        duration (int): Duration of the test in seconds.
        concurrency (int): Number of concurrent threads.
        latencies (list): List to store latencies of requests.
        errors (int): Counter for the number of errors.
        lock (threading.Lock): Lock for synchronizing access to shared resources.
        queue (Queue): Queue to manage the tasks.
    """

    def __init__(self, url, qps, duration, concurrency):
        """
        Constructs all the necessary attributes for the LoadTester object.

        Args:
            url (str): The URL to test.
            qps (int): Queries per second.
            duration (int): Duration of the test in seconds.
            concurrency (int): Number of concurrent threads.
        """
        self.url = url
        self.qps = qps
        self.duration = duration
        self.concurrency = concurrency
        self.latencies = []
        self.errors = 0
        self.lock = threading.Lock()
        self.queue = Queue()

    def worker(self):
        """
        Worker thread function to process tasks from the queue.

        Sends HTTP requests to the specified URL and records the latency and errors.
        """
        while True:
            try:
                # Get a task from the queue with a timeout to avoid infinite blocking
                self.queue.get(timeout=1)
                start_time = time.time()
                try:
                    response = requests.get(self.url)
                    latency = time.time() - start_time
                    with self.lock:
                        self.latencies.append(latency)
                        if response.status_code != 200:
                            self.errors += 1
                except Exception as e:
                    with self.lock:
                        self.errors += 1
                finally:
                    self.queue.task_done()
            except Empty:
                # Exit the loop if the queue is empty
                break

    def run(self):
        """
        Runs the load test by creating and managing worker threads.
        """
        threads = []
        for _ in range(self.concurrency):
            thread = threading.Thread(target=self.worker)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def start(self):
        """
        Starts the load test by populating the queue and managing the timing of requests.
        """
        total_requests = self.qps * self.duration
        for _ in range(total_requests):
            self.queue.put(None)

        start_time = time.time()
        while time.time() - start_time < self.duration:
            self.run()
            time.sleep(1 / self.qps)

        self.report()

    def report(self):
        """
        Prints the results of the load test, including total requests, successful requests, failed requests, and latency statistics.
        """
        print(f"Total Requests: {len(self.latencies) + self.errors}")
        print(f"Successful Requests: {len(self.latencies)}")
        print(f"Failed Requests: {self.errors}")
        if self.latencies:
            print(f"Average Latency: {statistics.mean(self.latencies):.4f} seconds")
            print(f"Median Latency: {statistics.median(self.latencies):.4f} seconds")
            print(f"99th Percentile Latency: {statistics.quantiles(self.latencies, n=100)[98]:.4f} seconds")

def main():
    """
    Main function to parse command-line arguments and start the load tester.
    """
    parser = argparse.ArgumentParser(description="HTTP Load Testing Tool")
    parser.add_argument("url", type=str, help="The URL to test")
    parser.add_argument("--qps", type=int, default=1, help="Queries per second")
    parser.add_argument("--duration", type=int, default=10, help="Duration of the test in seconds")
    parser.add_argument("--concurrency", type=int, default=1, help="Number of concurrent threads")

    args = parser.parse_args()

    tester = LoadTester(args.url, args.qps, args.duration, args.concurrency)
    tester.start()

if __name__ == "__main__":
    main()

# test run
#tester = LoadTester(url='http://httpbin.org/get',qps=2, duration=2, concurrency=2)
#tester.start()