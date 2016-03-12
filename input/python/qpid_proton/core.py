# Module core

# Core model

class Container(object):
    """
    A top-level container of connections, sessions, and links.
    
    A container gives a unique identity to each communicating
    peer.  It is often a process-level object.
    
    It serves as an entry point to the API, allowing connections
    and links to be established.  It can be supplied with an event
    handler in order to intercept important events, such as newly
    received messages or newly issued link credit for sending
    messages.
    """

    def __init__(self, handler=None, id=None):
        """
        Create a new container.

        :param handler: The main event handler for this container.
        :type handler: Handler
        :param id: Identifiers should be unique.  By default a UUID will be
        used.
        :type id: String
        :rtype: Container
        """

    def run(self):
        """
        Start processing events.  It returns when all connections
        and acceptors are closed or the container is stopped.

        """

    def stop(self):
        """
        Shutdown open connections and stop processing events.
        
        The operation is complete when on-stop fires.

        """

    def send(self, message, url):
        """
        Send a message.

        :type message: Message
        :type url: String
        :rtype: Delivery
        """

    def send_request(self, message, url):
        """
        Send a request message.  The message reply-to property is
        set automatically.

        :type message: Message
        :type url: String
        :rtype: Delivery
        """

    def send_response(self, message, request):
        """
        Send a response message.  The message to and
        correlation-id properties are set automatically.

        :type message: Message
        :type request: Message
        :rtype: Delivery
        """

    def connect(self, url, options=None):
        """
        Create and open an outbound connection.
        
        The operation is complete when on-connection-open fires.

        :type url: String
        :type options: ConnectionOptions
        :rtype: Connection
        """

    def listen(self, url, options=None):
        """
        Listen for incoming connections.
        
        The operation is complete when on-link-open fires.

        :type url: String
        :type options: ConnectionOptions
        :rtype: Acceptor
        """

    def open_receiver(self, url, options=None):
        """
        Create and open a receiving link.
        
        The operation is complete when on-link-open fires.

        :type url: String
        :type options: LinkOptions
        :rtype: Receiver
        """

    def open_sender(self, url, options=None):
        """
        Create and open a sending link.
        
        The operation is complete when on-link-open fires.

        :type url: String
        :type options: LinkOptions
        :rtype: Sender
        """

    def connections(self):
        """
        Get the connections inside this container.

        :rtype: Iterator
        """

    # End of class Container

class Client(Container):
    """
    A container that connects to a server.
    """

    def __init__(self, url, handler=None, id=None):
        """
        Create a new client.

        :param url: The host and port to connect to.
        :type url: String
        :param handler: The main event handler for this container.
        :type handler: Handler
        :param id: Identifiers should be unique.  By default a UUID will be
        used.
        :type id: String
        :rtype: Client
        """

    # End of class Client

class Server(Container):
    """
    A container that listens for client connections.
    """

    def __init__(self, url, handler=None, id=None):
        """
        Create a new server.

        :param url: The host and port to listen on.
        :type url: String
        :param handler: The main event handler for this container.
        :type handler: Handler
        :param id: Identifiers should be unique.  By default a UUID will be
        used.
        :type id: String
        :rtype: Server
        """

    # End of class Server

class Endpoint(object):
    """
    The base class for connection, session, and link.
    
    Every AMQP endpoint starts out in an uninitialized state and
    then proceeds linearly to an active and then closed state.
    This lifecycle occurs at both endpoints involved, and so the
    state model for an endpoint includes not only the known local
    state but also the last known state of the remote endpoint.
    
    The local and remote peers each maintain a set of
    corresponding local and remote endpoints.  Each peer evaluates
    and reconciles remote endpoint state changes as they are
    communicated over the wire.
    """

    # End of class Endpoint

