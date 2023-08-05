import json
from pathlib import Path
from typing import List, Optional, Union

from datagen.api.assets import (
    Background,
    Camera,
    GenerationRequest,
    DataRequest,
    SequenceRequest,
    Glasses,
    Human,
    HumanDatapoint,
    Light,
    Mask,
)
from datagen.api.client.schemas import DataResponse, DataResponseStatus, DownloadRequest, DownloadURL
from datagen.api.requests.datapoint.builder import HumanDatapointBuilder
from datagen.api.requests.director import DataRequestDirector
from datagen.config import settings
from datagen.core.tasks import TaskContainer
from datagen.core.tasks.task_runner import TaskRunner
from datagen.dev.logging import get_logger

logger = get_logger(__name__)

DEFAULT_DATAPOINT_REQUESTS_JSON_NAME = "datagen_data_request.json"


class DatagenAPI:
    def __init__(self):
        self._request_director = DataRequestDirector()
        self._task_container = TaskContainer()

    def create_datapoint(
        self,
        human: Human,
        camera: Camera,
        glasses: Optional[Glasses] = None,
        mask: Optional[Mask] = None,
        background: Optional[Background] = None,
        lights: Optional[List[Light]] = None,
    ) -> HumanDatapoint:
        self._request_director.builder = HumanDatapointBuilder(human, camera, glasses, mask, background, lights)
        return self._request_director.build_datapoint()

    def load(self, path: Union[Path, str]) -> GenerationRequest:
        if isinstance(path, str):
            path = self._get_request_json_path(path)
        request_dict = json.loads(path.read_text())
        return DataRequest(**request_dict) if "datapoints" in request_dict else SequenceRequest(**request_dict)

    def generate(
        self,
        request: GenerationRequest,
        generation_name: str,
    ) -> DataResponse:
        batches = DatagenAPI.batch_request(request)
        return TaskRunner().run(
            task=self._task_container.pipeline_factory.data_generation(number_of_batches=len(batches)),
            data=(batches, generation_name),
        )

    def stop(self, generation_id) -> None:
        TaskRunner().run(
            task=self._task_container.client_task(task_name="stop_generation"),
            data=generation_id,
        )

    def get_status(self, generation_id: str) -> DataResponseStatus:
        return TaskRunner().run(
            task=self._task_container.client_task(task_name="status"),
            data=generation_id,
        )

    def get_download_urls(self, generation_id: str) -> List[DownloadURL]:
        return TaskRunner().run(
            task=self._task_container.client_task(task_name="get_download_links"),
            data=generation_id,
        )

    def download(
        self, urls: List[DownloadURL], dest_folder: str, dataset_name: str, remove_tar_files: bool = True
    ) -> None:
        TaskRunner().run(
            task=self._task_container.pipeline_factory.download(
                number_of_files=len(urls), remove_tar_files=remove_tar_files
            ),
            data=DownloadRequest(urls=urls, path=dest_folder, dataset_name=dataset_name).batch(),
        )

    def dump(self, request: GenerationRequest, path: Union[Path, str] = None) -> None:
        if not isinstance(path, Path):
            path = self._get_request_json_path(path)
        path.write_text(json.dumps(request.dict(), indent=3, sort_keys=True))
        if isinstance(request, DataRequest):
            logger.info(
                f"Request was successfully dumped to path '{path.absolute()}' ({len(request)} datapoints total).",
            )
        else:
            logger.info(
                f"Request was successfully dumped to path '{path.absolute()}'.",
            )

    def _get_request_json_path(self, path: Optional[str]) -> Path:
        path_ = Path(path) if path else Path.cwd().joinpath(DEFAULT_DATAPOINT_REQUESTS_JSON_NAME)
        if not path_.parent.exists():
            raise FileNotFoundError(f"{path_.parent} folder does not exist, cannot dump requests")
        path_.touch()
        return path_

    @staticmethod
    def batch_request(request: GenerationRequest) -> List[GenerationRequest]:
        batches = []
        if isinstance(request, DataRequest):
            batch_size = settings["batch_size"]
            datapoints_num = len(request.datapoints)
            for dp_idx in range(0, datapoints_num, batch_size):
                batches.append(DataRequest(datapoints=request.datapoints[dp_idx : dp_idx + batch_size]))
        elif isinstance(request, SequenceRequest):
            batches = [request]
        return batches
