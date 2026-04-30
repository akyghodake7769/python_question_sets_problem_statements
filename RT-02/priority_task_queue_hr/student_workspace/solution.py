# from typing import List, Dict, Set, Optional, Any
# import sys

# # Complete the 'PriorityTaskQueue' class below.
# #
# # The class is expected to manage task priorities and dependencies.

# class PriorityTaskQueue:
#     def __init__(self):
#         # Initialize internal structures
#         pass

#     def add_task(self, name: str, priority: int, deps: List[str] = None):
#         # Implementation here
#         pass

#     def get_next_task(self) -> Optional[str]:
#         # Return the next available task
#         return None

# def process_tasks():
#     try:
#         input_data = sys.stdin.read().splitlines()
#         if not input_data:
#             return
            
#         n = int(input_data[0].strip())
#         queue = PriorityTaskQueue()
        
#         for i in range(1, n + 1):
#             line = input_data[i].strip()
#             if not line: continue
            
#             # Commands: "ADD <name> <priority> [<dep1>,<dep2>]" or "GET"
#             if line.startswith("ADD"):
#                 parts = line.split()
#                 name = parts[1]
#                 priority = int(parts[2])
#                 deps = parts[3].strip('[]').split(',') if len(parts) > 3 and parts[3] != '[]' else []
#                 queue.add_task(name, priority, deps)
#             elif line == "GET":
#                 next_task = queue.get_next_task()
#                 print(next_task if next_task else "None")
                
#     except Exception:
#         pass

# if __name__ == '__main__':
#     process_tasks()
from typing import List, Dict, Optional, Tuple, Callable
from functools import wraps
import json
import sys

# Reference Solution for RT-02: Priority Task Queue
# Maintains a set of tasks with priorities and dependencies.

def validate_task_data(func: Callable) -> Callable:
    """Decorator to validate task and priority data"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Validation logic can be added here
        return func(*args, **kwargs)
    return wrapper

class TaskQueue:
    """Core logic for managing prioritized tasks with dependencies"""
    def __init__(self):
        self.tasks: Dict[str, Dict] = {} # task_id -> {"priority": int, "deps": set}
        self.completed: set = set()
        self.insertion_order: List[str] = []

    @validate_task_data
    def add_task(self, task_id: str, priority: int, dependencies: List[str]) -> None:
        """Adds a new task to the queue"""
        self.tasks[task_id] = {"priority": priority, "deps": set(dependencies)}
        if task_id not in self.insertion_order:
            self.insertion_order.append(task_id)

    def is_ready(self, task_id: str) -> bool:
        """Returns True if all dependencies of the task are completed"""
        if task_id not in self.tasks or task_id in self.completed:
            return False
        return self.tasks[task_id]["deps"].issubset(self.completed)

    def complete_task(self, task_id: str) -> None:
        """Marks a task as completed"""
        if task_id in self.tasks:
            self.completed.add(task_id)

    def get_status(self, task_id: str) -> str:
        """Returns the current status of the task"""
        if task_id in self.completed:
            return "completed"
        if self.is_ready(task_id):
            return "ready"
        return "pending" if task_id in self.tasks else "unknown"

    def get_ready_tasks(self) -> List[str]:
        """Returns a list of tasks that are ready to be processed, 
        sorted by priority (desc) and then by insertion order.
        """
        ready = [tid for tid in self.insertion_order if tid not in self.completed and self.is_ready(tid)]
        # Sort by priority (desc) then by insertion order index
        ready.sort(key=lambda tid: (-self.tasks[tid]["priority"], self.insertion_order.index(tid)))
        return ready

    def get_next(self) -> Optional[str]:
        """Returns the next task to process"""
        ready = self.get_ready_tasks()
        return ready[0] if ready else None

def main():
    """HackerRank-style driver for processing operations"""
    try:
        input_data = sys.stdin.read().splitlines()
        if not input_data:
            return
        
        n_ops = int(input_data[0].strip())
        tq = TaskQueue()

        for i in range(1, n_ops + 1):
            line = input_data[i].strip().split(' ', 1)
            if not line: continue
            cmd = line[0]
            args_str = line[1] if len(line) > 1 else ""

            if cmd == "add_task":
                # Expecting: task_id priority [json_deps]
                parts = args_str.split(' ', 2)
                task_id = parts[0]
                priority = int(parts[1])
                deps = json.loads(parts[2])
                tq.add_task(task_id, priority, deps)
            elif cmd == "is_ready":
                print(str(tq.is_ready(args_str.strip())).lower())
            elif cmd == "complete_task":
                tq.complete_task(args_str.strip())
            elif cmd == "get_next":
                res = tq.get_next()
                print(res if res else "None")
            elif cmd == "get_status":
                print(tq.get_status(args_str.strip()))
            elif cmd == "get_ready_tasks":
                print(",".join(tq.get_ready_tasks()))
                
    except (EOFError, ValueError, IndexError):
        pass

if __name__ == '__main__':
    main()
