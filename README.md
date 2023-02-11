![Version](https://img.shields.io/github/v/release/MarcoGos/kleenex_nl_pollenradar?include_prereleases)
![Downloads](https://img.shields.io/github/downloads/MarcoGos/kleenex_nl_pollenradar/total)

# Kleenex NL pollenradar

This is a custom integration of the Kleenex NL pollenradar. It will provide information about pollen counts and levels for trees, grass and weeds. Information will only be available for positions in the Netherlands.

## Installation

Via HACS:

- Add a custom repository: MarcoGos/kleenex_nl_pollenradar as an integration
- Add the integration to Home Assiatant

## Setup

During the setup of the integration a name, latitude and longitude needs to be provides. The defaults are provided by Home Assistant.

## What to expect

The following sensor will be registered:

- Tree Pollen
- Grass Pollen
- Weed Pollen

Each sensor has additional attributes for value tomorrow, in 2, 3 and 4 days.

The information is updated every hour.

## Disclaimer

This integration will work only if Kleenex doesn't alter their interface.