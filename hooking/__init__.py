"""Hooking module"""
from threading import Lock
from functools import wraps
from collections import namedtuple


__all__ = ["H", "BEFORE", "AFTER", "ChainBreak", "HookInfo", "Context", "Error"]


# ============= CONSTANTS AND DTOs ==============


BEFORE = "before"
AFTER = "after"

HookInfo = namedtuple("HookInfo", ["hid", "hook", "tag", "spec"])


# ============= MAIN CLASS ==============


class H:
    """Main class"""
    # counter
    i = 0
    # 'hooks' is a dict of hooking.HookInfo. Keys are HIDs (Hook IDs)
    hooks = dict()
    # 'tags' is a dict to hold relationship between tags and HIDs. Keys are tags.
    # values are sets
    tags = dict()
    # lock
    lock = Lock()
    # frozen
    frozen = False
    # frozen_list
    frozen_tags = set()

    @classmethod
    def tag(cls, arg):
        """Tag a function or method with this decorator. Accepts an option label string"""
        label, target = init_decoration(arg)

        def deco(target):
            @wraps(target)
            def wrapper(*args, **kwargs):
                if H.frozen or label in H.frozen_tags:
                    return target(*args, **kwargs)
                runner = Runner(target, *args, **kwargs)
                return runner.run(label)
            return wrapper
        if target:
            return deco(target)
        return deco

    @classmethod
    def bind(cls, tag, hook, spec=BEFORE):
        """
        Bind a hook to a tag

        [parameters]
        - tag: label string
        - hook: callable
        - spec: either `hooking.BEFORE` or `hooking.AFTER`

        [return]
        Returns a HID (Hook ID)
        """
        if spec not in (BEFORE, AFTER):
            msg = "Unknown spec '{}'."
            raise Error(msg.format(spec))
        hid = gen_id()
        with H.lock:
            # update H.hooks
            hook_info = HookInfo(hid, hook, tag, spec)
            H.hooks[hid] = hook_info
            # update H.tags
            hids = H.tags.get(tag)
            if not hids:
                hids = set()
                H.tags[tag] = hids
            hids.add(hid)
        return hid

    @classmethod
    def unbind(cls, *hids):
        """Unbind all hooks previously bound (no arguments) or specific hooks by provided their HIDs"""
        with H.lock:
            if not hids:
                H.hooks = dict()
                return
            for hid in hids:
                try:
                    del H.hooks[hid]
                except KeyError as e:
                    pass

    @classmethod
    def freeze(cls, *tags):
        """Freeze the entire hooking mechanism (no arguments) or specific tags"""
        with H.lock:
            if not tags:
                H.frozen = True
                H.frozen_tags = set()
                return
            for tag in tags:
                H.frozen_tags.add(tag)

    @classmethod
    def unfreeze(cls, *tags):
        """Unfreeze the entire hooking mechanism (no arguments) or specific tags"""
        with H.lock:
            if not tags:
                H.frozen = False
                H.frozen_tags = set()
                return
            for tag in tags:
                try:
                    H.frozen_tags.remove(tag)
                except KeyError as e:
                    pass

    @classmethod
    def clear(cls):
        """Clear the hooking mechanism. Reset H.hooks, H.tags, H.frozen, H.frozen_tags"""
        with H.lock:
            H.hooks = dict()
            H.tags = dict()
            H.frozen = False
            H.frozen_tags = set()


# ============= EXTRA FUNCTIONS ==============


def gen_id():
    """Generate a new id"""
    with H.lock:
        H.i += 1
        new_id = H.i
    return new_id


def init_decoration(arg):
    if callable(arg):
        target = arg
        tag = target.__qualname__
    else:
        target = None
        tag = arg
    if not isinstance(tag, str):
        msg = "The tag should be a string not a ''."
        raise Error(msg.format(type(tag)))
    # update H.tags
    hids = H.tags.get(tag)
    if not hids:
        hids = set()
        H.tags[tag] = hids
    return tag, target


# ============= EXTRA CLASSES ==============


class Runner:
    """Run a target and hooks bound to it (indirectly bound, obviously)"""
    def __init__(self, target, *args, **kwargs):
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def run(self, tag):
        hids = H.tags.get(tag)
        if hids:
            before_hooks, after_hooks = self._get_hooks(hids)
            result = self._run_hooks(tag, before_hooks, after_hooks)
        else:
            result = self._target(*self._args, **self._kwargs)
        return result

    def _get_hooks(self, hids):
        before_hooks, after_hooks = list(), list()
        removable_hids = list()
        for hid in hids:
            hook_info = H.hooks.get(hid)
            if not hook_info:
                removable_hids.append(hid)
                continue
            if hook_info.spec == BEFORE:
                before_hooks.append(hook_info)
            elif hook_info.spec == AFTER:
                after_hooks.append(hook_info)
        # clean up hids
        with H.lock:
            for hid in removable_hids:
                hids.remove(hid)
        return before_hooks, after_hooks

    def _run_hooks(self, tag, before_hooks, after_hooks):
        target, args, kwargs, result = self._run_before_hooks(tag, before_hooks)
        return self._run_after_hooks(tag, target, args, kwargs, result, after_hooks)

    def _run_before_hooks(self, tag, hooks):
        """
        Run before_hooks

        [parameters]
        - tag: label
        - hooks: list of HookInfos

        [return]
        Return the updated versions of target, args, and kwargs
        """
        target, args, kwargs = self._target, self._args, self._kwargs
        result = None
        # run before hooks
        for hook_info in hooks:
            hid, hook, spec = hook_info.hid, hook_info.hook, hook_info.spec
            context = Context(hid, tag, spec, target, args, kwargs, result)
            try:
                hook(context)
            except ChainBreak as e:
                break
            finally:
                target = context.target
                args, kwargs, result = context.args, context.kwargs, context.result
        return target, args, kwargs, result

    def _run_after_hooks(self, tag, target, args, kwargs, result, hooks):
        """
        Run after_hooks

        [parameters]
        - tag: label
        - target: callable
        - args: arguments
        - kwargs: keyword arguments
        - result: result
        - hooks: list of HookInfos

        [return]
        Return the result returned by target
        """
        if target:
            result = target(*args, **kwargs)
        # run after hooks
        for hook_info in hooks:
            hid, hook, spec = hook_info.hid, hook_info.hook, hook_info.spec
            context = Context(hid, tag, spec, target, args, kwargs, result)
            try:
                hook(context)
            except ChainBreak as e:
                break
            finally:
                target = context.target
                result = context.result
        return result


class Context:
    """An instance of this class is passed to hooks"""
    def __init__(self, hid, tag, spec, target, args, kwargs, result):
        """
        Initialize a context object

        [parameters]
        - hid: hook id
        - tag: str, the label used to tag a function or method
        - spec: either BEFORE or AFTER
        - target: the tagged function or method
        - args: tuple representing arguments passed to the target
        - kwargs: dict representing keyword arguments passed to the target
        - result: if spec is set to AFTER, result is the value returned by the target
        """
        self._hid = hid
        self._tag = tag
        self._spec = spec
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._result = result

    @property
    def hid(self):
        """Get hid"""
        return self._hid

    @property
    def tag(self):
        """Get tag"""
        return self._tag

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


# ============= EXCEPTIONS ==============


class Error(Exception):
    """Error class"""
    pass


class ChainBreak(Error):
    """Break the execution of a chain of hooks"""
    pass
