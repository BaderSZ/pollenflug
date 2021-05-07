# pollenflug
CLI pollen/allergy calendar

![Screenshot](img/screenshot.png)

This script uses [Hexal's Pollenflugkalendar](https://allergie.hexal.de/pollenflug/vorhersage/) to fetch the predictions for the next week.

Currently, the intensity is printed as a numerical value between 0 and 3: 0 being none, 3 being severe.

pollenflug currently supports a configuration file as `~/.pollenflug.ini`, with an example configuration included in the repo

## License

The script is GPL-3.0

## Todo:
* Replace numbers with strings or emojis
* Add support for other countries
* Translate names to English
