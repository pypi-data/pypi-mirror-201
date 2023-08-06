# -*- coding: utf-8 -*-
# Copyright (C) Alexander Pace (2022)
#
# This file is part of igwn-alert-overseer
#
# lvalert-overseer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with igwn-alert-overseer.
# If not, see <http://www.gnu.org/licenses/>.

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient

class overseer_client(TCPClient):

    def __init__(self, host, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port
        self.msg_separator = b'\r\n'
        #self.io_loop = IOLoop.instance()

    @gen.coroutine
    def send_to_overseer(self, mdict,  logger):
        #IOLoop.instance().start()
        stream = yield self.connect(self.host, self.port)
        while True:
            try: 
                msg = mdict.encode('utf-8')
                yield stream.write(msg+self.msg_separator)
                rdict = yield stream.read_until_close()
            except StreamClosedError:
                if stream.closed():
                    IOLoop.instance().stop()
                    return rdict
