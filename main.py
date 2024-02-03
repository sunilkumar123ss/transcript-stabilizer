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

    def update(self, text, final=False):
        if not isinstance(text, str) or not isinstance(final, bool):
            raise ValueError('Require string text and boolean final')
        if self.finalized:
            raise ValueError('Stream already finalized')
        tokens = text.split()
        if tokens[:len(self.committed)] != self.committed:
            raise ValueError('Provider revised an already committed prefix; start a new segment')
        history = (self.history + [tokens])[-self.observations:]
        commit = list(self.committed)
        if final:
            commit = tokens
        elif len(history) == self.observations:
            common = []
            for group in zip(*history):
                if len(set(group)) != 1:
                    break
                common.append(group[0])
            if len(common) > len(commit):
                commit = common
        self.history = history
        self.committed = commit
        self.finalized = final
        return {'committed': ' '.join(commit), 'provisional': ' '.join(tokens[len(commit):]), 'final': final}

def stabilize(updates, observations=3):
    if not isinstance(updates, list):
        raise ValueError('updates must be a list')
    stream = Stabilizer(observations)
    result = []
    for update in updates:
        if not isinstance(update, dict) or 'text' not in update:
            raise ValueError('Every update needs text')
        result.append(stream.update(update['text'], update.get('final', False)))
    return result
