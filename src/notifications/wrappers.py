import asyncio

from django.conf import settings

from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient


async def async_post_message(client: AsyncWebClient, channel: str, message: str):
    try:
        await client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as error:
        print(error.response)


class SlackWrapper:
    def __init__(self):
        self.client = AsyncWebClient(token=settings.SLACK_BOT_TOKEN)

    def post_message(self, channel: str, message: str):
        client = self.client
        asyncio.run(async_post_message(client, channel, message))
