Back to [All Modules](https://github.com/pyrustic/hooking/blob/master/docs/modules/README.md#readme)

# Module Overview

**hooking.context**
 
Context class

> **Classes:** &nbsp; [Context](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking.context/content/classes/Context.md#class-context)
>
> **Functions:** &nbsp; None
>
> **Constants:** &nbsp; FIELDS

# Class Context
An instance of this class is passed to hooks

## Base Classes
object

## Class Attributes
No class attributes.

## Class Properties
|Property|Type|Description|Inherited from|
|---|---|---|---|
|args|getter|Get args||
|args|setter|Set args||
|cls|getter|Get hooking class||
|config|getter|Get config||
|hid|getter|Get hid||
|kwargs|getter|Get kwargs||
|kwargs|setter|Set kwargs||
|result|getter|Get result||
|result|setter|Set result||
|shared|getter|Get shared||
|spec|getter|Get spec||
|tag|getter|Get tag||
|target|getter|Get target||
|target|setter|Set target||



# All Methods
[\_\_init\_\_](#__init__) &nbsp;&nbsp; [update](#update)

## \_\_init\_\_
Initialize a context object




**Signature:** (self, cls=None, hid=None, tag=None, config=None, spec=None, target=None, args=None, kwargs=None, result=None, shared=None)

|Parameter|Description|
|---|---|
|cls|hooking class|
|hid|hook id|
|tag|str, the label used to tag a function or method|
|config|dict, data associated to the tag at the level of the decoration|
|spec|either `hooking.ENTER` or `hooking.LEAVE`|
|target|the target function or method|
|args|tuple representing arguments passed to the target|
|kwargs|dict representing keyword arguments passed to the target|
|result|if spec is set to `hooking.LEAVE`, result is the value returned by the target|
|shared|ordered dictionary to store shared data between hooks|





**Return Value:** None

[Back to Top](#module-overview)


## update
Update one or multiple fields



**Signature:** (self, \*\*kwargs)





**Return Value:** None

[Back to Top](#module-overview)



