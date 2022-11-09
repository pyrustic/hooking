"""Loose coupling module"""
from threading import Lock
from functools import wraps
from collections import OrderedDict
from hooking.runner import Runner
from hooking import dto
from hooking.constant import ENTER, LEAVE
from hooking.error import Error


class H:
    """Base Pyrustic Hooking class"""

    # counter
    i = 0

    # 'targets' is an ordered dict.
    # Keys are tags and values are lists of instances of hooking.TargetInfo.
    # Example: {"tag1": [TargetInfo(), TargetInfo(), ...], ...}
    targets = OrderedDict()

    # 'hooks' is an ordered dict.
    # Keys are tags and values are lists of instances of hooking.HookInfo
    # Example: {"tag1": [HookInfo(), HookInfo(), ...], ...}
    hooks = OrderedDict()

    # 'tags' is a set of tags
    tags = set()

    # frozen boolean
    frozen = False

    # threading.Lock object
    lock = Lock()

    @classmethod
    def tag(cls, label, **config):
        """Tag a function or method with this decorator.
        Accepts an optional label string and optional configuration keyword arguments"""
        label, target = init_decoration(label)

        def deco(target):
            # register target
            if not cls.targets.get(label):
                cls.targets[label] = list()
            cls.targets[label].append(dto.TargetInfo(cls, label, target, config))
            # register tag label
            cls.tags.add(label)
            if not cls.hooks.get(label):
                cls.hooks[label] = list()

            @wraps(target)
            def wrapper(*args, **kwargs):
                if cls.frozen:
                    return target(*args, **kwargs)
                upstream_hooks, downstream_hooks = cls.get_hooks(label)
                runner = Runner(cls=cls, tag=label, config=config,
                                target=target, args=args, kwargs=kwargs)
                return runner.run(upstream_hooks, downstream_hooks)
            return wrapper

        if target:
            return deco(target)
        return deco

    @classmethod
    def wrap(cls, tag, hook1, hook2):
        """
        Wrap a target with an upstream hook and a downstream hook

        [parameters]
        - tag: the tag label
        - hook1: upstream hook
        - hook2: downstream hook

        [return]
        Returns respective hook identifiers
        """
        hid1 = cls.on_enter(tag, hook1)
        hid2 = cls.on_leave(tag, hook2)
        return hid1, hid2

    @classmethod
    def on_enter(cls, tag, hook):
        """
        Register an upstream hook

        [parameters]
        - tag: tag label
        - hook: upstream hook

        [return]
        Returns the hook identifier
        """
        return cls.bind(tag, hook, spec=ENTER)

    @classmethod
    def on_leave(cls, tag, hook):
        """
        Register an downstream hook

        [parameters]
        - tag: tag label
        - hook: downstream hook

        [return]
        Returns the hook identifier
        """
        return cls.bind(tag, hook, spec=LEAVE)

    @classmethod
    def unbind(cls, *hids):
        """Unbind hooks by providing their HIDs"""
        with cls.lock:
            for key, val in cls.hooks.items():
                cache = cls.hooks[key]
                cache[:] = [x for x in cache if x.hid not in hids]

    @classmethod
    def freeze(cls):
        """Freeze the hooking mechanism"""
        with cls.lock:
            cls.frozen = True

    @classmethod
    def unfreeze(cls):
        """Unfreeze the hooking mechanism"""
        with cls.lock:
            cls.frozen = False

    @classmethod
    def get_hooks(cls, tag):
        """
        Get a tuple of hooks lists (upstream and downstream) for a given tag
        [parameters]
        - tag: str, the tag

        [return]
        Return a tuple containing the upstream list and the downstream list of hooks.
        Example: ([upstream_hook1, upstream_hook2], [downstream_hook1, downstream_hook2])
        """
        upstream_hooks, downstream_hooks = list(), list()
        hooks = cls.hooks.get(tag)
        if not hooks:
            return upstream_hooks, downstream_hooks
        for hook_info in hooks:
            if hook_info.spec == ENTER:
                upstream_hooks.append(hook_info)
            elif hook_info.spec == LEAVE:
                downstream_hooks.append(hook_info)
        return upstream_hooks, downstream_hooks

    @classmethod
    def clear(cls, *tags):
        """
        Clear hooks bound to specified tags
        """
        with cls.lock:
            for tag in tags:
                if tag not in cls.hooks:
                    continue
                cls.hooks[tag] = list()

    @classmethod
    def reset(cls):
        """Reset hooks, and frozen class variables"""
        with cls.lock:
            cls.hooks = OrderedDict()
            cls.tags = set(cls.targets.keys())
            cls.frozen = False

    @classmethod
    def subclass(cls, name):
        """
        Create a new class with its own class variables.

        [parameters]
        - name: the name (string) of the new class to create

        [return]
        Return the newly created class
        """
        new_class = type(name, (cls, ), dict())
        new_class.i = 0
        new_class.targets = OrderedDict()
        new_class.hooks = OrderedDict()
        new_class.tags = set()
        new_class.frozen = False
        new_class.lock = Lock()
        return new_class

    @classmethod
    def bind(cls, tag, hook, spec=ENTER):
        """
        Bind a hook to a tag

        [parameters]
        - tag: label string
        - hook: callable
        - spec: either `hooking.ENTER` or `hooking.LEAVE`

        [return]
        Returns a HID (Hook ID)
        """
        if spec not in (ENTER, LEAVE):
            msg = "Unknown spec '{}'."
            raise Error(msg.format(spec))
        hid = gen_id(cls)
        with cls.lock:
            # update cls.hooks
            hook_info = dto.HookInfo(cls, hid, hook, tag, spec)
            if not cls.hooks.get(tag):
                cls.hooks[tag] = list()
            cls.hooks[tag].append(hook_info)
        return hid


# ============= EXTRA FUNCTIONS ==============


def gen_id(cls):
    """Generate a new id"""
    with cls.lock:
        cls.i += 1
        new_id = cls.i
    return new_id


def init_decoration(arg):
    if callable(arg) and not isinstance(arg, type):
        target = arg
        tag = target.__qualname__
    elif isinstance(arg, str):
        target = None
        tag = arg
    else:
        msg = "Failed to decorate {}"
        raise Error(msg.format(type(arg)))
    return tag, target
