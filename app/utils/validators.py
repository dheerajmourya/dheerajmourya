from app.models import Task

def is_circular_dependency(task_id, dep_id):
    """
    Checks if adding dep_id as a dependency of task_id creates a circular loop.
    """
    visited = set()

    def dfs(current_id):
        if current_id == task_id:
            return True  # Loop found
        if current_id in visited:
            return False
        visited.add(current_id)

        task = Task.query.get(current_id)
        if not task:
            return False

        for dep in task.dependencies:
            if dfs(dep.id):
                return True
        return False

    return dfs(dep_id)