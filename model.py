import torch
import torch.nn as nn
import torch.nn.functional as F

import snntorch as snn
from snntorch import surrogate

from config import (
    INPUT_SIZE,
    HIDDEN_SIZE,
    OUTPUT_SIZE,
    TIME_STEPS,
    DEVICE
)


class HawkeyeSNN(nn.Module):
    def __init__(self):
        super().__init__()

        spike_grad = surrogate.fast_sigmoid()

        self.fc1 = nn.Linear(
            INPUT_SIZE,
            HIDDEN_SIZE
        )

        self.lif1 = snn.Leaky(
            beta=0.9,
            spike_grad=spike_grad
        )

        self.fc2 = nn.Linear(
            HIDDEN_SIZE,
            OUTPUT_SIZE
        )

        self.lif2 = snn.Leaky(
            beta=0.9,
            spike_grad=spike_grad
        )

    def forward(self, x):
        """
        x shape:
        [TIME_STEPS, INPUT_SIZE]

        Returns:
            spike_record:
            [TIME_STEPS, OUTPUT_SIZE]
        """

        mem1 = self.lif1.init_leaky()
        mem2 = self.lif2.init_leaky()

        spike_record = []

        for step in range(TIME_STEPS):
            current1 = self.fc1(x[step])

            spk1, mem1 = self.lif1(
                current1,
                mem1
            )

            current2 = self.fc2(spk1)

            spk2, mem2 = self.lif2(
                current2,
                mem2
            )

            spike_record.append(spk2)

        spike_record = torch.stack(spike_record)

        return spike_record

    def predict(self, x):
        """
        Returns:
            prediction,
            confidence,
            probabilities
        """

        self.eval()

        with torch.no_grad():
            spikes = self.forward(x)

            spike_counts = spikes.sum(dim=0)

            probabilities = F.softmax(
                spike_counts,
                dim=0
            )

            confidence, prediction = torch.max(
                probabilities,
                dim=0
            )

        return (
            prediction.item(),
            confidence.item(),
            probabilities.cpu().numpy()
        )