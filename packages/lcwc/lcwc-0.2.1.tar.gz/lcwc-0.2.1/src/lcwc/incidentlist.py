import asyncio
import aiohttp
from lcwc import feedclient
from lcwc.category import IncidentCategory
from lcwc.client import Client
from lcwc.incident import Incident

class IncidentList:

    def __init__(self) -> None:
        self.backing_store = {}
        self.client = feedclient.IncidentFeedClient()

    async def get_incidents(self, session: aiohttp.ClientSession = None) -> list[feedclient.FeedIncident]:
        incidents = await self.client.get_incidents()

        for incident in incidents:
            self.backing_store[incident.id] = incident

        




    