from invoke import task, Collection
if __package__ is None or __package__ == '':
    from one import tasks as one
    from two import tasks as two
else:
    from .one import tasks as one
    from .two import tasks as two

def full_name(obj):
  return obj.__module__ + "." + obj.__class__.__name__

# Works as expected
def wrap(task_list):
    for task in task_list: task.__name__ = full_name(task)
    return task_list

# Does not work: only one of the two subtasks is executed
def nowrap(task_list):
    return task_list

ns = Collection()

@task(pre = wrap([one.clean, two.clean]))
def clean(context):
    print("clean")
