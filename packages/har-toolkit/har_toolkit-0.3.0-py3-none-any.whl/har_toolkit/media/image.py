#!/usr/bin/env python3
from PIL import Image  # pylint: disable=import-error
from io import BytesIO
from urllib.parse import urlparse


class ImageEntry:
    """A class to represent an image from a HAR entry."""

    def __init__(self, entry):
        self.entry = entry
        self.url = urlparse(self.entry.request.url)
        self.filename = self.url.path.split("/")[-1]
        self.entry.response.content.decode()
        self.content = self.entry.response.content.text
        self.image = Image.open(BytesIO(self.content))

    def save(self, dir=".", filename=None):
        if filename is None:
            filename = self.filename

        self.image.save(f"{dir}/{filename}")
        self.image.close()

    def __str__(self):
        return f"{self.url}"

    def __repr(self):
        return f"<ImageEntry {str(self.url)}>"

