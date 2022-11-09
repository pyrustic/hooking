Back to [All Modules](https://github.com/pyrustic/hooking/blob/master/docs/modules/README.md#readme)

# Module Overview

**hooking.runner**
 
Runner module

> **Classes:** &nbsp; [Runner](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking.runner/content/classes/Runner.md#class-runner)
>
> **Functions:** &nbsp; None
>
> **Constants:** &nbsp; ENTER &nbsp;&nbsp; LEAVE

# Class Runner
Run a target and hooks directly or indirectly bound to it

## Base Classes
object

## Class Attributes
No class attributes.

## Class Properties


# All Methods
[\_\_init\_\_](#__init__) &nbsp;&nbsp; [run](#run) &nbsp;&nbsp; [\_run\_hooks](#_run_hooks)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.



**Signature:** (self, cls=None, tag=None, config=None, target=None, args=None, kwargs=None)





**Return Value:** None

[Back to Top](#module-overview)


## run
Run the target and hooks




**Signature:** (self, upstream\_hooks, downstream\_hooks)

|Parameter|Description|
|---|---|
|upstream\_hooks|list of upstream hooks|
|downstream\_hooks|list of downstream hooks |





**Return Value:** Return the result

[Back to Top](#module-overview)


## \_run\_hooks
No description



**Signature:** (self, hooks, spec=1)





**Return Value:** None

[Back to Top](#module-overview)



