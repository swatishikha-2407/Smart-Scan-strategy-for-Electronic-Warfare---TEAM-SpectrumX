"""
Virtual Receiver package.

This package provides a software-only simulated receiver,
detector, and uncertainty model for the Smart Scan Strategy
simulation.
"""

from .receiver import VirtualReceiver
from .detector import Detector
from .noise_model import NoiseModel

__all__ = [
    "VirtualReceiver",
    "Detector",
    "NoiseModel",
]
