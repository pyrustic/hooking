"""Tight coupling paradigm"""
from collections import OrderedDict
from functools import wraps
from hooking.runner import Runner
from hooking.context import Context
from hooking import dto
from hooking.error import ChainBreak


def override(hook, **config):
    """
    Override target with a hook

    [parameters]
    - hook: hook to override target
    - **config: configuration keyword arguments
    """
    def deco(target):

        @wraps(target)
        def wrapper(*args, **kwargs):
            context = Context(cls=None, tag=None, config=config, target=target,
                              args=args, kwargs=kwargs, shared=OrderedDict())
            try:
                result = hook(context, *args, **kwargs)
            except ChainBreak as e:
                pass
            return context.result
        return wrapper
    return deco


def wrap(hook1, hook2, **config):
    """
    Wrap a target with an upstream hook and a downstream hook

    [parameters]
    - hook1: upstream hook
    - hook2: downstream hook
    - **config: configuration keyword arguments
    """

    def deco(target):

        @wraps(target)
        def wrapper(*args, **kwargs):
            hook_info1 = dto.HookInfo(cls=None, hid=None, hook=hook1,
                                      tag=None, spec=None)
            hook_info2 = dto.HookInfo(cls=None, hid=None, hook=hook2,
                                      tag=None, spec=None)
            upstream_hooks, downstream_hooks = (hook_info1, ), (hook_info2, )
            runner = Runner(config=config, target=target, args=args, kwargs=kwargs)
            return runner.run(upstream_hooks, downstream_hooks)
        return wrapper
    return deco


def on_enter(hook, **config):
    """
    Bind an upstream hook to a target

    [parameters]
    - hook: upstream hook
    - **config: configuration keyword arguments
    """
    def deco(target):

        @wraps(target)
        def wrapper(*args, **kwargs):
            hook_info = dto.HookInfo(cls=None, hid=None, hook=hook,
                                     tag=None, spec=None)
            upstream_hooks, downstream_hooks = (hook_info, ), tuple()
            runner = Runner(config=config, target=target, args=args, kwargs=kwargs)
            return runner.run(upstream_hooks, downstream_hooks)
        return wrapper
    return deco


def on_leave(hook, **config):
    """
    Bind a downstream hook to a target

    [parameters]
    - hook: downstream hook
    - **config: configuration keyword arguments
    """
    def deco(target):

        @wraps(target)
        def wrapper(*args, **kwargs):
            hook_info = dto.HookInfo(cls=None, hid=None, hook=hook,
                                     tag=None, spec=None)
            upstream_hooks, downstream_hooks = tuple(), (hook_info, )
            runner = Runner(config=config, target=target, args=args, kwargs=kwargs)
            return runner.run(upstream_hooks, downstream_hooks)
        return wrapper
    return deco
