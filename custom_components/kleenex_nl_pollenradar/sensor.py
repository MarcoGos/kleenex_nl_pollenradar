import logging

from collections.abc import Mapping
from typing import Any

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import EntityCategory

from .coordinator import PollenDataUpdateCoordinator
from .const import DOMAIN, NAME

_LOGGER: logging.Logger = logging.getLogger(__package__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
) -> None:
    coordinator: PollenDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    INSTRUMENTS = [
        ("trees", "Tree Pollen", "trees", "mdi:tree", None, None),
        ("grass", "Grass Pollen", "grass", "mdi:grass", None, None),
        ("weeds", "Weed Pollen", "weeds", "mdi:cannabis", None, None),
        (
            "last_updated_pollen",
            "Last Updated (Pollen)",
            "",
            "mdi:clock-outline",
            None,
            EntityCategory.DIAGNOSTIC,
        ),
    ]

    sensors = [
        KleenexSensor(
            coordinator,
            entry,
            id,
            description,
            key,
            icon,
            device_class,
            entity_category,
        )
        for id, description, key, icon, device_class, entity_category in INSTRUMENTS
    ]

    async_add_devices(sensors, True)


class KleenexSensor(CoordinatorEntity[PollenDataUpdateCoordinator]):
    def __init__(
        self,
        coordinator: PollenDataUpdateCoordinator,
        entry: ConfigEntry,
        id: str,
        description: str,
        key: str,
        icon: str,
        device_class: str | None,
        entity_category: ConfigEntry | None,
    ) -> None:
        super().__init__(coordinator)
        self._id = id
        self.description = description
        self.key = key
        self._icon = icon
        self._device_class: str | None = device_class
        self._entry = entry
        self._attr_entity_category = entity_category

    @property
    def state(self):
        if self.key != "":
            return self.coordinator.data[0][self.key]["pollen"]
        else:
            return self.coordinator.last_updated

    @property
    def unit_of_measurement(self):
        if self.key != "":
            return self.coordinator.data[0][self.key]["unit_of_measure"]

    @property
    def icon(self):
        return self._icon

    @property
    def device_class(self):
        return self._device_class

    @property
    def name(self):
        return f"{self.description} ({self._entry.data['name']})"

    @property
    def id(self):
        return f"{DOMAIN}_{self._id}"

    @property
    def unique_id(self):
        return f"{DOMAIN}-{self._id}-{self._entry.data['name']}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.api.position)},
            "name": f"{NAME} ({self._entry.data['name']})",
            "manufacturer": NAME,
        }

    @property
    def available(self) -> bool:
        return not not self.coordinator.data

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        data: dict[str, Any] = {}
        if self.key != "":
            data["level"] = self.coordinator.data[0][self.key]["level"]
            data["date"] = self.coordinator.data[0]["date"]
            data["value_tomorrow"] = int(self.coordinator.data[1][self.key]["pollen"])
            data["value_in_2_days"] = int(self.coordinator.data[2][self.key]["pollen"])
            data["value_in_3_days"] = int(self.coordinator.data[3][self.key]["pollen"])
            data["value_in_4_days"] = int(self.coordinator.data[4][self.key]["pollen"])
            data["level_tomorrow"] = self.coordinator.data[1][self.key]["level"]
            data["level_in_2_days"] = self.coordinator.data[2][self.key]["level"]
            data["level_in_3_days"] = self.coordinator.data[3][self.key]["level"]
            data["level_in_4_days"] = self.coordinator.data[4][self.key]["level"]
            data["details"] = self.coordinator.data[0][self.key]["details"]
        return data
