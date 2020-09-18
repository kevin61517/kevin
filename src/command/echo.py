from utils.decorator import call
import re


@call
class Echo:
    def __call__(self):
        return "ha"

    def re(self) -> re: ...
