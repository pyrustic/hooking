"""Hooking module"""
from hooking.error import Error
from hooking import dto


ENTER = "enter"
LEAVE = "leave"
ANY = "any"


class Break(Exception):
    pass


class H:
    """Hooking class"""
    def __init__(self):
        self._events = dict()
        self._hooks = dict()
        self._frozen = False
        self._i = 0

    @property
    def events(self):
        """Get names of events"""
        return self._events.keys()

    @property
    def hids(self):
        """Get HIDs (Hook IDs)"""
        return self._hooks.keys()

    @property
    def frozen(self):
        return self._frozen

    def bind(self, event, hook, spec=ENTER, accept_input=True):
        """
        Bind a hook to an event. Typically called by the event consumer.

        [parameters]
        - event: the name of the event (str)
        - hook: a function to call when the event will occur given a specification.
        Note that this function must accept at least a context (hooking.dto.Context) argument.
        - spec: one of ENTER, LEAVE, or ANY. Defaults to ENTER
        - accept_input: set True if the hook expects some input data from the event producer

        [return]
        The HID (Hook ID)
        """
        if spec not in (ENTER, LEAVE, ANY):
            msg = "The specification must be either 'enter', 'leave' or 'any'."
            raise Error(msg)
        hid = self._gen_hid()
        self._hooks[hid] = {"hid": hid, "event": event, "hook": hook, "spec": spec,
                            "accept_input": accept_input}
        hids = self._events.get(event)
        if not hids:
            hids = list()
            self._events[event] = hids
        hids.append(hid)
        return hid

    def unbind(self, *hids):
        """
        Unbind hooks from an event

        [parameters]
        - *hids: Hook IDs
        """
        for hid in hids:
            try:
                del self._hooks[hid]
            except KeyError as e:
                pass

    def enter_event(self, event, *args, **kwargs):
        """
        Notify the beginning of an event. Typically called by the event producer.
        Note that this method won't complete if the H object is frozen.

        [parameters]
        - event: the name of the event (str)
        - *args: arguments to send to the hook(s) expected to be called
        - **kwargs: arguments to send to the hook(s) expected to be called

        [return]
        Returns True if hooks have been called without any Break raised

        """
        if self._frozen:
            return
        return self._raise(event, "enter", *args, **kwargs)

    def leave_event(self, event, *args, **kwargs):
        """
        Notify the end of an event. Typically called by the event producer.
        Note that this method won't complete if the H object is frozen.

        [parameters]
        - event: the name of the event (str)
        - *args: arguments to send to the hook(s) expected to be called
        - **kwargs: arguments to send to the hook(s) expected to be called

        [return]
        Returns True if hooks have been called without any Break raised

        """
        if self._frozen:
            return
        return self._raise(event, "leave", *args, **kwargs)

    def check_hook(self, hid):
        """
        Check whether a hook has been registered or not

        [parameters]
        - hid: Hook ID

        [return]
        Returns None if the hook doesn't exist.
        Returns a hooking.dto.HookInfo that is a namedtuple.
        The attributes of HookInfo are: hid, event, spec, accept_input
        """
        hook_info = self._hooks.get(hid)
        if not hook_info:
            return None
        return dto.HookInfo(hook_info["hid"],
                            hook_info["event"],
                            hook_info["spec"],
                            hook_info["accept_input"])

    def check_event(self, event):
        """
        Check if there are hooks bound to a specific event

        [parameters]
        - event: name of the event

        [return]
        Returns None if there are no hooks bound to the event.
        Returns a tuple of hids (Hook IDs) of bound hooks
        """
        hids = self._events.get(event)
        if not hids:
            return None
        return tuple(hids)

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

    def clear(self):
        """Clear events and hooks. Set the 'frozen' attribute to False"""
        self._events = dict()
        self._hooks = dict()
        self._frozen = False

    def _raise(self, event, spec, *args, **kwargs):
        hids = self._events.get(event)
        if not hids:
            return True
        for hid in hids:
            hook_info = self._hooks.get(hid)
            if not hook_info:
                continue
            hook_info_spec = hook_info["spec"]
            if hook_info_spec not in (ANY, spec):
                continue
            try:
                self._run_hook(hook_info, spec, *args, **kwargs)
            except Break as e:
                return False
        return True

    def _run_hook(self, info, spec, *args, **kwargs):
        hook = info["hook"]
        accept_input = info["accept_input"]
        context = dto.Context(self, info["hid"], info["event"], spec, accept_input)
        if not accept_input:
            args = list()
            kwargs = dict()
        hook(context, *args, **kwargs)

    def _gen_hid(self):
        self._i += 1
        return "hid{}".format(self._i)
