"""Binary sensor for Hyundai Connect Korea integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Final

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HyundaiConnectKoreaDataUpdateCoordinator
from .entity import HyundaiConnectKoreaEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class HyundaiConnectKoreaBinarySensorEntityDescription(BinarySensorEntityDescription):
    """A class that describes custom binary sensor entities."""

    value_fn: Callable[[dict], bool] | None = None
    on_icon: str | None = None
    off_icon: str | None = None


SENSOR_DESCRIPTIONS: Final[tuple[HyundaiConnectKoreaBinarySensorEntityDescription, ...]] = (
    HyundaiConnectKoreaBinarySensorEntityDescription(
        key="fuel_warning",
        name="Fuel Low Level",
        value_fn=lambda data: data.get("fuel_warning", False),
        on_icon="mdi:gas-station-off",
        off_icon="mdi:gas-station",
    ),
    HyundaiConnectKoreaBinarySensorEntityDescription(
        key="tire_pressure_warning",
        name="Tire Pressure Warning",
        value_fn=lambda data: data.get("tire_pressure_warning", False),
        on_icon="mdi:car-tire-alert",
        off_icon="mdi:car-tire-alert",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    HyundaiConnectKoreaBinarySensorEntityDescription(
        key="lamp_wire_warning",
        name="Lamp Wire Warning",
        value_fn=lambda data: data.get("lamp_wire_warning", False),
        on_icon="mdi:alert",
        off_icon="mdi:alert",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    HyundaiConnectKoreaBinarySensorEntityDescription(
        key="smart_key_battery_warning",
        name="Smart Key Battery Warning",
        value_fn=lambda data: data.get("smart_key_battery_warning", False),
        on_icon="mdi:battery-alert",
        off_icon="mdi:battery",
        device_class=BinarySensorDeviceClass.BATTERY,
    ),
    HyundaiConnectKoreaBinarySensorEntityDescription(
        key="washer_fluid_warning",
        name="Washer Fluid Warning",
        value_fn=lambda data: data.get("washer_fluid_warning", False),
        on_icon="mdi:wiper-wash-alert",
        off_icon="mdi:wiper-wash",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    HyundaiConnectKoreaBinarySensorEntityDescription(
        key="brake_oil_warning",
        name="Brake Oil Warning",
        value_fn=lambda data: data.get("brake_oil_warning", False),
        on_icon="mdi:car-brake-alert",
        off_icon="mdi:car-brake-fluid-level",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    HyundaiConnectKoreaBinarySensorEntityDescription(
        key="engine_oil_warning",
        name="Engine Oil Warning",
        value_fn=lambda data: data.get("engine_oil_warning", False),
        on_icon="mdi:oil-level",
        off_icon="mdi:oil-level",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    HyundaiConnectKoreaBinarySensorEntityDescription(
        key="ev_charging_status",
        name="EV Charging Status",
        value_fn=lambda data: data.get("ev_charging_status", False),
        on_icon="mdi:ev-station",
        off_icon="mdi:ev-station",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary_sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.unique_id]
    entities: list[HyundaiConnectKoreaBinarySensor] = []
    for description in SENSOR_DESCRIPTIONS:
        entities.append(HyundaiConnectKoreaBinarySensor(coordinator, description))
    async_add_entities(entities)
    return True


class HyundaiConnectKoreaBinarySensor(BinarySensorEntity, HyundaiConnectKoreaEntity):
    """Hyundai Connect Korea binary sensor class."""

    def __init__(
        self,
        coordinator: HyundaiConnectKoreaDataUpdateCoordinator,
        description: HyundaiConnectKoreaBinarySensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description: HyundaiConnectKoreaBinarySensorEntityDescription = description
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_name = f"{description.name}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self.entity_description.value_fn is not None:
            return self.entity_description.value_fn(self.coordinator.data)
        return None

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        if (
            self.entity_description.on_icon == self.entity_description.off_icon
        ) is None:
            return BinarySensorEntity.icon
        return (
            self.entity_description.on_icon
            if self.is_on
            else self.entity_description.off_icon
        )
