import logging
import os
import time
import datetime
import calendar

try:
    import zoneinfo  # pragma: no cover
except ImportError:
    from backports import zoneinfo  # pragma: no cover

from tzlocal import windows_tz


def get_system_offset():
    """Get system's timezone offset using built-in library time.

    For the Timezone constants (altzone, daylight, timezone, and tzname), the
    value is determined by the timezone rules in effect at module load time or
    the last time tzset() is called and may be incorrect for times in the past.

    To keep compatibility with Windows, we're always importing time module here.
    """

    localtime = calendar.timegm(time.localtime())
    gmtime = calendar.timegm(time.gmtime())
    offset = gmtime - localtime
    # We could get the localtime and gmtime on either side of a second switch
    # so we check that the difference is less than one minute, because nobody
    # has that small DST differences.
    if abs(offset - time.altzone) < 60:
        return -time.altzone  # pragma: no cover
    else:
        return -time.timezone  # pragma: no cover


def get_tz_offset(tz):
    """Get timezone's offset using built-in function datetime.utcoffset()."""
    return int(datetime.datetime.now(tz).utcoffset().total_seconds())


def assert_tz_offset(tz):
    """Assert that system's timezone offset equals to the timezone offset found.

    If they don't match, we probably have a misconfiguration, for example, an
    incorrect timezone set in /etc/timezone file in systemd distributions."""
    tz_offset = get_tz_offset(tz)
    system_offset = get_system_offset()
    if tz_offset != system_offset:
        msg = (
            "Timezone offset does not match system offset: {} != {}. "
            "Please, check your config files."
        ).format(tz_offset, system_offset)
        raise ValueError(msg)


def _tz_name_from_env(tzenv=None):
    if tzenv is None:
        tzenv = os.environ.get("TZ")

    if not tzenv:
        return None

    logging.debug(f"Found a TZ environment: {tzenv}")

    if tzenv[0] == ":":
        tzenv = tzenv[1:]

    if tzenv in windows_tz.tz_win:
        # Yup, it's a timezone
        return tzenv

    if os.path.isabs(tzenv) and os.path.exists(tzenv):
        # It's a file specification, expand it, if possible
        parts = os.path.realpath(tzenv).split(os.sep)

        # Is it a zone info zone?
        possible_tz = "/".join(parts[-2:])
        if possible_tz in windows_tz.tz_win:
            # Yup, it is
            return possible_tz

        # Maybe it's a short one, like UTC?
        if parts[-1] in windows_tz.tz_win:
            # Indeed
            return parts[-1]

    logging.debug("TZ does not contain a time zone name")
    return None


def _tz_from_env(tzenv=None):
    if tzenv is None:
        tzenv = os.environ.get("TZ")

    if not tzenv:
        return None

    # Some weird format that exists:
    if tzenv[0] == ":":
        tzenv = tzenv[1:]

    # TZ specifies a file
    if os.path.isabs(tzenv) and os.path.exists(tzenv):
        # Try to see if we can figure out the name
        tzname = _tz_name_from_env(tzenv)
        if not tzname:
            # Nope, not a standard timezone name, just take the filename
            tzname = tzenv.split(os.sep)[-1]
        with open(tzenv, "rb") as tzfile:
            return zoneinfo.ZoneInfo.from_file(tzfile, key=tzname)

    # TZ must specify a zoneinfo zone.
    try:
        tz = zoneinfo.ZoneInfo(tzenv)
        # That worked, so we return this:
        return tz
    except zoneinfo.ZoneInfoNotFoundError:
        # Nope, it's something like "PST4DST" etc, we can't handle that.
        raise zoneinfo.ZoneInfoNotFoundError(
            "tzlocal() does not support non-zoneinfo timezones like %s. \n"
            "Please use a timezone in the form of Continent/City" % tzenv
        ) from None
