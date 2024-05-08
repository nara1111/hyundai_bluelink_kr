"""Config flow for Hyundai Connect Korea integration."""
from __future__ import annotations

import hashlib
import logging
from typing import Any

from hyundai_kia_connect_api import Token, VehicleManager
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_REDIRECT_URI,
    DEFAULT_FORCE_REFRESH_INTERVAL,
    DEFAULT_NO_FORCE_REFRESH_HOUR_FINISH,
    DEFAULT_NO_FORCE_REFRESH_HOUR_START,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_CLIENT_ID): str,
        vol.Required(CONF_CLIENT_SECRET): str,
        vol.Required(CONF_REDIRECT_URI): str,
    }
)


async def validate_input(hass: HomeAssistant, user_input: dict[str, Any]) -> Token:
    """Validate the user input allows us to connect."""
    api = VehicleManager(
        client_id=user_input[CONF_CLIENT_ID],
        client_secret=user_input[CONF_CLIENT_SECRET],
        redirect_uri=user_input[CONF_REDIRECT_URI],
        region="Korea",
    )
    token: Token = await hass.async_add_executor_job(
        api.get_access_token, user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
    )

    if token is None:
        raise InvalidAuth

    return token


class HyundaiConnectKoreaOptionFlowHandler(config_entries.OptionsFlow):
    """Handle an option flow for Hyundai Connect Korea."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize option flow instance."""
        self.config_entry = config_entry
        self.schema = vol.Schema(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=15, max=999)),
            }
        )

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Handle options init setup."""
        if user_input is not None:
            return self.async_create_entry(
                title=self.config_entry.title, data=user_input
            )

        return self.async_show_form(step_id="init", data_schema=self.schema)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hyundai Connect Korea."""

    VERSION = 1
    reauth_entry: ConfigEntry | None = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """Initiate options flow instance."""
        return HyundaiConnectKoreaOptionFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            await validate_input(self.hass, user_input)
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            if self.reauth_entry is None:
                title = f"Hyundai Connect Korea {user_input[CONF_USERNAME]}"
                await self.async_set_unique_id(
                    hashlib.sha256(title.encode("utf-8")).hexdigest()
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=title, data=user_input)
            else:
                self.hass.config_entries.async_update_entry(
                    self.reauth_entry, data=user_input
                )
                await self.hass.config_entries.async_reload(self.reauth_entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_reauth(self, user_input=None):
        """Perform reauth upon an API authentication error."""
        self.reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        """Dialog that informs the user that reauth is required."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                data_schema=vol.Schema({}),
            )
        self._reauth_config = True
        return await self.async_step_user()


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
