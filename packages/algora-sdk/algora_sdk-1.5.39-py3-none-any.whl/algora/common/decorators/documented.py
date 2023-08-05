from typing import Callable, Union, Optional

from algora.common.errors import InvalidClassDefinition


def documented(
    _cls: object = None, *, docs: Optional[str] = None
) -> Union[Callable, object]:
    """
    This decorator adds the desired docs and adds validation that the class is documented.

    Args:
        _cls (object): The class being decorated
        docs (Optional[str]): Docs to be added to the class

    Returns:
        cls: The updated class with the __doc__ field populated
    """

    def wrap(cls):
        doc_str = cls.__doc__ or docs
        if doc_str is None or len(doc_str) == 0:
            raise InvalidClassDefinition(
                f"Class {cls} missing __doc__ field, either pass in docs to the decorator or "
                f"document the class"
            )
        cls.__doc__ = doc_str
        return cls

    if _cls is None:
        return wrap

    return wrap(_cls)
