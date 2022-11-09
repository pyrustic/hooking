Back to [All Modules](https://github.com/pyrustic/hooking/blob/master/docs/modules/README.md#readme)

# Module Overview

**hooking.tight**
 
Tight coupling paradigm

> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [on\_enter](#on_enter) &nbsp;&nbsp; [on\_leave](#on_leave) &nbsp;&nbsp; [wrap](#wrap)
>
> **Constants:** &nbsp; None

# All Functions
[on\_enter](#on_enter) &nbsp;&nbsp; [on\_leave](#on_leave) &nbsp;&nbsp; [wrap](#wrap)

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


