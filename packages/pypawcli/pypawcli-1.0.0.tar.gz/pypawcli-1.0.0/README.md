## pawcli

CLI tool for PythonAnywhere

## Install
Install via `pipx`
```shell
$ pipx install pypawcli
```
or `pip`
```shell
$ pip install --upgrade pypawcli --user
```

## Usage
[Get your api token](https://www.pythonanywhere.com/account/#api_token)

```shell
$ pawcli config api.username --set <your_username>
$ pawcli config api.token --set <your_token>
$ pawcli [COMMAND [SUBCOMMAND]] --help
```

## License
[MIT](./LICENSE)
