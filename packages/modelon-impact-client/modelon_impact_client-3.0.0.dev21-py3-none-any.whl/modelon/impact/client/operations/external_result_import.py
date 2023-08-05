from typing import Dict, Any
from modelon.impact.client import exceptions
from modelon.impact.client.entities.external_result import ExternalResult
from modelon.impact.client.sal.service import Service
from modelon.impact.client.operations.base import AsyncOperation, AsyncOperationStatus


class ExternalResultImportOperation(AsyncOperation):
    """An operation class for the modelon.impact.client.entities.

    external_result.ExternalResult class.

    """

    def __init__(self, location: str, service: Service):
        super().__init__()
        self._location = location
        self._sal = service

    def __repr__(self) -> str:
        return f"Result import operations for id '{self.id}'"

    def __eq__(self, obj: object) -> bool:
        return (
            isinstance(obj, ExternalResultImportOperation)
            and obj._location == self._location
        )

    @property
    def id(self) -> str:
        """Result import id."""
        return self._location.split('/')[-1]

    @property
    def name(self) -> str:
        """Return the name of operation."""
        return "Result import"

    def _info(self) -> Dict[str, Any]:
        return self._sal.imports.get_import_status(self._location)["data"]

    def data(self) -> ExternalResult:
        """Returns a new ExternalResult class instance.

        Returns:

            external_result:
                A ExternalResult class instance.

        """
        info = self._info()
        if info['status'] == AsyncOperationStatus.ERROR.value:
            raise exceptions.ExternalResultUploadError(
                f"External result upload failed! Cause: {info['error'].get('message')}"
            )
        resp = self._sal.external_result.get_uploaded_result(self.id)
        return ExternalResult(resp['data']['id'], self._sal)

    def status(self) -> AsyncOperationStatus:
        """Returns the upload status as an enumeration.

        Returns:

            upload_status:
                The AsyncOperationStatus enum. The status can have the enum values
                AsyncOperationStatus.READY, AsyncOperationStatus.RUNNING or
                AsyncOperationStatus.ERROR

        Example::

            workspace.upload_result('C:/A.mat').status()

        """
        return AsyncOperationStatus(self._info()["status"])
