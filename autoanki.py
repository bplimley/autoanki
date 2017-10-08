"""Anki deck tools"""

import os

IMAGE_EXTS = ('jpg, jpeg, png, bmp')
SOUND_EXTS = ('wav', 'mp3')


class AnkiError(Exception):
    """
    Exception raised by autoanki.py
    """
    pass


class AnkiDeck(object):
    """
    Represents an Anki deck
    """

    def __init__(self):
        pass

    @classmethod
    def from_file_pairs(self, image_list, sound_list):
        """
        Create an AnkiDeck from a list of images and a list of sounds.
        """

        if len(image_list) != len(sound_list):
            raise AnkiError('Input file lists unequal length')

        for fname in image_list:
            _, ext = os.path.splitext(fname)
            if ext not in IMAGE_EXTS:
                raise AnkiError('Bad image extension: {}'.format(fname))
        for fname in sound_list:
            _, ext = os.path.splitext(fname)
            if ext not in IMAGE_EXTS:
                raise AnkiError('Bad sound extension: {}'.format(fname))

    def to_apkg(self, fname):
        """
        Write to an *.apkg file for use in Anki.
        """

        pass
