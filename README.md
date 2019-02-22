# Gordon

*The angry cousin of [Geoffrey](https://github.com/Noxet/geoffrey), posting everyday lunch menus on slack.*

## Usage

Run Docker prebuilt docker image:
```bash
docker run --env-file default_env -it erikgartner/gordon:latest
```

Gordon reads its config from the environment that can be set using the `-e` or `--env-file` flags.

Gordon can also be run using Python 3 as:
```bash
python gordon.py
```
