""" types.py """
# This module handles various type conversions.

from collections import namedtuple
from datetime import date as DateType, datetime as DateTimeType, time as TimeType
import os

# Third Party
import dateutil
import pytz_deprecation_shim as pds


NoneType = type(None)

# Epoch is the range of 'business active' dates.
EPOCH_START_YEAR = 2020
EPOCH_END_YEAR = 2050
EPOCH_START_DATE = DateType(EPOCH_START_YEAR, 1, 1)
EPOCH_END_DATE = DateType(EPOCH_END_YEAR, 12, 31)

# These should be considered true Min/Max for all other calculations.
MIN_YEAR = 1970
MAX_YEAR = 2201
MIN_DATE = DateType(MIN_YEAR, 1, 1)
MAX_DATE = DateType(MAX_YEAR, 12, 31)

UTC = pds.timezone("UTC")

def validate_datatype(argument_name: str, argument_value: object, expected_type: type, mandatory=False):
	"""
	A helpful generic function for checking a variable's datatype, and throwing an error on mismatches.
	Absolutely necessary when dealing with extremely complex Python programs that talk to SQL, HTTP, Redis, etc.

	NOTE: Function is opt-out by default. Set environment variable 'TEMPORAL_TYPE_CHECKING' to opt-in.
	NOTE: expected_type can be a single Type, or a tuple of Types.
	"""

	# Function is opt-out by default to slightly improve the performance.
	if not os.getenv("TEMPORAL_TYPE_CHECKING") in ("1", 1, True):
		return argument_value

	if not isinstance(argument_name, str):
		raise ValueError("Invalid syntax why calling 'validate_datatype'; the first argument must be a String.")

	from temporal_lib import ArgumentMissing, ArgumentType  # Necessary to avoid circular reference issues

	# Throw error if missing mandatory argument.
	if mandatory and isinstance(argument_value, NoneType):
		raise ArgumentMissing(f"Argument '{argument_name}' is mandatory.")

	if not argument_value:
		return argument_value  # datatype is going to be a NoneType, which is okay if not mandatory.

	# Check argument type
	if not isinstance(argument_value, expected_type):
		if isinstance(expected_type, tuple):
			expected_type_names = [ each.__name__ for each in expected_type ]
			msg = f"Argument '{argument_name}' should be one of these types: '{', '.join(expected_type_names)}'"
			msg += f"<br>Found a {type(argument_value).__name__} with value '{argument_value}' instead."
		else:
			msg = f"Argument '{argument_name}' should be of type = '{expected_type.__name__}'"
			msg += f"<br>Found a {type(argument_value).__name__} with value '{argument_value}' instead."
		raise ArgumentType(msg)

	# Otherwise, return the argument to the caller.
	return argument_value


def date_to_iso_string(any_date: DateType) -> str:
	"""
	Given a date, create an ISO String.  For example, 2021-12-26.
	"""
	if not isinstance(any_date, DateType):
		raise TypeError(f"Argument should be of type 'datetime.date', not '{type(any_date)}'")
	return any_date.strftime("%Y-%m-%d")


def datetime_to_iso_string(any_datetime):
	"""
	Given a datetime, create a ISO String
	"""
	if not isinstance(any_datetime, DateTimeType):
		raise TypeError(f"Argument 'any_date' should have type 'datetime', not '{type(any_datetime)}'")

	return any_datetime.isoformat(sep=' ')  # Note: Frappe not using 'T' as a separator, but a space ''


def datetime_to_sql_datetime(any_datetime: DateTimeType):
	"""
	Convert a Python DateTime into a DateTime that can be written to MariaDB/MySQL.
	"""
	return any_datetime.strftime('%Y-%m-%d %H:%M:%S')


# ----------------
# DATES
# ----------------

def is_date_string_valid(date_string):
	# dateutil parser does not agree with dates like "0001-01-01" or "0000-00-00"
	if (not date_string) or (date_string or "").startswith(("0001-01-01", "0000-00-00")):
		return False
	return True

def any_to_date(date_as_unknown):
	"""
	Given an argument of unknown Type, try to return a Date.
	"""
	try:
		if not date_as_unknown:
			return None
		if isinstance(date_as_unknown, str):
			return DateTimeType.strptime(date_as_unknown,"%Y-%m-%d").date()
		if isinstance(date_as_unknown, DateType):
			return date_as_unknown

	except dateutil.parser._parser.ParserError as ex:  # pylint: disable=protected-access
		raise ValueError(f"'{date_as_unknown}' is not a valid date string.") from ex

	raise TypeError(f"Unhandled type ({type(date_as_unknown)}) for argument to function any_to_date()")

def any_to_iso_date_string(any_date):
	"""
	Given a date, create a String that MariaDB understands for queries (YYYY-MM-DD)
	"""
	if isinstance(any_date, DateType):
		return any_date.strftime("%Y-%m-%d")
	if isinstance(any_date, str):
		return any_date
	raise TypeError(f"Argument 'any_date' can be a String or datetime.date only (found '{type(any_date)}')")

