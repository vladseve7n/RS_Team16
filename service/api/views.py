from typing import List

from fastapi import APIRouter, Depends, FastAPI, Path, Request
from pydantic import BaseModel

from service.api.exceptions import ModelNotFoundError, UserNotFoundError
from service.api.rec_models import all_models
from service.api.token import has_access
from service.log import app_logger
from service.models import Error

PROTECTED = [Depends(has_access)]


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


class Error401Response(BaseModel):
    error: str = 'Unauthorized. No permission'
    errors: List[Error]


class Error404Response(BaseModel):
    error: str = 'Not Found. Nothing matches the given URI'
    errors: List[Error]


router = APIRouter()
router_no_auth = APIRouter()


@router_no_auth.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
    responses={404: {'model': Error404Response},
               401: {'model': Error401Response}}
)
async def get_reco(
    request: Request,
    model_name: str = Path(..., description='The name of testing model'),
    user_id: int = Path(..., description='The specific id of user'),
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    if user_id > 10 ** 9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    k_recs = request.app.state.k_recs

    try:
        model = all_models[model_name]
    except KeyError:
        raise ModelNotFoundError(
            error_message=f'There is no model with name {model_name}')

    model.prepare()
    reco = model.get_reco_for_user(user_id=user_id, k_recs=k_recs)

    if len(reco) < k_recs:
        pop_model = all_models['pop_reco_model_offline']
        pop_recos = pop_model.get_reco_for_user(user_id=user_id)
        reco.extend(pop_recos)
        reco = list(dict.fromkeys(reco))
        reco = reco[:k_recs]

    return RecoResponse(user_id=user_id, items=reco)


def add_views(app: FastAPI) -> None:
    app.include_router(router_no_auth)
    app.include_router(router, dependencies=PROTECTED)
