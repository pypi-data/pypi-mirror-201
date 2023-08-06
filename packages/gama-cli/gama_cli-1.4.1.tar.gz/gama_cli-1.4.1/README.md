# GAMA CLI

## Install

* `pip install -e ./tools/gama_cli`
* You may also need to `export PATH=$PATH:~/.local/bin` if you don't have `~/.local/bin` in your path
* Install autocomplete:
  * bash: `echo 'eval "$(_GAMA_CLI_COMPLETE=bash_source gama_cli)"' >> ~/.bashrc`
  * zsh: `echo 'eval "$(_GAMA_CLI_COMPLETE=zsh_source gama_cli)"' >> ~/.zshrc` (this is much nicer)

## Help
* `gama_cli --help` (or similar) to get help with the CLI

## Modes

The GAMA system has 3 main components, each of these has several modes:

* Vessel
  * Mode: sim (when running the simulator) **default**
  * Mode: stubs (when stubbing the simulator outputs)
  * Mode: hw (when connected to real hardware)
* Groundstation
  * Mode: dev (when running with stubs or sim) **default**
  * Mode: hw (when connected to real hardware)
* Simulator:
  * Mode: dev (when using the ue4 editor)
  * Mode: standalone (when using the ue4 standlone) **default**


## Launch

Build all components. Use `-m` to build/run in different modes.

```bash
gama_cli sim build
gama_cli vessel build
gama_cli gs build
```

Start all the components:
```bash
gama_cli sim up
gama_cli vessel up
gama_cli gs up

# or

gama_cli sim up --build
gama_cli vessel up --build
gama_cli gs up --build
```
