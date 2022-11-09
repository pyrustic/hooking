"""Context class"""
from hooking.error import Error


FIELDS = ("cls", "hid", "tag", "config", "spec", "target",
          "args", "kwargs", "result", "shared")


class Context:
    """An instance of this class is passed to hooks"""
    def __init__(self, cls=None, hid=None, tag=None, config=None,
                 spec=None, target=None, args=None, kwargs=None,
                 result=None, shared=None):
        """
        Initialize a context object

        [parameters]
        - cls: hooking class
        - hid: hook id
        - tag: str, the label used to tag a function or method
        - config: dict, data associated to the tag at the level of the decoration
        - spec: either `hooking.ENTER` or `hooking.LEAVE`
        - target: the target function or method
        - args: tuple representing arguments passed to the target
        - kwargs: dict representing keyword arguments passed to the target
        - result: if spec is set to `hooking.LEAVE`, result is the value returned by the target
        - shared: ordered dictionary to store shared data between hooks
        """
        self._cls = cls
        self._hid = hid
        self._tag = tag
        self._config = config
        self._spec = spec
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._result = result
        self._shared = shared

    @property
    def cls(self):
        """Get hooking class"""
        return self._cls

    @property
    def hid(self):
        """Get hid"""
        return self._hid

    @property
    def tag(self):
        """Get tag"""
        return self._tag

    @property
    def config(self):
        """Get config"""
        return self._config

    @property
    def spec(self):
        """Get spec"""
        return self._spec

    @property
    def target(self):
        """Get target"""
        return self._target

    @target.setter
    def target(self, val):
        """Set target"""
        self._target = val

    @property
    def args(self):
        """Get args"""
        return self._args

    @args.setter
    def args(self, val):
        """Set args"""
        self._args = val

    @property
    def kwargs(self):
        """Get kwargs"""
        return self._kwargs

    @kwargs.setter
    def kwargs(self, val):
        """Set kwargs"""
        self._kwargs = val

    @property
    def result(self):
        """Get result"""
        return self._result

    @result.setter
    def result(self, val):
        """Set result"""
        self._result = val

    @property
    def shared(self):
        """Get shared"""
        return self._shared

    def update(self, **kwargs):
        """Update one or multiple fields"""
        for key, val in kwargs.items():
            if key not in FIELDS:
                msg = ("Invalid field '{}'.".format(key),
                       "Valid fields are: {}".format(" ".join(FIELDS)))
                raise Error(" ".join(msg))
            field = "_" + key
            setattr(self, field, val)
