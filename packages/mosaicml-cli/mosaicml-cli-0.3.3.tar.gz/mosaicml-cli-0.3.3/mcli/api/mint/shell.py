"""
connection engine to MINT
"""

from __future__ import annotations

import asyncio
import logging
import select
import ssl
import sys
from typing import Dict, Optional

from websockets.client import WebSocketClientProtocol
from websockets.client import connect as ws_connect
from websockets.exceptions import ConnectionClosedError, InvalidStatusCode

from mcli.api.exceptions import MintException
from mcli.api.mint import tty
from mcli.utils.utils_logging import FAIL, WARN

logger = logging.getLogger(__name__)


class MintShell:
    """Interactive shell into MINT (Mosaic Interactive service)

    Args:
        api_key: The user's API key. If not specified, the value of the $MOSAICML_API_KEY
            environment variable will be used. If that does not exist, the value in the
            user's config file will be used. The key is authenticated in MINT through MAPI
        endpoint: The MINT URL to hit for all requests. If not specified, the value of the
            $MOSAICML_MINT_ENDPOINT environment variable will be used. If that does not
            exist, the default setting will be used.
    """
    api_key: str
    endpoint: str

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        self._load_from_environment(api_key, endpoint)

        self._loop = asyncio.get_event_loop_policy().get_event_loop()

    def _load_from_environment(self, api_key: Optional[str] = None, endpoint: Optional[str] = None) -> None:
        # pylint: disable-next=import-outside-toplevel
        from mcli import config
        conf = config.MCLIConfig.load_config(safe=True)
        if api_key is None:
            api_key = conf.api_key

        if not api_key:
            api_key = ''

        self.api_key = api_key

        if endpoint is None:
            endpoint = conf.mint_endpoint
        self.endpoint = endpoint

    @property
    def header(self) -> Dict[str, str]:
        return {"Authorization": self.api_key}

    async def _connect(self, uri: str):
        """
        Connection helper

        Given a uri, connects to a websocket and streams data in the terminal shell
        """
        # setup tty and save old settings. if settings aren't reset, the terminal will likely become non-responsive

        shell_tty = tty.TTY()

        def get_char(timeout=None):
            """
            gets a single character from stdin
            """
            try:
                # Wait until one or more file descriptors are ready for some kind of I/O.
                rw, _, _ = select.select([shell_tty.fd], [], [], timeout)
            except select.error:
                return  # Stdin not readable, some OSError. Don't return a character

            if rw:
                return sys.stdin.read(1)

        async def read_stdin(ws: WebSocketClientProtocol):
            """
            reads the stdin and write to the websocket
            """
            while True:
                msg = await self._loop.run_in_executor(None, get_char)
                if msg:
                    await ws.send(msg)

        async def write_stdout(ws: WebSocketClientProtocol):
            """
            reads from the websocket and writes to stdout
            """
            while True:
                msg = await ws.recv()
                if msg:
                    sys.stdout.write(str(msg))
                    sys.stdout.flush()

        connect_params = {"uri": uri, "extra_headers": self.header}
        if uri.startswith("wss:"):
            connect_params["ssl"] = ssl.SSLContext(ssl.PROTOCOL_TLS)

        try:
            async with ws_connect(**connect_params) as ws:
                # Run the write and reads forever until the connection is terminated
                await asyncio.gather(write_stdout(ws), read_stdin(ws))
        except ConnectionClosedError as e:
            raise MintException("MINT Shell unexpectedly closed") from e
        except OSError as e:
            if "Errno 61" in str(e):  # https://bugs.python.org/issue29980
                e = MintException(f'Could not connect to {self.endpoint}')
            raise e
        except InvalidStatusCode as e:
            raise MintException(f"Failed to run mint websocket with status code {e.status_code}") from e
        finally:
            shell_tty.reset()

    def connect(self, run_name: str, rank: int = 0) -> int:
        """
        Connect to a run using the MINT Shell

        args:
            run_name (str): Name of run to connect to
            rank (int): Integer of node rank. By default, selects the first.
        """
        if not tty.TTY_SUPPORTED:
            logger.warning(f'{WARN} MCLI Connect does not currently support TTY for your OS')

        uri = f"{self.endpoint}/{run_name}/{rank}"

        try:
            self._loop.run_until_complete(self._connect(uri))
        except MintException as e:
            logger.error(f'{FAIL} {e}')
            return 1

        return 0
