from typing import Callable, List, Optional

class Result:
    def get(self) -> bytes: ...

class Function:
    def __call__(self, params: Optional[bytes] = None) -> Optional[Result]: ...

def get_function(name: str, *, namespace: Optional[str] = None) -> Function: ...
def parallel(
    function: Function,
    *,
    params: Optional[List[bytes]] = None,
    count: Optional[int] = None,
) -> List[Optional[Result]]: ...
def register(
    outer_function: Optional[Callable] = ...,
    *,
    name: Optional[str] = ...,
    namespace: Optional[str] = ...,
) -> Callable: ...
