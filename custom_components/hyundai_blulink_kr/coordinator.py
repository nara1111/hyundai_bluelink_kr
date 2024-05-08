"""Coordinator for Hyundai Connect Korea integration."""
from __future__ import annotations

from datetime import timedelta

import logging

from hyundai_kia_connect_api import VehicleManager
from hyundai_kia_connect_api.exceptions import *

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_REDIRECT_URI,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    ERROR_MESSAGES,
)

_LOGGER = logging.getLogger(__name__)


class HyundaiConnectKoreaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize."""
        self.vehicle_manager = VehicleManager(
            client_id=config_entry.data.get(CONF_CLIENT_ID),
            client_secret=config_entry.data.get(CONF_CLIENT_SECRET),
            redirect_uri=config_entry.data.get(CONF_REDIRECT_URI),
            region="Korea",
        )
        self.scan_interval: int = (
            config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL) * 60
        )
        self.access_token = None
        self.car_id = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=self.scan_interval),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            if not self.access_token:
                self.access_token = await self.hass.async_add_executor_job(
                    self.vehicle_manager.get_access_token
                )
                if not self.access_token:
                    raise ConfigEntryAuthFailed("Authentication failed")

            if not self.car_id:
                car_list = await self.hass.async_add_executor_job(
                    self.vehicle_manager.get_car_list, self.access_token
                )
                if car_list and "cars" in car_list:
                    self.car_id = car_list["cars"][0]["carId"]
                else:
                    raise Exception("No car found")

            data = {}

            odometer = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_odometer, self.access_token, self.car_id
            )
            if odometer and "odometers" in odometer:
                data["odometer"] = odometer["odometers"][0]["value"]

            dte = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_dte, self.access_token, self.car_id
            )
            if dte and "value" in dte:
                data["dte"] = dte["value"]

            ev_battery = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_ev_battery, self.access_token, self.car_id
            )
            if ev_battery and "soc" in ev_battery:
                data["ev_battery_level"] = ev_battery["soc"]

            ev_charging = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_ev_charging, self.access_token, self.car_id
            )
            if ev_charging:
                data["ev_charging_status"] = ev_charging.get("batteryCharge")
                if "remainTime" in ev_charging:
                    data["ev_remaining_time"] = ev_charging["remainTime"]["value"]

            fuel_warning = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_fuel_warning, self.access_token, self.car_id
            )
            if fuel_warning and "status" in fuel_warning:
                data["fuel_warning"] = fuel_warning["status"]

            tire_pressure_warning = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_tire_pressure_warning,
                self.access_token,
                self.car_id,
            )
            if tire_pressure_warning and "status" in tire_pressure_warning:
                data["tire_pressure_warning"] = tire_pressure_warning["status"]

            lamp_wire_warning = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_lamp_wire_warning, self.access_token, self.car_id
            )
            if lamp_wire_warning and "status" in lamp_wire_warning:
                data["lamp_wire_warning"] = lamp_wire_warning["status"]

            smart_key_battery_warning = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_smart_key_battery_warning,
                self.access_token,
                self.car_id,
            )
            if smart_key_battery_warning and "status" in smart_key_battery_warning:
                data["smart_key_battery_warning"] = smart_key_battery_warning["status"]

            washer_fluid_warning = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_washer_fluid_warning,
                self.access_token,
                self.car_id,
            )
            if washer_fluid_warning and "status" in washer_fluid_warning:
                data["washer_fluid_warning"] = washer_fluid_warning["status"]

            brake_oil_warning = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_brake_oil_warning, self.access_token, self.car_id
            )
            if brake_oil_warning and "status" in brake_oil_warning:
                data["brake_oil_warning"] = brake_oil_warning["status"]

            engine_oil_warning = await self.hass.async_add_executor_job(
                self.vehicle_manager.get_engine_oil_warning, self.access_token, self.car_id
            )
            if engine_oil_warning and "status" in engine_oil_warning:
                data["engine_oil_warning"] = engine_oil_warning["status"]

            return data

        except Exception as err:
            err_msg = str(err)
            err_code = err_msg.split("(")[1].split(")")[0]
            if err_code in ERROR_MESSAGES:
                raise UpdateFailed(f"{ERROR_MESSAGES[err_code]} ({err_code})") from err
            else:
                raise err
