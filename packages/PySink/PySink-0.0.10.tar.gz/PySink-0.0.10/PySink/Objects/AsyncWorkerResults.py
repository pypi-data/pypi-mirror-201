
class AsyncWorkerResults:
    """Class to store the results of an AsyncWorker. Custom result types should inherit from this class."""

    warnings = []  #: list: Warnings encountered by the worker.
    errors = []  #: list: Errors encountered by the worker.
    id = None  #: str: The worker's unique identifier
    results_dict = {}  #: dict: Results of the worker's task defined as key-value pairs.

    def __str__(self):
        return f'Results of Worker {self.id}: Warnings = {self.warnings}, Errors = {self.errors}, ResultsDict = {self.results_dict}'


