import threading

class Thread(threading.Thread):
    def __init__(self, threadID, func, args=None, kwargs=None):
        super().__init__()
        self.threadID = threadID
        self.func = func
        self.args = self._parse_args(args)
        self.kwargs = self._parse_kwargs(kwargs)
        self.result = None
    def run(self):
        print("Starting Thread: " + self.func.__name__)
        self.result = self.func(*self.args, **self.kwargs)
        print("Exiting Thread: " + self.func.__name__)
    
    def _parse_args(self, args):
        if args is None:
            return ()
        elif isinstance(args, tuple):
            return args
        elif isinstance(args, list):
            return tuple(args)
        else:
            return (args,)
        
    def _parse_kwargs(self, kwargs):
        if kwargs is None:
            return {}
        elif isinstance(kwargs, dict):
            return kwargs
        else:
            raise ValueError(f"kwargs must be dict type, but {type(kwargs)} is given.")


if __name__ == "__main__":
    pass