class Connection(Endpoint):
    """
    A top-level channel for communication.
    
    In current implementations, a connection corresponds to a TCP
    connection, represented by a transport.
    
    A connection object contains zero or more session objects,
    which in turn contain zero or more link objects.  Each link
    object contains an ordered sequence of delivery objects.
    """

    def open(self, options=None):
        """
        Open the connection.
        
        The operation is complete when on-connection-open fires.

        :type options: ConnectionOptions
        """

    def close(self, condition=None):
        """
        Close the connection.
        
        The operation is complete when on-connection-close fires.

        :type condition: Condition
        """

    def send(self, message):
        """
        Send a message on the default session.

        :type message: Message
        :rtype: Delivery
        """

    def send_request(self, message):
        """
        Send a request message.  The message reply-to property is
        set automatically.

        :type message: Message
        :rtype: Delivery
        """

    def send_response(self, response_message, request_message):
        """
        Send a response message.  The message to and
        correlation-id properties are set automatically.

        :type response_message: Message
        :type request_message: Message
        :rtype: Delivery
        """

    def open_sender(self, address, options=None):
        """
        Create and open a sender using the default session.
        
        The operation is complete when on-link-open fires.

        :type address: String
        :type options: LinkOptions
        :rtype: Sender
        """

    def open_receiver(self, address, options=None):
        """
        Create and open a receiver using the default session.
        
        The operation is complete when on-link-open fires.

        :type address: String
        :type options: LinkOptions
        :rtype: Receiver
        """

    def open_session(self, options=None):
        """
        Create and open a session.

        :type options: SessionOptions
        :rtype: Session
        """

    def sessions(self):
        """
        Get the sessions contained in this connection.

        :rtype: Iterator
        """

    def links(self):
        """
        Get the links contained in this connection.

        :rtype: Iterator
        """

    def deliveries(self):
        """
        Get the deliveries contained in this connection.

        :rtype: Iterator
        """

    # End of class Connection

class Session(Endpoint):
    """
    A container of links.
    """

    def open(self, options=None):
        """
        Open the session.
        
        The operation is complete when on-session-open fires.

        :type options: SessionOptions
        """

    def close(self, condition=None):
        """
        Close the session.
        
        The operation is complete when on-session-close fires.

        :type condition: Condition
        """

    def send(self, message):
        """
        Send a message on a link with the given address.

        :type message: Message
        :rtype: Delivery
        """

    def send_request(self, message):
        """
        Send a request message.  The message.reply-to property is
        set automatically.

        :type message: Message
        :rtype: Delivery
        """

    def send_response(self, response_message, request_message):
        """
        Send a response message.  The message.to property is set
        automatically.

        :type response_message: Message
        :type request_message: Message
        :rtype: Delivery
        """

    def open_receiver(self, address, options=None):
        """
        Create and open a receiving link.
        
        The operation is complete when on-link-open fires.

        :type address: String
        :type options: LinkOptions
        :rtype: Receiver
        """

    def open_sender(self, address, options=None):
        """
        Create and open a sending link.
        
        The operation is complete when on-link-open fires.

        :type address: String
        :type options: LinkOptions
        :rtype: Sender
        """

    def links(self):
        """
        Get the links contained in this session.

        :rtype: Iterator
        """

    def deliveries(self):
        """
        Get the deliveries contained in this session.

        :rtype: Iterator
        """

    # End of class Session

class Link(Endpoint):
    """
    A channel for sending or receiving messages.  A link can be a sender
    or a receiver, but never both.  A link contains an ordered sequence
    of delivery objects.
    """

    def open(self, options=None):
        """
        Open the link.
        
        The operation is complete when on-link-open fires.

        :type options: LinkOptions
        """

    def close(self, condition=None):
        """
        Close the link.
        
        The operation is complete when on-link-close fires.

        :type condition: Condition
        """

    def detach(self, condition=None):
        """
        Detach the link without closing it.  For durable
        subscriptions this means the subscription is inactive but
        not canceled.
        
        The operation is complete when on-link-detach fires.

        :type condition: Condition
        """

    def deliveries(self):
        """
        Get the deliveries contained in this link.

        :rtype: Iterator
        """

    # End of class Link

