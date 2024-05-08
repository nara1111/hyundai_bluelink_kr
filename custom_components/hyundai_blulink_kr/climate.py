"""Climate controls for Hyundai Connect Korea integration."""
from __future__ import annotations

import logging

from homeassistant.components.climate import ClimateEntity, ClimateEntityDescription
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HyundaiConnectKoreaDataUpdateCoordinator
from .entity import HyundaiConnectKoreaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up climate controls."""
    coordinator = hass.data[DOMAIN][config_entry.unique_id]
    async_add_entities([HyundaiConnectKoreaClimateControl(coordinator)])


class HyundaiConnectKoreaClimateControl(HyundaiConnectKoreaEntity, ClimateEntity):
    """Hyundai Connect Korea Car Climate Control."""

    def __init__(
        self,
        coordinator: HyundaiConnectKoreaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Climate Control."""
        super().__init__(coordinator)
        self.entity_description = ClimateEntityDescription(
            key="climate_control",
            icon="mdi:air-conditioner",
            name="Climate Control",
        )
        self._attr_unique_id = f"{DOMAIN}_climate_control"
        self._attr_name = "Climate Control"

    @property
    def temperature_unit(self) -> str:
        """Get the Temperature Unit."""
        return "°C"

    @property
    def current_temperature(self) -> float | None:
        """Get the current temperature."""
        return None

    @property
    def target_temperature(self) -> float | None:
        """Get the desired target temperature."""
        return None

    @property
    def target_temperature_step(self) -> float | None:
        """Get the step size for adjusting the target temperature."""
        return None

    @property
    def min_temp(self) -> float:
        """Get the minimum settable temperature."""
        return None

    @property
    def max_temp(self) -> float:
        """Get the maximum settable temperature."""
        return None

    @property
    def hvac_mode(self) -> str:
        """Get the configured climate control operation mode."""
        return HVACMode.OFF

    @property
    def hvac_action(self) -> str | None:
        """Get what the climate control is currently doing."""
        return None

    @property
    def hvac_modes(self) -> list[str]:
        """Supported climate control modes."""
        return [HVACMode.OFF]

    @property
    def supported_features(self) -> int:
        """Supported climate control features."""
        return ClimateEntityFeature.TARGET_TEMPERATURE

    async def async_set_hvac_mode(self, hvac_mode):
        """Set the operation mode of the climate control."""
        raise NotImplementedError("Hyundai Connect Korea does not support setting HVAC mode.")

    async def async_set_temperature(self, **kwargs):
        """Set the desired temperature."""
        raise NotImplementedError("Hyundai Connect Korea does not support setting temperature.")
