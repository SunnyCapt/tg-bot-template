from functools import wraps
from logging import getLogger

logger = getLogger("general")


def log(func):
    @wraps(func)
    def inner(update, context):
        logger.info(
            f"New {func.__name__} request from "
            f"{update.message.chat.username if hasattr(update.message.chat, 'username') else ''}"
            f"[{update.message.chat.id}]. "
            f"Source: {update.message.text}"
        )
        return func(update, context)

    return inner


class WrongCommand(Exception):
    pass


class WrongData(Exception):
    pass


class Views:
    @classmethod
    def render_start(cls):
        return f"<strong>You are gay</strong>"

    @classmethod
    def render_example_command(cls, data: dict = None):
        # TODO: make a decorator checking the presence of all necessary fields
        if data is None:
            raise WrongData("data is None")
        if "exampleField" not in data:
            raise WrongData("lacks: exampleField")
        return f"<strong>exampleField</strong>: {data.get('exampleField')}\n"

    @classmethod
    def render_help(cls):
        return "\n/example_command_&lt;number&gt; - <code>some kind of command with a variable part</code>\n" \
               "/help - <code>command information</code>"


class DataManager:
    @classmethod
    def get_example_command_data(cls, *args, **kwargs) -> dict:
        """
        Getting some data for example command
        :exception: WrongCommand if auth cookies is wrong
        """
        logger.info(f"Getting some data for example command; args={args}; kwargs={kwargs}")
        return {
            "exampleField": "example data"
        }
