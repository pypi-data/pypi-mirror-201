# cython: embedsignature = True
# cython: language_level = 3str

"""This extension module provides class definitions used in other modules."""

# from __future__ import annotations
from win32com.client import Dispatch
import win32gui, win32api, win32con, win32clipboard, pythoncom
import keyboard, threading, queue
import  windowHelper as winHelper
from traceback import format_tb, format_exc
from pynput.keyboard import Controller as kbController
from pynput.mouse import Controller as mController
from time import time
from collections import deque
from pyWinhook.HookManager import KeyboardEvent
from macropy import configurations

cpdef enum KB_Con:
    # """
    # Description:
    #     An enum class for storing keyboard `keyID` and `scancode` constants that are not present in the `win32con` module.
    # ---
    # Naming Scheme:
    #     `AS`: Ascii value.
    #     `VK`: Virtual keyID.
    #     `SC`: Scancode
    # ---
    # Notes:
    #     - From what I have seen, keys may send different `Ascii` values depending on the pressed modifier(s), but they send the same `keyID` and `scancode`.
    #         - If you need a code that is independent of the pressed modifiers, use `keyID`.
    #         - If you need a code that may have different values, use `Ascii` (ex, Ascii of: `=` is `61`, `+` (Shift + '=') is `41`.)
    #     - `KeyID` and `scancode` constants are stored only one time for each physical key.
    #         - These constants are named with respect to the sent key when the corresponding physical key is pressed with no modifiers.
    #         - Letter keys are named with the uppercase letter, not the lowercase letters unlike what is mentioned above.
    #     - Capital letters (Shift + letter key) have Ascii values equal to their VK values. As such, Only lowercase letters Ascii values are stored in this class.
    # """
    
    # Letter keys - Uppercase letters
    AS_a = 97, VK_A = 65,  SC_A = 30
    AS_b = 98, VK_B = 66,  SC_B = 48
    AS_c = 99, VK_C = 67,  SC_C = 46
    AS_d = 100, VK_D = 68,  SC_D = 32
    AS_e = 101, VK_E = 69,  SC_E = 18
    AS_f = 102, VK_F = 70,  SC_F = 33
    AS_g = 103, VK_G = 71,  SC_G = 34
    AS_h = 104, VK_H = 72,  SC_H = 35
    AS_i = 105, VK_I = 73,  SC_I = 23
    AS_j = 106, VK_J = 74,  SC_J = 36
    AS_k = 107, VK_K = 75,  SC_K = 37
    AS_l = 108, VK_L = 76,  SC_L = 38
    AS_m = 109, VK_M = 77,  SC_M = 50
    AS_n = 110, VK_N = 78,  SC_N = 49
    AS_o = 111, VK_O = 79,  SC_O = 24
    AS_p = 112, VK_P = 80,  SC_P = 25
    AS_q = 113, VK_Q = 81,  SC_Q = 16
    AS_r = 114, VK_R = 82,  SC_R = 19
    AS_s = 115, VK_S = 83,  SC_S = 31
    AS_t = 116, VK_T = 84,  SC_T = 20
    AS_u = 117, VK_U = 85,  SC_U = 22
    AS_v = 118, VK_V = 86,  SC_V = 47
    AS_w = 119, VK_W = 87,  SC_W = 17
    AS_x = 120, VK_X = 88,  SC_X = 45
    AS_y = 121, VK_Y = 89,  SC_Y = 21
    AS_z = 122, VK_Z = 90,  SC_Z = 44
    
    # Number keys
    VK_0 = 48,  SC_0 = 11
    VK_1 = 49,  SC_1 = 2
    VK_2 = 50,  SC_2 = 3
    VK_3 = 51,  SC_3 = 4
    VK_4 = 52,  SC_4 = 5
    VK_5 = 53,  SC_5 = 6
    VK_6 = 54,  SC_6 = 7
    VK_7 = 55,  SC_7 = 8
    VK_8 = 56,  SC_8 = 9
    VK_9 = 57,  SC_9 = 10
    
    # Symbol keys
    AS_EXCLAM               = 33
    AS_DOUBLE_QUOTES        = 34,   VK_DOUBLE_QUOTES = 222,       SC_DOUBLE_QUOTES = 40
    AS_HASH                 = 35
    AS_DOLLAR               = 36
    AS_PERCENT              = 37
    AS_AMPERSAND            = 38
    AS_SINGLE_QUOTE         = 39
    AS_OPEN_PAREN           = 40
    AS_CLOSE_PAREN          = 41
    AS_ASTERISK             = 42
    AS_PLUS                 = 43
    AS_COMMA                = 44,   VK_COMMA  = 188,                SC_COMMA  = 51
    AS_MINUS                = 45,   VK_MINUS  = 189,                SC_MINUS  = 12
    AS_PERIOD               = 46,   VK_PERIOD = 190,                SC_PERIOD = 52
    AS_SLASH                = 47,   VK_SLASH  = 191,                SC_SLASH  = 53
    
    AS_COLON                = 58
    AS_SEMICOLON            = 59,   VK_SEMICOLON = 186,             SC_SEMICOLON = 39
    AS_LESS_THAN            = 60
    AS_EQUALS               = 61,   VK_EQUALS = 187,                SC_EQUALS = 13
    AS_GREATER_THAN         = 62
    AS_QUESTION_MARK        = 63
    AS_AT                   = 64
    
    AS_OPEN_SQUARE_BRACKET  = 91,   VK_OPEN_SQUARE_BRACKET = 219,   SC_OPEN_SQUARE_BRACKET = 26
    AS_BACKSLASH            = 92,   VK_BACKSLASH = 220,             SC_BACKSLASH = 43
    AS_CLOSE_SQUARE_BRACKET = 93,   VK_CLOSE_SQUARE_BRACKET = 221,  SC_CLOSE_SQUARE_BRACKET = 27
    AS_CARET                = 94
    AS_UNDERSCORE           = 95
    AS_BACKTICK             = 96,   VK_BACKTICK = 192,              SC_BACKTICK = 41 # '`'
    
    AS_OPEN_CURLY_BRACE     = 123
    AS_PIPE                 = 124
    AS_CLOSE_CURLY_BRACE    = 125
    AS_TILDE                = 126
    AS_OEM_102_CTRL         = 28,   VK_AS_OEM_102 = 226,            SC_OEM_102 = 86 # '\' in European keyboards (between LShift and Z).
    
    # Miscellaneous keys
    SC_RETURN      = 28 # Enter
    SC_BACK        = 14 # Backspace
    SC_MENU        = 56 # 'LMenu' and 'RMenu'
    SC_HOME        = 71
    SC_UP          = 72
    SC_RIGHT       = 77
    SC_DOWN        = 80
    SC_LEFT        = 75
    SC_VOLUME_UP   = 48 # Make sure that this doesn't conflict with `KB_Con.SC_B` as both have the same value.
    SC_VOLUME_DOWN = 46


