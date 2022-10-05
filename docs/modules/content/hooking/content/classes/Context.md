Back to [All Modules](https://github.com/pyrustic/hooking/blob/master/docs/modules/README.md#readme)

# Module Overview

**hooking**
 
Hooking module

> **Classes:** &nbsp; [ChainBreak](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/ChainBreak.md#class-chainbreak) &nbsp;&nbsp; [Context](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/Context.md#class-context) &nbsp;&nbsp; [Error](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/Error.md#class-error) &nbsp;&nbsp; [H](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/H.md#class-h) &nbsp;&nbsp; [HookInfo](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/HookInfo.md#class-hookinfo)
>
> **Functions:** &nbsp; None
>
> **Constants:** &nbsp; AFTER &nbsp;&nbsp; BEFORE

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
|hid|getter|Get hid||
|kwargs|getter|Get kwargs||
|kwargs|setter|Set kwargs||
|result|getter|Get result||
|result|setter|Set result||
|spec|getter|Get spec||
|tag|getter|Get tag||
|target|getter|Get target||
|target|setter|Set target||



# All Methods
[\_\_init\_\_](#__init__)

## \_\_init\_\_
Initialize a context object




**Signature:** (self, hid, tag, spec, target, args, kwargs, result)

|Parameter|Description|
|---|---|
|hid|hook id|
|tag|str, the label used to tag a function or method|
|spec|either BEFORE or AFTER|
|target|the tagged function or method|
|args|tuple representing arguments passed to the target|
|kwargs|dict representing keyword arguments passed to the target|
|result|if spec is set to AFTER, result is the value returned by the target|





**Return Value:** None

[Back to Top](#module-overview)



