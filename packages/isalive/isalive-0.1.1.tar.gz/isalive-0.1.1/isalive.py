"""
"isalive is a small python script with no external dependencies
that runs a simple telegram bot to notify the status of http resources"

developed by saladware (04.04.2023)
"""

import importlib.metadata
import sys
import json
import time
import argparse
import pathlib
import logging
import urllib.request
import urllib.error
import urllib.parse


__version__ = importlib.metadata.version("isalive")

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="isalive.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def start_monitoring(
    bot_token: str,
    resources: list[dict[str, str]],
    chat_ids: list[int],
    interval_seconds: int,
):
    """check the resource status at a set interval and send notifications to
    chats via telegram bot if the status has been changed"""

    def send_notification(message: str, chat_id: int):
        params = {"chat_id": chat_id, "text": message, "parse_mode": "markdown"}
        send_message_url = (
            f"https://api.telegram.org/bot"
            f"{bot_token}"
            f"/sendMessage?{urllib.parse.urlencode(params)}"
        )
        with urllib.request.urlopen(send_message_url):
            logger.info("notification sent to chat %d", chat_id)

    logger.info("start monitoring")
    resource_status = dict.fromkeys([r["url"] for r in resources])
    names = {r["url"]: r["name"] for r in resources}
    while True:
        for url, status in resource_status.items():
            try:
                with urllib.request.urlopen(url):
                    ...
            except urllib.error.URLError:
                if status is None:
                    content = f"❌ resource [{names[url]}]({url}) is not available now!"
                    logger.error("resource %s is not available now", url)
                elif status:
                    content = f"❌ resource [{names[url]}]({url}) stopped working now!"
                    logger.error("resource %s stopped working now", url)
                else:
                    logger.warning("resource %s is still unavailable", url)
                    continue
                resource_status[url] = False
            else:
                if status is None:
                    content = f"✅ resource [{names[url]}]({url}) is available now!"
                    logger.info("resource %s is available", url)
                elif not status:
                    content = f"✅ resource [{names[url]}]({url}) is available again!"
                    logger.info("resource %s is available again", url)
                else:
                    logger.info("resource %s is still available", url)
                resource_status[url] = True
            for chat in chat_ids:
                send_notification(content, chat)
        time.sleep(interval_seconds)


def init_command(parser: argparse.ArgumentParser, args: argparse.Namespace):
    """'init' argparse command: create json configuration file from template"""

    path = pathlib.Path(args.file).absolute()
    if path.exists():
        parser.error(f"file with name '{path}' is already exists")
        parser.exit(1)
    template = {
        "bot_token": "",
        "interval_seconds": 3600,
        "chat_ids": [],
        "resources": [
            {"name": "google", "url": "https://google.com/"},
            {"name": "python", "url": "https://python.org/"},
        ],
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(template, file, ensure_ascii=False, indent=4)
    print("the configuration has been created! please fill it out")


def start_command(parser: argparse.ArgumentParser, args: argparse.Namespace):
    """'start' argparse command: validate configuration file and start monitoring"""

    path = pathlib.Path(args.file).absolute()
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        parser.error("json parsing error! wrong format!")
    except FileNotFoundError:
        parser.error(
            f"the configuration file named '{path}' does not exist. "
            f"please create it with the command 'isalive init -f {path}'"
        )
        parser.exit(1)
    try:
        bot_token = data["bot_token"]
        if bot_token == "":
            parser.error(
                "wrong configuration format! 'bot_token' field must have non-empty value!"
            )
        interval_seconds = int(data["interval_seconds"])
        chat_ids = list(map(int, data["chat_ids"]))
        resources = data["resources"]
        for resource in resources:
            if resource.get("name") is None or resource.get("url") is None:
                parser.error(
                    "wrong configuration format! resource object must have 'name' and 'url' fields"
                )
                parser.exit(1)
    except KeyError as error:
        parser.error(f"wrong configuration format! '{error.args[0]} is required!'")
        parser.exit(1)
    except (TypeError, ValueError):
        parser.error("wrong configuration format!")
        parser.exit(1)
    else:
        print('start monitoring')
        try:
            start_monitoring(
                bot_token=bot_token,
                resources=resources,
                chat_ids=chat_ids,
                interval_seconds=interval_seconds,
            )
        except KeyboardInterrupt:
            parser.exit(0, "monitoring is over")


def get_argument_parser() -> argparse.ArgumentParser:
    """build argument parser for command-line interface"""

    parser = argparse.ArgumentParser(
        prog="isalive",
        description="isalive is a small python script with no external dependencies "
        "that runs a simple telegram bot to notify the status of http resources",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit.",
    )

    subparsers = parser.add_subparsers(title="subcommands")

    init_parser = subparsers.add_parser(
        "init",
        help="create json configuration file from template",
    )
    init_parser.add_argument(
        "-f",
        "--file",
        help="set the name of the configuration file (default: config.json)",
        default="config.json",
        type=str,
    )
    init_parser.set_defaults(func=init_command)

    start_parser = subparsers.add_parser("start", help="start monitoring")
    start_parser.add_argument(
        "-f",
        "--file",
        help="configuration file name (default: config.json)",
        default="config.json",
        type=str,
    )
    start_parser.set_defaults(func=start_command)

    return parser


def main():
    """entry point. is called at program startup"""

    parser = get_argument_parser()
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        args.func(parser, args)


if __name__ == "__main__":
    main()
