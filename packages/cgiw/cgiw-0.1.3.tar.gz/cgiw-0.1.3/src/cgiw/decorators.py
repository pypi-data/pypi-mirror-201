from typing import Any, Callable, Optional

from .types import PostHandlerType, BodyWrapperType, QueryType, HeadersType, ReturnType, HeadersWrapperType, HandlerType


def wrap_body(process_body: BodyWrapperType) -> Callable[[PostHandlerType], PostHandlerType]:
    def wrap(post_handler: PostHandlerType) -> PostHandlerType:
        def wrapper(query: QueryType, headers: HeadersType, body: Any) -> ReturnType:
            return post_handler(query, headers, process_body(body))
        return wrapper
    return wrap

def wrap_headers(process_headers: HeadersWrapperType) -> Callable[[HandlerType], HandlerType]:
    def wrap(handler: HandlerType) -> HandlerType:
        def wrapper(query: QueryType, headers: HeadersType, *args, **kwargs) -> ReturnType:
            return handler(query, process_headers(headers), *args, **kwargs)
        return wrapper
    return wrap