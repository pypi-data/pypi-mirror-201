from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from openapify.core.models import (
    Body,
    Cookie,
    Header,
    QueryParam,
    SecurityRequirement,
)
from openapify.core.openapi.models import Example, HttpCode, Parameter

__openapify__ = "__openapify__"


Handler = TypeVar("Handler")


@overload
def request_schema(
    body: Optional[Body] = None,
    *,
    query_params: Optional[Dict[str, Union[Type, QueryParam]]] = None,
    headers: Optional[Dict[str, Union[str, Header]]] = None,
    cookies: Optional[Dict[str, Union[str, Cookie]]] = None,
) -> Callable[[Handler], Handler]:
    ...


@overload
def request_schema(
    body: Optional[Type] = None,
    *,
    media_type: str = "application/json",
    body_required: bool = False,
    body_description: Optional[str] = None,
    body_example: Optional[Any] = None,
    body_examples: Optional[Dict[str, Union[Example, Any]]] = None,
    query_params: Optional[Dict[str, Union[Type, QueryParam]]] = None,
    headers: Optional[Dict[str, Union[str, Header]]] = None,
    cookies: Optional[Dict[str, Union[str, Cookie]]] = None,
) -> Callable[[Handler], Handler]:
    ...


def request_schema(
    body: Optional[Type] = None,
    *,
    media_type: str = "application/json",
    body_required: bool = False,
    body_description: Optional[str] = None,
    body_example: Optional[Any] = None,
    body_examples: Optional[Dict[str, Union[Example, Any]]] = None,
    query_params: Optional[Dict[str, Union[Type, QueryParam]]] = None,
    headers: Optional[Dict[str, Union[str, Header]]] = None,
    cookies: Optional[Dict[str, Union[str, Cookie]]] = None,
) -> Callable[[Handler], Handler]:
    def decorator(handler: Handler) -> Handler:
        meta = getattr(handler, __openapify__, [])
        if not meta:
            handler.__openapify__ = meta
        meta.append(
            (
                "request",
                {
                    "body": body,
                    "media_type": media_type,
                    "body_required": body_required,
                    "body_description": body_description,
                    "body_example": body_example,
                    "body_examples": body_examples,
                    "query_params": query_params,
                    "headers": headers,
                    "cookies": cookies,
                },
            ),
        )
        return handler

    return decorator


def response_schema(
    schema: Type,
    http_code: HttpCode = 200,
    media_type: str = "application/json",
    description: Optional[str] = None,
    headers: Optional[Dict[str, Union[str, Header]]] = None,
    deprecated: Optional[bool] = None,
    example: Optional[Any] = None,
    examples: Optional[Dict[str, Union[Example, Any]]] = None,
):
    def decorator(handler):
        meta = getattr(handler, __openapify__, [])
        if not meta:
            handler.__openapify__ = meta
        meta.append(
            (
                "response",
                {
                    "schema": schema,
                    "http_code": http_code,
                    "media_type": media_type,
                    "description": description,
                    "headers": headers,
                    "deprecated": deprecated,
                    "example": example,
                    "examples": examples,
                },
            ),
        )
        return handler

    return decorator


def path_docs(
    summary: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[Sequence[str]] = None,
    parameters: Optional[Dict[str, Union[str, Parameter]]] = None,
    external_docs: Optional[Union[str, Tuple[str, str]]] = None,
):
    def decorator(handler):
        meta = getattr(handler, __openapify__, [])
        if not meta:
            handler.__openapify__ = meta
        meta.append(
            (
                "path_docs",
                {
                    "summary": summary,
                    "description": description,
                    "tags": tags,
                    "parameters": parameters,
                    "external_docs": external_docs,
                },
            ),
        )
        return handler

    return decorator


def security_requirements(
    requirements: Optional[
        Union[SecurityRequirement, List[SecurityRequirement]]
    ] = None,
):
    def decorator(handler):
        meta = getattr(handler, __openapify__, [])
        if not meta:
            handler.__openapify__ = meta
        meta.append(("security_requirements", {"requirements": requirements}))
        return handler

    return decorator
