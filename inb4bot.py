## inb4bot v1r2
#
#	Useless waste of time that fulfils inb4s.
#	Requires stock python2.6 libraries, as well as twisted.
#	Usage: python inb4bot.py irc.server 6667 channel
#	   eg: nohup irc.stormbit.net 6667 test &
#
#	Copyright (c) 2011 Alex "Antoligy" Wilson <antoligy@antoligy.com>
#
#	Permission is hereby granted, free of charge, to any person obtaining a copy
#	of this software and associated documentation files (the "Software"), to deal
#	in the Software without restriction, including without limitation the rights
#	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#	copies of the Software, and to permit persons to whom the Software is
#	furnished to do so, subject to the following conditions:
#
#	The above copyright notice and this permission notice shall be included in
#	all copies or substantial portions of the Software.
#
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#	THE SOFTWARE.

import sys, string, os
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

class inb4(irc.IRCClient):
	nickname = 'inb4'
	realname = 'inb4bot v1 by Antoligy'
	username = 'inb4'
	userinfo = 'inb4'
	fingerReply = 'inb4finger'
	versionName = 'inb4'
	versionNum = '1'
	versionEnv = 'IRC'
	sourceURL = 'http://git.antoligy.com/'

	def signedOn(self):
        	self.join(self.factory.channel)
		print "Connected as %s." % (self.nickname,)

	def joined(self, channel):
		print "Joined %s." % (channel,)

	def privmsg(self, user, channel, msg):
		if not user:
        		return

		if msg.startswith('inb4'):
			self.msg(self.factory.channel, string.strip(msg[4:]))
			print "Repeated \"%s\" by \"%s\"" % (string.strip(msg[4:]), user,)

	def action(self, user, channel, data):
		if not user:
			return

		if data.startswith('inb4'):
			self.describe(self.factory.channel, string.strip(data[4:]))
			print "Repeated \"%s\" by \"%s\" (action)" % (string.strip(data[4:]), user,)

	def kickedFrom(self, channel, kicker, message):
		print "Kicked by %s." % (kicker,)
		self.join(self.factory.channel)

class inb4Factory(protocol.ClientFactory):
	protocol = inb4
	def __init__(self, channel,):
		self.channel = channel
		self.nickname = 'inb4bot'

	def clientConnectionLost(self, connector, reason):
		print "Lost connection: %s, reconnecting." % (reason,)
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print "Could not connect: %s" % (reason,)

if __name__ == "__main__":
	try:
		serv = sys.argv[1]
		port = int(sys.argv[2])
		chan = sys.argv[3]

	except IndexError:
		print "Please specify server, port and channel."
		print "Example:"
		print "python inb4bot.py irc.stormbit.net 6667 test"

	reactor.connectTCP(serv, port, inb4Factory('#' + chan))
	reactor.run()
