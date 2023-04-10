import socket
import time
from concurrent import futures
from queue import Queue

import grpc
from terminal import userTerminal_pb2, userTerminal_pb2_grpc
import proxy.proxy_pb2_grpc as proxy_pb2_grpc
from terminal.controller.controller import Controller
from terminal.view.terminalWindow import TerminalWindow


class ResultsServiceServicer(proxy_pb2_grpc.ResultsServiceServicer):
    def SendResults(self, result, context):
        t.resultsQueue.put(result)
        print("Result: " + result.__str__())
        response = proxy_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class Terminal:
    def __init__(self):
        self._server = None
        self._subscribeChannel = None
        self._resultsQueue = Queue()
        sock = socket.socket()
        sock.bind(('', 0))
        self._port = sock.getsockname()[1]
        self.subscribeToProxy()

    def subscribeToProxy(self):
        # subscribe channel to send the chosen port to the LB
        self._subscribeChannel = grpc.insecure_channel('localhost:50055')
        try:
            connectionT = userTerminal_pb2.ConnectionT()
            connectionT.port = self._port
            print("Chosen port for terminal: " + str(self._port))
            stub = userTerminal_pb2_grpc.ConnectionTServiceStub(self._subscribeChannel)
            stub.SubscribeToProxy(connectionT)
        except Exception as e:
            print("There is a problem establishing connection with the proxy server.")
            print(e)

    def listen(self):
        print("Listening for results on port " + str(self._port) + " for proxy to send results.")
        with futures.ThreadPoolExecutor(max_workers=10) as pool:
            self._server = grpc.server(pool)
            proxy_pb2_grpc.add_ResultsServiceServicer_to_server(
                ResultsServiceServicer(), self._server)
            try:
                self._server.add_insecure_port('[::]:' + str(self._port))
                self._server.start()
                try:
                    self._server.wait_for_termination()
                except KeyboardInterrupt or Exception:
                    print("Server stopped.")
            except Exception as e:
                print("There is a problem with the port, maybe it is being used by other application.")
                print(e)

    @property
    def resultsQueue(self):
        return self._resultsQueue


if __name__ == '__main__':
    t = Terminal()
    view = TerminalWindow()
    controller = Controller(view=view, model=t)
    view.setController(controller)

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(t.listen)
        executor.submit(controller.runWindow)
        executor.submit(controller.initPlot)



