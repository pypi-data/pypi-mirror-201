import apispec as _apispec
from typing import Sequence, Any, Optional, Union, List, Dict
from openapify.core.openapi.models import Server, SecurityScheme


class APISpec(_apispec.APISpec):
    def __init__(
        self,
        title: str,
        version: str,
        openapi_version: str,
        plugins: Sequence[_apispec.BasePlugin] = (),
        servers: Optional[List[Union[str, Server]]] = None,
        security_schemes: Optional[Dict[str, SecurityScheme]] = None,
        **options: Any,
    ) -> None:
        _servers = []
        for server in servers or ():
            if isinstance(server, str):
                _servers.append({"url": server})
            else:
                _servers.append(server.to_dict())
        super().__init__(
            title=title,
            version=version,
            openapi_version=openapi_version,
            plugins=plugins,
            servers=_servers or None,
            **options,
        )
        if security_schemes:
            for name, scheme in security_schemes.items():
                self.components.security_scheme(name, scheme.to_dict())
