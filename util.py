from twisted.web import server, http
import re
import config

class ProxyRequest(server.Request):
  ip_re = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")
  def validIP(self, ip):
    m = self.ip_re.match(ip)
    if m is None:
      return False

    return all(int(m.group(x)) < 256 for x in range(1, 4+1))

  def getClientIP(self):
    real_ip = http.Request.getClientIP(self)
    if real_ip not in config.FORWARDED_FOR_IPS:
      return real_ip
      
    fake_ips = self.getHeader(config.FORWARDED_FOR_HEADER)
    if fake_ips is None:
      return real_ip
      
    fake_ip = fake_ips.split(",")[-1].strip()
    if not self.validIP(fake_ip):
      return real_ip
      
    return fake_ip