class Receiver(Link):
    """
    A link for receiving messages.
    """

    def add_credit(self, count):
        """
        Issue credit to the sending end.  This increases the credit
        issued to the remote sender by the specified number of messages.

        :type count: Uint
        """

    def flush(self):
        """
        Request any messages available at the sending end.  This tells
        the sender to use all existing credit immediately to send
        deliveries and then discard any excess credit.
        
        The sending end is notified of the flush request by the
        *on-sender-flush* event.  The operation is complete when
        *on-receiver-flush* fires.

        """

    # End of class Receiver

class Sender(Link):
    """
    A link for sending messages.
    """

    def send(self, message):
        """
        Send a message on the link.

        :type message: Message
        :rtype: Delivery
        """

    def send_request(self, message):
        """
        Send a request message.  The message reply-to property is
        set automatically.

        :type message: Message
        :rtype: Delivery
        """

    def send_response(self, response, request):
        """
        Send a response message.  The message address and
        correlation-id properties are set automatically.

        :type response: Message
        :type request: Message
        :rtype: Delivery
        """

    # End of class Sender

class Terminus(object):
    """
    A source or target for messages.
    """

    # End of class Terminus

class Message(object):
    """
    A mutable holder of application content.
    """

    def __init__(self, body=None):
        """
        Create a new message.

        :type body: Object
        :rtype: Message
        """

    def clear(self):
        """
        Delete the content of the message.  All fields are reset to
        their default values.

        """

    def encode(self):
        """
        Encode the message to bytes.

        :rtype: Binary
        """

    def decode(self, bytes):
        """
        Decode the message from bytes.

        :type bytes: Binary
        """

    # End of class Message

class Delivery(object):
    """
    A message transfer.  Every delivery exists within the context
    of a link.
    
    A delivery attempt can fail.  As a result, a particular
    message may correspond to multiple deliveries.
    """

    def settle(self):
        """
        Mark the delivery settled.  A settled delivery can never
        be used again.

        """

    def accept(self):
        """
        Change the delivery state to ACCEPTED and settle.

        """

    def reject(self):
        """
        Change the delivery state to REJECTED and settle.

        """

    def release(self):
        """
        Change the delivery state to RELEASED and settle.

        """

    def modify(self):
        """
        Change the delivery state to MODIFIED and settle.

        """

    # End of class Delivery

class Condition(object):
    """
    An endpoint error state.
    """

    def __init__(self, name, description=None, properties=None):
        """
        Create a new condition.

        :type name: Symbol
        :type description: String
        :type properties: Map
        :rtype: Condition
        """

    # End of class Condition

# Configuration

class EndpointOptions(object):
    """
    The base class for connection-options, session-options, and
    link-options.
    """

    # End of class EndpointOptions

class ConnectionOptions(EndpointOptions):
    """
    Options for new connections.
    """

    def __init__(self):
        """
        Create a new connection-options instance.

        :rtype: ConnectionOptions
        """

    # End of class ConnectionOptions

class SessionOptions(EndpointOptions):
    """
    Options for new sessions.
    """

    def __init__(self):
        """
        Create a new session-options instance.

        :rtype: SessionOptions
        """

    # End of class SessionOptions

class LinkOptions(EndpointOptions):
    """
    Options for new links.
    """

    def __init__(self):
        """
        Create a new link-options instance.

        :rtype: LinkOptions
        """

    # End of class LinkOptions

class TerminusOptions(object):
    """
    Source and target options.
    """

    # End of class TerminusOptions

# Event processing

class Event(object):
    """
    The Proton event object.  It is passed to the methods on
    handler.
    """

    # End of class Event

