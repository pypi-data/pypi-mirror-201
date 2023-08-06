from dataclasses import dataclass, asdict
from ..logger.logger import Logger
from .exception import BugCreationException


@dataclass(frozen=True)
class BugPriority:
    LOW: str = 'low'
    MINOR: str = 'minor'
    MAJOR: str = 'major'
    CRITICAL: str = 'critical'
    BLOCKER: str = 'blocker'


class BugMeta(type):
    """
    Meta class for raising BugCreationException
    """

    # Calls for each instance creation
    def __call__(cls, *args, **kwargs):
        try:
            cls._instance = super().__call__(*args, **kwargs)
        except Exception as e:
            # Catch python class instance creation exceptions
            raise BugCreationException(msg=str(e).replace('Bug.__init__()', '').strip().capitalize())
        # Validate _instance message, priority, actual_result, expected_result and steps_to_reproduce
        cls._validate()
        # Update the bug priority to lowercase
        cls._instance.priority = cls._instance.priority.lower()
        # Raise bug
        raise BugException(bug=cls._instance)

    def _validate(self):
        """
        Validate message, priority, actual_result, expected_result and steps_to_reproduce
        """
        self._validate_datatype()
        self._validate_priority()

    def _validate_datatype(self):
        """
        Checks
        ------
        1. message is a valid string
        2. priority is a valid string
        3. actual_result is a valid string
        4. expected_result is a valid string
        5. steps_to_reproduce is a valid string
        """
        for item in ('message', 'priority', 'actual_result', 'expected_result', 'steps_to_reproduce'):
            # Get item value
            value = getattr(self._instance, item)
            # If value is Logger instance, convert it to string and set the value
            if isinstance(value, Logger):
                setattr(self._instance, item, str(value))
            if not isinstance(getattr(self._instance, item), str):
                raise BugCreationException(msg=f'Invalid data type for {item}. Please provide a valid string')

    def _validate_priority(self):
        """
        Checks
        ------
        1. Valid bug priority
        """
        bug_priority_list = asdict(BugPriority()).values()
        # Check if the priority value is valid
        if self._instance.priority.lower() not in bug_priority_list:
            raise BugCreationException(
                msg=f'Invalid bug priority value.\n\nSupported bug priorities: {", ".join(bug_priority_list)}')


class Bug(metaclass=BugMeta):
    """
    Class for creating a bug
    """
    PRIORITY = BugPriority()

    def __init__(self,
                 message: str = "",
                 priority: str = BugPriority.LOW,
                 actual_result: str = "",
                 expected_result: str = "",
                 steps_to_reproduce: str = ""):
        self.message = message
        self.priority = priority
        self.actual_result = actual_result
        self.expected_result = expected_result
        self.steps_to_reproduce = steps_to_reproduce


class BugException(Exception):
    """
    Exception raised when a Bug class instance is created.
    """

    def __init__(self, bug: Bug):
        self._no_data_to_display = 'No data to display'
        self.priority = bug.priority
        self.message = f"""
BUG
---------
{bug.message.strip() if bug.message else self._no_data_to_display}

PRIORITY
---------
{bug.priority.strip() if bug.priority else self._no_data_to_display}

ACTUAL RESULT
---------
{bug.actual_result.strip() if bug.actual_result else self._no_data_to_display}

EXPECTED RESULT
---------
{bug.expected_result.strip() if bug.expected_result else self._no_data_to_display}

STEPS TO REPRODUCE
-------------
{bug.steps_to_reproduce.strip() if bug.steps_to_reproduce else self._no_data_to_display}
"""
        super().__init__(self.message)
