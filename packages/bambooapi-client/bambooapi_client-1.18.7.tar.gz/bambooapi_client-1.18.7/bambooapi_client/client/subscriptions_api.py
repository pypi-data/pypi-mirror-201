"""Sites are physical locations where flexibility devices are deployed."""
import typing as tp
from typing import List, Optional

from bambooapi_client.openapi.apis import SubscriptionApi as _SubscriptionApi
from bambooapi_client.openapi.models import (
    EventTypeEnum,
    MediumEnum,
    Subscription,
    User,
)


class SubscriptionsApi(object):
    """Implementation for '/v1/sites' endpoints."""

    def __init__(self, bambooapi_client):
        """Initialize defaults."""
        self._bambooapi_client = bambooapi_client
        self._api_instance = _SubscriptionApi(bambooapi_client.api_client)

    def get_users_subscribed_to_event_type(
        self,
        event_type: EventTypeEnum,
        site_id: int,
    ) -> tp.List[User]:
        """Get all users subscribed to an event type of a site."""
        return self._api_instance.get_users_subscribed_to_event_type(
            event_type=event_type,
            site_id=site_id,
        )

    def create_or_update_subscription(
        self,
        user_id: int,
        event_type: EventTypeEnum,
        medium: MediumEnum,
        site_ids: Optional[List[int]] = None
    ) -> Subscription:
        """Create a subscription."""
        kwargs = {}
        if site_ids:
            kwargs.update(site_ids=site_ids)
        return self._api_instance.create_or_update_subscription(
            user_id=user_id,
            event_type=event_type,
            medium=medium,
            **kwargs,
        )

    def delete_subscription(
        self,
        user_id: int,
        event_type: EventTypeEnum,
        medium: MediumEnum,
        site_ids: Optional[List[int]] = None,
    ) -> Subscription:
        """Delete a subscription."""
        kwargs = {}
        if site_ids:
            kwargs.update(site_ids=site_ids)
        return self._api_instance.delete_subscription(
            user_id=user_id,
            event_type=event_type,
            medium=medium,
            **kwargs,
        )