class Handler(object):
    """
    The Proton event handler.  It allows users to intercept and
    change Proton behaviors.
    """

    def on_start(self, event, container):
        """
        The event loop is started.

        :type event: Event
        :type container: Container
        """

    def on_stop(self, event, container):
        """
        The event loop is stopped.

        :type event: Event
        :type container: Container
        """

    def on_message(self, event, message):
        """
        A message is received.

        :type event: Event
        :type message: Message
        """

    def on_sendable(self, event, sender):
        """
        A message can be sent.
        
        The sender has credit and messages can therefore be
        transferred.

        :type event: Event
        :type sender: Sender
        """

    def on_unhandled(self, event):
        """
        Fallback event handling.
        
        Called if an event handler function is not overriden to
        handle an event.

        :type event: Event
        """

    def on_unhandled_error(self, event, condition):
        """
        Fallback error handling.
        
        Called if an error handler function is not overriden to
        handle an error.

        :type event: Event
        :type condition: Condition
        """

    def on_connection_open(self, event, connection):
        """
        The remote peer opened the connection.

        :type event: Event
        :type connection: Connection
        """

    def on_connection_close(self, event, connection):
        """
        The remote peer closed the connection.

        :type event: Event
        :type connection: Connection
        """

    def on_connection_error(self, event, connection):
        """
        The remote peer closed the connection with an error
        condition.

        :type event: Event
        :type connection: Connection
        """

    def on_session_open(self, event, session):
        """
        The remote peer opened the session.

        :type event: Event
        :type session: Session
        """

    def on_session_close(self, event, session):
        """
        The remote peer closed the session.

        :type event: Event
        :type session: Session
        """

    def on_session_error(self, event, session):
        """
        The remote peer closed the session with an error
        condition.

        :type event: Event
        :type session: Session
        """

    def on_link_open(self, event, link):
        """
        The remote peer opened the link.

        :type event: Event
        :type link: Link
        """

    def on_link_detach(self, event, link):
        """
        The remote peer detached the link.

        :type event: Event
        :type link: Link
        """

    def on_link_close(self, event, link):
        """
        The remote peer closed the link.

        :type event: Event
        :type link: Link
        """

    def on_link_error(self, event, link):
        """
        The remote peer closed the link with an error condition.

        :type event: Event
        :type link: Link
        """

    def on_sender_flush(self, event, sender):
        """
        The remote end of the sender requested flushing.

        :type event: Event
        :type sender: Sender
        """

    def on_receiver_flush(self, event, receiver):
        """
        The remote end of the receiver finished flushing.

        :type event: Event
        :type receiver: Receiver
        """

    def on_delivery_accept(self, event, delivery):
        """
        The remote peer accepted an outgoing message.

        :type event: Event
        :type delivery: Delivery
        """

    def on_delivery_reject(self, event, delivery):
        """
        The remote peer rejected an outgoing message.
        
        XXX error condition

        :type event: Event
        :type delivery: Delivery
        """

    def on_delivery_release(self, event, delivery):
        """
        The remote peer released an outgoing message.  Note that
        this may be in response to either the RELEASE or MODIFIED
        state as defined by the AMQP specification.

        :type event: Event
        :type delivery: Delivery
        """

    def on_delivery_settle(self, event, delivery):
        """
        The remote peer settled an outgoing message.  This is the
        point at which it should never be retransmitted.

        :type event: Event
        :type delivery: Delivery
        """

    def on_transport_open(self, event, transport):
        """
        The underlying network channel opened.

        :type event: Event
        :type transport: Transport
        """

    def on_transport_close(self, event, transport):
        """
        The underlying network channel closed.

        :type event: Event
        :type transport: Transport
        """

    def on_transport_error(self, event, transport):
        """
        The underlying network channel closed with an error
        condition.

        :type event: Event
        :type transport: Transport
        """

    # End of class Handler

# Network

class Transport(object):
    """
    A network channel supporting an AMQP connection.
    """

    # End of class Transport

class Acceptor(object):
    """
    A context for accepting inbound connections.
    """

    def close(self):
        """
        Close the acceptor.

        """

    # End of class Acceptor

class Sasl(object):
    """
    SASL properties for a connection.
    """

    # End of class Sasl

class Ssl(object):
    """
    SSL properties for a connection.
    """

    # End of class Ssl

# Error handling

class ProtonError(object):
    """
    The base class for Proton errors.
    """

    # End of class ProtonError

class TimeoutError(ProtonError):
    """
    An operation timed out.
    """

    # End of class TimeoutError

class ConversionError(ProtonError):
    """
    A type conversion failed.
    """

    # End of class ConversionError

# End of module core
