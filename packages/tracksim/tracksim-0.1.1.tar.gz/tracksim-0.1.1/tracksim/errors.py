""" Errors returned by the API """

_error_map = {
    "steam_profile_private": "The requested steam user profile is private.",
    "resource_already_exists": (
        "The selected driver is already connected to your company."
    ),
    "driver_no_compatible_games": (
        "The requested steam user doesn't own ETS2 or ATS "
        "(This could be due to it being private on their profile.)"
    ),
    "max_driver_limit_reached": (
        "You reached the maximum number of drivers for your account. "
        "Please upgrade to continue adding more drivers."
    ),
    "driver_does_not_exist": "Driver could not be found.",
}


class TrackSimError(Exception):
    def __init__(self, error):
        Exception.__init__(self, _error_map.get(error["error"]))
