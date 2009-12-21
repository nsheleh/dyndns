import dns_server
import config
import web_server

from twisted.application import internet, service

application = service.Application("dyndns")

dynamic_zone = dns_server.DynamicZone(config.ZONE, config.SOA_RECORD)

dns_ = internet.UDPServer(53, dns_server.DNSServerFactory([dynamic_zone]), interface=config.DNS_INTERFACE)
dns_.setServiceParent(application)

web_ = internet.TCPServer(config.PORT, web_server.WebRegistrarFactory(dynamic_zone), interface=config.WEB_INTERFACE)
web_.setServiceParent(application)

