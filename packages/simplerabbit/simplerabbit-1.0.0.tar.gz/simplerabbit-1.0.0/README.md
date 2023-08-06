# Atom Rabbit Lib
Rabbit Lib is a Python library for sending and receiving messages using RabbitMQ. It includes two classes, RabbitSender and RabbitReceiver, that provide a simple interface for sending and receiving messages over a RabbitMQ broker.
## Installation
You can install Rabbit Lib using pip:
``` python
pip install rabbit_lib
```

Rabbit Lib requires Python 3.6 or later, as well as the pika library (version 1.2.0)

## Usage
Here's an example of how to use RabbitSender to send a message:
``` python
from rabbit_lib import RabbitSender

sender = RabbitSender('amqp://guest:guest@localhost:5672/', 'my_queue')
sender.send_message('Hello, world!')
```

And here's an example of how to use RabbitReceiver to receive messages:
``` python
from rabbit_lib import RabbitReceiver

receiver = RabbitReceiver('amqp://guest:guest@localhost:5672/', 'my_queue')
message = receiver.receive_message()
print(message)
```

## License
Rabbit Lib is licensed under the MIT License. See LICENSE for more information.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
