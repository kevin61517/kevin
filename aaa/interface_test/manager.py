from .interface import InterFace


class Manager:
    def __init__(self):
        self._register = {class_.__name__.lower(): class_() for class_ in InterFace.__subclasses__()}

    def get_teammate(self, name) -> InterFace:
        teammate = self._register.get(name.lower())
        if teammate:
            return teammate
        raise ValueError(f'組員 {name} 未實作')

    @property
    def teammates(self):
        for teammate in self._register:
            yield teammate


team_manager = Manager()
