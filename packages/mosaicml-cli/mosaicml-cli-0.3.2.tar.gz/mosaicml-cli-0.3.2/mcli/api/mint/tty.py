"""tty for mint shell, defined by OS
"""

import os
import sys

TTY_SUPPORTED = False


class TTY:  # pyright: ignore
    """TTY to be used in the mint shell
    """

    fd: int = 0

    def __init__(self):
        self.fd = sys.stdin.fileno()

    def setup(self):
        """Setup the TTY
        """
        pass

    def reset(self):
        """Reset the TTY to the original settings
        """
        pass


if os.name != 'nt' and os.environ.get("SKIP_TTY", "false").lower() != "true":
    # termios and tty only supported for Unix versions that support Posix termios style tty I/O control
    import termios
    import tty

    TTY_SUPPORTED = True

    class TTY:  # pylint: disable=function-redefined
        """Unix TTY to be used in the mint shell
        """

        fd: int = 0
        old_settings = None

        def __init__(self):
            self.fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.fd)
            self.setup()

        def setup(self, when=termios.TCSAFLUSH):
            mode = termios.tcgetattr(self.fd)

            # Turn off echo input characters and stopping using canonical mode (default)
            # https://man7.org/linux/man-pages/man3/termios.3.html
            mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)

            # Set the mode
            termios.tcsetattr(self.fd, when, mode)

        def reset(self):
            if self.old_settings:
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
