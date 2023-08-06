import base64
import json


class List(list):
    """Custom List Class to beautify output"""

    __slots__ = []

    def __str__(self) -> None:
        return TrackSimType.__str__(self)

    def __repr__(self) -> None:
        return (
            f"tracksim.types.List([{','.join(TrackSimType.__repr__(i) for i in self)}])"
        )


class TrackSimType:
    def __init__(self) -> None:
        pass

    @staticmethod
    def default(obj: "TrackSimType"):
        if isinstance(obj, bytes):
            return repr(obj)

        return {
            "_": obj.__class__.__name__,
            **{
                attr: getattr(obj, attr)
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            },
        }

    def __str__(self) -> str:
        return json.dumps(self, indent=4, default=TrackSimType.default)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.__dict__}>"


class Driver(TrackSimType):
    id: int
    steam_id: str
    username: str
    profile_photo_url: str
    client: "Client"
    settings: "Settings"
    is_banned: bool
    last_active: str

    def __init__(
        self,
        id: int,
        steam_id: str,
        username: str,
        profile_photo_url: str,
        client: object,
        settings: object,
        is_banned: bool,
        last_active: str,
    ) -> None:
        self.id = id
        self.steam_id = steam_id
        self.username = (
            # ! Fix this shit lmao
            # This is such a mess because the API returns non-ASCII characters
            # as B64 encoded strings as they're stored like that in the DB.
            # * TrackSim devs are aware.
            base64.b64decode(username.replace("B64_", "")).decode()
            if username.startswith("B64_")
            else username
        )
        self.profile_photo_url = profile_photo_url
        self.client = Client(**client)
        self.settings = Settings(**settings)
        self.is_banned = is_banned
        self.last_active = last_active


class Client(TrackSimType):
    is_installed: bool
    version: "Version"

    def __init__(self, is_installed: bool, version: object) -> None:
        self.is_installed = is_installed
        self.version = Version(**version)


class Version(TrackSimType):
    version: str
    branch: str
    platform: str

    def __init__(self, version: str, branch: str, platform: str) -> None:
        self.version = version
        self.branch = branch
        self.platform = platform


class Settings(TrackSimType):
    eut2: "EUT2"
    ats: "ATS"

    def __init__(self, eut2: object, ats: object) -> None:
        self.eut2 = EUT2(**eut2)
        self.ats = ATS(**ats)


class EUT2(TrackSimType):
    job_logging: bool
    live_tracking: bool

    def __init__(self, job_logging: bool, live_tracking: bool) -> None:
        self.job_logging = job_logging
        self.live_tracking = live_tracking


class ATS(TrackSimType):
    job_logging: bool
    live_tracking: bool

    def __init__(self, job_logging: bool, live_tracking: bool) -> None:
        self.job_logging = job_logging
        self.live_tracking = live_tracking
