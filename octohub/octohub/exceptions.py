# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

import simplejson as json

class ResponseError(Exception):
    """Accessible attributes: error
        error (AttrDict): Parsed error response
    """
    def __init__(self, error):
        Exception.__init__(self, error)
        self.error = error

    def __str__(self):
        return json.dumps(self.error, indent=1)


class OctoHubError(Exception):
    pass

