"""Runner module"""
from collections import OrderedDict
from hooking.context import Context
from hooking.constant import ENTER, LEAVE
from hooking.error import Error, ChainBreak


class Runner:
    """Run a target and hooks directly or indirectly bound to it"""
    def __init__(self, cls=None, tag=None, config=None,
                 target=None, args=None, kwargs=None):
        self._context = Context(cls=cls, tag=tag, config=config, target=target,
                                args=args, kwargs=kwargs, shared=OrderedDict())

    def run(self, upstream_hooks, downstream_hooks):
        """
        Run the target and hooks

        [parameters]
        - upstream_hooks: list of upstream hooks
        - downstream_hooks: list of downstream hooks

        [return]
        Return the result
        """
        if upstream_hooks or downstream_hooks:
            self._run_hooks(upstream_hooks, spec=ENTER)
            target = self._context.target
            if target:
                args, kwargs = self._context.args, self._context.kwargs
                self._context.result = target(*args, **kwargs)
            self._run_hooks(downstream_hooks, spec=LEAVE)
        else:
            target = self._context.target
            args, kwargs = self._context.args, self._context.kwargs
            self._context.result = target(*args, **kwargs)
        return self._context.result

    def _run_hooks(self, hooks, spec=ENTER):
        self._context.update(spec=spec)
        # run upstream hooks
        for hook_info in hooks:
            hook = hook_info.hook
            self._context.update(hid=hook_info.hid)
            args, kwargs = self._context.args, self._context.kwargs
            try:
                hook(self._context, *args, **kwargs)
            except ChainBreak as e:
                break
