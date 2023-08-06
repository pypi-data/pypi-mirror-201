from typing import List, Optional

from codenames.game.state import GameState
from pydantic import BaseModel, root_validator

from .base import ModelIdentifier, Solver


class LoadModelsRequest(BaseModel):
    model_identifiers: List[ModelIdentifier] = []
    load_default_models: bool = True


class BaseGenerateRequest(BaseModel):
    solver: Solver = Solver.NAIVE
    model_identifier: Optional[ModelIdentifier]
    game_state: GameState


class GenerateHintRequest(BaseGenerateRequest):
    pass


class GenerateGuessRequest(BaseGenerateRequest):
    pass


class StemRequest(BaseModel):
    word: str
    model_identifier: ModelIdentifier


class MostSimilarRequest(BaseModel):
    word: Optional[str]
    vector: Optional[List[float]]
    model_identifier: ModelIdentifier
    top_n: int = 10

    @root_validator
    def check_word_xor_vector(cls, values):  # pylint: disable=no-self-argument
        word = values.get("word")
        vector = values.get("vector")
        if word and vector:
            raise ValueError("Exactly one of word or vector must be provided (both were provided).")
        if not word and not vector:
            raise ValueError("Exactly one of word or vector must be provided (neither were provided).")
        return values
