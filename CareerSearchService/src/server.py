from multiprocessing.synchronize import Lock
import db
from CareerSearch.gen import Links
from CareerSearch.gen.ttypes import Link
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from settings import SERVICE_CONFIG


_lock = Lock()


class LinksHandler(Links.Iface):

    DEFAULT_PORT = SERVICE_CONFIG['port']

    def getLinks(self, predicate, pendings):
        try:
            _lock.acquire()
            print "[%s]get links ..." % predicate.source
            result = db.get_links(predicate.source, pendings)
            return [Link(link[0]) for link in result] if result else []
        finally:
            _lock.release()

    def reportStatus(self, statusList):
        try:
            _lock.acquire()
            print "report status ..."
            if statusList[0].pages:
                print "status:%s, type:%s, pages:%s" % (statusList[0].status, statusList[0].type, statusList[0].pages)
            db.update_links(statusList)
        finally:
            _lock.release()


handler = LinksHandler()
processor = Links.Processor(handler)
transport = TSocket.TServerSocket(port=LinksHandler.DEFAULT_PORT)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print "Starting server..."
server.serve()
