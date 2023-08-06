#!/usr/bin/env python3
from .bases import SimpleHarType


class Header(SimpleHarType):

    def __repr__(self):
        return f"{type(self).__name__} {self.name}={self.value}\n\t"
