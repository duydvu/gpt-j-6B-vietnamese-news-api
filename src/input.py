'''Input data validation module'''
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class BaseInput(BaseModel):  # pylint: disable=too-few-public-methods
    '''Type of input data.

    Attributes:
        text: a string marks the start of the generated text
        top_k: filter k most likely next words
        top_p: chooses from the smallest possible set of words whose cumulative probability exceeds the probability p
        n_samples: number of samples to return'''
    text: str
    top_k: int = 50
    top_p: float = 0.9
    n_samples: int = 10
