Back to [All Modules](https://github.com/pyrustic/hooking/blob/master/docs/modules/README.md#readme)

# Module Overview

**hooking**
 
No description

> **Classes:** &nbsp; [ChainBreak](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/ChainBreak.md#class-chainbreak) &nbsp;&nbsp; [Context](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/Context.md#class-context) &nbsp;&nbsp; [Error](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/Error.md#class-error) &nbsp;&nbsp; [H](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/H.md#class-h) &nbsp;&nbsp; [HookInfo](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/HookInfo.md#class-hookinfo) &nbsp;&nbsp; [TargetInfo](https://github.com/pyrustic/hooking/blob/master/docs/modules/content/hooking/content/classes/TargetInfo.md#class-targetinfo)
>
> **Functions:** &nbsp; [on\_enter](#on_enter) &nbsp;&nbsp; [on\_leave](#on_leave) &nbsp;&nbsp; [override](#override) &nbsp;&nbsp; [wrap](#wrap)
>
> **Constants:** &nbsp; ENTER &nbsp;&nbsp; LEAVE

# All Functions
[on\_enter](#on_enter) &nbsp;&nbsp; [on\_leave](#on_leave) &nbsp;&nbsp; [override](#override) &nbsp;&nbsp; [wrap](#wrap)

## on\_enter
Bind an upstream hook to a target




**Signature:** (hook, \*\*config)

|Parameter|Description|
|---|---|
|hook|upstream hook|
|\*\*config|configuration keyword arguments|





**Return Value:** None

[Back to Top](#module-overview)


## on\_leave
Bind a downstream hook to a target




**Signature:** (hook, \*\*config)

|Parameter|Description|
|---|---|
|hook|downstream hook|
|\*\*config|configuration keyword arguments|





**Return Value:** None

[Back to Top](#module-overview)


## override
Override target with a hook




**Signature:** (hook, \*\*config)

|Parameter|Description|
|---|---|
|hook|hook to override target|
|\*\*config|configuration keyword arguments|





**Return Value:** None

[Back to Top](#module-overview)


## wrap
Wrap a target with an upstream hook and a downstream hook




**Signature:** (hook1, hook2, \*\*config)

|Parameter|Description|
|---|---|
|hook1|upstream hook|
|hook2|downstream hook|
|\*\*config|configuration keyword arguments|





**Return Value:** None

[Back to Top](#module-overview)


