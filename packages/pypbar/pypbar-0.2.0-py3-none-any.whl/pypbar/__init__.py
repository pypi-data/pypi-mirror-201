"""
This file is part of PyPBar.

Copyright (C) 2022  Koviubi56

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "0.2.0"
__author__ = "Koviubi56"
__email__ = "koviubi56@duck.com"
__license__ = "GNU GPLv3"
__copyright__ = "Copyright (C) 2022 Koviubi56"
__description__ = "Python ProgressBar"
__url__ = "https://github.com/koviubi56/pypbar"

import dataclasses
import itertools
import secrets
import shutil
import sys
import threading
import time
import warnings
from math import nan
from typing import (
    Collection,
    Generator,
    Generic,
    Iterable,
    List,
    NoReturn,
    Optional,
    Union,
)

from typing_extensions import Any, Protocol, Self, TypeAlias, TypeVar

Number: TypeAlias = Union[int, float]
T = TypeVar("T")
BLOCK = "\u2588"
TOP_HALF_BLOCK = "\u2580"
BOTTOM_HALF_BLOCK = "\u2584"
SQUARE = "\u25a0"
HIGH_DENSITY_DOTTED = "\u2593"
MEDIUM_DENSITY_DOTTED = "\u2592"
LOW_DENSITY_DOTTED = "\u2591"
SPINNERS = (
    [TOP_HALF_BLOCK, SQUARE, BOTTOM_HALF_BLOCK, SQUARE],
    ["|", "/", "-", "\\"],
    [
        ".  ",
        ".. ",
        "...",
        " ..",
        "  .",
        " ..",
        "...",
        ".. ",
        ".  ",
        "   ",
    ],
    [
        LOW_DENSITY_DOTTED,
        MEDIUM_DENSITY_DOTTED,
        HIGH_DENSITY_DOTTED,
        BLOCK,
        HIGH_DENSITY_DOTTED,
        MEDIUM_DENSITY_DOTTED,
    ],
)


def is_nan(obj: Any) -> bool:  # noqa: ANN401
    """
    Check if `obj` is nan.

    >>> from math import nan
    >>> is_nan(nan)
    True
    >>> is_nan(nan * 6.9)
    True
    >>> is_nan(6.9)
    False
    >>> is_nan(420)
    False
    >>> is_nan("hello")
    False
    >>> is_nan("nan")
    False

    Args:
        obj (Any): Any object.

    Returns:
        bool: True if `obj` is nan, False otherwise.
    """
    return obj is nan or obj == nan or repr(obj).lower() == "nan"


def avg_time(times: Collection[float]) -> float:
    """
    Calculate the average time of a list of times.

    >>> avg_time([1, 2, 3, 4, 5])
    3.0

    Args:
        times (List[float]): List of times.

    Returns:
        float: Average time.
    """
    try:
        return sum(times) / len(times)
    except ZeroDivisionError:
        return nan


def show_forever(progress_bar: "Bar[Any]", wait: float) -> None:
    """
    While `bar.allow`: call `bar.show()` and then sleep for `wait` seconds.

    Args:
        progress_bar (Bar[Any]): Bar to show.
        wait (float): Time to sleep in seconds.
    """
    while progress_bar.allow:
        progress_bar.show(from_thread=True)
        time.sleep(wait)


class WriteableAndFlushable(Protocol):
    def write(self, __s: str) -> int:
        ...

    def flush(self) -> None:
        ...


@dataclasses.dataclass(order=True)
class ShutUp:
    # Thanks for /u/The_Real_Slim_Lemon with the idea at
    # <https://yerl.org/OSntU>
    estimated_seconds: float
    # To make the user experience better, estimated_seconds SHOULD BE ROUNDED
    # UP, and a couple of seconds SHOULD BE ADDED to it.
    # So if the avg time is 10 sec, make it 12.

    time_started: Optional[float] = dataclasses.field(init=False)
    done: bool = dataclasses.field(init=False, default=False)

    @property
    def time_since_started(self) -> float:
        assert (  # noqa: S101
            self.time_started is not None
        ), "self.time_started MUST NOT be None"
        return time.perf_counter() - self.time_started

    def get_percent(self) -> float:
        if self.done:
            return 1.0
        if self.time_since_started / self.estimated_seconds < 0.95:
            return self.time_since_started / self.estimated_seconds
        return min(
            0.95
            + (0.003 * (self.time_since_started - self.estimated_seconds)),
            0.99,
        )


@dataclasses.dataclass(order=True)
class Bar(Generic[T]):
    """
    A progress bar.

    Args:
        iterable_or_max (Optional[Union[Iterable[T], int]]): Iterable to
        iterate. If it's an integer, it will be `range(iterable_or_max)`. If
        it's None, the progress bar will not have a `max` attribute.
        desc (Optional[str], optional): Description of the progress bar. This
        can be changed while the progress bar is being shown. Defaults to None.
        unit (str, optional): Unit of the progress bar. Defaults to "it".
        fillchar (str, optional): Character to fill the progress bar with.
        Defaults to "\u2588".
        empty_fillchar (str, optional): Character to fill the progress bar
        with when the progress bar is empty. Defaults to " ".
        underflow_char (str, optional): Character that is shown if the
        progress bar underflows. Defaults to "!".
        overflow_char (str, optional): Character that is shown if the
        progress bar overflows. Defaults to ">".
        flush (bool, optional): Whether to flush the output. Defaults to
        True.
        calculate_length_for_iterable (bool, optional): Calculate length of
        the iterable. Ignored for non-iterables. Defaults to True.
    """

    iterable_or_max: Optional[Union[Iterable[T], int, ShutUp]]
    desc: Optional[str] = None
    unit: str = "it"
    fillchar: str = BLOCK
    empty_fillchar: str = " "
    underflow_char: str = "!"
    overflow_char: str = ">"
    flush: bool = True
    stream: WriteableAndFlushable = sys.stdout
    leave: bool = True
    calculate_length_for_iterable: bool = True

    def __post_init__(self) -> None:
        """Initialize the progress bar."""
        self.iterable: Union[None, range, Iterable[T]]
        self.max: Optional[int]

        self.underflow = False
        self.start_time = time.perf_counter()
        self.last_time = time.perf_counter()
        self.pos = 0
        self.spinners = itertools.cycle(secrets.choice(SPINNERS))
        self.spinner = next(self.spinners)
        self.times: List[float] = []
        self.lock = threading.Lock()
        self.allow = True
        if self.iterable_or_max is None:
            self.iterable = None
            self.max = None
        elif isinstance(self.iterable_or_max, ShutUp):
            self.iterable = None
            self.max = None
            self.iterable_or_max.time_started = self.start_time
        elif isinstance(self.iterable_or_max, int):
            self.iterable = range(self.iterable_or_max)
            self.max = self.iterable_or_max
        else:
            if (not hasattr(self.iterable_or_max, "__iter__")) and (
                not hasattr(self.iterable_or_max, "__next__")
            ):
                raise TypeError(
                    "iterable_or_max must be an iterable, an"
                    " integer, or None"
                )
            self.iterable = self.iterable_or_max
            if self.calculate_length_for_iterable:
                try:
                    self.max = len(self.iterable)  # type: ignore
                except Exception:  # noqa: BLE001
                    try:
                        self.iterable = tuple(self.iterable)
                    except Exception as exc:  # noqa: BLE001
                        warnings.warn(
                            f"{exc.__class__.__name__}: {exc}; iterable and"
                            " max is set to None",
                            stacklevel=2,
                        )
                        self.iterable = None
                    self.max = (
                        len(self.iterable)
                        if self.iterable is not None
                        else None
                    )
            else:
                self.max = None

    def __iter__(self) -> Generator[T, None, None]:
        """
        Iterate over the iterable. This function also updates, and shows the
        progress bar. If there's nothing to yield or self.allow is False, it
        will call exit.

        Yields:
            T: Next item in the iterable. If the iterable is None, yield None.
        """
        # sourcery skip: hoist-if-from-if
        if self.iterable is None:
            while self.allow:
                yield None
                if self.allow:
                    self.update()
                    self.show()
        else:
            for item in self.iterable:
                if self.allow:
                    yield item
                    if self.allow:
                        self.update()
                        # // self.show()
        self.exit()

    def __next__(self) -> T:
        """
        Get the next item in the iterable. This function does NOT update, or
        show the progress bar. If there's nothing to yield or self.allow is
        False, it will call exit.

        Raises:
            StopIteration: If self.allow is False; if the progress bar exited.

        Returns:
            T: Next item in the iterable. If the iterable is None, return None.
        """
        if not self.allow:
            raise StopIteration
        return (None) if (self.iterable is None) else (next(self.iterable))

    def __enter__(self) -> Self:
        """
        Enter the context manager. This function starts a thread, that shows
        this progress bar every 0.07 seconds.

        Returns:
            Self: This progress bar.
        """
        self.start_thread()
        return self

    def __exit__(self, *_: Any) -> None:  # noqa: ANN401
        """Exit the context manager. This function stops the progress bar; it
        calls exit."""
        self.exit()

    def start_thread(self) -> None:
        """Start the thread that shows the progress bar every 0.07 seconds."""
        thread = threading.Thread(
            target=show_forever,
            args=(self, 0.07),
            name=f"Thread-Bar-{time.time_ns()}",
            daemon=True,
        )
        return thread.start()

    def get_avg_time(self) -> float:
        """
        Get the average time between updates.
        Equals to:
        ```py
        sum(self.times) / len(self.times)
        ```

        Returns:
            float: Average time between updates.
        """
        return avg_time(self.times)

    def time_until_end(self) -> float:
        """
        Get the time until the progress bar is finished.
        Equals to:
        ```py
        # get the average time between updates
        # ---------------------------------
        (sum(self.times) / len(self.times)) * (self.max - self.pos)
        ```

        Returns:
            float: Time until the progress bar is finished.
        """
        return (
            (nan)
            if (self.max is None)
            else (self.get_avg_time() * (self.max - self.pos))
        )

    def get_percent(self) -> float:
        """
        Get the percent of the progress bar.
        Equals to:
        ```py
        self.pos / self.max
        ```

        Returns:
            float: Percent of the progress bar. [0,1]
        """
        if isinstance(self.iterable_or_max, ShutUp):
            return self.iterable_or_max.get_percent()
        return nan if self.max is None else self.pos / self.max

    @property
    def overflow(self) -> bool:
        """
        Get whether the progress bar overflows.
        Equals to:
        ```py
        (self.max is not None) and (self.pos > self.max)
        ```py

        Returns:
            bool: Whether the progress bar overflows.
        """
        return (self.max is not None) and (self.pos > self.max)

    @staticmethod
    def zfill_num(num: Number, width: int) -> str:
        """
        Get a string of the given number with the given width.
        Equals to:
        ```py
        str(int(num)).zfill(width)
        ```

        Args:
            num (Number): Number to get the string of.
            width (int): Width of the string.

        Returns:
            str: String of the given number with the given width.
        """
        return str(int(num)).zfill(width)

    @classmethod
    def second_to_str(cls, seconds: float) -> str:  # noqa: PLR0911
        """
        Convert a number of seconds to a string.

        Args:
            seconds (float): Number of seconds to convert.

        Returns:
            str: String of the given number of seconds.
        """
        if is_nan(seconds):
            return "?"

        if seconds < 0.0001:
            return f"{cls.zfill_num(seconds * 1e9, 1)} ns"
        if seconds < 0.001:
            return f"{cls.zfill_num(seconds * 1e6, 1)} µs"
        if seconds < 1:
            return f"{cls.zfill_num(seconds * 1000, 1)} ms"
        if seconds < 60:
            return f"00:{cls.zfill_num(seconds, 2)}"
        if seconds < 3600:
            return (
                f"{cls.zfill_num(seconds / 60, 2)}:"
                f"{cls.zfill_num(seconds % 60, 2)}"
            )
        return (
            f"{int(seconds / 3600)}:"
            f"{cls.zfill_num(seconds % 3600 / 60, 2)}"
            f":{cls.zfill_num(seconds % 60, 2)}"
        )

    def get_time_spent(self) -> float:
        """
        Get the time spent on the progress bar.
        Equals to:
        ```py
        time.time() - self.start_time
        ```

        Returns:
            float: Time spent on the progress bar.
        """
        return time.perf_counter() - self.start_time

    def update(self) -> None:
        """
        Update the progress bar. This function also updates the time spent on
        the progress bar.
        ! [WARNING] This function does NOT show the progress bar!
        """
        self.pos += 1
        self.times.append(time.perf_counter() - self.last_time)
        while len(self.times) > 200:
            self.times.pop(0)
        self.last_time = time.perf_counter()

    @staticmethod
    def add_spaces(num: int) -> str:
        """
        Add spaces to a number, so it's easier to read.

        >>> Bar.add_spaces(1234567)
        '1 234 567'

        Args:
            num (int): Number to add spaces to.

        Returns:
            str: Number with spaces.
        """
        string = str(num)
        if len(string) < 5:
            return string
        rv = ""
        for idx, ch in enumerate(reversed(string)):
            if (idx % 3 == 0) and (idx != 0):
                rv = f" {rv}"
            rv = ch + rv
        return rv

    def _text_no_max(self) -> str:
        """
        Get the text of the progress bar without the max.

        Returns:
            str: Text of the progress bar without the max.
        """
        return (
            f'{f"{self.desc} " if self.desc else ""}'
            f"{self.add_spaces(self.pos)} {self.unit} $ ["
            f"{self.second_to_str(self.get_time_spent())}<?,"
            f" {self.second_to_str(self.get_avg_time())}/{self.unit}]"
        )

    def _text_shutup(self) -> str:
        assert isinstance(  # noqa: S101
            self.iterable_or_max, ShutUp
        ), "to use _text_shutup iterable_or_max MUST be an instance of ShutUp"
        _desc = f"{self.desc} " if self.desc else ""
        _percent = int(self.get_percent() * 100)
        _time_spent = self.second_to_str(self.get_time_spent())
        _time_until_end = self.second_to_str(
            self.iterable_or_max.estimated_seconds
        )
        rv = f"{_desc}{_percent}% |$| $ [{_time_spent}<{_time_until_end}]"
        return self._do_progress_bar(rv)

    def _gen_bar(self, characters_for_bar: int) -> str:
        """
        Get the bar of the progress bar.

        Args:
            characters_for_bar (int): Number of characters for the bar.

        Raises:
            ValueError: If the bar underflows AND overflows.

        Returns:
            str: Bar of the progress bar.
        """
        if self.underflow and self.overflow:
            raise ValueError(
                "Bar cannot be underflow and overflow at the same time"
            )
        bar_length = int(characters_for_bar * self.get_percent())
        progress_bar = self.fillchar * bar_length
        progress_bar = progress_bar[:characters_for_bar]
        if self.underflow:
            progress_bar += self.underflow_char
        if self.overflow:
            progress_bar += self.overflow_char
        return progress_bar.ljust(characters_for_bar, self.empty_fillchar)

    def _text_with_max(self) -> str:
        """
        Get the text of the progress bar with the max.

        Raises:
            ValueError: If characters_for_bar is less than 1.

        Returns:
            str: Text of the progress bar with the max.
        """
        assert (  # noqa: S101
            self.max is not None
        ), "to use _text_with_max max MUST NOT be None"
        _desc = f"{self.desc} " if self.desc else ""
        _percent = int(self.get_percent() * 100)
        _time_spent = self.second_to_str(self.get_time_spent())
        _time_until_end = self.second_to_str(self.time_until_end())
        _avg_time = self.second_to_str(self.get_avg_time())
        rv = (
            f"{_desc}{_percent}% |$| {self.add_spaces(self.pos)}/"
            f"{self.add_spaces(self.max)} $ [{_time_spent}<{_time_until_end}, "
            f"{_avg_time}/{self.unit}]"
        )
        return self._do_progress_bar(rv)

    def _do_progress_bar(self, rv: str) -> str:
        characters_for_bar = shutil.get_terminal_size().columns - len(rv) - 1
        if characters_for_bar < 1:
            raise ValueError("Terminal is too small")
        progress_bar = self._gen_bar(characters_for_bar)
        return rv.replace("$", progress_bar, 1)

    def _write(self, text: str) -> None:
        """
        Write the given text to the stream. If self.flush, the stream is
        flushed.
        ! [WARNING] This function MAY INTERFERE WITH THE PROGRESS BAR!

        Args:
            text (str): Text to write.
        """
        self.stream.write(text)
        if self.flush:
            self.stream.flush()

    def show(self, *, from_thread: bool = False) -> bool:
        """
        Show the progress bar.

        Args:
            from_thread (bool, optional): Is this function called from the
            thread? If you don't know what this means LEAVE IT AS FALSE.
            Defaults to False.

        Raises:
            ValueError: If "$" is in self.desc

        Returns:
            bool: Whether the progress bar was shown. If it is False, no
            further attempts should be made to show the progress bar.
        """
        if self.desc and ("$" in self.desc):
            raise ValueError('Description cannot contain "$"')
        if not self.allow:
            return False
        with self.lock:
            if isinstance(self.iterable_or_max, ShutUp):
                text = self._text_shutup()
            elif (self.max is None) or (self.iterable is None):
                text = self._text_no_max()
            else:
                text = self._text_with_max()
            if from_thread:
                self.spinner = next(self.spinners)
            text = text.replace("$", self.spinner, 1)
            self._write(text.ljust(shutil.get_terminal_size().columns) + "\r")
            return True

    def exit(self, *, force: bool = False) -> None:  # noqa: A003
        r"""
        Exit the progress bar.

        ```text
        +------------+          +-------+          +--------+
        │ self.allow |--false-->│ force |--false-->│ return │
        +------------+          +-------+          +--------+
            true                    │
              │                   true
              │ <-------------------+
              v
        +------------+          +-----------------------+
        │ Underflow? |--true--> │ self.underflow = True │
        +------------+          +-----------+-----------+
              │ <---------------------------+
              v
        +------+
        | show |
        +------+
            |
            v
        +--------------------+
        │ self.allow = False │
        +--------------------+
                  │
                  v
        +------------+          +--------------------+
        │ self.leave |--true--> │ self._write("\n")  │
        +------------+          +--------------------+
               │
               v
        +-----------------------------------------------------------+
        │ self._write(                                              │
        │   "\r" + " " * shutil.get_terminal_size().columns + "\r"  │
        │ )                                                         │
        +-----------------------------------------------------------+
        ```

        Args:
            force (bool, optional): Force the exit even if self.allow is
            False. Defaults to False.
        """
        if (not self.allow) and (not force):
            return
        if (self.max is not None) and (self.pos < self.max):
            self.underflow = True
        if isinstance(self.iterable_or_max, ShutUp):
            self.iterable_or_max.done = True
        self.show()
        self.allow = False
        if self.leave:
            self._write("\n")
        else:
            self._write("\r" + " " * shutil.get_terminal_size().columns + "\r")

    def write(self, text: str, ljust: bool = True) -> None:
        # sourcery skip: remove-unnecessary-cast
        """
        Write the given text to the stream. If self.flush, the stream is
        flushed.
        This function makes sure that the text shown doesn't interfere with
        the progress bar.

        Args:
            text (str): Text to write.
            ljust (bool, optional): Whether to left-justify the text.
        """
        with self.lock:
            self._write(
                (  # noqa: UP034
                    str(text).ljust(shutil.get_terminal_size().columns)
                    if ljust
                    else str(text)
                )
                # ? idk if it's needed
                # // + "\n"
            )


def not_in_external(*_: Any, **__: Any) -> NoReturn:  # noqa: ANN401
    raise AttributeError("External bar doesn't have that attribute")


class External(Bar):
    """
    A progress bar, but the position is obtained from an external source (for
    example: downloading a file)
    """

    def __init__(
        self,
        max_: int,
        desc: Optional[str] = None,
        unit: str = "it",
    ) -> None:
        """
        Create an `External` object.
        Most other attributes (e.g. fillchar, flush, stream, leave, etc...)
        can still be changed manually, but I just didn't want to add them here.

        Args:
            max_ (int): The maximum value. Required!
            desc (Optional[str], optional): The description. Defaults to None.
            unit (str, optional): Unit to use. Defaults to "it".
        """
        self.max = max_
        # most other attributes still exist and are in use, but these are the
        # more important ones. if the user wants to modify another, they will
        # have to modify the attribute manually
        self.desc = desc
        self.unit = unit

        # --- __post_init__ ---
        self.iterable = None
        self.underflow = None
        self.start_time = time.perf_counter()
        self.last_time = time.perf_counter()
        self.pos = 0
        self.spinners = itertools.cycle(secrets.choice(SPINNERS))
        self.spinner = next(self.spinners)
        self.lock = threading.Lock()
        self.allow = True

    # these attributes do not exist
    __iter__ = (
        __next__
    ) = update = _text_no_max = _text_shutup = not_in_external

    def get_avg_time(self) -> float:
        """
        Get the average time for one position to change.

        Returns:
            float: Average time for one position to change or nan. (0,inf)
        """
        try:
            return (self.last_time - self.start_time) / self.pos
        except ZeroDivisionError:
            return nan

    def get_percent(self) -> float:
        """
        Get the percent of the progress bar.
        Equals to:
        ```py
        self.pos / self.max
        ```

        Returns:
            float: Percent of the progress bar. [0,1]
        """
        return self.pos / self.max

    def update_with_new(self, extra: int) -> None:
        """
        Update the progress bar with `extra`. This function also updates
        `.last_time`. This function does NOT show the progress bar!

        Args:
            extra (int): The amount to add to `.pos`
        """
        self.pos += extra
        self.last_time = time.perf_counter()

    def show(self, *, from_thread: bool = False) -> bool:
        """
        Write the current progress bar to the stream, and flush if needed.

        Args:
            from_thread (bool, optional): Whether or not this function was
            called from the thread. You should leave it as False. Defaults to
            False.

        Raises:
            ValueError: If $ is in the description

        Returns:
            bool: `self.allow`
        """
        if self.desc and ("$" in self.desc):
            raise ValueError('Description cannot contain "$"')
        if not self.allow:
            return False
        with self.lock:
            text = self._text_with_max()
            if from_thread:
                self.spinner = next(self.spinners)
            text = text.replace("$", self.spinner, 1)
            self._write(text.ljust(shutil.get_terminal_size().columns) + "\r")
            return True

    def exit(self, *, force: bool = False) -> None:  # noqa: A003
        """
        Exit the progress bar.
        Show the progress bar for the last time (with underflow as necessary),
        set `self.allow` to False, and hide the progress bar if
        `leave is False`.

        Args:
            force (bool, optional): Force exiting even if
            `self.allow is False`. Defaults to False.
        """
        if (not self.allow) and (not force):
            return
        if self.pos < self.max:
            self.underflow = True
        self.show()
        self.allow = False
        if self.leave:
            self._write("\n")
        else:
            self._write("\r" + " " * shutil.get_terminal_size().columns + "\r")


if __name__ == "__main__":
    with External(1_000_000, "downloading", "kB") as bar:
        while bar.pos != bar.max:
            bar.update_with_new(1000)
            time.sleep(0.1)
