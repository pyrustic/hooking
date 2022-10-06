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
<b> Generic hooking mechanism for Python </b>


This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).
> [Modules documentation](https://github.com/pyrustic/hooking/tree/master/docs/modules#readme)


## Table of contents
- [Overview](#overview)
- [Tagging mechanism](#tagging-mechanism)
- [Bind hooks](#bind-hooks)
- [Anatomy of a hook](#anatomy-of-a-hook)
- [Chain break](#chain-break)
- [Freeze tags](#freeze-tags)
- [Exposed variables](#exposed-variables)
- [Clear data](#clear-data)
- [Examples](#examples)
- [Miscellaneous](#miscellaneous)
- [Installation](#installation)

# Overview
This library, written in **Python**, implements an intuitive and minimalist [hooking](https://en.wikipedia.org/wiki/Hooking) mechanism. It exposes a [decorator](https://peps.python.org/pep-0318/) to tag **methods** and **functions** (targets), and so when they are called, user-defined hooks will be executed upstream or downstream according to the spec (either `BEFORE` or `AFTER`) provided by the user. 

Arguments to targets are passed to hooks which can modify them or replace the targets themselves with an arbitrary [callable](https://en.wikipedia.org/wiki/Callable_object) or `None`. 

Thanks to the tagging mechanism, hooks are not directly tied to targets but to tags (either user-defined or derived from functions or methods themselves). Thus, hooks are loosely coupled to targets and dynamically bound to tags.

## Why use this library
This library allows the programmer to **augment** a function or method. It is therefore the perfect solution to create a [plugin mechanism](https://en.wikipedia.org/wiki/Plug-in_(computing)) for a project. It can also be used for **debugging** or **benchmarking**. Thanks to its generic nature, one can consider "tags" as "events" and use this library to perform [event-driven programming](https://en.wikipedia.org/wiki/Event-driven_programming). This project can also help implement routing in a web development framework ([Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) uses decorators to implement [routing](https://divpusher.com/glossary/routing/)).

The interface of this library is designed to be intuitive not only for an API author who needs to implement hooking, but also for API consumers who need an easy and efficient way to interact with an API.

Check out few [examples](#examples).

## About decoration
This library uses Python [decorators](https://peps.python.org/pep-0318/) to tag functions and methods. This is a change from earlier iterations where the programmer had to store and pass a reference to an instance of the `Hooking` class. Decorators make the interface more intuitive and convenient to interact with.


# Tagging mechanism
The `H.tag` class method allows you to tag a function or a method:
```python
from hooking import H

@H.tag
def my_func(*args, **kwargs):
    pass

class MyClass:
    @H.tag
    def my_method(self, *args, **kwargs):
        pass
```
`H.tag` accepts a `label` string as argument. By default, when this argument isn't provided, the library uses the [qualified name](https://peps.python.org/pep-3155/) of the method or function as the `label`.

Here we provide the `label` argument:
```python
from hooking import H

@H.tag("my_func")
def my_func(*args, **kwargs):
    pass

class MyClass:
    @H.tag("MyClass.my_method")
    def my_method(self, *args, **kwargs):
        pass
```

# Bind hooks
Hooks are not directly bound to functions or methods but to tags. The `H.bind` class method  allows the user to bind a hook to a tag and specify with the `spec` parameter whether the hook should be run upstream or downstream.

```python
from hooking import H, BEFORE, AFTER

@H.tag("target")
def my_func(*args, **kwargs):
    pass

def my_hook1(context):
    pass

def my_hook2(context):
    pass

# bind my_hook1 to "target" and run it upstream
H.bind("target", my_hook1) # by default, spec == BEFORE

# bind my_hook1 to "target" and run it downstream
hook_id = H.bind("target", my_hook2, spec=AFTER)
```
The `H.bind` class method returns a Hook ID (HID) which could be used later to **unbind** the hook:

```python
from hooking import H

def hook(context):
    pass

# bind
hid = H.bind("tag", hook)

# unbind
H.unbind(hid)
```

**Multiple** hooks can be unbound in a single statement:

```python
from hooking import H

def hook1(context):
    pass

def hook2(context):
    pass

# bind
hid1 = H.bind("tag", hook1)
hid2 = H.bind("tag", hook2)

# unbind multiple hooks manually
H.unbind(hid1, hid2)

# unbind all hooks automatically
H.unbind()
```

# Anatomy of a hook
A hook is a callable that accepts an instance of `hooking.Context` that exposes the following attributes:
- `hid`: the Hook ID (HID) as returned by `H.bind`;
- `tag`: the label string used to tag a function or method;
- `spec`: one of the `BEFORE` or `AFTER` constants;
- `target`: the function or method tagged with the `H.tag` decorator;
- `args`: tuple representing the arguments passed to the target;
- `kwargs`: dictionary representing the keyword arguments passed to the target;
- `result`: when spec is set to `AFTER`, this attribute contains the value returned by the target.

```python
from hooking import H, BEFORE, AFTER

@H.tag("target")
def my_func(*args, **kwargs):
    pass

def my_hook(context):
    if context.tag != "target":
        raise Exception("Wrong tag !")

H.bind("target", my_hook)
```

# Chain break
This library exposes an exception subclass to allow the programmer to break the execution of a chain of hooks:
```python
from hooking import H, ChainBreak

@H.tag("target")
def my_func(*args, **kwargs):
    pass

def hook1(context):
    pass

def hook2(context):
    raise ChainBreak

def hook3(context):
    pass

# bind hook1, hook2 and hook3 to 'target'
for hook in (hook1, hook2, hook3):
    H.bind("target", hook)

# call the target
my_func()

# since the target was called,
# the chain of hooks (hook1, hook2, hook3)
# must be executed.

# hook2 having used ChainBreak,
# the chain of execution will be broken
# and hook3 will be ignored

```

# Freeze tags
We could freeze a tag and thus prevent the execution of hooks bound to this tag:
```python
from hooking import H, BEFORE, AFTER

@H.tag
def my_func(*args, **kwargs):
    pass

H.freeze("my_func")

# from now on hooks bound to `my_func` will no longer be executed
```
The `H.freeze` class method can freeze multiple tags at once, or the entire hooking mechanism:
```python
from hooking import H, BEFORE, AFTER

# freeze all tags manually
H.freeze("tag1", "tag2", "tag3", "tagx")

# freeze the entire hooking mechanism
H.freeze()

# from now, no hook will be executed anymore
```

To **unfreeze** specific tags or the entire hooking mechanism, use the `H.unfreeze` class method:
```python
from hooking import H, BEFORE, AFTER

# unfreeze all tags manually
H.unfreeze("tag1", "tag2", "tag3", "tagx")

# unfreeze the entire hooking mechanism
H.unfreeze()

# from now, hooks will be executed when needed
```

# Exposed variables
The `H` class exposes the following class variables:
- `hooks`: dict, keys are HIDs (Hook IDs), values are instances of `HookInfo`; 
- `tags`: dict to hold relationship between tags and HIDs. Keys are tags, and values are sets; 
- `frozen`: boolean to tell whether the hooking mechanism is frozen or not;
- `frozen_tags`: set containing frozen tags.

# Clear data
The `H.clear` class method resets the following class variables: `H.hooks`, `H.tags`, `H.frozen`, `H.frozen_tags`.


# Examples
Just few examples.

## Event-driven programming


```python
from hooking import H, BEFORE, AFTER
from myapp import App


class Dashboard(App):
        
    H.tag
    def on_login(self, event, username, password):
        pass

# hook to run before login
def before_login(context):
    pass

# hook to run after login
def after_login(context):
    pass
    

# bind hooks to the "Dashboard.on_login" tag
H.bind("Dashboard.on_login", before_login)  # by default spec == BEFORE
H.bind("Dashboard.on_login", after_login, spec=AFTER)


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()
    # from now, before_login hook will be executed before the login
    # and after_login hook will be executed after the login
```

## Micro web framework

```python
from hooking import H, BEFORE, AFTER
from mywebframework import App


class Dashboard(App):
        
    H.tag("/site/login")
    def on_login(self, event, username, password):
        pass

# hook to run before login
def before_login(context):
    pass

# hook to run after login
def after_login(context):
    pass
    

# bind hooks to the "Dashboard.on_login" tag
H.bind("/site/login", before_login)  # by default spec == BEFORE
H.bind("/site/login", after_login, spec=AFTER)


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()
    # from now, before_login hook will be executed before the login
    # and after_login hook will be executed after the login
```


# Miscellaneous
Whenever threads are introduced into a program, the state shared between threads becomes vulnerable to corruption. To avoid this situation, this library uses [threading.Lock](https://docs.python.org/3/library/threading.html#lock-objects) as a synchronization tool.

# Installation
**Hooking** is **cross-platform** and should work on **Python 3.5** or [newer](https://www.python.org/downloads/).

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
