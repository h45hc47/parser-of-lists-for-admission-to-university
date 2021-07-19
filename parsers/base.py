import abc


class BaseParser(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def __call__(cls, print_results: bool = True) -> None:
        pass
