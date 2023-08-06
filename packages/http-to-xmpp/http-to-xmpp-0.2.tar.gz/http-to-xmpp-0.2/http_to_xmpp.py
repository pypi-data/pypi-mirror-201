"""HTTP to XMPP gateway."""

import argparse
import asyncio
import os
import signal
import socket
import json
import sys

import aioxmpp
import aioxmpp.dispatcher
from aiohttp import web

__version__ = "0.2"


class XMPPClient:
    def __init__(self, jid, password):
        self.jid = jid
        self.password = password

    async def setup(self):
        self.hostname = socket.gethostname()
        self.client = aioxmpp.Client(
            aioxmpp.JID.fromstr(self.jid), aioxmpp.make_security_layer(self.password)
        )
        self.client.start()

    def send(self, msg: str, to: str):
        message = aioxmpp.Message(
            aioxmpp.MessageType.CHAT,
            to=aioxmpp.JID.fromstr(to),
        )
        message.body[None] = msg
        self.client.enqueue(message)


class HTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def setup(self):
        self.app = web.Application()
        self.app.add_routes([web.post("/", self.on_post)])
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()

    def forward_to(self, to_jid, xmpp_client):
        self.to_jid = to_jid
        self.xmpp_client = xmpp_client

    async def on_post(self, request):
        if not self.xmpp_client:
            return
        data = await request.text()
        try:
            self.xmpp_client.send(json.dumps(json.loads(data), indent=4), self.to_jid)
        except json.JSONDecodeError:
            self.xmpp_client.send(data, self.to_jid)
        return web.Response(text="")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--http-host", default="localhost")
    parser.add_argument("--http-port", default=1985, type=int)
    parser.add_argument(
        "--xmpp-jid",
        default=os.environ.get("XMPP_JID"),
        help="XMPP account of the bot."
        "if not given it's read from XMPP_JID environment variable.",
    )
    parser.add_argument(
        "--xmpp-password",
        default=os.environ.get("XMPP_PASSWORD"),
        help="XMPP password of the bot, "
        "if not given it's read from XMPP_PASSWORD environment variable.",
    )
    parser.add_argument(
        "--xmpp-dest-jid",
        default=os.environ.get("XMPP_DEST_JID"),
        help="XMPP account for the human to receive messages."
        "if not given it's read from XMPP_DEST_JID environment variable.",
    )
    args = parser.parse_args()
    for mandatory in "xmpp_password", "xmpp_jid", "xmpp_dest_jid":
        if not getattr(args, mandatory):
            print(
                f"No {mandatory.replace('_', ' ')} found neither via "
                f"--{mandatory.replace('_', '-')} neither via "
                f"{mandatory.upper()} env var.",
                file=sys.stderr,
            )
            sys.exit(1)
    return args


async def amain():
    args = parse_args()

    http_server = HTTPServer(args.http_host, args.http_port)
    await http_server.setup()

    xmpp_client = XMPPClient(args.xmpp_jid, args.xmpp_password)
    await xmpp_client.setup()

    http_server.forward_to(args.xmpp_dest_jid, xmpp_client)

    event = asyncio.Event()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, event.set)
    await event.wait()


def main():
    asyncio.run(amain())


if __name__ == "__main__":
    main()