cdef static_class(cls):
    """Class decorator that turns a class into a static class."""
    
    class _StaticClass(type):
        def __call__(cls, *args, **kwargs):
            raise TypeError("This is a static class, it cannot be instantiated.")
    
    return _StaticClass(cls.__name__, (cls,), {})


@static_class
class Management:
    """A static data class for storing variables and functions used for managing to the script."""
    
    # Counts the number of times a key has been pressed (mod 10k).
    counter = 0
    
    # For suppressing terminal output. Defaults to True.
    silent = True
    
    # For suppressing all keyboard keys. Defaults to False.
    suppress_all_keys = False
    
    # Used as indicating the the script is still running. Set it to begin the termination process. Defaults to False.
    terminate_script = False
    
    @staticmethod
    def LogUncaughtExceptions(exc_type, exc_value, exc_traceback) -> int:
        """Logs uncaught exceptions to the console and displays an error message with the exception traceback."""
        
        message = f"{exc_type.__name__}: {exc_value}\n  "
        message += ''.join(format_tb(exc_traceback)).strip()
        print(f'\nUncaught exception: """{message}"""', end="\n\n")
        
        return winHelper.ShowMessageBox(message)


@static_class
class WindowHouse:
    """A static data class for storing window class names and their corresponding window handles."""
    
    # Stores the class names and the corresponding window handle for some progarms.
    classNames: dict[str, int] = {"MediaPlayerClassicW": None}
    
    # Stores the addresses of the 10 most recently closed windows explorers.
    closedExplorers: deque[str] = deque(maxlen=10)
    
    @staticmethod
    def GetHandleByClassName(className: str) -> int:
        """Returns the window handle of the specified class name from the `WindowHouse.classNames` dict."""
        
        return WindowHouse.classNames.get(className, None) or 0
    
    @staticmethod
    def SetHandleByClassName(className: str, value: int) -> None:
        """Assigns the given window handle to the specified class name in the `WindowHouse.classNames` dict."""
        
        WindowHouse.classNames[className] = value
    
    @staticmethod
    def RememberActiveProcessTitle(fg_hwnd=0) -> None:
        """Stores the title of the active window into the `closedExplorers` variable.
        The title of a windows explorer window is the address of the opened directory."""
        
        cdef str explorerAddress = win32gui.GetWindowText(fg_hwnd or win32gui.GetForegroundWindow())
        
        if explorerAddress in WindowHouse.closedExplorers:
            WindowHouse.closedExplorers.remove(explorerAddress)
        
        WindowHouse.closedExplorers.append(explorerAddress)


