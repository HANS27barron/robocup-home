"""
This type stub file was generated by pyright.
"""

import logging
import threading
from rospy.core import *
from rospy.impl.transport import Transport

"""Internal use: common TCPROS libraries"""
logger = logging.getLogger('rospy.tcpros')
DEFAULT_BUFF_SIZE = 65536
TCPROS = "TCPROS"
_PARAM_TCP_KEEPALIVE = '/tcp_keepalive'
_use_tcp_keepalive = None
_use_tcp_keepalive_lock = threading.Lock()
def recv_buff(sock, b, buff_size):
    """
    Read data from socket into buffer.
    @param sock: socket to read from
    @type  sock: socket.socket
    @param b: buffer to receive into
    @type  b: StringIO
    @param buff_size: recv read size
    @type  buff_size: int
    @return: number of bytes read
    @rtype: int
    """
    ...

class TCPServer(object):
    """
    Simple server that accepts inbound TCP/IP connections and hands
    them off to a handler function. TCPServer obeys the
    ROS_IP/ROS_HOSTNAME environment variables
    """
    def __init__(self, inbound_handler, port=...) -> None:
        """
        Setup a server socket listening on the specified port. If the
        port is omitted, will choose any open port.
        @param inbound_handler: handler to invoke with
        new connection
        @type  inbound_handler: fn(sock, addr)
        @param port: port to bind to, omit/0 to bind to any
        @type  port: int
        """
        ...
    
    def start(self):
        """Runs the run() loop in a separate thread"""
        ...
    
    def run(self):
        """
        Main TCP receive loop. Should be run in a separate thread -- use start()
        to do this automatically.
        """
        ...
    
    def get_full_addr(self):
        """
        @return: (ip address, port) of server socket binding
        @rtype: (str, int)
        """
        ...
    
    def shutdown(self):
        """shutdown I/O resources uses by this server"""
        ...
    


_tcpros_server = None
def init_tcpros_server(port=...):
    """
    starts the TCPROS server socket for inbound connections
    @param port: listen on the provided port. If the port number is 0, the port will
        be chosen randomly
    @type  port: int
    """
    ...

def start_tcpros_server():
    """
    start the TCPROS server if it has not started already
    """
    ...

def get_tcpros_server_address():
    """
    get the address of the tcpros server.
    @raise Exception: if tcpros server has not been started or created
    """
    ...

class TCPROSServer(object):
    """
    ROS Protocol handler for TCPROS. Accepts both TCPROS topic
    connections as well as ROS service connections over TCP. TCP server
    socket is run once start_server() is called -- this is implicitly
    called during init_publisher().
    """
    def __init__(self, port=...) -> None:
        """
        Constructur
        @param port: port number to bind to (default 0/any)
        @type  port: int
        """
        ...
    
    def start_server(self):
        """
        Starts the TCP socket server if one is not already running
        """
        ...
    
    def get_address(self):
        """
        @return: address and port of TCP server socket for accepting
        inbound connections
        @rtype: str, int
        """
        ...
    
    def shutdown(self, reason=...):
        """stops the TCP/IP server responsible for receiving inbound connections"""
        ...
    


class TCPROSTransportProtocol(object):
    """
    Abstraction of TCPROS connections. Implementations Services/Publishers/Subscribers must implement this
    protocol, which defines how messages are deserialized from an inbound connection (read_messages()) as
    well as which fields to send when creating a new connection (get_header_fields()).
    """
    def __init__(self, resolved_name, recv_data_class, queue_size=..., buff_size=...) -> None:
        """
        ctor
        @param resolved_name: resolved service or topic name
        @type  resolved_name: str
        @param recv_data_class: message class for deserializing inbound messages
        @type  recv_data_class: Class
        @param queue_size: maximum number of inbound messages to maintain
        @type  queue_size: int
        @param buff_size: receive buffer size (in bytes) for reading from the connection.
        @type  buff_size: int
        """
        ...
    
    def read_messages(self, b, msg_queue, sock):
        """
        @param b StringIO: read buffer        
        @param msg_queue [Message]: queue of deserialized messages
        @type  msg_queue: [Message]
        @param sock socket: protocol can optionally read more data from
        the socket, but in most cases the required data will already be
        in b
        """
        ...
    
    def get_header_fields(self):
        """
        Header fields that should be sent over the connection. The header fields
        are protocol specific (i.e. service vs. topic, publisher vs. subscriber).
        @return: {str : str}: header fields to send over connection
        @rtype: dict
        """
        ...
    


class TCPROSTransport(Transport):
    """
    Generic implementation of TCPROS exchange routines for both topics and services
    """
    transport_type = ...
    def __init__(self, protocol, name, header=...) -> None:
        """
        ctor
        @param name str: identifier
        @param protocol TCPROSTransportProtocol protocol implementation    
        @param header dict: (optional) handshake header if transport handshake header was
        already read off of transport.
        @raise TransportInitError if transport cannot be initialized according to arguments
        """
        ...
    
    def get_transport_info(self):
        """
        Get detailed connection information.
        Similar to getTransportInfo() in 'libros/transport/transport_tcp.cpp'
        e.g. TCPROS connection on port 41374 to [127.0.0.1:40623 on socket 6]
        """
        ...
    
    def fileno(self):
        """
        Get descriptor for select
        """
        ...
    
    def set_endpoint_id(self, endpoint_id):
        """
        Set the endpoint_id of this transport.
        Allows the endpoint_id to be set before the socket is initialized.
        """
        ...
    
    def set_socket(self, sock, endpoint_id):
        """
        Set the socket for this transport
        @param sock: socket
        @type  sock: socket.socket
        @param endpoint_id: identifier for connection endpoint
        @type  endpoint_id: str
        @raise TransportInitError: if socket has already been set
        """
        ...
    
    def connect(self, dest_addr, dest_port, endpoint_id, timeout=...):
        """
        Establish TCP connection to the specified
        address/port. connect() always calls L{write_header()} and
        L{read_header()} after the connection is made
        @param dest_addr: destination IP address
        @type  dest_addr: str
        @param dest_port: destination port
        @type  dest_port: int                
        @param endpoint_id: string identifier for connection (for statistics)
        @type  endpoint_id: str
        @param timeout: (optional keyword) timeout in seconds
        @type  timeout: float
        @raise TransportInitError: if unable to create connection
        """
        ...
    
    def write_header(self):
        """Writes the TCPROS header to the active connection."""
        ...
    
    def read_header(self):
        """
        Read TCPROS header from active socket
        @raise TransportInitError if header fails to validate
        """
        ...
    
    def send_message(self, msg, seq):
        """
        Convenience routine for services to send a message across a
        particular connection. NOTE: write_data is much more efficient
        if same message is being sent to multiple connections. Not
        threadsafe.
        @param msg: message to send
        @type  msg: Msg
        @param seq: sequence number for message
        @type  seq: int
        @raise TransportException: if error occurred sending message
        """
        ...
    
    def write_data(self, data):
        """
        Write raw data to transport
        @raise TransportInitialiationError: could not be initialized
        @raise TransportTerminated: no longer open for publishing
        """
        ...
    
    def receive_once(self):
        """
        block until messages are read off of socket
        @return: list of newly received messages
        @rtype: [Msg]
        @raise TransportException: if unable to receive message due to error
        """
        ...
    
    def receive_loop(self, msgs_callback):
        """
        Receive messages until shutdown
        @param msgs_callback: callback to invoke for new messages received    
        @type  msgs_callback: fn([msg])
        """
        ...
    
    def close(self):
        """close i/o and release resources"""
        ...
    

