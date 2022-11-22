import random
from abc import ABC, abstractmethod
from typing import Dict, List, Type


class RecModel(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def prepare(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def get_reco_for_user(self, user_id: int,
                          k_recs: int,
                          **kwargs) -> List[int]:
        return list(range(k_recs))


class RandomModel(RecModel):
    def prepare(self, *args, **kwargs) -> None:
        pass

    def get_reco_for_user(self, user_id: int,
                          k_recs: int,
                          **kwargs) -> List[int]:
        random.seed(user_id)
        return random.sample(range(0, 256), k_recs)


all_models: Dict[str, Type[RecModel]] = {
    'random_model': RandomModel
}
