from pydantic import BaseSettings


class Config(BaseSettings):

    class Config:
        case_sensitive = False


class LogConfig(Config):
    level: str = "INFO"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        case_sensitive = False
        fields = {
            "level": {
                "env": ["log_level"]
            },
        }


class ServiceConfig(Config):
    service_name: str = "reco_service"
    k_recs: int = 10
    SECRET_KEY: str
    bm25_itemknn_offline_path: str = 'saved_models/bm25_itemknn_offline.json'
    pop_sum_weight_offline_path: str = 'saved_models/' \
                                       'pop_sum_weight_offline.json'
    pop_default_answer_path: str = 'saved_models/pop_default_answer.json'

    ann_recs_json: str = 'saved_models/ann_recs.json'

    log_config: LogConfig


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )
