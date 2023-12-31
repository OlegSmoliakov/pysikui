# module for storing pysikuli global variables with user access
import pymsgbox as pmb
import pymonctl as pmc
import platform
import os

from pynput.keyboard import Key
from pynput.mouse import Button


_MONITOR_REGION = pmc.getPrimary().box
_MONITOR_RESOLUTION = (
    _MONITOR_REGION[2],
    _MONITOR_REGION[3],
)


def getOS():
    OSX, WIN, UNIX = False, False, False
    system = platform.system()

    if system == "Darwin":
        OSX = True
    elif system == "Windows":
        WIN = True
    elif system == "Linux":
        UNIX = True
    else:
        raise OSError(f"Can't recognize OS: {system}")

    return OSX, WIN, UNIX


def getPlatformModule(OSX, WIN, UNIX):
    if OSX:
        from . import _osx as platformModule
    elif WIN:
        from . import _win as platformModule
    elif UNIX:
        from . import _unix as platformModule
    else:
        raise OSError(f"No OS is selected")
    return platformModule


def getDefaultFailsafeHotkey(OSX):
    if OSX:
        return [Key.option, Key.shift, "c"]
    else:
        return [Key.ctrl, Key.alt, "k"]


class Config:
    # TODO: Sleep value should vary with the platform. http://stackoverflow.com/q/1133857

    # platform selection
    OSX, WIN, UNIX = getOS()
    platformModule = getPlatformModule(OSX, WIN, UNIX)

    # The number of seconds to pause after EVERY public action function call. Useful for debugging:
    PAUSE_BETWEEN_ACTION = 0

    # Failsafe constants

    # If the mouse is over a coordinate in FAILSAFE_REGIONS and FAILSAFE is True, the FailSafeException is raised.
    # The rest of the points are added to the FAILSAFE_REGIONS list at the bottom of this file, after size() has been defined.
    # The points are for the corners of the screen, but note that these points don't automatically change if the screen resolution changes.
    FAILSAFE = True
    FAILSAFE_REGIONS = [(0, 0, 0, 0)]

    @property
    def FAILSAFE_HOTKEY(self):
        if self._FAILSAFE_HOTKEY is None:
            self._FAILSAFE_HOTKEY = getDefaultFailsafeHotkey(self.OSX)
        return self._FAILSAFE_HOTKEY

    @FAILSAFE_HOTKEY.setter
    def FAILSAFE_HOTKEY(self, val):
        self._FAILSAFE_HOTKEY = val

    # Constants for image search function

    # This option almost doubles the speed by using compressed images in image recognition,
    # but degrades unambiguous image recognition.
    # Use this parameter as a compression multiplier, for instance:
    # if the value is 1 - the image size doesn't change (width / 1 and height / 1)
    # if the value is 2 - the image will become x4 times smaller, (width / 2 and height / 2).
    COMPRESSION_RATIO = 2

    # This parameter increases speed by about 30%, but degrades unambiguous image recognition
    GRAYSCALE = True

    # Main score for detection match
    MIN_PRECISION = 0.8
    # After this time a image search will return a None result
    MAX_SEARCH_TIME = 2.0

    REFRESH_RATE = None
    if not REFRESH_RATE:
        REFRESH_RATE = int(pmc.getPrimary().frequency)

    # Each TIME_STEP in seconds a image searching takes a new screenshot for next analysis
    # Each TIME_STEP in seconds tap and write takes after each key press
    TIME_STEP = 0

    # Constants for window control function
    WINDOW_WAITING_CONFIRMATION = True

    @property
    def MONITOR_REGION(self) -> tuple[int, int, int, int]:
        return _MONITOR_REGION

    @property
    def MONITOR_RESOLUTION(self) -> tuple[int, int, int, int]:
        return _MONITOR_RESOLUTION

    # Constants for pymsgbox module
    @property
    def OK_TEXT(self):
        return self._OK_TEXT

    @OK_TEXT.setter
    def OK_TEXT(self, val: str):
        self._OK_TEXT = val
        pmb.OK_TEXT = str(val)

    @property
    def CANCEL_TEXT(self):
        return self._CANCEL_TEXT

    @CANCEL_TEXT.setter
    def CANCEL_TEXT(self, val: str):
        self._CANCEL_TEXT = val
        pmb.CANCEL_TEXT = str(val)

    @property
    def ROOT_WINDOW_POSITION(self):
        return self._ROOT_WINDOW_POSITION

    @ROOT_WINDOW_POSITION.setter
    def ROOT_WINDOW_POSITION(self, val: tuple[int]):
        self._ROOT_WINDOW_POSITION = val
        pmb.rootWindowPosition = f"+{val[0]}" f"+{val[1]}"

    @property
    def PROPORTIONAL_FONT_SIZE(self):
        return self._PROPORTIONAL_FONT_SIZE

    @PROPORTIONAL_FONT_SIZE.setter
    def PROPORTIONAL_FONT_SIZE(self, val: int):
        self._PROPORTIONAL_FONT_SIZE = val
        pmb.PROPORTIONAL_FONT_SIZE = val

    @property
    def MONOSPACE_FONT_SIZE(self):
        return self._MONOSPACE_FONT_SIZE

    @MONOSPACE_FONT_SIZE.setter
    def MONOSPACE_FONT_SIZE(self, val: int):
        self._MONOSPACE_FONT_SIZE = val
        pmb.MONOSPACE_FONT_SIZE = val

    @property
    def TEXT_ENTRY_FONT_SIZE(self):
        return self._TEXT_ENTRY_FONT_SIZE

    @TEXT_ENTRY_FONT_SIZE.setter
    def TEXT_ENTRY_FONT_SIZE(self, val: int):
        self._TEXT_ENTRY_FONT_SIZE = val
        pmb.TEXT_ENTRY_FONT_SIZE = val

    # Constants for the mouse button names:
    MOUSE_PRIMARY_BUTTON = Button.left
    MOUSE_SECONDARY_BUTTON = Button.right
    MOUSE_MOVE_SPEED = 1

    # Constants for tools module
    SOUND_ON = True
    SOUND_CAPTURE_PATH = os.path.join(
        os.path.dirname(__file__), "tools_data/_capture.mp3"
    )
    SOUND_FINISH_PATH = os.path.join(
        os.path.dirname(__file__), "tools_data/_finish.mp3"
    )

    DEBUG_SETTINGS = {
        "PAUSE_BETWEEN_ACTION": 0.5,
        "TIME_STEP": round(1 / REFRESH_RATE, 5),
        "WAIT_WINDOW_ACTIVATION": True,
        "MOUSE_MOVE_DURATION": 0.1,
        "MOUSE_MOVE_STEPS": min(_MONITOR_RESOLUTION) / 4,
    }

    @property
    def DEBUG(self):
        return self._DEBUG

    @DEBUG.setter
    def DEBUG(self, val):
        self._DEBUG = val
        for key, value in self.DEBUG_SETTINGS.items():
            setattr(self, key, value)

    def __init__(self):
        self._OK_TEXT = "OK"
        self._CANCEL_TEXT = "Cancel"

        # 400 and 100 is min size of pymsgbox window
        root_x = int(_MONITOR_RESOLUTION[0] / 2 - 400 / 2)
        root_y = int(_MONITOR_RESOLUTION[1] / 2 - 100 / 2)

        self._ROOT_WINDOW_POSITION = (root_x, root_y)
        self._PROPORTIONAL_FONT_SIZE = 10
        self._MONOSPACE_FONT_SIZE = 9
        self._TEXT_ENTRY_FONT_SIZE = 12

        self._DEBUG = False

        self._FAILSAFE_HOTKEY = None


