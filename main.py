"""Commit token prefixes shared by several ASR hypotheses, without running ASR."""
import argparse
import json
from pathlib import Path

class Stabilizer:

    def __init__(self, observations=3):
        if isinstance(observations, bool) or not isinstance(observations, int) or observations < 2:
            raise ValueError('observations must be an integer >=2')
        self.observations = observations
        self.history = []
        self.committed = []
        self.finalized = False
