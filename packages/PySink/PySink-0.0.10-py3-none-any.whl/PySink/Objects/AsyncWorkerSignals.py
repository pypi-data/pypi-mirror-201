from PySide6.QtCore import QObject, Signal
from PySink.Objects import AsyncWorkerProgress, AsyncWorkerResults


class AsyncWorkerSignals(QObject):
    """Class to store the signals of an AsyncWorkers. For custom signals, inherit from this class."""

    #: Signal(str): Signals that the worker has started its task. Contains the workers unique identified.
    started = Signal(str)
    #: Signal(:class:`~AsyncWorkerProgress`): Signal that contains progress information for the worker.
    progress = Signal(AsyncWorkerProgress)
    #: Signal(:class:`~AsyncWorkerResults`): Signals that a worker has finished its task and contains the results of the worker's task.
    finished = Signal(AsyncWorkerResults)
