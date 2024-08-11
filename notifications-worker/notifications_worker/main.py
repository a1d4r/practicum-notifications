from faststream import FastStream

from notifications_worker.broker import broker

app = FastStream(broker, title="Notifications worker", version="0.1.0")

import notifications_worker.handlers  # noqa: F401, E402
