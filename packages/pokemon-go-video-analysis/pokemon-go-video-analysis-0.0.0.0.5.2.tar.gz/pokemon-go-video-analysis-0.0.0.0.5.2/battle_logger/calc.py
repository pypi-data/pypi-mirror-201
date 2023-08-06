from typing import List

from ocr_ops.run_finding.interval import Interval


def find_runs_with_tol(vals: List[int], tol: int) -> List[Interval]:
    """
    Find runs in vals list of integers with tolerance of tol.

    param vals: List of integers.
    param tol: Maximum difference of consecutive integers in a run.

    return:
        List of runs.
    """
    runs = []
    run_start = None
    for i, val in enumerate(vals):
        if run_start is None:
            run_start = vals[i]
        elif val - vals[i - 1] > tol:
            runs.append(Interval(start=run_start, end=vals[i - 1]))
            run_start = vals[i]
    if run_start is not None:
        runs.append(Interval(start=run_start, end=vals[-1]))
    return runs
