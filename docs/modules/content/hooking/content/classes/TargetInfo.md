Back to [All Modules](https://github.com/pyrustic/hooking/blob/master/docs/modules/README.md#readme)

# Module Overview

**hooking**
 
No description

> **Classes:** &nbsp; [ChainBreak](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/ChainBreak.md#class-chainbreak) &nbsp;&nbsp; [Context](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/Context.md#class-context) &nbsp;&nbsp; [Error](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/Error.md#class-error) &nbsp;&nbsp; [H](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/H.md#class-h) &nbsp;&nbsp; [HookInfo](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/HookInfo.md#class-hookinfo) &nbsp;&nbsp; [TargetInfo](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/TargetInfo.md#class-targetinfo)
>
> **Functions:** &nbsp; [on\_enter](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/functions.md#on_enter) &nbsp;&nbsp; [on\_leave](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/functions.md#on_leave) &nbsp;&nbsp; [wrap](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/functions.md#wrap)
>
> **Constants:** &nbsp; ENTER &nbsp;&nbsp; LEAVE

# Class TargetInfo
TargetInfo(cls, tag, target, config)

## Base Classes
tuple

## Class Attributes
\_field\_defaults &nbsp;&nbsp; \_fields &nbsp;&nbsp; \_fields\_defaults &nbsp;&nbsp; \_make &nbsp;&nbsp; cls &nbsp;&nbsp; config &nbsp;&nbsp; tag &nbsp;&nbsp; target

## Class Properties


# All Methods
[count](#count) &nbsp;&nbsp; [index](#index) &nbsp;&nbsp; [\_asdict](#_asdict) &nbsp;&nbsp; [\_replace](#_replace)

## count
Return number of occurrences of value.

**Inherited from:** tuple

**Signature:** (self, value, /)





**Return Value:** None

[Back to Top](#module-overview)


## index
Return first index of value.

Raises ValueError if the value is not present.

**Inherited from:** tuple

**Signature:** (self, value, start=0, stop=9223372036854775807, /)





**Return Value:** None

[Back to Top](#module-overview)


## \_asdict
Return a new dict which maps field names to their values.



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_replace
Return a new TargetInfo object replacing specified fields with new values



**Signature:** (self, /, \*\*kwds)





**Return Value:** None

[Back to Top](#module-overview)



