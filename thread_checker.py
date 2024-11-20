from synchronized_database import SynchronizedDatabase
import threading


class ThreadChecker:
    def __init__(self, db_path):
        self.db = SynchronizedDatabase(db_path, mode="threads")

    def run(self):
        threads = []

        def reader():
            try:
                print(f"Reader: {self.db.get_value('key')}")
            except KeyError:
                print("Reader: Key not found.")

        def writer():
            print("Writer: Writing 'key'.")
            self.db.set_value("key", "value")
            print("Writer: Finished writing.")

        # Add a writer
        threads.append(threading.Thread(target=writer))

        # Add multiple readers
        for _ in range(5):
            threads.append(threading.Thread(target=reader))

        # Start and join all threads
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        print("ThreadChecker tests completed.")
