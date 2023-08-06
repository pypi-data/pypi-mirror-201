import asyncio
import builtins
from typing import Any

from datagen.core.tasks.task import Task


class TaskRunner:
    @classmethod
    def run(cls, task: Task, data: Any) -> Any:
        task.setup()

        if hasattr(builtins, "__IPYTHON__"):
            # In case of running in a IPYTHON environment
            import nest_asyncio

            nest_asyncio.apply()

        response = asyncio.run(cls._internal_run(task=task, data=data))
        return response

    @classmethod
    async def _internal_run(cls, task: Task, data: Any) -> Any:
        await task.input_channel.put(data)
        await task.execute()
        return await task.output_channel.take()
