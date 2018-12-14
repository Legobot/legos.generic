# legos.generic

## Usage

- `!command` does a thing!

## Installation

You can install locally (by cloning the repo) or from PyPi

### Local

cd into the current directory
`pip3 install .`

### From PyPi

`pip3 install legos.lego_name`

### Add to Legobot

This is a Lego designed for use with [Legobot](https://github.com/Legobot/Legobot), so you'll get Legobot along with this.

To deploy it, import the package and add it to the active legos. See the default [chatbot](chatbot/chatbot.py) included with this repo as an example.

## Tweaking

While you can use this one as-is, you could also add a localized version to your Legobot deployment by grabbing [lego_name.py](legos/lego_name.py) and deploying it as a local module. [Example of a Legobot instance with local modules](https://github.com/voxpupuli/thevoxfox/)

## Contributing

As always, pull requests are welcome.

Contributing guidelines are outlined in the main [Legobot Repo](https://github.com/Legobot/Legobot/blob/master/README.md#contributing).

This repo uses (develop branch|feature branches|direct commits).