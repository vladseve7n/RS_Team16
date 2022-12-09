import json
import random
from abc import ABC, abstractmethod
from typing import List


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


class UserKnnBM25Offline(RecModel):

    def __init__(self) -> None:
        super().__init__()
        with open('saved_models/bm25_itemknn_offline.json', 'r') as handle:
            self.json_with_recos = json.load(handle)

    def prepare(self) -> None:
        pass

    def get_reco_for_user(self, user_id: int, k_recs: int) -> List[int]:
        if str(user_id) not in self.json_with_recos:
            return []
        return self.json_with_recos[str(user_id)]


class PopRecoModelOffline(RecModel):
    def __init__(self) -> None:
        super().__init__()
        with open('saved_models/pop_sum_weight_offline.json', 'r') as handle:
            self.json_with_recos = json.load(handle)

    def prepare(self) -> None:
        pass

    def get_reco_for_user(self, user_id: int, k_recs: int) -> List[int]:
        if str(user_id) not in self.json_with_recos:
            return [10440, 15297, 4151, 6192, 14,
                    13865, 9728, 9996, 16228, 496]
        return self.json_with_recos[str(user_id)][:k_recs]


all_models = {
    'random_model': RandomModel(),
    'user_knn_bm25_offline': UserKnnBM25Offline(),
    'pop_reco_model_offline': PopRecoModelOffline()
}
