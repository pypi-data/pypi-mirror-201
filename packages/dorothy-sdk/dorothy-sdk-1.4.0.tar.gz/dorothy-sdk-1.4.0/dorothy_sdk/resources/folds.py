from dataclasses import dataclass, field
from io import BytesIO
from os.path import exists
from os import mknod
from typing import Dict, Any, Optional, Iterable, List

from PIL import Image as PILImage
from requests import Session

from dorothy_sdk.utils import url_join


@dataclass()
class Fold:
    name: str = field()
    train: Dict[str, Any] = field(default_factory=list)
    test: Optional[Dict[str, Any]] = field(default_factory=list)
    validation: Optional[Dict[str, Any]] = field(default_factory=list)


class ImageFoldInstance:

    def __init__(self, session,
                 dataset_name: str,
                 image_url: str,
                 project_id: str,
                 image_path: str,
                 has_tb: int):
        self._session = session
        self.dataset_name = dataset_name
        self._image_url = image_url
        self.project_id = project_id
        self._image_path = image_path
        self.has_tb = has_tb

    @property
    def pillow(self) -> PILImage:
        buffer = BytesIO()
        if exists(self._image_path):
            with open(self._image_path, mode='rb') as file:
                buffer.write(file.read())
            buffer.seek(0)
            return PILImage.open(buffer)
        else:
            mknod(self._image_path, mode=755)
            request = self._session.get(self._image_url)
            request.raise_for_status()
            buffer.write(request.content)
            buffer.seek(0)
            with open(self._image_path, mode='wb') as file:
                file.write(request.content)
            return PILImage.open(buffer)


class CrossValidationFold:
    resource = "dataset/{name}/folds/"
    dataset: str = None
    cluster_id: str = None
    file_url: str = None

    def __init__(self, session: Session, host: str, **kwargs):
        self._session: Session = session
        self._service_host = host
        if kwargs.get("datasets"):
            self.datasets = kwargs.get("datasets")
            if isinstance(self.datasets, str):
                self.datasets = [self.datasets]
            if not isinstance(self.datasets, list):
                raise ValueError("'datasets' must bu a list-like object")

    def _fetch_api_data(self, dataset) -> List[Dict[str, Any]]:
        results = []
        url = url_join(self._service_host, self.resource.format_map({"name": dataset}))
        request = self._session.get(url)
        request.raise_for_status()
        if request.status_code == 200:
            response = request.json()
            while response.get("next", None) is not None:
                for data in response.get("results"):
                    results.append(data)
                request = self._session.get(response.get("next"))
                response = request.json()
            if response.get("next", None) is None and len(response.get("results", [])) > 0:
                for data in response.get("results"):
                    results.append(data)
        return results

    def _generate_fold_aggregation(self):
        agg = {f"fold_{x}_{y}": Fold(name=f"fold_{x}_{y}") for x in range(10) for y in range(9)}
        for dataset in self.datasets:
            results = self._fetch_api_data(dataset)
            for element in results:
                image_instance = ImageFoldInstance(self._session,
                                                   dataset_name=dataset,
                                                   image_url=element.get("image_url"),
                                                   project_id=element.get("image_project_id"),
                                                   image_path=element.get("image_path"),
                                                   has_tb=element.get("has_tb")
                                                   )
                fold = agg[element.get("fold_name")]
                role = element.get("role")
                if role.upper() == "TRAIN":
                    fold.train.append(image_instance)
                elif role.upper() == "TEST":
                    fold.test.append(image_instance)
                else:
                    fold.validation.append(image_instance)
        return agg

    def get_folds(self, fold_name: str = None) -> Iterable[Fold]:
        fold_images: Dict[str, Any] = self._generate_fold_aggregation()
        if fold_name:
            yield fold_images[fold_name]
        else:
            for _, value in sorted(fold_images.items()):
                yield value
