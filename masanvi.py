import random
import numpy as np

from config import (
    FRAME_HEIGHT,
    FRAME_WIDTH,
    TIME_STEPS,
    SIMULATION_EVENTS_PER_BATCH
)


class EventCameraSimulator:
    """
    Simulates an event-based camera by generating sparse event streams.

    Event format:
        (t, x, y, polarity)

    where:
        t         : time step
        x, y      : pixel coordinates
        polarity  : -1 or +1
    """

    def __init__(self):
        self.height = FRAME_HEIGHT
        self.width = FRAME_WIDTH

    def generate_events(self, scenario="random"):
        """
        Generate synthetic event streams for different scenarios.

        Args:
            scenario (str):
                "random"  -> No threat
                "animal"  -> Wildlife detected
                "poacher" -> Poacher detected

        Returns:
            list: List of events in the format
                  (t, x, y, polarity)
        """

        events = []

        for i in range(SIMULATION_EVENTS_PER_BATCH):
            # Distribute events across time bins
            t = i % TIME_STEPS

            if scenario == "animal":
                # Wildlife cluster
                x = int(
                    np.clip(
                        np.random.normal(self.width * 0.30, 5),
                        0,
                        self.width - 1,
                    )
                )

                y = int(
                    np.clip(
                        np.random.normal(self.height * 0.30, 5),
                        0,
                        self.height - 1,
                    )
                )

            elif scenario == "poacher":
                # Poacher cluster
                x = int(
                    np.clip(
                        np.random.normal(self.width * 0.70, 5),
                        0,
                        self.width - 1,
                    )
                )

                y = int(
                    np.clip(
                        np.random.normal(self.height * 0.70, 5),
                        0,
                        self.height - 1,
                    )
                )

            else:
                # Random background activity
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

            polarity = random.choice([-1, 1])

            events.append((t, x, y, polarity))

        return events