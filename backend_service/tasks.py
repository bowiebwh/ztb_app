from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any
import uuid

executor = ThreadPoolExecutor(max_workers=4)
task_futures = {}


def submit_task(fn: Callable, *args, **kwargs) -> str:
    task_id = str(uuid.uuid4())
    future = executor.submit(fn, *args, **kwargs)
    task_futures[task_id] = future
    return task_id


def get_task_status(task_id: str):
    future = task_futures.get(task_id)
    if not future:
        return {"state": "not_found"}
    if future.running():
        return {"state": "running"}
    if future.done():
        if future.exception():
            return {"state": "failed", "error": str(future.exception())}
        return {"state": "completed", "result": future.result()}
    return {"state": "pending"}