@static_class
class ControllerHouse:
    """A static data class for storing information and functions for managing and controlling keyboard."""
    
    # An int packing the states of the keyboard modifier keys (pressed or not). Each of the least significant 14 bits represent a single modifier key:
    # 0b00_0000_0000 => CTRL = 8192 | LCTRL = 4096 | RCTRL = 2048 | SHIFT = 1024 | LSHIFT = 512 | RSHIFT = 256 | ALT = 128 | LALT = 64 | RALT = 32 | WIN = 16 | LWIN = 8 | RWIN = 4 | FN = 2 | BACKTICK = 1
    modifiers = 0
    
    # Masks for extracting individual keys from the `modifiers` packed int.
    CTRL     = 0b10000000000000 # 1 << 13 = 8192
    LCTRL    = 0b1000000000000  # 1 << 12 = 4096
    RCTRL    = 0b100000000000   # 1 << 11 = 2048
    SHIFT    = 0b10000000000    # 1 << 10 = 1024
    LSHIFT   = 0b1000000000     # 1 << 9  = 512
    RSHIFT   = 0b100000000      # 1 << 8  = 256
    ALT      = 0b10000000       # 1 << 7  = 128
    LALT     = 0b1000000        # 1 << 6  = 64
    RALT     = 0b100000         # 1 << 5  = 32
    WIN      = 0b10000          # 1 << 4  = 16
    LWIN     = 0b1000           # 1 << 3  = 8
    RWIN     = 0b100            # 1 << 2  = 4
    FN       = 0b10             # 1 << 1  = 2
    BACKTICK = 0b1              # 1 << 0  = 1
    
    # Composite Modifier keys masks
    CTRL_ALT_FN_WIN = 0b10000010010010 # 8338
    CTRL_ALT_WIN    = 0b10000010010000 # 8336
    CTRL_FN_WIN     = 0b10000000010010 # 8210
    CTRL_SHIFT      = 0b10010000000000 # 9216
    CTRL_FN         = 0b10000000000010 # 8194
    CTRL_WIN        = 0b10000000001100 # 8204
    LCTRL_RCTRL     = 0b01100000000000 # 6144
    SHIFT_FN        = 0b00010000000010 # 1026
    LSHIFT_RSHIFT   = 0b00001100000000 # 768
    ALT_FN          = 0b00000010000010 # 130
    LALT_RALT       = 0b00000001100000 # 96
    FN_WIN          = 0b00000000010010 # 18
    LWIN_RWIN       = 0b00000000001100 # 12
    
    # An int packing the states of the keyboard lock keys (on or off).
    locks = (win32api.GetKeyState(win32con.VK_CAPITAL) << 2) | \
            (win32api.GetKeyState(win32con.VK_SCROLL)  << 1) | \
            win32api.GetKeyState(win32con.VK_NUMLOCK)
    
    # Masks for extracting individual lock keys from the `locks` packed int.
    CAPITAL = 0b100
    SCROLL = 0b10
    NUMLOCK = 0b1
    
    # Holds the pressed character keys for the key expansion events.
    pressed_chars = ""
    
    # A dictionary of abbreviations and their corresponding path address.
    locations = configurations.locations
    
    # A dictionary of abbreviations and their corresponding expansion.
    abbreviations = configurations.abbreviations
    
    # https://nitratine.net/blog/post/simulate-keypresses-in-python/
    pynput_kb = kbController()
    pynput_mouse = mController()
    keyboard_send = keyboard.send
    keyboard_write = keyboard.write
    
    def UpdateModifiers_KeyDown(event: KeyboardEvent) -> None:
        """Updates the `modifiers` packed int with the current state of the modifier keys when a key is pressed."""
        
        ControllerHouse.modifiers |= (
                            (event.KeyID == win32con.VK_LCONTROL) << 12 | # LCTRL
                            (event.KeyID == win32con.VK_RCONTROL) << 11 | # RCTRL
                            (event.KeyID == win32con.VK_LSHIFT)   << 9  | # LSHIFT
                            (event.KeyID == win32con.VK_RSHIFT)   << 8  | # RSHIFT
                            (event.KeyID == win32con.VK_LMENU)    << 6  | # LALT
                            (event.KeyID == win32con.VK_RMENU)    << 5  | # RALT
                            (event.KeyID == win32con.VK_LWIN)     << 3  | # LWIN
                            (event.KeyID == win32con.VK_RWIN)     << 2  | # RWIN
                            (event.KeyID == 255)                  << 1  | # FN
                            (event.KeyID == KB_Con.VK_BACKTICK)           # BACKTICK
        )
        
        ControllerHouse.modifiers |= (
                            ((ControllerHouse.modifiers & ControllerHouse.LCTRL_RCTRL)   != 0) << 13 | # CTRL
                            ((ControllerHouse.modifiers & ControllerHouse.LSHIFT_RSHIFT) != 0) << 10 | # SHIFT
                            ((ControllerHouse.modifiers & ControllerHouse.LALT_RALT)     != 0) << 7  | # ALT
                            ((ControllerHouse.modifiers & ControllerHouse.LWIN_RWIN)     != 0) << 4    # WIM
        )
    
    def UpdateModifiers_KeyUp(event: KeyboardEvent) -> None:
        """Updates the `modifiers` packed int with the current state of the modifier keys when a key is released."""
        
        ControllerHouse.modifiers &= ~(
                            (1 << 13) | (1 << 10) | (1 << 7) | (1 << 4) | # Reseeting CTRL, SHIFT, ALT, WIN
                            (event.KeyID == win32con.VK_LCONTROL) << 12 | # LCTRL
                            (event.KeyID == win32con.VK_RCONTROL) << 11 | # RCTRL
                            (event.KeyID == win32con.VK_LSHIFT)   << 9  | # LSHIFT
                            (event.KeyID == win32con.VK_RSHIFT)   << 8  | # RSHIFT
                            (event.KeyID == win32con.VK_LMENU)    << 6  | # LALT
                            (event.KeyID == win32con.VK_RMENU)    << 5  | # RALT
                            (event.KeyID == win32con.VK_LWIN)     << 3  | # LWIN
                            (event.KeyID == win32con.VK_RWIN)     << 2  | # RWIN
                            (event.KeyID == 255)                  << 1  | # FN
                            (event.KeyID == KB_Con.VK_BACKTICK)           # BACKTICK
        )
        
        ControllerHouse.modifiers &= ~( # Reseeting CTRL, SHIFT, ALT, WIN
                            ((ControllerHouse.modifiers & ControllerHouse.LCTRL_RCTRL)   != 0) << 13 | # CTRL
                            ((ControllerHouse.modifiers & ControllerHouse.LSHIFT_RSHIFT) != 0) << 10 | # SHIFT
                            ((ControllerHouse.modifiers & ControllerHouse.LALT_RALT)     != 0) << 7  | # ALT
                            ((ControllerHouse.modifiers & ControllerHouse.LWIN_RWIN)     != 0) << 4    # WIM
        )
    
    @staticmethod
    def UpdateLocks(event: KeyboardEvent) -> None:
        """Updates the `locks` packed int with the current state of the lock keys when a key is pressed."""
        
        ControllerHouse.locks ^= (
                            (event.KeyID == win32con.VK_CAPITAL) << 2 | # CAPITAL
                            (event.KeyID == win32con.VK_SCROLL)  << 1 | # SCROLL
                            (event.KeyID == win32con.VK_NUMLOCK)        # NUMLOCK
        )
    
    @staticmethod
    def SendMouseScroll(dist: int) -> None:
        """Sends a mouse scroll event with the given distance."""
        
        keyboard.press("ctrl")
        ControllerHouse.pynput_mouse.scroll(0, dist)
        keyboard.release("ctrl")
    
    @staticmethod
    def PrintModifiers() -> None:
        """Prints the states of the modifier keys after extracting them from the packed int `modifiers`."""
        
        print(f"CTRL={bool(ControllerHouse.modifiers & ControllerHouse.CTRL)}", end=", ")
        print(f"SHIFT={bool(ControllerHouse.modifiers & ControllerHouse.SHIFT)}", end=", ")
        print(f"ALT={bool(ControllerHouse.modifiers & ControllerHouse.ALT)}", end=", ")
        print(f"WIN={bool(ControllerHouse.modifiers & ControllerHouse.WIN)}", end=", ")
        print(f"FN={bool(ControllerHouse.modifiers & ControllerHouse.FN)}", end=", ")
        print(f"BACKTICK={bool(ControllerHouse.modifiers & ControllerHouse.BACKTICK)}", end=" | ")
    
    @staticmethod
    def PrintLockKeys() -> None:
        """Prints the states of the lock keys after extracting them from the packed int `locks`."""
        
        print(f"CAPSLOCK={bool(ControllerHouse.locks & ControllerHouse.CAPITAL)}", end=", ")
        print(f"SCROLL={bool(ControllerHouse.locks & ControllerHouse.SCROLL)}", end=", ")
        print(f"NUMLOCK={bool(ControllerHouse.locks & ControllerHouse.NUMLOCK)}")


