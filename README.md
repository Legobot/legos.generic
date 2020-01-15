# legos.generic

[![Travis](https://img.shields.io/travis/Legobot/legos.generic.svg)]()

## Usage

This lego is a generic, config-driven lego. Instead of writing the logic of the listening for and handling for basic text triggered responses, this lego accomplishes that with a config file. See the [example config](chatbot/example-config.yaml)
As you'll see in the example chatbot file you can specify the config file's location on invocation. If the lego will assume the config is located in the directory you are running the chatbot from and is named config.py.

### Config structure

The config is a YAML file that consists of an array of configs under the attribute `configs`.

Each config in the array must have the following attributes
`id, listening_for, handler`. You may optionally include `help`.

#### id

`id` is a unique string that identifies the config

#### listening_for

`listening_for` is an object that describes what the lego should listen for in order to trigger a response.  Currently this is case insensitive. Its attributes and potential values are:

- `type`: the type of listener
  - allowed values: `startswith | contains`
- `value`: an array of one or more values you wish to evaluate against

#### handler

`handler` is an object that describes what action to perform if the `listening_for` returns `True`. Its attributes and potential values are:

- `type`: the source type for your response(s)
  - allowed values: `config | file`
- `selector`: how you want to select from response(s) to which to return.
  - allowed values: `single | random`
- `responses`: an array of responses to pick from. only used if type is `config`
- `file_type`: the file type of the file that holds the response(s)
  - allowed values: `json | yaml`
  - if respones are in a file they must be formatted as a response file (below.)
- `path`: the path to the file, relative to the config file.
  
#### help

`help` is a section that provides help text for this particular configuration of the lego. It is an object with one attribute, `text`. `text` is a string of help text returned on request by the help lego.

#### Response File

If your responses are stored in a json or yaml file they must be formatted this way.

- Highest level, the file is an object where each attribute corresponds to the id of its relevant config.
- The id is an object that contains the attribute `responses`.
- `responses` is an array of desired responses available for the lego to process.

## Installation

You can install locally (by cloning the repo) or from PyPi

### Local

cd into the current directory
`pip3 install .`

### From PyPi

`pip3 install legos.generic`

### Add to Legobot

This is a Lego designed for use with [Legobot](https://github.com/Legobot/Legobot), so you'll get Legobot along with this.

To deploy it, import the package and add it to the active legos. See the default [chatbot](chatbot/example-chatbot.py) included with this repo as an example.

## Tweaking

While you can use this one as-is, you could also add a localized version to your Legobot deployment by grabbing [generic.py](legos/generic.py) and deploying it as a local module. [Example of a Legobot instance with local modules](https://github.com/voxpupuli/thevoxfox/)

## Contributing

As always, pull requests are welcome.

Contributing guidelines are outlined in the main [Legobot Repo](https://github.com/Legobot/Legobot/blob/master/README.md#contributing).

This repo uses feature branches.
