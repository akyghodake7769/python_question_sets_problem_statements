class TaskRegistry:
    """Manage tasks with pending and completed status tracking."""

    def __init__(self):
        """Initialize an empty task list."""
        self.tasks = []

    def add_task(self, description: str) -> None:
        """
        Add a new task to the registry with [P] (Pending) status.
        
        Parameters:
            description (str): Task description
        
        Returns:
            None
        
        Behavior:
            - Prepend "[P] " to task description
            - Add to internal task list
            - Store full task string (e.g., "[P] Buy Milk")
        """
        task = f"[P] {description}"
        self.tasks.append(task)

    def complete_task(self, description: str) -> bool:
        """
        Mark a task as completed by changing [P] to [D].
        
        Parameters:
            description (str): Task description (without status prefix)
        
        Returns:
            bool: True if task was found and completed, False otherwise
        
        Behavior:
            - Search for "[P] description" in task list
            - If found, replace "[P]" with "[D]"
            - Return True if successful, False if task not found
            - Preserve exact description text
        """
        for i, task in enumerate(self.tasks):
            if task == f"[P] {description}":
                self.tasks[i] = f"[D] {description}"
                return True
        return False

    def get_count(self, status_code: str) -> int:
        """
        Get count of tasks with specified status.
        
        Parameters:
            status_code (str): "P" for Pending or "D" for Done
        
        Returns:
            int: Count of tasks with the specified status
        
        Behavior:
            - Count tasks starting with "[P]" if status_code is "P"
            - Count tasks starting with "[D]" if status_code is "D"
            - Return integer count
        """
        prefix = f"[{status_code}]"
        return sum(1 for task in self.tasks if task.startswith(prefix))

    def delete_task(self, description: str) -> None:
        """
        Delete a task from the registry.
        
        Parameters:
            description (str): Task description (without status prefix)
        
        Returns:
            None
        
        Behavior:
            - Search for task with "[P] description" or "[D] description"
            - Remove task if found
            - Do nothing if task not found (graceful failure)
            - No error should be raised
        """
        for i, task in enumerate(self.tasks):
            if task.endswith(description):
                self.tasks.pop(i)
                return

    def get_all(self) -> list:
        """
        Get all tasks in the registry.
        
        Returns:
            list: List of all tasks with status prefixes
        
        Behavior:
            - Return copy of internal task list
            - Preserve status prefixes ([P] or [D])
            - Maintain order of tasks
            - Return empty list if no tasks
        """
        return self.tasks.copy()
