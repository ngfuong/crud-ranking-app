import traceback
import sys
from PyQt6.QtCore import QThread, QRunnable, pyqtSignal, pyqtSlot


"""
Code from Martin Fitzpatrick on https://www.pythonguis.com/
"""

class WorkerSignals(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__ ()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        # self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function
        '''
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc ()
            exctype, value = sys.exc_info ()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc ()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()      # Done
