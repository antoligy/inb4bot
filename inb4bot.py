##
##
##
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

		if 'inb4' in msg:
			self.msg(self.factory.channel, string.strip(msg[4:]))
			print "Repeated \"%s\" by \"%s\"" % (string.strip(msg[4:]), user,)

	def action(self, user, channel, data):
		if not user:
			return
		if 'inb4' in data:
			self.describe(self.factory.channel, string.strip(data[4:]))
			print "Repeated \"%s\" by \"%s\" (action)" % (string.strip(data[4:]), user,)

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
