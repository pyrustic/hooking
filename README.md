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
<b> Generic dual-paradigm hooking mechanism </b>


This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).
> [Modules documentation](https://github.com/pyrustic/hooking/tree/master/docs/modules#readme)


## Table of contents
- [Overview](#overview)
- [Examples](#examples)
- [Functions and methods as targets](#functions-and-methods-as-targets)
- [Anatomy of a hook](#anatomy-of-a-hook)
- [Tight coupling](#tight-coupling)
    - [Override a target](#override-a-target)
    - [Wrap a target](#wrap-a-target)
- [Loose coupling](#loose-coupling)
    - [Tagging mechanism](#tagging-mechanism)
    - [Bind hooks to tags](#bind-hooks-to-tags)
    - [Chain break](#chain-break)
    - [Freeze the hooking class](#freeze-the-hooking-class)
    - [Exposed data](#exposed-data)
    - [Reset the hooking class](#reset-the-hooking-class)
    - [Subclassing the hooking class](#subclassing-the-hooking-class)
- [Miscellaneous](#miscellaneous)
- [Installation](#installation)

# Overview
This project is a minimalist [Python](https://www.python.org) library that implements an intuitive, flexible, and generic dual-paradigm [hooking](https://en.wikipedia.org/wiki/Hooking) mechanism.

In short, **methods** and **functions**, called **targets**, are [decorated](https://peps.python.org/pep-0318/) and assigned user-defined **hooks**. So when a target is called, the assigned hooks will be automatically executed **upstream** or **downstream** according to the specification provided by the programmer.

The programmer may wish to have **tight** or **loose** [coupling](https://en.wikipedia.org/wiki/Coupling_(computer_programming)) between targets and hooks, depending on the requirement. Hence, for a nice developer experience, this library provides two interfaces each representing a **paradigm** (tight or loose coupling) to cover the needs.

From a hook, the programmer has access to the keyword arguments passed to the decorator, the arguments passed to the target, the target itself, and other useful information through a `Context` object.

Depending on whether the hook is executed upstream or downstream, the programmer can modify arguments to target, override the target itself with an arbitrary [callable](https://en.wikipedia.org/wiki/Callable_object), break the execution of the chain of hooks, modify the return of the target, et cetera.


## Why use this library
This library allows the programmer to **wrap**, **augment**, or **override** a function or method with either a tight or loose coupling. It is therefore the perfect solution to create a [plugin mechanism](https://en.wikipedia.org/wiki/Plug-in_(computing)) for a project.

It can also be used for **debugging**, **benchmarking**, [event-driven programming](https://en.wikipedia.org/wiki/Event-driven_programming), implementing routing in a web development framework ([Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) uses decorators to implement [routing](https://hackersandslackers.com/flask-routes/)), et cetera.

The interface of this library is designed to be intuitive to use not only for **crafting** an [API](https://en.wikipedia.org/wiki/API) but also for **consuming** it.


<p align="right"><a href="#readme">Back to top</a></p>

# Examples
Here are some examples of using this library in the tight and loose coupling paradigm.

## Measure execution time
Here we will use the tight coupling paradigm to override the target function with a hook. From inside the hook, the target will be executed and we will measure the execution time.

The following example can be copy-pasted into a file (e.g. `test.py`) and run as is:

```python
import time
from hooking import override


def timeit(context, *args, **kwargs):
    # execute and measure the target run time
    start_time = time.perf_counter()
    context.result = context.target(*args, **kwargs)
    total_time = time.perf_counter() - start_time
    # print elapsed time
    text = context.config.get("text")  # get 'text' from config data
    print(text.format(total=total_time))


# decorate 'heavy_computation' with 'override' (tight coupling)
# here, 'timeit' is the hook to execute when the target is called
# all following keyword arguments are part of the configuration data
@override(timeit, text="Done in {total:.3f} seconds !")
def heavy_computation(a, b):
    time.sleep(2)  # doing some heavy computation !
    return a*b


if __name__ == "__main__":
    # run 'heavy_computation'
    result = heavy_computation(6, 9)
    print("Result:", result)
```

```bash
$ python -m test
Done in 2.001 seconds !
Result: 54
```

<p align="right"><a href="#readme">Back to top</a></p>

## Routing by a fictional web framework
This example is divided into two parts:
- the server-side Python script;
- and the internals of the web framework.


### Server-side Python script

```python
# Script for the server-side (API consumer side)
# web_script.py
from my_web_framework import Routing, start

# bind to 'home_view', three tags representing
# three paths. This view will be executed when
# the user will request the home page for example
@Routing.tag("/")
@Routing.tag("/home")
@Routing.tag("/index")
def home_view():
    return "Welcome !"


@Routing.tag("/about")
def about_view():
    return "About..."


if __name__ == "__main__":
    start()
```

### Web framework internals
```python
# Framework internals (API creator side)
# my_web_framework.py
import random
from hooking import H

# implementing custom routing mechanism by subclassing hooking.H
Routing = H.subclass("Routing")

def start():
    # entry point of the web framework
    # Get user request, then serve the appropriate page
    path = get_user_request()
    serve_page(path)

def get_user_request():
    # use randomness to simulate user page request
    paths = ("/", "/home", "/index", "/about")
    return random.choice(paths)

def serve_page(path):
    # get the list of functions and methods
    # tagged with the Routing.tag decorator
    cache = Routing.targets.get(path, list())
    for target_info in cache:
        view = target_info.target
        html = view()
        render_html(html)

def render_html(html):
    print(html)
```


<p align="right"><a href="#readme">Back to top</a></p>


# Functions and methods as targets
As mentioned in the [Overview](#overview) section, functions and methods are the targets to which hooks are attached with a tight or loose coupling. A hook is a function that can be attached one or more times to one or more targets.

Static methods, class methods, or decorated methods or functions should work fine with this library as long as one comes as close as possible to the native definition of the function or method. Example:

```python
from hooking import H, on_enter, on_leave

class MyClass:
    # Good !
    @staticmethod
    @H.tag  # innermost
    def do_something1(arg):
        pass

    # BAD !!!
    @H.tag  # outermost
    @classmethod
    def do_something2(cls, arg):
        pass

def my_hook(context, *arg, **kwargs):
    pass

# Good !
@ExoticDecorator
@on_enter(my_hook)  # innermost
def my_func():
    pass

# BAD !!!
@on_leave(my_hook)  # outermost
@ExoticDecorator
def my_func():
    pass
```


<p align="right"><a href="#readme">Back to top</a></p>

# Anatomy of a hook
A hook is a callable that accepts an instance of `hooking.Context` and arguments passed to the target.

The `hooking.Context` instance exposes the following attributes:

- **cls**: the hook class;
- **hid**: the Hook ID (HID) as returned by the class methods `H.wrap`, `H.on_enter`, and `H.on_leave`;
- **tag**: label string used to tag a function or method;
- **config**: dictionary representing keyword arguments passed to the decorator;
- **spec**: either the `hooking.ENTER` constant or the `hooking.LEAVE` constant;
- **target**: the decorated function or method;
- **args**: tuple representing the positional arguments passed to the target;
- **kwargs**: dictionary representing the keyword arguments passed to the target;
- **result**: depending on the context, this attribute may contain the value returned by the target;
- **shared**: ordered dictionary to store shared data between hooks (from upstream to downstream).

The attributes listed above can be updated with the `Context.update` method that accepts keyword arguments.


```python
from hooking import H

# defining my_hook
def my_hook(context, *args, **kwargs):
    if context.tag != "target":
        raise Exception("Wrong tag !")
    # reset arguments
    context.update(args=tuple(), kwargs=dict())

@H.tag("target")  # tagging my_func with "target"
def my_func(*args, **kwargs):
    pass

# binding my_hook to the tag "target"
H.on_enter("target", my_hook)
```

## Modify arguments to target
From an upstream hook, we can change the arguments passed to a target:
```python
# ...

def upstream_hook(context, *args, **kwargs):
    # positional arguments are represented with a tuple
    context.args = (val1, val2)
    # keywords arguments are represented with a dictionary
    context.kwargs = {"item1": val1, "item2": val2}
 
# ...
``` 

<p align="right"><a href="#readme">Back to top</a></p>

## Override the target from a hook
The library exposes the `hooking.override` to override a target function:

```python
from hooking import override

def myhook(context, *args, **kwargs):
    context.result = new_target_function(*args, **kwargs)

@override(myhook) 
def target():
    pass
```

but one can still override the target from an arbitrary **upstream** hook:

```python
from hooking import on_enter

def upstream_hook(context, *args, **kwargs):
    # override target with a new target that
    # that accepts same type signature
    context.target = new_target_function
 
@on_enter(upstream_hook) 
def target():
    pass
``` 

Note that you can set `None` to `context.target` to prevent the library for automatically running the target between the execution of upstream and downstream hooks.

<p align="right"><a href="#readme">Back to top</a></p>

## Modify the return of a target
From a downstream hook, we can change the return of a target:
```python
# ...

def downstream_hook(context, *args, **kwargs):
    context.result = new_value
 
# ...
``` 

<p align="right"><a href="#readme">Back to top</a></p>


# Tight coupling
In this paradigm, hooks are directly bound to target. The library exposes the following decorators to decorate targets:

|Decorator|Description|Signature
|---|---|---|
|`hooking.override`|Bind to a target a hook that will override it|`@override(hook, **config)`|
|`hooking.wrap`|Bind to a target two hooks that will be executed upstream and downstream|`@wrap(hook1, hook2, **config)`|
|`hooking.on_enter`|Bind to a target a hook that will be executed upstream, i.e, before the target|`@on_enter(hook, **config)`|
|`hooking.on_leave`|Bind to a target a hook that will be executed downstream, i.e, after the target|`@on_leave(hook, **config)`|

## Override a target
The library exposes the `hooking.override` decorator to bind to a target a hook that will override it:


```python
from hooking import override

def myhook(context, *args, **kwargs):
    context.result = context.target(*args, **kwargs)
    # or
    my_new_target = lambda *args, **kwargs: print("New Target Here !")
    context.result = my_new_target(*args, **kwargs)

# override target with myhook
@override(hook3, foo=42, bar="Alex")  # foo and bar are config data
def target():
    pass
```

> Note that with the `hooking.override` decorator, the programmer must execute the target or its replacement inside the hook and set the result to `context.result`.

<p align="right"><a href="#readme">Back to top</a></p>

## Wrap a target
The `hooking.wrap` decorator allows the programmer to wrap the target between two hooks that will be executed upstream and downstream. Two additional decorators `hooking.on_enter` and `hooking.on_leave` allow the programmer to bind either a upstream or a downstream hook to a target.

```python
from hooking import wrap, on_enter, on_leave

def hook1(context, *args, **kwargs):
    pass

def hook2(context, *args, **kwargs):
    pass

# bind an upstream hook and a downstream hook to my_func1
@wrap(hook1, hook2, foo=42, bar="Alex")  # foo and bar are config data
def my_func1():
    pass

# bind an upstream hook to my_func2
@on_enter(hook1, foo=42, bar="Alex")
def my_func2():
    pass

# bind a downstream hook to my_func3
@on_leave(hook2, foo=42, bar="Alex")
def my_func3():
    pass

```

<p align="right"><a href="#readme">Back to top</a></p>

# Loose coupling
In this paradigm, hooks aren't directly bound to target but to tags which are linked to targets. The library exposes the `hooking.H` class to support the loose coupling paradigm. In short, the `hooking.H.tag` decorator is used to tag targets, then class methods `hooking.H.on_enter`, `hooking.H.on_leave`, and `hooking.H.wrap` are used to bind hooks to tags.

## Tagging mechanism
The `hooking.H.tag` class method allows you to tag a function or a method:
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
The `hooking.H.tag` decorator accepts a `label` string as argument. By default, when this argument isn't provided, the library uses the [qualified name](https://peps.python.org/pep-3155/) of the method or function as the `label`.

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

<p align="right"><a href="#readme">Back to top</a></p>

## Bind hooks to tags
These are the `hooking.H` class methods to bind hooks to tags:

|Class method|Description|Signature
|---|---|---|
|`hooking.H.on_enter`|Bind to a tag a hook that will be executed downstream, i.e, before the target|`on_enter(tag, hook)`|
|`hooking.H.on_leave`|Bind to a tag a hook that will be executed downstream, i.e, after the target|`on_leave(tag, hook)`|
|`hooking.H.wrap`|Bind to a tag two hooks that will be executed upstream and downstream|`wrap(tag, hook1, hook2)`|


```python
from hooking import H

@H.tag("target")
def my_func(*args, **kwargs):
    pass

def my_hook1(context, *args, **kwargs):
    pass

def my_hook2(context, *args, **kwargs):
    pass

# bind my_hook1 to "target" and run it upstream
hook_id = H.on_enter("target", my_hook1)

# bind my_hook2 to "target" and run it downstream
hook_id = H.on_leave("target", my_hook2)

# bind my_hook1 and my_hook2 to "target"
hook_id1, hook_id2 = H.wrap("target", my_hook1, my_hook2)
```

### Unbind hooks

Whenever a hook is bound to a tag, the Hook ID (HID) which could be used later to **unbind** the hook, is returned:

```python
from hooking import H

def hook(context, *args, **kwargs):
    pass

# bind
hid = H.on_enter("tag", hook)

# unbind
H.unbind(hid)
```

**Multiple** hooks can be unbound in a single statement:

```python
from hooking import H

def hook1(context, *args, **kwargs):
    pass

def hook2(context, *args, **kwargs):
    pass

# bind
hid1 = H.on_enter("tag", hook1)
hid2 = H.on_leave("tag", hook2)

# unbind multiple hooks manually
H.unbind(hid1, hid2)
```


### Clear hooks bound to a specific tag
The `clear` class method of `hooking.H` unbinds all hooks bound to a specific tag:
```python
from hooking import H

def hook1(context, *args, **kwargs):
    pass

def hook2(context, *args, **kwargs):
    pass

@H.tag
def target():
    pass

# bind
hid1 = H.on_enter("target", hook1)
hid2 = H.on_enter("target", hook2)

# unbind hook1 and hook2 from "target"
H.clear("target")

```

You can clear **multiple** tags in a single statement:
```python
from hooking import H

def hook1(context, *args, **kwargs):
    pass

def hook2(context, *args, **kwargs):
    pass

@H.tag
def target1():
    pass

@H.tag
def target2():
    pass

# bind
hid1 = H.on_enter("target1", hook1)
hid2 = H.on_enter("target2", hook2)

# unbind hook1 and hook2 from "target1" and "target2"
H.clear("target1", "target2")

```


<p align="right"><a href="#readme">Back to top</a></p>


## Chain break
This library exposes an [Exception](https://docs.python.org/3/library/exceptions.html#Exception) subclass to allow the programmer to break the execution of a chain of hooks:

```python
from hooking import H, ChainBreak

@H.tag("target")
def my_func(*args, **kwargs):
    pass
    
def hook1(context, *args, **kwargs):
    pass

def hook2(context, *args, **kwargs):
    raise ChainBreak

def hook3(context, *args, **kwargs):
    pass


# bind hook1, hook2 and hook3 to 'target'
for hook in (hook1, hook2, hook3):
    H.on_enter("target", hook)

# call the target
my_func()

# since the target was called,
# the chain of hooks (hook1, hook2, hook3)
# must be executed.

# hook2 having used ChainBreak,
# the chain of execution will be broken
# and hook3 will be ignored

```

<p align="right"><a href="#readme">Back to top</a></p>

## Freeze the hooking class
We could freeze the hooking class and thus prevent the execution of all hooks:
```python
from hooking import H

@H.tag
def my_func(*args, **kwargs):
    pass

H.freeze()

# from now, no hook will be executed anymore
```

### Unfreeze the hooking class

To **unfreeze** the hooking class, use the `H.unfreeze` class method:
```python
from hooking import H

H.unfreeze()

# from now, hooks will be executed when needed
```

<p align="right"><a href="#readme">Back to top</a></p>

## Exposed data
The library exposes data through a class method, class variables, and data transfer objects (namedtuples).

### Get the list of upstream and downstream hooks
Upstream and downstream hooks bound to a specific tag can be retrieved with the `get_hooks` class method.

```python
from hooking import H

# returns a 2-tuple of upstream hooks and
# downstream hooks
upstream_hooks, downstream_hooks = H.get_hooks("tag")

# iterate through upstream_hooks which is
# a list of instances of hooking.HookInfo
for hook_info in upstream_hooks:
    print(hook_info)
```

### Read-only class variables
The `hooking.H` class exposes the following class variables:

|Class variable|Description|
|---|---|
|`targets`| Ordered dictionary. Keys are tags and values are lists of instances of `hooking.TargetInfo`. Example: {"tag1": [TargetInfo(), TargetInfo(), ...], ...}|
|`hooks`| Ordered dictionary. Keys are tags and values are lists of instances of `hooking.HookInfo`. Example: {"tag1": [HookInfo(), HookInfo(), ...], ...}| 
|`tags`| The set of registered tags|
|`frozen`| Boolean to tell whether the hooking mechanism is frozen or not|

> **Note:** it is not recommended to modify the contents of these class variables directly. Use the appropriate class methods for this purpose.

Both `hooking.TargetInfo` and `hoooking.HookInfo` are namedtuples that will be explored in the next subsection.

### Data transfer object
Here are the fields from the `hooking.TargetInfo` namedtuple:
- **cls**: the hooking class;
- **tag**: the string label that represents the tag;
- **target**: the target method or function;
- **config**: dictionary containing the configuration data passed to the decorator.

Here are the fields from the `hooking.HookInfo` namedtuple:
- **cls**: the hooking class;
- **hid**: the hook identifier;
- **hook**: the callable representing the hook;
- **tag**: the string label that represents the tag;
- **spec**: either `hooking.ENTER` or `hooking.LEAVE`.


<p align="right"><a href="#readme">Back to top</a></p>


## Reset the hooking class
You may need to reset the hooking class, i.e., reinitialize the contents of the following class variables: `hooking.H.hooks`, `hooking.H.tags`, and `hooking.H.frozen`. In this case, you just have to call the `hooking.H.reset` class method.

> **Note:** targets won't be removed.

<p align="right"><a href="#readme">Back to top</a></p>

## Subclassing the hooking class
This library is flexible enough to allow the programmer to create their own subclass of `hooking.H` like this:

```python
from hooking import H

MyCustomHookingClass = H.subclass("MyCustomHookingClass")
```

Subclassing `hooking.H` allows the programmer to apply the [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns). For example, a web framework creator might create a `Routing` subclass to implement a routing mechanism, and also create an `Extension` subclass to implement a plugin mechanism. Each subclass would have its own set of tags, hooks, and targets.

> **Note:** class variables are automatically reset when subclassing `hooking.H`.

<p align="right"><a href="#readme">Back to top</a></p>

# Miscellaneous

## Multithreading
Whenever threads are introduced into a program, the state shared between threads becomes vulnerable to corruption. To avoid this situation, this library uses [threading.Lock](https://docs.python.org/3/library/threading.html#lock-objects) as a synchronization tool.


<p align="right"><a href="#readme">Back to top</a></p>

# Installation
**Hooking** is **cross-platform** and should work on **Python 3.5** or [newer](https://www.python.org/downloads/).

## First time

```bash
$ pip install hooking
```

## Upgrade
```bash
$ pip install hooking --upgrade --upgrade-strategy eager

```

## Show package information
```bash
$ pip show hooking
```


<br>
<br>
<br>

[Back to top](#readme)
