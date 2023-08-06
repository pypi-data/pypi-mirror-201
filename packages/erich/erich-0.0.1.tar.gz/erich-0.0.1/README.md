# Erich
enrich local errors without repeated try except using decorators

## Example

main.py
```py 
from typing import Callable

import erich

# Print a formatted message where format field names must 
# be present in the function signature.
@erich.fmt("Tried starting task {name} ({desc})")
def start_task(name: str, prio: int, fn: Callable, desc: str = None):
    schedule(prio, fn)

# Print that this function has been called but only include the prio
# in the output
@erich.with_args("prio")
def schedule(prio: int, fn: Callable):
    can_schedule(prio)
    fn()

# add some nicer output to the final result
@erich.fmt("Cannot schedule task due to")
def can_schedule(prio: int):
    can_schedule_internal(prio)

# here the exception is actually raised with a limited
# amount of information which will be enriched by
# parent/calling functions.
def can_schedule_internal(prio: int):
    raise Exception(f"Cannot schedule something with prio {prio}. It's invalid")

start_task("test", -1, lambda: None, desc="very important")

```

```sh
> python main.py

..
stack trace
..

Tried starting task test (very important)
↳ during call of schedule(prio = -1)
 ↳ Cannot schedule task due to
  ↳ Cannot schedule something with prio -1. It's invalid
```


## Build
```sh
python -m build
```
