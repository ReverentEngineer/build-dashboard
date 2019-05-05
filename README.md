# build-dashboard

A CLI dashboard for buildbot

## How to run

```
build_dashboard  --protocol https --host buildbot.example.com
```

## Configuration file

build_dashboard looks for a TOML-based `.buildbotrc` in the users home directory. If it finds one it, it will use the parameters in the file. Any arguments passed on the command line will override the configuration file.

Example configuration file:
```
protocol = "http"
host = "localhost"
unix = "/var/run/buildbot.sock"
```
