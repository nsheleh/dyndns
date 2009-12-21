from twisted.names import dns, client, server, common, authority

#resolver = client.createResolver(resolvconf="/etc/resolv.conf")

class DynamicZone(authority.FileAuthority):
  def __init__(self, soa_name, soa_record):
    common.ResolverBase.__init__(self)
    self._cache = {}
    self.records = {}
    self.soa = (soa_name, soa_record)

  def _name(self, name):
    return "%s.%s" % (name.lower(), self.soa[0])

  def add(self, name, record):
    self.records[self._name(name)] = [record]

  def remove(self, name, record):
    name = self._name(name)
    if self.records.get(name):
      del self.records[name]

  def __iter__(self):
    return iter(self.records)

  def __len__(self):
    return len(self.records)

def DNSServerFactory(zones):
  factory = server.DNSServerFactory(zones, None, []) # resolver])
  return dns.DNSDatagramProtocol(factory)

