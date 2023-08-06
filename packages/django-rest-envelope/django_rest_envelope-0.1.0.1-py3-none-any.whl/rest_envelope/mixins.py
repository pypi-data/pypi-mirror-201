from rest_framework.request import Request
from rest_framework.response import Response


class ListEnvelopeMixin:
    envelope: str | None = None

    def get_envelope(self):
        assert self.envelope is not None, (
            f"'{self.__class__.__name__}' should either include a `envelope` attribute,"
            "or override the `get_envelope()` method."
        )
        return self.envelope

    def list(self, request: Request, *args, **kwargs) -> Response:
        response = super().list(request, *args, **kwargs)  # type: ignore
        return Response({self.get_envelope(): response.data})
