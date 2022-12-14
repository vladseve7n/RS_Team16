import json
import random
from abc import ABC, abstractmethod
from typing import List

from service.settings import get_config

service_config = get_config()


class RecModel(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def prepare(self) -> None:
        pass

    @abstractmethod
    def get_reco_for_user(
            self,
            user_id: int,
            k_recs: int
    ) -> List[int]:
        return list(range(k_recs))


class RandomModel(RecModel):
    def prepare(self) -> None:
        pass

    def get_reco_for_user(
            self,
            user_id: int,
            k_recs: int
    ) -> List[int]:
        random.seed(user_id)
        return random.sample(range(0, 256), k_recs)


class ItemKNNBM25Offline(RecModel):
    path_to_weights: str = service_config.bm25_itemknn_offline_path

    def __init__(self) -> None:
        super().__init__()
        with open(self.path_to_weights, 'r') as handle:
            self.recos = json.load(handle)
            self.recos = {int(k): v for k, v in self.recos.items()}

    def prepare(self) -> None:
        pass

    def get_reco_for_user(self, user_id: int, k_recs: int) -> List[int]:
        return self.recos.get(user_id, [])


class PopRecoModelOffline(RecModel):
    path_to_weights: str = service_config.pop_sum_weight_offline_path
    path_to_default_answer: str = service_config.pop_default_answer_path

    def __init__(self) -> None:
        super().__init__()
        with open(self.path_to_weights, 'r') as handle:
            self.recos = json.load(handle)
            self.recos = {int(k): v for k, v in self.recos.items()}

        with open(self.path_to_default_answer, 'r') as handle:
            self.default_answer = json.load(handle)['default']

    def prepare(self) -> None:
        pass

    def get_reco_for_user(self, user_id: int, k_recs: int = None) -> List[int]:
        if k_recs:
            return self.recos.get(user_id, self.default_answer)[:k_recs]
        return self.recos.get(user_id, self.default_answer)


class AnnRecoMidelOffline(ItemKNNBM25Offline):
    path_to_weights: str = service_config.ann_recs_json


all_models = {
    'random_model': RandomModel(),
    'user_knn_bm25_offline': ItemKNNBM25Offline(),
    'pop_reco_model_offline': PopRecoModelOffline(),
    'ann_recs_offline': AnnRecoMidelOffline()
}
