
from random import randrange


def quicksortcib(ciblist):
    """Implement quicksort (ie "partition-exchange" sort).
        that makes on average, O(n log n) comparisons to sort n items.
        This solution benefits from "list comprehensions", which keeps
        the syntax concise and easy to read.
        Quicksort dedicated to a list of Targets.
    """
    # an empty list is already sorted, so just return it
    if len(ciblist) == 0:
        return ciblist

    # Select a random pivot value and remove it from the list
    pivot = ciblist.pop(randrange(len(ciblist)))
    # Filter all items less than the pivot and quicksort them
    lesser = quicksortcib([l for l in ciblist if l.get_x() < pivot.get_x()])
    # Filter all items greater than the pivot and quicksort them
    greater = quicksortcib([l for l in ciblist if l.get_x() >= pivot.get_x()])
    # Return the sorted results
    return lesser + [pivot] + greater
