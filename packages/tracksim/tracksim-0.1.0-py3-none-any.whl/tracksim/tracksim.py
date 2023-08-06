import requests
from typing import Union
from .errors import TrackSimError
from .types import Driver


class TrackSim:
    """TrackSim Class for the API"""

    def __init__(self, token: str, host: str = "https://api.tracksim.app/v1") -> None:
        """TrackSim Class to interfact with the

        Parameters:
            ``token`` (``str``):
                The Authentication Token from the Integrations Page
                https://tracksim.app/integrations

            ``host`` (``str``, optional):
                The API Host. Defaults to "https://api.tracksim.app/v1".

        """
        self._host = host
        self._session = requests.Session()
        self._session.headers.update(
            {"Content-Type": "application/json", "Authorization": f"Api-Key {token}"}
        )

    def _make_request(self, path: str, method: str = "get", **kwargs):
        """Make HTTP Requests against the API

        Parameters:
            ``path`` (``str``):
                The API calls' path for the request

            ``method`` (``str``, optional):
                HTTP Method (GET, POST, PUT, etc). Defaults to "GET".

            ``**kwargs``:
                Additional arguments passed to the API call.

        Returns:
            JSON serialized data

        """
        req = self._session.request(method, f"{self._host}/{path}", **kwargs)
        if req.status_code in [200, 201]:
            return req.json()
        else:
            raise TrackSimError(req.json())

    def add_driver(self, steam_id: Union[int, str]) -> Driver:
        """
        Adds a driver to the company.

        ---
        Parameters:
            ``steam_id`` (``int`` | ``str``):
                The drivers' SteamID64.

        ---
        Returns:
            ``Driver``: The Driver as a JSON object

        """
        req = self._make_request(
            path="drivers/add", method="POST", json={"steam_id": f"{steam_id}"}
        )
        return Driver(**req)

    def remove_driver(self, steam_id: Union[int, str]) -> None:
        """Removes a Driver from the company.

        ---
        Parameters:
            ``steam_id`` (``int`` | ``str``):
                The drivers' SteamID64.

        ---
        Returns:
            ``None``: On success, nothing is returned.

        """
        req = self._make_request(
            path="drivers/remove", method="DELETE", json={"steam_id": f"{steam_id}"}
        )
        return req

    def get_driver(self, steam_id: Union[int, str]) -> Driver:
        """Retrieves information about a Driver from the company.

        ---
        Parameters:
            ``steam_id`` (``str``):
                The drivers' SteamID64.

        Returns:
            ``Driver``: The driver as a JSON object

        """
        req = self._make_request(path=f"drivers/{steam_id}/details")
        return Driver(**req)

    def manage_driver(
        self,
        steam_id: Union[int, str],
        ets_job_logging: bool = True,
        ets_live_tracking: bool = True,
        ats_job_logging: bool = True,
        ats_live_tracking: bool = True,
    ) -> Driver:
        """Change settings about a driver.

        ---
        Parameters:
            ``steam_id`` (``str``):
                The drivers' SteamID64.

            ``ets_job_logging`` (``bool``, optional):
                Whether to log jobs for the driver. Defaults to True.

            ``ets_live_tracking`` (``bool``, optional):
                Whether to show the driver on the ETS2 Live Map. Defaults to True.

            ``ats_job_logging`` (``bool``, optional):
                Whether to log jobs for the driver in ATS. Defaults to True.

            ``ats_live_tracking`` (``bool``, optional):
                Whether tho show the driver on the ATS Live Map. Defaults to True.

        ---
        Returns:
            ``Driver``: The driver as a JSON object.

        """
        req = self._make_request(
            path=f"drivers/{steam_id}/manage",
            method="PATCH",
            json={
                "eut2_job_logging": ets_job_logging,
                "eut2_live_tracking": ets_live_tracking,
                "ats_job_logging": ats_job_logging,
                "ats_live_tracking": ats_live_tracking,
            },
        )
        return Driver(**req)

    def get_job_route(self, job_id: Union[int, str]) -> list:
        """Get the route details about as specific job.

        ---
        Parameters:
            ``job_id`` (``int`` | ``str``):
                The ID of the job

        ---
        Returns:
            ``list``:
                An array of ``dict``s containing X and Z coordinates and a UNIX Timestamp
        """
        req = self._make_request(
            path=f"jobs/{job_id}/route",
        )
        return req
