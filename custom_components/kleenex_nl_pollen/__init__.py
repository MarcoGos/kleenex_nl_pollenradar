"""The Kleenex NL pollen integration."""
from __future__ import annotations

from .api import PollenApi
from .const import (
    # DEFAULT_SYNC_INTERVAL,
    DOMAIN,
    PLATFORMS,
)

# from datetime import timedelta
import logging
from homeassistant.config_entries import ConfigEntry

# from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.core import Config
from homeassistant.helpers.aiohttp_client import async_get_clientsession

# from homeassistant.helpers.update_coordinator import UpdateFailed, DataUpdateCoordinator
from homeassistant.exceptions import ConfigEntryNotReady

from .coordinator import PollenDataUpdateCoordinator

from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE

# SCAN_INTERVAL = timedelta(hours=1)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kleenex NL pollen from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    _LOGGER.debug(f"entry.data: {entry.data}")

    session = async_get_clientsession(hass)
    api = PollenApi(
        session=session,
        latitude=entry.data[CONF_LATITUDE],
        longitude=entry.data[CONF_LONGITUDE],
    )

    coordinator = PollenDataUpdateCoordinator(hass, api=api)
    _LOGGER.debug("Trying to perform async_refresh")
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    _LOGGER.debug(f"Info about entry: {entry.entry_id}")

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # _LOGGER.info(f"hass data: {hass.data}")

    for platform in PLATFORMS:
        _LOGGER.debug(f"Adding platform: {platform}")
        coordinator.platforms.append(platform)

    # hass.async_add_job(
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # )
    # entry.async_on_unload(entry.add_update_listener(async_options_updated))
    # await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
