[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI package version](https://img.shields.io/pypi/v/hooking)](https://pypi.org/project/hooking)
[![Downloads](https://pepy.tech/badge/hooking)](https://pepy.tech/project/hooking)

<!-- Cover -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/assets/hooking/hooks.jpg" alt="Hooks" width="960">
    <p align="center">
        <a href="https://commons.wikimedia.org/wiki/File:%D0%9A%D0%B0%D0%BD%D0%B0%D1%82%D0%BD%D1%8B%D0%B9_%D1%81%D1%82%D1%80%D0%BE%D0%BF%D1%8B.jpg">HardMediaGroup</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0">CC BY-SA 3.0</a>, via Wikimedia Commons
    </p>
</div>


<!-- Intro Text -->
# Pyrustic Hooking
<b> Event lifecycle oriented hooking </b>


This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).
> [Modules documentation](https://github.com/pyrustic/hooking/tree/master/docs/modules#readme)


## Table of contents
- [Overview](#overview)
- [Bind hooks to an event](#bind-hooks-to-an-event)
- [Unbind hooks from an event](#unbind-hooks-from-an-event)
- [Enter an event](#enter-an-event)
- [Leave an event](#leave-an-event)
- [Break an event](#break-an-event)
- [Check a hook](#check-a-hook)
- [Check an event](#check-an-event)
- [Freeze and unfreeze a session](#freeze-and-unfreeze-a-session)
- [Clear events and hooks](#clear-events-and-hooks)
- [Miscellaneous](#miscellaneous)
- [Installation](#installation)

# Overview
This library, written in **Python**, allows the programmer to perform event lifecycle oriented [hooking](https://en.wikipedia.org/wiki/Hooking). Typically, an [event](https://en.wikipedia.org/wiki/Event_(computing)) has a beginning and an end, therefore a lifecycle. A callback function called a `hook` can be bound to an arbitrary stage of an event's lifecycle.

# Bind hooks to an event

Let's bind a hook to a specific event:

```python
from hooking import H

def hook1(context):
    """
    context is an instance of the namedtuple hooking.dto.Context
    Here are its attributes: h, hid, event, spec, accept_input
    """
    print("Hook 1")
    
def hook2(context):
    print("Hook 2")
    
h = H()
# bind hook1 and hook2 to the event "my-event"
h.bind("my-event", hook1)
h.bind("my-event", hook2)
```
When the event `my-event` will start, `hook1` and `hook2` will be called:
```python
# notify hooks of beginning of "my-event"
h.enter_event("my-event")
# hook1 will be called -> "Hook 1"
# hook2 will be called -> "Hook 2"
```

> Note that the `bind` method returns a unique hook id (`hid`).
> 
> The `hooks` property returns registered hids (Hook IDs).
> 
> The `events` property returns events previously referenced.

## Specify an event lifecycle stage
By default, a hook is bound to the beginning of an event. More specifically, the `spec` parameter defaults to `ENTER`. The `spec` parameter can accept `ENTER`, `LEAVE`, and `ANY`.

```python
from hooking import H, ENTER, LEAVE, ANY

def hook1(context):
    pass

def hook2(context):
    pass

def hook3(context):
    pass

h = H()

# hook1 will be called at the beginning of 'my-event'
h.bind("my-event", hook1, spec=ENTER)

# hook2 will be called at the end of 'my-event'
h.bind("my-event", hook2, spec=LEAVE)

# hook3 will be called at the beginning and the end of 'my-event'
h.bind("my-event", hook3, spec=ANY)

# ...

# notify hooks of beginning of "my-event"
h.enter_event("my-event")

# ...

# notify hooks of end of "my-event"
h.leave_event("my-event")
```

## Pass data to a hook
In the following script, we will bind a hook to an event, then pass data to the hook while notifying it of the beginning of that event:
```python
from hooking import H

def hook1(context, age, name):
    pass

def hook2(context, name, age):
    pass

h = H()

# by default, accept_input is set to True
h.bind("my-event", hook1, accept_input=True)
h.bind("my-event", hook2, accept_input=True)

# ...

# notify hook1 and hook2 of beginning of "my-event"
# pass data (age and name) to these hooks
h.enter_event("my-event", age=42, name="John Doe")
```

# Unbind hooks from an event
You can unbind hooks previously bound to an event by passing hooks ids (`hid`) to the `unbind` method:
```python
from hooking import H

def hook1(context):
    pass

def hook2(context):
    pass

h = H()

# bind
hid1 = h.bind("my-event", hook1)
hid2 = h.bind("my-event", hook2)

# unbind
h.unbind(hid1, hid2)
```

# Enter an event
Entering an event is synonymous with notifying hooks of the start of an event:
```python
from hooking import H

def hook1(context):
    pass

h = H()

# bind
h.bind("my-event", hook1)

# notify hooks of the beginning of "my-event"
h.enter_event("my-event")
```

# Leave an event
Leaving an event is synonymous with notifying hooks of the end of an event:
```python
from hooking import H

def hook1(context):
    pass

h = H()

# bind
h.bind("my-event", hook1)

# notify hooks of the beginning of "my-event"
h.enter_event("my-event")

# notify hooks of the end of "my-event"
h.leave_event("my-event")
```

# Break an event
From a hook, we might need to break the execution of a running event:
```python
import sys
from hooking import H, Break

def hook1(context):
    # raising Break will make H.enter_event or H.leave_event method
    # returns False instead of True
    raise Break
    
h = H()

# bind
h.bind("my-event", hook1)

# notify hooks of the beginning of "my-event"
if not h.enter_event("my-event"):  # if method returns False
    # break the event
    sys.exit()  # exit !
    
# ...

# notify hooks of the end of "my-event"
h.leave_event("my-event")
```

# Check a hook
You can check if a hook has been registered or not:
```python
from hooking import H

def hook1(context):
    pass

h = H()
hid = h.bind("my-event", hook1)

# Check 
hook_info = h.check_hook(hid)
# hook_info would be None if the hid (Hook ID) doesn't exist,
# but in the current case, the hid exists, thus hook_info is not None,
# instead, hook_info contains an instance of hooking.dto.HookInfo
# HookInfo has the following attributes: hid, event, spec, accept_input
```

# Check an event
You can check whether there are hooks bound to a given event or not:
```python
from hooking import H

def hook1(context):
    pass

h = H()
h.bind("my-event", hook1)

# Check 
hids = h.check_event("my-event")
# 'hids' would be None if there are no hooks bound to "my-event",
# but in the current case, hook1 is bound to "my-event", 
# thus 'hids' is not None, instead, 'hids' is a
# tuple that contains the hids (Hook IDs) of hooks bound to "my-event"
```

# Freeze and unfreeze a session
The programmer may need to temporarily **freeze** the hooking session, and in this case no hook will be called when an event occurs:
```python
from hooking import H

def hook1(context):
    pass

h = H()

# bind
h.bind("my-event", hook1)

# freeze the session
h.freeze()

# no hook will be called
h.enter_event("my-event")
# ...
h.leave_event("my-event")
```

**Unfreezing** the hooking session is as simple as calling the `unfreeze` method:
```python
h.unfreeze()
```

> The `frozen` property is a boolean that indicates whether the session is frozen or not.

# Clear events and hooks
The `clear` method resets the hooking session:
```python
from hooking import H

def hook1(context):
    pass

h = H()

# bind
h.bind("my-event", hook1)

# delete events and the references to hooks
h.clear()  # also unfreeze the session (if previously frozen)
```

# Miscellaneous
Loading...

# Installation
**Hooking** is **cross platform** and versions under **1.0.0** will be considered **Beta** at best. It should work on **Python 3.5** or [newer](https://www.python.org/downloads/).

## For the first time

```bash
$ pip install hooking
```

## Upgrade
```bash
$ pip install hooking --upgrade --upgrade-strategy eager

```

## Show information
```bash
$ pip show hooking
```


<br>
<br>
<br>

[Back to top](#readme)