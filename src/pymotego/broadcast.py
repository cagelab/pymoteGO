import httpx
from concurrent.futures import ThreadPoolExecutor, Future
from urllib.parse import urljoin
from typing import Dict, Any

from pymotego.constants import DEFAULT_API_BASE_URL

_BASEURL = urljoin(DEFAULT_API_BASE_URL, "broadcast/data/")


class Broadcast:
    """
    Asynchronous HTTP broadcast client for sending experimental data to cogmoteGO.

    Uses a thread pool to execute non-blocking HTTP requests with HTTP/2 support.
    All methods return Future objects for fire-and-forget usage patterns.
    """

    def __init__(self) -> None:
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.client = httpx.Client(http2=True)

    def close(self) -> None:
        """
        Release HTTP client and thread pool resources.

        Should be called when the Broadcast instance is no longer needed.
        """
        self.client.close()
        self.executor.shutdown(wait=False)

    def send(
        self, data: Dict[str, Any], endpoint: str = "default"
    ) -> Future[httpx.Response]:
        """
        Send data to a broadcast endpoint.

        Parameters
        ----------
        data : Dict[str, Any]
            Dictionary payload to be sent (auto-serialized to JSON).
        endpoint : str, optional
            Target endpoint name. Default is "default".

        Returns
        -------
        Future[httpx.Response]
            Future object containing HTTP response.

        Examples
        --------
        >>> broadcaster = Broadcast()
        >>> future = broadcaster.send({"trial_id": 1, "result": "correct"})
        """
        return self.executor.submit(self._post, endpoint, data)

    def create(self, name: str) -> Future[httpx.Response]:
        """
        Create a new broadcast endpoint.

        Parameters
        ----------
        name : str
            Name of the endpoint to create.

        Returns
        -------
        Future[httpx.Response]
            Future object containing HTTP response.
        """
        return self.executor.submit(self._post_create, name)

    def delete(self, name: str) -> Future[httpx.Response]:
        """
        Delete a broadcast endpoint.

        Parameters
        ----------
        name : str
            Name of the endpoint to delete.

        Returns
        -------
        Future[httpx.Response]
            Future object containing HTTP response.
        """
        return self.executor.submit(self._delete, name)

    def list(self) -> Future[httpx.Response]:
        """
        List all broadcast endpoints.

        Returns
        -------
        Future[httpx.Response]
            Future object containing JSON response with endpoint names.
        """
        return self.executor.submit(self._get, "")

    def latest(self, endpoint: str = "default") -> Future[httpx.Response]:
        """
        Get latest data from a broadcast endpoint.

        Parameters
        ----------
        endpoint : str, optional
            Target endpoint name. Default is "default".

        Returns
        -------
        Future[httpx.Response]
            Future object containing latest data as JSON.
        """
        return self.executor.submit(self._get, f"{endpoint}/latest")

    def _get(self, path: str) -> httpx.Response:
        return self.client.get(urljoin(_BASEURL, path))

    def _post(self, endpoint: str, data: Dict[str, Any]) -> httpx.Response:
        return self.client.post(urljoin(_BASEURL, endpoint), json=data)

    def _post_create(self, name: str) -> httpx.Response:
        return self.client.post(_BASEURL, json={"name": name})

    def _delete(self, name: str) -> httpx.Response:
        return self.client.delete(urljoin(_BASEURL, name))
