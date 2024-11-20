from synchronized_database import SynchronizedDatabase
import multiprocessing


def writer_task(db_path, lock):
    print("Writer: Writing 'key'.")
    with lock:
        db = SynchronizedDatabase(db_path, mode="processes")
        db.set_value("key", "value")
    print("Writer: Finished writing.")


def reader_task(db_path, lock):
    with lock:
        db = SynchronizedDatabase(db_path, mode="processes")
        try:
            print(f"Reader: {db.get_value('key')}")
        except KeyError:
            print("Reader: Key not found.")


class ProcessChecker:
    def __init__(self, db_path):
        self.db_path = db_path

    def run(self):
        # Create a Lock for synchronization across processes
        lock = multiprocessing.Lock()

        processes = []

        # Add a writer process
        processes.append(multiprocessing.Process(target=writer_task, args=(self.db_path, lock)))

        # Add multiple reader processes
        for _ in range(5):
            processes.append(multiprocessing.Process(target=reader_task, args=(self.db_path, lock)))

        # Start and join all processes
        for process in processes:
            process.start()

        for process in processes:
            process.join()

        print("ProcessChecker tests completed.")
