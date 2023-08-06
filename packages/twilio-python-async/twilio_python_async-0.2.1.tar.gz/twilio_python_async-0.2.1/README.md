# Asynchronous Twilio Client

[![Tests Status](https://github.com/sanders41/twilio-python-async/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/twilio-python-async/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/twilio-python-async/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/twilio-python-async/main)
[![Coverage](https://codecov.io/github/sanders41/twilio-python-async/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/twilio-python-async)
[![PyPI version](https://badge.fury.io/py/twilio-python-async.svg)](https://badge.fury.io/py/twilio-python-async)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twilio-python-async?color=5cc141)](https://github.com/sanders41/twilio-python-async)

An asynchronous [Twilio](https://www.twilio.com/) client

## Installation

Using a virtual environment is recommended for installing this package. Once the virtual environment is created and activated install the package with:

```sh
pip install twilio-python-async
```

## Useage

When creating a client the twilio account sid and token can either be read from a `TWILIO_ACCOUNT_SID`
and `TWILIO_AUTH_TOKEN` variables, or passed into the client at creation. Using environment variables
is recommended. Examples below will assume the use of environment variables.

### Send an SMS message

Messages can be sent by either using a Twilio messaging service sid, or by passing a `from_` phone
number. The messaging service sid can be read from a `TWILIO_MESSAGING_SERVICE_SID` environment
variable. The examples below assumes the use of the environment variable.

```py
from twilio_async import AsyncClient


async with AsyncClient() as client:
    await client.message_create("My message", "+12068675309")
```

### Retrieve message logs

```py
from twilio_async import AsyncClient


async with AsyncClient() as client:
    response = await client.get_message_logs()
```

## Contributing

Contributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)
