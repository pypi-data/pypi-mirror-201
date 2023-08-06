from PySink import AsyncWorker


class CancellableAsyncWorker(AsyncWorker):
    def __init__(self, *args, **kwargs):
        """A class that represents a cancellable AsyncWorker. Any workers that need to be cancellable should
        inherit from this class. CancellableAsyncWorker inherits from :class:`AsyncWorker`, and offers the ability to
        cancel the worker's task at any time by calling the :meth:`~cancel` method.

        IMPORTANT NOTE: While calling :meth:`~cancel` effectively halts the worker's task, it DOES NOT terminate the
        execution of :meth:`run()<AsyncWorker.run>` (doing so could result in unwanted data corruption). Within
        :meth:`run()<AsyncWorker.run>`, you should poll the :attr:`~cancelled` flag intermittently and return early if
        it is True.
        """
        super(CancellableAsyncWorker, self).__init__(*args, **kwargs)
        self.cancelled: bool = False

    def cancel(self) -> None:
        """Cancels the worker. A 'Cancelled' message is appended to both :attr:`~PySink.AsyncWorkerResults.warnings`
        and :attr:`~PySink.AsyncWorkerResults.errors`, and the :attr:`~PySink.AsyncWorkerSignals.finished` signal is
        emitted (similar to calling :meth:`~complete`). Once this method is called, all internal method calls/signal
        updates will be ignored, and an internal flag called :attr:`~cancelled` is set to True.

        IMPORTANT NOTE: While calling :meth:`~cancel` effectively halts the worker's task, it DOES NOT terminate the
        execution of :meth:`run()<AsyncWorker.run>` (doing so could result in unwanted data corruption). Within
        :meth:`run()<AsyncWorker.run>`, you should poll the :attr:`~cancelled` flag intermittently and return early if
        it is True.
        """
        self.errors.append('Cancelled')
        self.warnings.append('Cancelled')
        self.cancelled = True
        self.signals.finished.emit(self._load_default_results())

    def reset(self):
        self.cancelled = False
        super().reset()

    def update_progress(self, progress_value: int, message=None) -> None:
        if not self.cancelled:
            super().update_progress(progress_value, message)

    def emit_start(self):
        if not self.cancelled:
            super().emit_start()

    def complete(self, **kwargs) -> None:
        if not self.cancelled:
            super().complete(**kwargs)
