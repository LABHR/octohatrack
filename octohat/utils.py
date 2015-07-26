# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

import os
import logging

class AttrDict(dict):
    """Attribute Dictionary (set and access attributes 'pythonically')"""
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError('no such attribute: %s' % name)

    def __setattr__(self, name, val):
        self[name] = val

def get_logger(name, level=None):
    """Returns logging handler based on name and level (stderr)
        name (str): name of logging handler
        level (str): see logging.LEVEL
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        stderr = logging.StreamHandler()
        stderr.setFormatter(logging.Formatter(
            '%(levelname)s [%(name)s]: %(message)s'))
        logger.addHandler(stderr)

        level = level if level else os.environ.get('OCTOHUB_LOGLEVEL', 'CRITICAL')
        logger.setLevel(getattr(logging, level))

    return logger

