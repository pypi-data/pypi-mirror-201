"""Kickoff Project: models / team.py

This module contains the Team class.

This file is Copyright (c) 2023 Ram Raghav Sharma, Harshith Latchupatula, Vikram Makkar and Muhammad Ibrahim.
"""

from __future__ import annotations
from dataclasses import dataclass
import kickoff_epl.models.match as match


@dataclass
class Team:
    """A football team playing in a particular season of the Premier League.

    Instance Attributes:
        - name: The name of this team.
        - matches: A chronologically ordered list of the matches played by this team in the season.
        - seasons: The seasons this team has participated in.

    Representation Invariants:
        - len(self.matches) > 0
        - len(self.seasons) > 0
        - all({ self == match.home_team or self == match.away_team for match in self.matches })
    """

    name: str
    matches: list[match.Match]
    seasons: set[str]
