Back to [All Modules](https://github.com/pyrustic/hooking/blob/master/docs/modules/README.md#readme)

# Module Overview

**hooking**
 
Hooking module

> **Classes:** &nbsp; [Break](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/Break.md#class-break) &nbsp;&nbsp; [H](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/H.md#class-h)
>
> **Functions:** &nbsp; None
>
> **Constants:** &nbsp; ANY &nbsp;&nbsp; ENTER &nbsp;&nbsp; LEAVE

# Class H
Hooking class

## Base Classes
object

## Class Attributes
No class attributes.

## Class Properties
|Property|Type|Description|Inherited from|
|---|---|---|---|
|events|getter|Get names of events||
|frozen|getter|Get the value of frozen state||
|hids|getter|Get HIDs (Hook IDs)||



# All Methods
[\_\_init\_\_](#__init__) &nbsp;&nbsp; [bind](#bind) &nbsp;&nbsp; [check\_event](#check_event) &nbsp;&nbsp; [check\_hook](#check_hook) &nbsp;&nbsp; [clear](#clear) &nbsp;&nbsp; [enter\_event](#enter_event) &nbsp;&nbsp; [freeze](#freeze) &nbsp;&nbsp; [leave\_event](#leave_event) &nbsp;&nbsp; [unbind](#unbind) &nbsp;&nbsp; [unfreeze](#unfreeze) &nbsp;&nbsp; [\_gen\_hid](#_gen_hid) &nbsp;&nbsp; [\_raise](#_raise) &nbsp;&nbsp; [\_run\_hook](#_run_hook)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## bind
Bind a hook to an event. Typically called by the event consumer.




**Signature:** (self, event, hook, spec='enter', accept\_input=True)

|Parameter|Description|
|---|---|
|event|the name of the event (str)|
|hook|a function to call when the event will occur given a specification. Note that this function must accept at least a context (hooking.dto.Context) argument.|
|spec|one of ENTER, LEAVE, or ANY. Defaults to ENTER|
|accept\_input|set True if the hook expects some input data from the event producer |





**Return Value:** The HID (Hook ID)

[Back to Top](#module-overview)


## check\_event
Check if there are hooks bound to a specific event




**Signature:** (self, event)

|Parameter|Description|
|---|---|
|event|name of the event |





**Return Value:** Returns None if there are no hooks bound to the event.
Returns a tuple of hids (Hook IDs) of bound hooks

[Back to Top](#module-overview)


## check\_hook
Check whether a hook has been registered or not




**Signature:** (self, hid)

|Parameter|Description|
|---|---|
|hid|Hook ID |





**Return Value:** Returns None if the hook doesn't exist.
Returns a hooking.dto.HookInfo that is a namedtuple.
The attributes of HookInfo are: hid, event, spec, accept_input

[Back to Top](#module-overview)


## clear
Clear events and hooks. Set the 'frozen' attribute to False



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## enter\_event
Notify the beginning of an event. Typically called by the event producer.
Note that this method won't complete if the H object is frozen.




**Signature:** (self, event, \*args, \*\*kwargs)

|Parameter|Description|
|---|---|
|event|the name of the event (str)|
|\*args|arguments to send to the hook(s) expected to be called|
|\*\*kwargs|arguments to send to the hook(s) expected to be called |





**Return Value:** Returns True if hooks have been called without any Break raised

[Back to Top](#module-overview)


## freeze
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## leave\_event
Notify the end of an event. Typically called by the event producer.
Note that this method won't complete if the H object is frozen.




**Signature:** (self, event, \*args, \*\*kwargs)

|Parameter|Description|
|---|---|
|event|the name of the event (str)|
|\*args|arguments to send to the hook(s) expected to be called|
|\*\*kwargs|arguments to send to the hook(s) expected to be called |





**Return Value:** Returns True if hooks have been called without any Break raised

[Back to Top](#module-overview)


## unbind
Unbind hooks from an event




**Signature:** (self, \*hids)

|Parameter|Description|
|---|---|
|\*hids|Hook IDs|





**Return Value:** None

[Back to Top](#module-overview)


## unfreeze
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_gen\_hid
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_raise
No description



**Signature:** (self, event, spec, \*args, \*\*kwargs)





**Return Value:** None

[Back to Top](#module-overview)


## \_run\_hook
No description



**Signature:** (self, info, spec, \*args, \*\*kwargs)





**Return Value:** None

[Back to Top](#module-overview)



