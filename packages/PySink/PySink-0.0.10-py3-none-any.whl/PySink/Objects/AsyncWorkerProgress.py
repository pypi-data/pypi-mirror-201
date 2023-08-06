

class AsyncWorkerProgress:
    """Class to store the progress of an AsyncWorker."""

    value = 0               #: Union[int, float]: Current progress value. For determinate progress, value should be [0, 100]. Indeterminate progress value should be -1.
    message: str = None     #: str, optional: Status message about the worker's progress (Downloading, Calculating, etc).
    id: str = None          #: str: The worker's unique identifier.

    def __str__(self):
        return f'Progress from Worker {self.id}: Value = {self.value}, Message = {self.message}'