def datestr_to_date(date_as_string):
	"""
	Converts an ISO 8601 extended string (YYYY-MM-DD) to datetime.date object.
	"""
	# Don't make assumptions about duck types.
	if not date_as_string:
		return None
	if isinstance(date_as_string, DateType):
		return date_as_string  # was already a Date
	if not isinstance(date_as_string, str):
		raise TypeError(f"Argument 'date_as_string' should be of type String, not '{type(date_as_string)}'")
	if not is_date_string_valid(date_as_string):
		return None

	try:
		# The original function I was using was completely asinine.
		# If you pass a string representing a day of week (e.g. "Friday"), it returns the next Friday in the calendar.  Instead of an error.
		# return dateutil.parser.parse(date_as_string, yearfirst=True, dayfirst=False).date()

		return DateTimeType.strptime(date_as_string,"%Y-%m-%d").date()

	except dateutil.parser._parser.ParserError as ex:  # pylint: disable=protected-access
		raise ValueError("Value '{date_as_string}' is not a valid ISO 8601 extended string.") from ex

# ----------------
# TIMES
# ----------------

def date_to_datetime_midnight(any_date):
	"""
	Return a Date as a Datetime set to midnight.
	"""
	return DateTimeType.combine(any_date, DateTimeType.min.time())


def any_to_time(generic_time):
	"""
	Given an argument of a generic, unknown Type, try to return a Time.
	"""
	try:
		if not generic_time:
			return None
		if isinstance(generic_time, str):
			return timestr_to_time(generic_time)
		if isinstance(generic_time, TimeType):
			return generic_time

	except dateutil.parser._parser.ParserError as ex:  # pylint: disable=protected-access
		raise ValueError(f"'{generic_time}' is not a valid Time string.") from ex

	raise TypeError(f"Function argument 'generic_time' in any_to_time() has an unhandled data type: '{type(generic_time)}'")


def timestr_to_time(time_as_string):
	"""
	Converts a string time (8:30pm) to datetime.time object.
	Examples:
		8pm
		830pm
		830 pm
		8:30pm
		20:30
		8:30 pm
	"""
	time_as_string = time_as_string.lower()
	time_as_string = time_as_string.replace(':', '')
	time_as_string = time_as_string.replace(' ', '')

	am_pm = None
	hour = None
	minute = None

	if 'am' in time_as_string:
		am_pm = 'am'
		time_as_string = time_as_string.replace('am', '')
	elif 'pm' in time_as_string:
		am_pm = 'pm'
		time_as_string = time_as_string.replace('pm', '')
	time_as_string = time_as_string.replace(' ', '')

	# Based on length of string, make some assumptions:
	if len(time_as_string) == 0:
		raise ValueError(f"Invalid time string '{time_as_string}'")
	if len(time_as_string) == 1:
		hour = time_as_string
		minute = 0
	elif len(time_as_string) == 2:
		raise ValueError(f"Invalid time string '{time_as_string}'")
	elif len(time_as_string) == 3:
		hour = time_as_string[0]
		minute = time_as_string[1:3]  # NOTE: Python string splicing; last index is not included.
	elif len(time_as_string) == 4:
		hour = time_as_string[0:2]  # NOTE: Python string splicing; last index is not included.
		minute = time_as_string[2:4] # NOTE: Python string splicing; last index is not included.
		if int(hour) > 12 and am_pm == 'am':
			raise ValueError(f"Invalid time string '{time_as_string}'")
	else:
		raise ValueError(f"Invalid time string '{time_as_string}'")

	if not am_pm:
		if int(hour) > 12:
			am_pm = 'pm'
		else:
			am_pm = 'am'
	if am_pm == 'pm':
		hour = int(hour) + 12

	return TimeType(int(hour), int(minute), 0)

# ----------------
# DATETIMES
# ----------------

def any_to_datetime(datetime_as_unknown):
	"""
	Given an argument of unknown Type, try to return a DateTime.
	"""
	datetime_string_format = "%Y-%m-%d %H:%M:%S"
	try:
		if not datetime_as_unknown:
			return None
		if isinstance(datetime_as_unknown, str):
			return DateTimeType.strptime(datetime_as_unknown, datetime_string_format)
		if isinstance(datetime_as_unknown, DateTimeType):
			return datetime_as_unknown

	except dateutil.parser._parser.ParserError as ex:  # pylint: disable=protected-access
		raise ValueError(f"'{datetime_as_unknown}' is not a valid datetime string.") from ex

	raise TypeError(f"Unhandled type ({type(datetime_as_unknown)}) for argument to function any_to_datetime()")

# ----------------
# OTHER
# ----------------

def int_to_ordinal_string(some_integer) -> str:
	"""
	Convert an integer into its ordinal representation::
		int_to_ordinal_string(0)   => '0th'
		int_to_ordinal_string(3)   => '3rd'
		int_to_ordinal_string(122) => '122nd'
		int_to_ordinal_string(213) => '213th'
	"""
	# Shamelessly borrowed from here: https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
	some_integer = int(some_integer)
	if 11 <= (some_integer % 100) <= 13:
		suffix = 'th'
	else:
		suffix = ['th', 'st', 'nd', 'rd', 'th'][min(some_integer % 10, 4)]
	return str(some_integer) + suffix

WeekTuple = namedtuple('WeekTuple', 'year week_index')
