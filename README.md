![Version](https://img.shields.io/github/v/release/MarcoGos/kleenex_nl_pollenradar?include_prereleases)
![Downloads](https://img.shields.io/github/downloads/MarcoGos/kleenex_nl_pollenradar/total)

# Kleenex NL pollenradar

This is a custom integration of the Kleenex NL pollenradar. It will provide information about pollen counts and levels for trees, grass and weeds. Information will only be available for positions in the Netherlands.

## Installation

Via HACS:

- Add the following custom repository as an integration:
    - MarcoGos/kleenex_nl_pollenradar
    - Restart Home Assistant
- Add the integration to Home Assistant

## Setup

During the setup of the integration a name, latitude and longitude needs to be provided.

## What to expect

The following sensor will be registered:

- Tree Pollen
- Grass Pollen
- Weed Pollen

Each sensor has additional attributes for value and level tomorrow, in 2, 3 and 4 days.

The sensor information is updated every hour although the values on the Kleenex pollenradar website are updated every 3 hours.

## Disclaimer

This integration will work only if Kleenex doesn't alter their interface.