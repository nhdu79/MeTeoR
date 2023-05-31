from meteor_reasoner.classes.interval import *
from meteor_reasoner.classes.atom import *
import copy

def coalescing(old_intervals, predicate=None, entity=None, graph=None):
    if len(old_intervals) == 0:
        return old_intervals
    new_intervals = []
    old_intervals = sorted(old_intervals, key=lambda t: (t.left_value, t.left_open))
    i = 1
    mover = old_intervals[0]
    if graph is not None:
        merged_interval = []
    while i <= len(old_intervals)-1:
        tmp_interval = Interval.union(mover, old_intervals[i])
        if tmp_interval is None:
            # no intersection
            if graph is not None and len(merged_interval) > 0:
                atom = Atom(predicate, entity=entity, interval=mover)
                interval_strs = map(lambda x: Atom(predicate, entity=entity, interval=x).__str__(), merged_interval)
                el = {
                    "succ": atom.__str__(),
                    "rule" : "coalescing",
                    "pred": [*interval_strs]
                }
                merged_interval = []
                if el not in graph and len(el["pred"]) > 1:
                    graph.append(el)

            new_intervals.append(mover)
            mover = old_intervals[i]
        else:
            if graph is not None and old_intervals[i] not in merged_interval:
                merged_interval.append(old_intervals[i])

            mover = tmp_interval
        i += 1
    new_intervals.append(mover)
    return new_intervals


def coalescing_d(D, graph=None):
    """
    Merge two overlapped intervals into one interval.
    Args:
        D (a dictionary object): store facts.
    Returns:
    """
    for predicate in D:
        for entity, old_intervals in D[predicate].items():
                old_intervals = D[predicate][entity]
                if len(old_intervals) == 0:
                    continue
                if graph is not None:
                    new_intervals = coalescing(old_intervals, predicate=predicate, entity=entity, graph=graph)
                else:
                    new_intervals = coalescing(old_intervals)
                D[predicate][entity] = new_intervals
