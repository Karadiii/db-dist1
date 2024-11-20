from synchronized_database import SynchronizedDatabase
import multiprocessing


class ProcessChecker:
    def __init__(self, db_path):
        self.db = SynchronizedDatabase(db_path, mode="processes")

    def run(self):
        processes = []

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
        processes.append(multiprocessing.Process(target=writer))

        # Add multiple readers
        for _ in range(5):
            processes.append(multiprocessing.Process(target=reader))

        # Start and join all processes
        for process in processes:
            process.start()

        for process in processes:
            process.join()

        print("ProcessChecker tests completed.")