@static_class
class ShellAutomationObjectWrapper:
    """Thread-safe wrapper class for accessing an Automation object in a multithreaded environment."""
    # The wrapper object acquires a lock before accessing the Automation object, ensuring that only one thread can access it at a time.
    # This can help prevent problems that can occur when multiple threads try to access the Automation object concurrently.
    # If two or more threads tried to access an automation object wrapper, only one would be able to acquire the lock to the automation object at a time.
    # The other threads would be blocked until the lock is released by the thread that currently holds it.
    # When a thread lock object is used in a `with` statement, the lock is released when the `with` block ends.
    # The lock is automatically acquired at the beginning of the block and released when the block ends.
    
    # An explorer Automation object.
    explorer = Dispatch("Shell.Application")
    
    # A lock object used to ensure that only one thread can access the Automation object at a time.
    _lock = threading.Lock()
    
    @staticmethod
    def __getattr__(name: str):
        # Acquire lock before accessing the Automation object
        with ShellAutomationObjectWrapper._lock:
            return getattr(ShellAutomationObjectWrapper.explorer, name)


# Source: https://stackoverflow.com/questions/6552097/threading-how-to-get-parent-id-name
class PThread(threading.Thread):
    """An extension of threading.Thread. Stores some relevant information about the threads."""
    
    # Used in the Throttle decorator to make it thread-safe.
    # A lock object used to ensure that only one thread can access the critical section in the Throttle decorator.
    throttle_lock = threading.Lock()
    
    # A queue used for message passing between threads.
    msgQueue: Queue[bool] = queue.Queue()
    
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.parent = threading.current_thread()
        self.coInitializeCalled = False
    
    # Propagating exceptions from a thread and showing an error message.
    def run(self):
        cdef str error_msg, class_name
        
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            error_msg = format_exc()
            class_name = str(type(e)).split("'")[1]
            print(f'Warning! An error occurred in thread {self.name}.\nClass: {class_name}\nValue: {str(e)}\n\n"""\n{error_msg}"""')
            winHelper.ShowMessageBox(error_msg)
            
            # Management.LogUncaughtExceptions(*sys.exc_info())
            # logging.error(f"Warning! An error occurred in thread {self.name}. Traceback:{str(e)}", exc_info=True)
    
    @staticmethod
    def InMainThread() -> bool:
        """Returns where the current thread is the main thread for the current process."""
        
        return threading.get_ident() == threading.main_thread().ident
    
    @staticmethod
    def GetParentThread() -> int:
        """
        Description:
            Returns the parent thread id of the current thread.
        ---
        Returns:
            - `int > 0` (the parent thread id): if the current thread is not the main thread.
            - `0`: if it was the main thread.
            - `-1`: if the parent thread is unknown (i.e., the current thread was not created using this class).
        """
        
        if threading.current_thread().name != "MainThread":
            if hasattr(threading.current_thread(), 'parent'):
                return threading.current_thread().parent.ident
            else:
                return -1 # Unknown. The current thread does not have a `parent` property.
        else:
            return 0 # "MainThread"
    
    @staticmethod
    def CoInitialize() -> bool:
        """Initializes the COM library for the current thread if it was not previously initialized."""
        
        if not PThread.InMainThread() and not threading.current_thread().coInitializeCalled:
            print(f"CoInitialize called from: {threading.current_thread().name}")
            threading.current_thread().coInitializeCalled = True
            pythoncom.CoInitialize()
            return True
        return False
    
    @staticmethod
    def CoUninitialize() -> None:
        """Un-initializes the COM library for the current thread if `initializer_called` is True."""
        if threading.current_thread().coInitializeCalled:
            print(f"CoUninitialize called from: {threading.current_thread().name}")
            pythoncom.CoUninitialize()
            threading.current_thread().coInitializeCalled = False
    
    # Source: https://github.com/salesforce/decorator-operations/blob/master/decoratorOperations/throttle_functions/throttle.py
    # For a comparison between Throttling and Debouncing: https://stackoverflow.com/questions/25991367/difference-between-throttling-and-debouncing-a-function
    @staticmethod
    def Throttle(wait_time: float):
        """
        Description:
            Decorator function that ensures that a wrapped function is called only once in each time slot.
        """
        
        def decorator(function):
            def throttled(*args, **kwargs):
                def call_function():
                    return function(*args, **kwargs)
                
                if PThread.throttle_lock.acquire(blocking = False):
                    if time() - throttled._last_time_called >= wait_time:
                        call_function()
                        throttled._last_time_called = time()
                    PThread.throttle_lock.release()
                
                else: # Lock is already acquired by another thread, so return without calling the wrapped function
                    return
            
            throttled._last_time_called = 0
            
            return throttled
        
        return decorator
    
    # Source: https://github.com/salesforce/decorator-operations/blob/master/decoratorOperations/debounce_functions/debounce.py
    @staticmethod
    def Debounce(wait_time: float):
        """
        Decorator that will debounce a function so that it is called after `wait_time` seconds.
        If the decorated function is called multiple times within a time slot, it will debounce
        (wait for a new time slot from the last call).
        
        If no calls arrive after wait_time seconds from the last call, then execute the last call.
        """
        
        def decorator(function):
            def debounced(*args, **kwargs):
                def call_function():
                    debounced._timer = None
                    return function(*args, **kwargs)
                
                if debounced._timer is not None:
                    debounced._timer.cancel()
                
                debounced._timer = threading.Timer(wait_time, call_function)
                debounced._timer.start()
            
            debounced._timer = None
            return debounced
        
        return decorator


cpdef str ReadFromClipboard(int CF=win32clipboard.CF_TEXT): # CF: Clipboard format.
    """Reads the top of the clipboard if it was the same type as the specified."""
    
    win32clipboard.OpenClipboard()
    if win32clipboard.IsClipboardFormatAvailable(CF):
        clipboard_data = win32clipboard.GetClipboardData()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
    else:
        return ""
    
    return clipboard_data


cpdef void SendToClipboard(data, int CF=win32clipboard.CF_UNICODETEXT):
    """Copies the given data to the clipboard."""
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(CF, data)
    win32clipboard.CloseClipboard()
