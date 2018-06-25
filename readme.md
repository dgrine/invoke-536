# Sample repository

## Context

See [pyinvoke - issue 536](https://github.com/pyinvoke/invoke/issues/536)

## Message

Thanks for the extensive reply!

My understanding is that task deduplication prevents the _same_ task from running more than once during a session. 
As you said, it all boils down to the definition of task equality.

I would argue that tasks located in different files should never be considered equal, regardless of their name. In the
original example, not only are the names the same, they even share the same body. However, they refer to different data,
making them - imo - _different_ tasks: the results of the two tasks cannot be assumed to be equal.

As for our use case, you guessed correctly: we indeed have multiple subpackages located in some folder where each
subpackage is assumed to implement a set of tasks (this forms the __interface__, in a sense). These subpackages are not
known beforehand: they are put there by some external mechanism. The top-level `tasks.py` file is in charge of:

* collecting the subpackage tasks in their own namespace, and
* creating new tasks (same interface) where each task has its `pre=` given all the relevant tasks discovered

Put simply: it provides an abstraction that forwards to the actual subpackage implementations.

As for the current task equality check, I thought it was based only on the `__name__` attribute. However, I've
played a bit more with it and was surprised that it is _not_ just the name that is taken into account. Consider a slight
variation on the original example:

```
├── __init__.py
├── one
│   ├── __init__.py
│   └── tasks.py
├── tasks.py
└── two
    ├── __init__.py
    └── tasks.py
```

If `one/tasks.py` and `two/tasks.py` have the same content:

```
from invoke import task
@task
def clean(context):
    print("clean sub")
```

Running the top-level `clean` task with `nowrap` (see original example) results in:

```
$ inv clean
clean sub
clean
```

Running it with `wrap` results in:

```
$ inv clean
clean sub
clean sub
clean
```

This is in accordance with the `__name__` attribute being used to differentiate task equality. So far, so good.

However, when changing the body of `two/tasks.py` to:

```
from invoke import task
@task
def clean(context):
    print("something else")
    print("clean sub")
```

Surprisingly, this results in:

```
clean sub
something else
clean sub
clean
```

In other words: the tasks are considered to be different, even though they have the same `__name__` attribute!

I've created a small example repository that reproduces this: https://github.com/dgrine/invoke-536

Finally, regarding work-arounds: this is not a blocking issue, I can cope with using the `wrap`/`nowrap` decorators.
Everything else is working smoothly :-)
