from dataclasses import dataclass
from typing import Optional

from bovine.types import Visibility

from .activity_factory import ActivityFactory
from .object_factory import ObjectFactory
from .ordered_collection_builder import OrderedCollectionBuilder
from .ordered_collection_page_builder import OrderedCollectionPageBuilder


def build_ordered_collection(url: str):
    return OrderedCollectionBuilder(url)


def build_ordered_collection_page(url: str, part_of: str):
    return OrderedCollectionPageBuilder(url, part_of)


def factories_for_actor_object(actor_object):
    return ActivityFactory(actor_object), ObjectFactory(actor_information=actor_object)


@dataclass
class Actor:
    """Actor class represents the basic ActivityStreams actor."""

    id: str
    type: str = "Person"
    name: Optional[str] = None
    preferred_username: Optional[str] = None
    inbox: Optional[str] = None
    outbox: Optional[str] = None
    followers: Optional[str] = None
    following: Optional[str] = None
    public_key: Optional[str] = None
    public_key_name: Optional[str] = None
    event_source: Optional[str] = None
    proxy_url: Optional[str] = None

    def build(self, visibility=Visibility.PUBLIC):
        """Creates the json-ld representation of the actor."""
        result = {
            "@context": self._build_context(),
            "id": self.id,
            "type": self.type,
            **self._build_public_key(),
            **self._build_endpoints(visibility=visibility),
        }

        if self.preferred_username:
            result["preferredUsername"] = self.preferred_username

        if visibility == Visibility.WEB:
            return result

        if self.name:
            result["name"] = self.name
        elif self.preferred_username:
            result["name"] = self.preferred_username

        return result

    def _build_context(self):
        if self.public_key:
            return [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
            ]

        return "https://www.w3.org/ns/activitystreams"

    def _build_public_key(self):
        if self.public_key:
            return {
                "publicKey": {
                    "id": f"{self.id}#{self.public_key_name}",
                    "owner": self.id,
                    "publicKeyPem": self.public_key,
                }
            }
        return {}

    def _build_endpoints(self, visibility):
        result = {}

        if visibility == Visibility.WEB:
            return result

        if self.inbox:
            result["inbox"] = self.inbox
        else:
            result["inbox"] = self.id

        if self.outbox:
            result["outbox"] = self.outbox
        else:
            result["outbox"] = self.id

        if visibility != Visibility.OWNER:
            return result

        endpoints = self._build_user_endpoints()
        if endpoints:
            result["endpoints"] = endpoints

        if self.followers:
            result["followers"] = self.followers
        if self.following:
            result["following"] = self.following

        return result

    def _build_user_endpoints(self):
        endpoints = {}
        if self.event_source:
            endpoints["eventSource"] = self.event_source
        if self.proxy_url:
            endpoints["proxyUrl"] = self.proxy_url
        return endpoints