class Key:
    alt = Key.alt
    alt_r = Key.alt_r
    alt_gr = Key.alt_gr
    caps_lock = Key.caps_lock
    ctrl = Key.ctrl
    ctrl_r = Key.ctrl_r
    down = Key.down
    end = Key.end
    esc = Key.esc
    f1 = Key.f1
    f2 = Key.f2
    f3 = Key.f3
    f4 = Key.f4
    f5 = Key.f5
    f6 = Key.f6
    f7 = Key.f7
    f8 = Key.f8
    f9 = Key.f9
    f10 = Key.f10
    f11 = Key.f11
    f12 = Key.f12
    f13 = Key.f13
    f14 = Key.f14
    f15 = Key.f15
    f16 = Key.f16
    f17 = Key.f17
    f18 = Key.f18
    f19 = Key.f19
    f20 = Key.f20
    home = Key.home
    left = Key.left
    page_down = Key.page_down
    page_up = Key.page_up
    right = Key.right
    shift = Key.shift
    shift_r = Key.shift_r
    space = Key.space
    tab = Key.tab
    up = Key.up

    media_play_pause = Key.media_play_pause
    media_volume_mute = Key.media_volume_mute
    media_volume_down = Key.media_volume_down
    media_volume_up = Key.media_volume_up
    media_previous = Key.media_previous
    media_next = Key.media_next

    if Config.OSX:
        cmd = Key.cmd
        cmd_r = Key.cmd_r
        delete = Key.backspace

        option = Key.alt
        option_r = Key.alt_r
        return_r = Key.enter
    else:
        win = Key.cmd
        enter = Key.enter
        delete = Key.delete
        backspace = Key.backspace

        insert = Key.insert
        menu = Key.menu
        num_lock = Key.num_lock
        pause = Key.pause
        print_screen = Key.print_screen
        scroll_lock = Key.scroll_lock


config = Config()
