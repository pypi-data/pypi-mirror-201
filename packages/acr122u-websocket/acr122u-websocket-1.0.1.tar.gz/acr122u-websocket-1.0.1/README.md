# ACR122U Websocket

[![PyPI - Version](https://img.shields.io/pypi/v/acr122u-websocket)](https://pypi.org/project/acr122u-websocket/)
[![PyPI - License](https://img.shields.io/pypi/l/acr122u-websocket)](https://pypi.org/project/acr122u-websocket/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/acr122u-websocket)](https://pypi.org/project/acr122u-websocket/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/acr122u-websocket)](https://pypi.org/project/acr122u-websocket/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/acr122u-websocket)](https://pypi.org/project/acr122u-websocket/)

This project enables you to connect an usb ACR122U NFC card scanner to a computer and access it using websocket.

## Features

- Read UUID from nfc cards and send them over websocket.
- Websocket messages to start and stop the polling for cards.
- Websocket messages to give a confirmation or error beep and light signal.
- Automatically reconnect to the reader when interrupted.

## Installation
You can install this package from [PyPI](https://pypi.org/project/acr122u-websocket/).

```shell
pip install acr122u-websocket
```

## Usage

1. Connect the ACR122U reader to the computer
2. Run the app
    ```shell
    python -m acr122u_websocket.app
    ```

## API