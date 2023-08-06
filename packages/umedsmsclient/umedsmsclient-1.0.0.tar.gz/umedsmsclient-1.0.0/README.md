# Umed Sms Client

Umed Sms Client is a Python library that provides a simple interface for accessing the Fire Text Sms API. With Umed Sms Client, you can easily send sms to your clients.

## Installation

You can install Umed Sms Client using pip:

```terminal
pip install umedsmsclient
```

## Usage

To use Umed Sms Client, you'll need to create a new instance of the `FireTextApiClient` class:

#### Using Api Key method:

```python
from umedsmsclient.fire_text_api_client import FireTextApiClient

client = FireTextApiClient(api_key="your-firetext-apikey")
```

#### Using Username and Password method:

```python
from umedsmsclient.fire_text_api_client import FireTextApiClient

client = FireTextApiClient(username="your-firetext-username", password="your-firetext-token")
```

You can then use the client to interact with the Fire Text Sms API.:

#### Send sms:

```python

# Send an instant sms
client.send_sms("sender-name", "receiver-phone-number", "text-message")

# Send a scheduled sms
client.send_sms("sender-name", "receiver-phone-number", "text-message", "YYYY-MM-DD HH:MM")
```

## Documentation

For more information on how to use Umed Sms Client, check out the documentation.

Contributing
Contributions are welcome! If you'd like to contribute to Umed Sms Client, please read the contribution guidelines.

## License
Umed Sms Client is licensed under the MIT License. See the LICENSE file for more information.

```terminal
This `README.md` file provides an introduction to the library, instructions on how to install and use it, and information on how to contribute to the project. It also includes a license section to indicate the licensing terms of the project.
```

