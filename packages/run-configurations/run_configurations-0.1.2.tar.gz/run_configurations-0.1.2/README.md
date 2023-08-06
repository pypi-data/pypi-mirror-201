A small script that allows quickly executing run configurations from the command
line including shell completions.

A run configurations can be any executable placed in a `.run_configs` directory
in any parent of the current working directory. Configurations are always
executed in the directory containing the `.run_configs` folder to get the same
behavior independent of the current working directory.

```
Usage: rc [OPTIONS] RUN_CONFIG [ARGS]...

  Run a run config

  A run config can be any executable file in the .run_configs directory.

Options:
  -e, --edit                      Edit run config instead of running.
  -l, --list                      List available run configs.
  -x, --make-executable           Make run config executable if it isn't
                                  already.
  --base-dir DIRECTORY            Base directory to run from. Defaults to the
                                  first directory containing a .run_configs
                                  directory. Should contain a .run_configs
                                  directory with executable run configs.
  --get-base-dir                  Print base directory.
  --get-rc-dir                    Print run configuration directory.
  --zsh-completion                Print zsh completion script.
  --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Log level.
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```
