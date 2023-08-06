from typing import List

from codenames.game.move import Guess, Hint
from pydantic import BaseModel

from .base import ModelIdentifier, Solver


class BaseResponse(BaseModel):
    pass


class LoadModelsResponse(BaseResponse):
    success_count: int
    fail_count: int


class GenerateHintResponse(BaseResponse):
    suggested_hint: Hint
    used_solver: Solver
    used_model_identifier: ModelIdentifier


class GenerateGuessResponse(BaseResponse):
    suggested_guess: Guess
    used_solver: Solver
    used_model_identifier: ModelIdentifier


class StemResponse(BaseResponse):
    root: str


class Similarity(BaseModel):
    word: str
    similarity: float


class MostSimilarResponse(BaseResponse):
    most_similar: List[Similarity]
