import threading

def shorten_string(text: str) -> str:
    assert isinstance(text, str), f"text must be str type, but {type(text)} is given."
    if len(text) > 10:
        return text[:10] + "..."
    return text
    

class Thread(threading.Thread):
    """Please use start method to start thread. start method will call run method.

    example:
        # Initialize threads
        thread1 = concurrent_utils.Thread(1, count_million_and_print_name, 1, {"name":"name_1"})
        thread2 = concurrent_utils.Thread(2, count_million_and_print_name, 2, {"name":"name_2"})
        
        # Start threads
        thread1.start()
        thread2.start()

        # Wait for threads to finish (this is optional: accessing result will call join method anyway)
        thread1.join()
        thread2.join()
        
        # Get results
        result1 = thread1.result
        result2 = thread2.result
    """
    # Static variable
    cnt = 0
    def __init__(self, target, args=None, kwargs=None):
        super().__init__()
        Thread.cnt += 1
        self.threadID = Thread.cnt
        self.func = target
        self.args = self._parse_args(args)
        self.kwargs = self._parse_kwargs(kwargs)
        self._result = None
    
    @property
    def result(self):
        if self.is_alive():
            self.join()
        return self._result
    
    def run(self):
        post_fix = f"Thread {self.threadID}: {self.func.__name__}(args={shorten_string(str(self.args))}, kwargs={shorten_string(str(self.kwargs))})"
        print(f"Starting {post_fix}")
        self._result = self.func(*self.args, **self.kwargs)
        print(f"Exiting {post_fix}")
    
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