import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    Platform,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_PIN,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, ConfigEntryAuthFailed
import hashlib

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_FORCE_SCAN_INTERVAL,
    DEFAULT_NO_FORCE_SCAN_HOUR_START,
    DEFAULT_NO_FORCE_SCAN_HOUR_FINISH,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_REDIRECT_URI,
)
from .coordinator import HyundaiConnectKoreaDataUpdateCoordinator
from .services import async_setup_services, async_unload_services

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.LOCK,
    Platform.NUMBER,
    # Platform.CLIMATE,
]


async def async_setup(hass: HomeAssistant, config_entry: ConfigEntry):
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Hyundai Connect Korea from a config entry."""
    coordinator = HyundaiConnectKoreaDataUpdateCoordinator(hass, config_entry)
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as ex:
        raise ConfigEntryNotReady(f"Config Not Ready: {ex}")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.unique_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    async_setup_services(hass)
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    ):
        del hass.data[DOMAIN][config_entry.unique_id]
    if not hass.data[DOMAIN]:
        async_unload_services(hass)
    return unload_ok


async def async_migrate_entry(hass, config_entry: ConfigEntry):
    if config_entry.version == 1:
        _LOGGER.debug(f"{DOMAIN} - config data- {config_entry}")
        username = config_entry.data.get(CONF_USERNAME)
        password = config_entry.data.get(CONF_PASSWORD)
        pin = config_entry.data.get(CONF_PIN)
        scan_interval = config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        force_scan_interval = config_entry.data.get(
            CONF_FORCE_SCAN_INTERVAL, DEFAULT_FORCE_SCAN_INTERVAL
        )
        no_force_scan_hour_start = config_entry.data.get(
            CONF_NO_FORCE_SCAN_HOUR_START, DEFAULT_NO_FORCE_SCAN_HOUR_START
        )
        no_force_scan_hour_finish = config_entry.data.get(
            CONF_NO_FORCE_SCAN_HOUR_FINISH, DEFAULT_NO_FORCE_SCAN_HOUR_FINISH
        )
        client_id = config_entry.data.get(CONF_CLIENT_ID)
        client_secret = config_entry.data.get(CONF_CLIENT_SECRET)
        redirect_uri = config_entry.data.get(CONF_REDIRECT_URI)
        
        title = f"Hyundai Connect Korea {username}"
        unique_id = hashlib.sha256(title.encode("utf-8")).hexdigest()
        
        new_data = {
            CONF_USERNAME: username,
            CONF_PASSWORD: password,
            CONF_PIN: pin,
            CONF_SCAN_INTERVAL: scan_interval,
            CONF_FORCE_SCAN_INTERVAL: force_scan_interval,
            CONF_NO_FORCE_SCAN_HOUR_START: no_force_scan_hour_start,
            CONF_NO_FORCE_SCAN_HOUR_FINISH: no_force_scan_hour_finish,
            CONF_CLIENT_ID: client_id,
            CONF_CLIENT_SECRET: client_secret,
            CONF_REDIRECT_URI: redirect_uri,
        }
        
        registry = hass.helpers.entity_registry.async_get(hass)
        entities = hass.helpers.entity_registry.async_entries_for_config_entry(
            registry, config_entry.entry_id
        )
        for entity in entities:
            registry.async_remove(entity.entity_id)

        hass.config_entries.async_update_entry(
            config_entry, unique_id=unique_id, title=title, data=new_data
        )
        config_entry.version = 2
        _LOGGER.info("Migration to version %s successful", config_entry.version)
    return True
