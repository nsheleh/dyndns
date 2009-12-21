import config

from twisted.web.resource import Resource
from twisted.web import server
from twisted.names import dns
from util import ProxyRequest

class RootResource(Resource):
  isLeaf = True

  def __init__(self, dynamic_zone):
    Resource.__init__(self)
    self.dynamic_zone = dynamic_zone

  @classmethod
  def extract_request(cls, request):
    record_name = request.args["name"][0]
    ip = request.args.get("ip", [request.getClientIP()])[0]

    return dict(record_name=record_name, record=dns.Record_A(ip))

  @classmethod
  def error(cls, request, code):
    request.setResponseCode(code)
    request.write(repr(code))
    request.finish()

  def render_DELETE(self, request):
    r = RootResource.extract_request(request)
    record_name, record = r["record_name"], r["record"]
 
    if not record_name in config.ALLOWABLE:
      RootResource.error(request, 403)
      return

    self.dynamic_zone.remove(record)
    return ""

  def render_POST(self, request):
    r = RootResource.extract_request(request)
    record_name, record = r["record_name"], r["record"]

    if not record_name in config.ALLOWABLE:
      RootResource.error(request, 403)
      return

    self.dynamic_zone.add(record_name, record)
    return ""

class RootSite(server.Site):
  if hasattr(config, "FORWARDED_FOR_HEADER"):
    requestFactory = ProxyRequest

def WebRegistrarFactory(dynamic_zone):
  return RootSite(RootResource(dynamic_zone))

