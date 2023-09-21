
from typing import List, Set, Union, Optional
import pandas as pd


class Threshold:
    """
    Class for defining a threshold value and operator for comparison.

    Args:
        threshold (Union[int, float]): The threshold value to compare with.
        operator (str): The comparison operator ('==', '<', or '>').

    Methods:
        __eq__(self, other): Compares the threshold value with 'other' based on the defined operator.
        __str__(self): Returns a string representation of the threshold object.
    """

    def __init__(self, threshold, operator: str):
        self.threshold = threshold
        self.operator = operator

    def __eq__(self, other) -> bool:
        """
        Compares the threshold value with 'other' based on the defined operator.

        Args:
            other: The value to compare with.

        Returns:
            bool: True if the comparison is successful; False otherwise.
        """
        if self.operator == "==":
            return other == self.threshold
        elif self.operator == "<":
            return other < self.threshold
        elif self.operator == ">":
            return other > self.threshold
        else:
            raise ValueError("Operator is not supported")

    def __str__(self) -> str:
        """
        Returns a string representation of the threshold object.

        Returns:
            str: A string representation of the threshold object.
        """
        return f"Threshold: {self.operator} {self.threshold}"


import pandas as pd


class Schedule:
    """
    Class for defining a schedule with days of the week and a time range.

    Args:
        days (Set[int]): A set of integers representing days of the week (0-6, where 0 is Sunday).
        time_range (Tuple[str, str]): A tuple containing a start and end time in HH:MM format.
        tz (Optional[str]): Timezone information.

    Methods:
        __eq__(self, other): Checks if a given day and time are in the schedule.
        __str__(self): Returns a string representation of the schedule.
    """

    def __init__(self, days: set[int], time_range: tuple[str, str], tz=None):
        self.days = days
        self.time_range = pd.date_range(time_range[0], time_range[1], freq="min").time
        self.tz = tz

    def __eq__(self, other) -> bool:
        """
        Checks if a given day and time are in the schedule.

        Args:
            other (Union[int, float, pd.Timestamp, pd.DatetimeIndex]): Input representing day and time.

        Returns:
            bool: True if the day and time are in the schedule; False otherwise.
        """
        if isinstance(other, (int, float, pd.Timestamp, pd.DatetimeIndex)):
            if isinstance(other, (int, float)):
                if self.tz:
                    other = pd.Timestamp(int(other), unit="s", tz=self.tz).floor("min")
                else:
                    other = pd.Timestamp(int(other), unit="s").floor("min")
            elif isinstance(other, pd.Timestamp):
                other = other.floor("min")
            return (
                other.dayofweek + 1
            ) % 7 in self.days and other.time() in self.time_range
        else:
            return False

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the schedule.

        Returns:
            str: A human-readable string representation of the schedule.
        """

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        s_sorted = []
        for i in self.days:
            s_sorted.append((i + 6) % 7)
        s_sorted.sort()

        # code to format list of integers to replace more than 2 consecutive integers with a range
        formatted = []
        consecutive = []
        for i in s_sorted:
            if len(consecutive) < 2:
                consecutive.append(i)
            else:
                if i - consecutive[-1] == 1 and i - consecutive[-2] == 2:
                    consecutive.append(i)
                else:
                    if len(consecutive) > 2:
                        formatted.append([consecutive[0], consecutive[-1]])
                        consecutive = [i]
                    elif len(consecutive) == 2:
                        formatted.append(consecutive[0])
                        consecutive[0] = consecutive[1]
                        consecutive[1] = i
                    else:
                        consecutive = [i]
        if len(consecutive) > 2:
            formatted.append([consecutive[0], consecutive[-1]])
        else:
            formatted.extend(consecutive)
        formatted_days = ""
        for i in formatted:
            if isinstance(i, list):
                if len(formatted_days) > 0:
                    formatted_days = formatted_days + ","
                formatted_days = formatted_days + f"{weekdays[i[0]]}-{weekdays[i[1]]}"
            else:
                if len(formatted_days) > 0:
                    formatted_days = formatted_days + ","
                formatted_days = formatted_days + f"{weekdays[i]}"

        start_time = str(self.time_range[0])[:-3]
        end_time = str(self.time_range[-1])[:-3]

        return f"{formatted_days} from: {start_time} to {end_time}"
