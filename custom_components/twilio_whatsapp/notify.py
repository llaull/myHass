"""
Twilio Whatsapp platform for notify component.

For more details about this platform, please refer to the documentation at
https://en.techblog.co.il/2019/01/24/easily-send-home-assistant-notifications-using-whatsapp/
"""
import logging

import voluptuous as vol

# from homeassistant.components.twilio import DATA_TWILIO
import homeassistant.helpers.config_validation as cv
from homeassistant.components.notify import (
    ATTR_TARGET, PLATFORM_SCHEMA, BaseNotificationService)

_LOGGER = logging.getLogger(__name__)
# DEPENDENCIES = ["twilio"]

CONF_FROM_NUMBER = "from_number"
CONF_ACCOUNT_SID = "account_sid"
CONF_AUTH_TOKEN = "auth_token"

DOMAIN = "twilio"
DATA_TWILIO = DOMAIN

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_FROM_NUMBER): vol.All(cv.string),
        vol.Required(CONF_ACCOUNT_SID): vol.All(cv.string),
        vol.Required(CONF_AUTH_TOKEN): vol.All(cv.string),
    }
)

def get_service(hass, config, discovery_info=None):
    """Get the Twilio Whatsapp notification service."""
    from twilio.rest import Client

    hass.data[DATA_TWILIO] = Client(
        config[CONF_ACCOUNT_SID], config[CONF_AUTH_TOKEN]
    )

    return TwilioWhatsappNotificationService(
        hass.data[DATA_TWILIO], config[CONF_FROM_NUMBER])


class TwilioWhatsappNotificationService(BaseNotificationService):
    """Implement the notification service for the Twilio Whatsapp service."""

    def __init__(self, twilio_client, from_number):
        """Initialize the service."""
        self.client = twilio_client
        self.from_number = from_number

    def send_message(self, message="", **kwargs):
        """Send Whatsapp to specified target user cell."""
        targets = kwargs.get(ATTR_TARGET)

        if not targets:
            _LOGGER.info("At least 1 target is required")
            return

        for target in targets:
            self.client.messages.create(
                to='whatsapp:'+target, body=message, from_=self.from_number)
