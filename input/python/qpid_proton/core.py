# Module core

import _qpid_proton_impl.core as _core

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
        :type id: str
        :rtype: Container
        """

        self._impl = _core.Container(handler, id)

    @property
    def id(self):
        """
        A globally unique container identifier.  It is used to
        identify this container in any connections it establishes.
        """

        return self._impl.id

    @property
    def client_connection_options(self):
        """
        Default options for new outbound connections.
        """

        return self._impl.client_connection_options

    @property
    def server_connection_options(self):
        """
        Default options for new inbound connections.
        """

        return self._impl.server_connection_options

    @property
    def session_options(self):
        """
        Default options for new sessions.
        """

        return self._impl.session_options

    @property
    def link_options(self):
        """
        Default options for new links.
        """

        return self._impl.link_options

    def run(self):
        """
        Start processing events.  It returns when all connections
        and acceptors are closed or the container is stopped.

        """

        return self._impl.run()

    def stop(self):
        """
        Shutdown open connections and stop processing events.
        
        The operation is complete when on-stop fires.

        """

        return self._impl.stop()

    def send(self, message, url):
        """
        Send a message.

        :type message: Message
        :type url: str
        :rtype: Delivery
        """

        return self._impl.send(message, url)

    def send_request(self, message, url):
        """
        Send a request message.  The message reply-to property is
        set automatically.

        :type message: Message
        :type url: str
        :rtype: Delivery
        """

        return self._impl.send_request(message, url)

    def send_response(self, message, request):
        """
        Send a response message.  The message to and
        correlation-id properties are set automatically.

        :type message: Message
        :type request: Message
        :rtype: Delivery
        """

        return self._impl.send_response(message, request)

    def connect(self, url, options=None):
        """
        Create and open an outbound connection.
        
        The operation is complete when on-connection-open fires.

        :type url: str
        :type options: ConnectionOptions
        :rtype: Connection
        """

        return self._impl.connect(url, options)

    def listen(self, url, options=None):
        """
        Listen for incoming connections.
        
        The operation is complete when on-link-open fires.

        :type url: str
        :type options: ConnectionOptions
        :rtype: Acceptor
        """

        return self._impl.listen(url, options)

    def open_receiver(self, url, options=None):
        """
        Create and open a receiving link.
        
        The operation is complete when on-link-open fires.

        :type url: str
        :type options: LinkOptions
        :rtype: Receiver
        """

        return self._impl.open_receiver(url, options)

    def open_sender(self, url, options=None):
        """
        Create and open a sending link.
        
        The operation is complete when on-link-open fires.

        :type url: str
        :type options: LinkOptions
        :rtype: Sender
        """

        return self._impl.open_sender(url, options)

    def connections(self):
        """
        Get the connections inside this container.

        :rtype: object
        """

        return self._impl.connections()

    # End of class Container

class Client(Container):
    """
    A container that connects to a server.
    """

    def __init__(self, url, handler=None, id=None):
        """
        Create a new client.

        :param url: The host and port to connect to.
        :type url: str
        :param handler: The main event handler for this container.
        :type handler: Handler
        :param id: Identifiers should be unique.  By default a UUID will be
        used.
        :type id: str
        :rtype: Client
        """

        self._impl = _core.Client(url, handler, id)

    # End of class Client

class Server(Container):
    """
    A container that listens for client connections.
    """

    def __init__(self, url, handler=None, id=None):
        """
        Create a new server.

        :param url: The host and port to listen on.
        :type url: str
        :param handler: The main event handler for this container.
        :type handler: Handler
        :param id: Identifiers should be unique.  By default a UUID will be
        used.
        :type id: str
        :rtype: Server
        """

        self._impl = _core.Server(url, handler, id)

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

    def __init__(self):
        self._impl = _core.Endpoint()

    @property
    def local_uninitialized(self):
        """
        The local endpoint is uninitialized.
        """

        return self._impl.local_uninitialized

    @property
    def remote_uninitialized(self):
        """
        The remote endpoint is uninitialized.
        """

        return self._impl.remote_uninitialized

    @property
    def local_active(self):
        """
        The local endpoint is active.
        """

        return self._impl.local_active

    @property
    def remote_active(self):
        """
        The remote endpoint is active.
        """

        return self._impl.remote_active

    @property
    def local_closed(self):
        """
        The local endpoint is closed.
        """

        return self._impl.local_closed

    @property
    def remote_closed(self):
        """
        The remote endpoint is closed.
        """

        return self._impl.remote_closed

    @property
    def remote_condition(self):
        """
        The error condition of the remote peer.
        """

        return self._impl.remote_condition

    @property
    def remote_properties(self):
        """
        Application properties defined by the remote peer.
        """

        return self._impl.remote_properties

    @property
    def remote_offered_capabilities(self):
        """
        Extensions the remote peer supports.
        """

        return self._impl.remote_offered_capabilities

    @property
    def remote_desired_capabilities(self):
        """
        Extensions the remote peer can use.
        """

        return self._impl.remote_desired_capabilities

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

    def __init__(self):
        self._impl = _core.Connection()

    @property
    def transport(self):
        """
        The associated transport.
        """

        return self._impl.transport

    @property
    def default_session(self):
        """
        The session used by open-sender and open-receiver.
        """

        return self._impl.default_session

    @property
    def remote_container_id(self):
        """
        The unique identity of the remote container.
        """

        return self._impl.remote_container_id

    @property
    def remote_virtual_host(self):
        """
        The virtual host name of the remote peer.
        """

        return self._impl.remote_virtual_host

    @property
    def remote_user(self):
        """
        The user name for authentication.
        """

        return self._impl.remote_user

    @property
    def remote_idle_timeout(self):
        """
        The idle timeout of the remote peer.
        """

        return self._impl.remote_idle_timeout

    @property
    def remote_max_sessions(self):
        """
        The maximum active sessions allowed by the remote peer.
        """

        return self._impl.remote_max_sessions

    @property
    def remote_max_frame_size(self):
        """
        The maximum frame size allowed by the remote peer.
        """

        return self._impl.remote_max_frame_size

    def open(self, options=None):
        """
        Open the connection.
        
        The operation is complete when on-connection-open fires.

        :type options: ConnectionOptions
        """

        return self._impl.open(options)

    def close(self, condition=None):
        """
        Close the connection.
        
        The operation is complete when on-connection-close fires.

        :type condition: Condition
        """

        return self._impl.close(condition)

    def send(self, message):
        """
        Send a message on the default session.

        :type message: Message
        :rtype: Delivery
        """

        return self._impl.send(message)

    def send_request(self, message):
        """
        Send a request message.  The message reply-to property is
        set automatically.

        :type message: Message
        :rtype: Delivery
        """

        return self._impl.send_request(message)

    def send_response(self, response_message, request_message):
        """
        Send a response message.  The message to and
        correlation-id properties are set automatically.

        :type response_message: Message
        :type request_message: Message
        :rtype: Delivery
        """

        return self._impl.send_response(response_message, request_message)

    def open_sender(self, address, options=None):
        """
        Create and open a sender using the default session.
        
        The operation is complete when on-link-open fires.

        :type address: str
        :type options: LinkOptions
        :rtype: Sender
        """

        return self._impl.open_sender(address, options)

    def open_receiver(self, address, options=None):
        """
        Create and open a receiver using the default session.
        
        The operation is complete when on-link-open fires.

        :type address: str
        :type options: LinkOptions
        :rtype: Receiver
        """

        return self._impl.open_receiver(address, options)

    def open_session(self, options=None):
        """
        Create and open a session.

        :type options: SessionOptions
        :rtype: Session
        """

        return self._impl.open_session(options)

    def sessions(self):
        """
        Get the sessions contained in this connection.

        :rtype: object
        """

        return self._impl.sessions()

    def links(self):
        """
        Get the links contained in this connection.

        :rtype: object
        """

        return self._impl.links()

    def deliveries(self):
        """
        Get the deliveries contained in this connection.

        :rtype: object
        """

        return self._impl.deliveries()

    # End of class Connection

class Session(Endpoint):
    """
    A container of links.
    """

    def __init__(self):
        self._impl = _core.Session()

    @property
    def connection(self):
        """
        The containing connection.
        """

        return self._impl.connection

    @property
    def incoming_bytes(self):
        """
        The number of incoming bytes currently buffered.
        """

        return self._impl.incoming_bytes

    @property
    def outgoing_bytes(self):
        """
        The number of outgoing bytes currently buffered.
        """

        return self._impl.outgoing_bytes

    @property
    def remote_incoming_window(self):
        """
        The remote peer's max number of incoming transfer frames.
        """

        return self._impl.remote_incoming_window

    @property
    def remote_outgoing_window(self):
        """
        The remote peer's max number of outgoing transfer frames.
        """

        return self._impl.remote_outgoing_window

    def open(self, options=None):
        """
        Open the session.
        
        The operation is complete when on-session-open fires.

        :type options: SessionOptions
        """

        return self._impl.open(options)

    def close(self, condition=None):
        """
        Close the session.
        
        The operation is complete when on-session-close fires.

        :type condition: Condition
        """

        return self._impl.close(condition)

    def send(self, message):
        """
        Send a message on a link with the given address.

        :type message: Message
        :rtype: Delivery
        """

        return self._impl.send(message)

    def send_request(self, message):
        """
        Send a request message.  The message.reply-to property is
        set automatically.

        :type message: Message
        :rtype: Delivery
        """

        return self._impl.send_request(message)

    def send_response(self, response_message, request_message):
        """
        Send a response message.  The message.to property is set
        automatically.

        :type response_message: Message
        :type request_message: Message
        :rtype: Delivery
        """

        return self._impl.send_response(response_message, request_message)

    def open_receiver(self, address, options=None):
        """
        Create and open a receiving link.
        
        The operation is complete when on-link-open fires.

        :type address: str
        :type options: LinkOptions
        :rtype: Receiver
        """

        return self._impl.open_receiver(address, options)

    def open_sender(self, address, options=None):
        """
        Create and open a sending link.
        
        The operation is complete when on-link-open fires.

        :type address: str
        :type options: LinkOptions
        :rtype: Sender
        """

        return self._impl.open_sender(address, options)

    def links(self):
        """
        Get the links contained in this session.

        :rtype: object
        """

        return self._impl.links()

    def deliveries(self):
        """
        Get the deliveries contained in this session.

        :rtype: object
        """

        return self._impl.deliveries()

    # End of class Session

class Link(Endpoint):
    """
    A channel for sending or receiving messages.  A link can be a sender
    or a receiver, but never both.  A link contains an ordered sequence
    of delivery objects.
    """

    def __init__(self):
        self._impl = _core.Link()

    @property
    def type(self):
        """
        SENDER or RECEIVER.
        """

        return self._impl.type

    @property
    def session(self):
        """
        The containing session.
        """

        return self._impl.session

    @property
    def name(self):
        """
        The link name.
        """

        return self._impl.name

    @property
    def credit(self):
        """
        The number of messages the receiving end can accept.
        """

        return self._impl.credit

    @property
    def remote_source(self):
        """
        The properties of the link source at the remote peer.
        """

        return self._impl.remote_source

    @property
    def remote_target(self):
        """
        The properties of the link target at the remote peer.
        """

        return self._impl.remote_target

    @property
    def remote_delivery_mode(self):
        """
        The message delivery guarantee at the remote peer.
        """

        return self._impl.remote_delivery_mode

    @property
    def remote_max_message_size(self):
        """
        The maximum message size allowed by the remote peer.
        """

        return self._impl.remote_max_message_size

    def open(self, options=None):
        """
        Open the link.
        
        The operation is complete when on-link-open fires.

        :type options: LinkOptions
        """

        return self._impl.open(options)

    def close(self, condition=None):
        """
        Close the link.
        
        The operation is complete when on-link-close fires.

        :type condition: Condition
        """

        return self._impl.close(condition)

    def detach(self, condition=None):
        """
        Detach the link without closing it.  For durable
        subscriptions this means the subscription is inactive but
        not canceled.
        
        The operation is complete when on-link-detach fires.

        :type condition: Condition
        """

        return self._impl.detach(condition)

    def deliveries(self):
        """
        Get the deliveries contained in this link.

        :rtype: object
        """

        return self._impl.deliveries()

    # End of class Link

class Receiver(Link):
    """
    A link for receiving messages.
    """

    def __init__(self):
        self._impl = _core.Receiver()

    def add_credit(self, count):
        """
        Issue credit to the sending end.  This increases the credit
        issued to the remote sender by the specified number of messages.

        :type count: long
        """

        return self._impl.add_credit(count)

    def flush(self):
        """
        Request any messages available at the sending end.  This tells
        the sender to use all existing credit immediately to send
        deliveries and then discard any excess credit.
        
        The sending end is notified of the flush request by the
        *on-sender-flush* event.  The operation is complete when
        *on-receiver-flush* fires.

        """

        return self._impl.flush()

    # End of class Receiver

class Sender(Link):
    """
    A link for sending messages.
    """

    def __init__(self):
        self._impl = _core.Sender()

    def send(self, message):
        """
        Send a message on the link.

        :type message: Message
        :rtype: Delivery
        """

        return self._impl.send(message)

    def send_request(self, message):
        """
        Send a request message.  The message reply-to property is
        set automatically.

        :type message: Message
        :rtype: Delivery
        """

        return self._impl.send_request(message)

    def send_response(self, response, request):
        """
        Send a response message.  The message address and
        correlation-id properties are set automatically.

        :type response: Message
        :type request: Message
        :rtype: Delivery
        """

        return self._impl.send_response(response, request)

    # End of class Sender

class Terminus(object):
    """
    A source or target for messages.
    """

    def __init__(self):
        self._impl = _core.Terminus()

    @property
    def type(self):
        """
        SOURCE or TARGET.
        """

        return self._impl.type

    @property
    def address(self):
        """
        The address of the message source or target.
        """

        return self._impl.address

    @property
    def durability_mode(self):
        """
        The persistence mode of the source or target.
        """

        return self._impl.durability_mode

    @property
    def distribution_mode(self):
        """
        The message distribution mode at the remote peer.  This is a
        source-only option.
        """

        return self._impl.distribution_mode

    @property
    def filters(self):
        """
        Filters set by the remote peer.  This is a source-only option.
        """

        return self._impl.filters

    @property
    def dynamic(self):
        """
        On-demand creation of a source or target at the remote peer.
        """

        return self._impl.dynamic

    @property
    def properties(self):
        """
        The properties of a dynamic source or target.
        """

        return self._impl.properties

    @property
    def timeout(self):
        """
        The period after which the source or target is discarded.
        """

        return self._impl.timeout

    @property
    def expiry_policy(self):
        """
        When expiration of the source or target begins.
        """

        return self._impl.expiry_policy

    @property
    def capabilities(self):
        """
        Extensions supported or desired.
        """

        return self._impl.capabilities

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

        self._impl = _core.Message(body)

    @property
    def id(self):
        """
        A globally unique message identifier.
        
        **XXX List legal types**
        
        **XXX Used to remove duplicates**
        """

        return self._impl.id

    @id.setter
    def id(self, value):
        self._impl.id = value

    @property
    def user(self):
        """
        The identity of the user producing the message.
        """

        return self._impl.user

    @user.setter
    def user(self, value):
        self._impl.user = value

    @property
    def to(self):
        """
        The destination address.
        """

        return self._impl.to

    @to.setter
    def to(self, value):
        self._impl.to = value

    @property
    def reply_to(self):
        """
        The address for replies.
        """

        return self._impl.reply_to

    @reply_to.setter
    def reply_to(self, value):
        self._impl.reply_to = value

    @property
    def correlation_id(self):
        """
        An identifier for matching related messages.
        """

        return self._impl.correlation_id

    @correlation_id.setter
    def correlation_id(self, value):
        self._impl.correlation_id = value

    @property
    def subject(self):
        """
        Summary information.
        """

        return self._impl.subject

    @subject.setter
    def subject(self, value):
        self._impl.subject = value

    @property
    def body(self):
        """
        The main message content.
        """

        return self._impl.body

    @body.setter
    def body(self, value):
        self._impl.body = value

    @property
    def content_type(self):
        """
        The MIME type of the body.
        """

        return self._impl.content_type

    @content_type.setter
    def content_type(self, value):
        self._impl.content_type = value

    @property
    def content_encoding(self):
        """
        The encoding of the body.
        """

        return self._impl.content_encoding

    @content_encoding.setter
    def content_encoding(self, value):
        self._impl.content_encoding = value

    @property
    def expiry_time(self):
        """
        The absolute time past which the message should be discarded.
        """

        return self._impl.expiry_time

    @expiry_time.setter
    def expiry_time(self, value):
        self._impl.expiry_time = value

    @property
    def creation_time(self):
        """
        The absolute time of message creation.
        """

        return self._impl.creation_time

    @creation_time.setter
    def creation_time(self, value):
        self._impl.creation_time = value

    @property
    def inferred(self):
        """
        Determine the AMQP section type from the body type.
        """

        return self._impl.inferred

    @inferred.setter
    def inferred(self, value):
        self._impl.inferred = value

    @property
    def durable(self):
        """
        Durability requirement.  The durable property indicates
        that the message should be held durably by any
        intermediaries taking responsibility for the message.  A
        durable message is saved even if the intermediary is
        unexpectedly terminated and restarted.
        """

        return self._impl.durable

    @durable.setter
    def durable(self, value):
        self._impl.durable = value

    @property
    def priority(self):
        """
        Relative message priority.  Higher numbers indicate higher
        priority.
        """

        return self._impl.priority

    @priority.setter
    def priority(self, value):
        self._impl.priority = value

    @property
    def ttl(self):
        """
        The time to live.  The message must be discarded after
        'ttl' milliseconds.
        """

        return self._impl.ttl

    @ttl.setter
    def ttl(self, value):
        self._impl.ttl = value

    @property
    def first_acquirer(self):
        """
        The recipient is first to acquire the message.
        """

        return self._impl.first_acquirer

    @first_acquirer.setter
    def first_acquirer(self, value):
        self._impl.first_acquirer = value

    @property
    def delivery_count(self):
        """
        The number of prior unsuccessful delivery attempts.
        """

        return self._impl.delivery_count

    @delivery_count.setter
    def delivery_count(self, value):
        self._impl.delivery_count = value

    @property
    def group_id(self):
        """
        The identifier of the group the message belongs to.
        """

        return self._impl.group_id

    @group_id.setter
    def group_id(self, value):
        self._impl.group_id = value

    @property
    def group_sequence(self):
        """
        The relative position of this message within its group.
        """

        return self._impl.group_sequence

    @group_sequence.setter
    def group_sequence(self, value):
        self._impl.group_sequence = value

    @property
    def reply_to_group_id(self):
        """
        The group a reply message belongs to.
        """

        return self._impl.reply_to_group_id

    @reply_to_group_id.setter
    def reply_to_group_id(self, value):
        self._impl.reply_to_group_id = value

    @property
    def properties(self):
        """
        Application-defined message attributes.
        """

        return self._impl.properties

    @properties.setter
    def properties(self, value):
        self._impl.properties = value

    @property
    def delivery_annotations(self):
        """
        Delivery-specific transport attributes.
        """

        return self._impl.delivery_annotations

    @delivery_annotations.setter
    def delivery_annotations(self, value):
        self._impl.delivery_annotations = value

    @property
    def message_annotations(self):
        """
        Message-specific transport attributes.
        """

        return self._impl.message_annotations

    @message_annotations.setter
    def message_annotations(self, value):
        self._impl.message_annotations = value

    @property
    def footer(self):
        """
        Transport attributes that can only be evaluated after the
        whole message has been seen.
        """

        return self._impl.footer

    @footer.setter
    def footer(self, value):
        self._impl.footer = value

    def clear(self):
        """
        Delete the content of the message.  All fields are reset to
        their default values.

        """

        return self._impl.clear()

    def encode(self):
        """
        Encode the message to bytes.

        :rtype: bytes
        """

        return self._impl.encode()

    def decode(self, bytes):
        """
        Decode the message from bytes.

        :type bytes: bytes
        """

        return self._impl.decode(bytes)

    # End of class Message

class Delivery(object):
    """
    A message transfer.  Every delivery exists within the context
    of a link.
    
    A delivery attempt can fail.  As a result, a particular
    message may correspond to multiple deliveries.
    """

    def __init__(self):
        self._impl = _core.Delivery()

    @property
    def id(self):
        """
        The delivery identifier.
        """

        return self._impl.id

    @property
    def link(self):
        """
        The link on which the delivery was sent or received.
        """

        return self._impl.link

    @property
    def local_settled(self):
        """
        True if the delivery has been settled locally.
        """

        return self._impl.local_settled

    @property
    def remote_settled(self):
        """
        True if the delivery has been settled by the remote peer.
        """

        return self._impl.remote_settled

    @property
    def local_state(self):
        """
        The local delivery state.
        """

        return self._impl.local_state

    @property
    def remote_state(self):
        """
        The delivery state at the remote peer.
        """

        return self._impl.remote_state

    @property
    def updated(self):
        """
        
        """

        return self._impl.updated

    @property
    def readable(self):
        """
        
        """

        return self._impl.readable

    @property
    def writable(self):
        """
        
        """

        return self._impl.writable

    def settle(self):
        """
        Mark the delivery settled.  A settled delivery can never
        be used again.

        """

        return self._impl.settle()

    def accept(self):
        """
        Change the delivery state to ACCEPTED and settle.

        """

        return self._impl.accept()

    def reject(self):
        """
        Change the delivery state to REJECTED and settle.

        """

        return self._impl.reject()

    def release(self):
        """
        Change the delivery state to RELEASED and settle.

        """

        return self._impl.release()

    def modify(self):
        """
        Change the delivery state to MODIFIED and settle.

        """

        return self._impl.modify()

    # End of class Delivery

class Condition(object):
    """
    An endpoint error state.
    """

    def __init__(self, name, description=None, properties=None):
        """
        Create a new condition.

        :type name: str
        :type description: str
        :type properties: dict
        :rtype: Condition
        """

        self._impl = _core.Condition(name, description, properties)

    @property
    def name(self):
        """
        The AMQP condition name.
        """

        return self._impl.name

    @name.setter
    def name(self, value):
        self._impl.name = value

    @property
    def description(self):
        """
        A message describing the condition.
        """

        return self._impl.description

    @description.setter
    def description(self, value):
        self._impl.description = value

    @property
    def properties(self):
        """
        Extra properties of the condition.
        """

        return self._impl.properties

    @properties.setter
    def properties(self, value):
        self._impl.properties = value

    # End of class Condition

class LinkType(object):
    pass

LinkType.SENDER = LinkType()
LinkType.RECEIVER = LinkType()

class TerminusType(object):
    pass

TerminusType.SOURCE = TerminusType()
TerminusType.TARGET = TerminusType()

class DeliveryState(object):
    pass

DeliveryState.NONE = DeliveryState()
DeliveryState.RECEIVED = DeliveryState()
DeliveryState.ACCEPTED = DeliveryState()
DeliveryState.REJECTED = DeliveryState()
DeliveryState.RELEASED = DeliveryState()
DeliveryState.MODIFIED = DeliveryState()

# Configuration

class EndpointOptions(object):
    """
    The base class for connection-options, session-options, and
    link-options.
    """

    def __init__(self):
        self._impl = _core.EndpointOptions()

    @property
    def properties(self):
        """
        Application properties defined by the local endpoint.
        """

        return self._impl.properties

    @properties.setter
    def properties(self, value):
        self._impl.properties = value

    @property
    def offered_capabilities(self):
        """
        Extensions the local endpoint supports.
        """

        return self._impl.offered_capabilities

    @offered_capabilities.setter
    def offered_capabilities(self, value):
        self._impl.offered_capabilities = value

    @property
    def desired_capabilities(self):
        """
        Extensions the local endpoint can use.
        """

        return self._impl.desired_capabilities

    @desired_capabilities.setter
    def desired_capabilities(self, value):
        self._impl.desired_capabilities = value

    @property
    def handler(self):
        """
        The event handler for the endpoint.
        """

        return self._impl.handler

    @handler.setter
    def handler(self, value):
        self._impl.handler = value

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

        self._impl = _core.ConnectionOptions()

    @property
    def container_id(self):
        """
        The connection container identifier.
        """

        return self._impl.container_id

    @container_id.setter
    def container_id(self, value):
        self._impl.container_id = value

    @property
    def virtual_host(self):
        """
        The virtual host name.
        """

        return self._impl.virtual_host

    @virtual_host.setter
    def virtual_host(self, value):
        self._impl.virtual_host = value

    @property
    def user(self):
        """
        The user name for authentication.
        """

        return self._impl.user

    @user.setter
    def user(self, value):
        self._impl.user = value

    @property
    def password(self):
        """
        The user's authentication secret.
        """

        return self._impl.password

    @password.setter
    def password(self, value):
        self._impl.password = value

    @property
    def sasl_enabled(self):
        """
        Enable or disable the SASL security layer.
        """

        return self._impl.sasl_enabled

    @sasl_enabled.setter
    def sasl_enabled(self, value):
        self._impl.sasl_enabled = value

    @property
    def sasl_allow_insecure_mechs(self):
        """
        Allow or deny clear-text authentication mechanisms.
        """

        return self._impl.sasl_allow_insecure_mechs

    @sasl_allow_insecure_mechs.setter
    def sasl_allow_insecure_mechs(self, value):
        self._impl.sasl_allow_insecure_mechs = value

    @property
    def sasl_allowed_mechs(self):
        """
        The SASL mechanisms the local peer permits.  The value is a
        space-separated string of mechanism names.
        """

        return self._impl.sasl_allowed_mechs

    @sasl_allowed_mechs.setter
    def sasl_allowed_mechs(self, value):
        self._impl.sasl_allowed_mechs = value

    @property
    def idle_timeout(self):
        """
        Expire the connection after a period of inactivity.
        """

        return self._impl.idle_timeout

    @idle_timeout.setter
    def idle_timeout(self, value):
        self._impl.idle_timeout = value

    @property
    def max_sessions(self):
        """
        Limit the number of active sessions.
        """

        return self._impl.max_sessions

    @max_sessions.setter
    def max_sessions(self, value):
        self._impl.max_sessions = value

    @property
    def max_frame_size(self):
        """
        Limit the size of AMQP frames.
        """

        return self._impl.max_frame_size

    @max_frame_size.setter
    def max_frame_size(self, value):
        self._impl.max_frame_size = value

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

        self._impl = _core.SessionOptions()

    @property
    def incoming_capacity(self):
        """
        Control the number of incoming bytes the session will buffer.
        """

        return self._impl.incoming_capacity

    @incoming_capacity.setter
    def incoming_capacity(self, value):
        self._impl.incoming_capacity = value

    @property
    def max_links(self):
        """
        Limit the number of links on this session.
        """

        return self._impl.max_links

    @max_links.setter
    def max_links(self, value):
        self._impl.max_links = value

    @property
    def incoming_window(self):
        """
        Limit the number of incoming transfer frames.
        """

        return self._impl.incoming_window

    @incoming_window.setter
    def incoming_window(self, value):
        self._impl.incoming_window = value

    @property
    def outgoing_window(self):
        """
        Limit the number of outgoing transfer frames.
        """

        return self._impl.outgoing_window

    @outgoing_window.setter
    def outgoing_window(self, value):
        self._impl.outgoing_window = value

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

        self._impl = _core.LinkOptions()

    @property
    def source(self):
        """
        Options for the link source.
        """

        return self._impl.source

    @property
    def target(self):
        """
        Options for the link target.
        """

        return self._impl.target

    @property
    def delivery_mode(self):
        """
        Control the message delivery guarantee.
        """

        return self._impl.delivery_mode

    @delivery_mode.setter
    def delivery_mode(self, value):
        self._impl.delivery_mode = value

    @property
    def name(self):
        """
        The name of the link.
        """

        return self._impl.name

    @name.setter
    def name(self, value):
        self._impl.name = value

    @property
    def message_window(self):
        """
        Maintain credit for the given number of messages.
        """

        return self._impl.message_window

    @message_window.setter
    def message_window(self, value):
        self._impl.message_window = value

    @property
    def max_message_size(self):
        """
        Limit the size of messages on the link.
        """

        return self._impl.max_message_size

    @max_message_size.setter
    def max_message_size(self, value):
        self._impl.max_message_size = value

    # End of class LinkOptions

class TerminusOptions(object):
    """
    Source and target options.
    """

    def __init__(self):
        self._impl = _core.TerminusOptions()

    @property
    def address(self):
        """
        The address of the message source or target.
        """

        return self._impl.address

    @address.setter
    def address(self, value):
        self._impl.address = value

    @property
    def durability_mode(self):
        """
        Control the persistence of source or target state.
        """

        return self._impl.durability_mode

    @durability_mode.setter
    def durability_mode(self, value):
        self._impl.durability_mode = value

    @property
    def distribution_mode(self):
        """
        Control whether messsages are browsed or consumed.  This
        is a receiver-only option.
        """

        return self._impl.distribution_mode

    @distribution_mode.setter
    def distribution_mode(self, value):
        self._impl.distribution_mode = value

    @property
    def filters(self):
        """
        Select messages by criteria.
        """

        return self._impl.filters

    @filters.setter
    def filters(self, value):
        self._impl.filters = value

    @property
    def dynamic(self):
        """
        Request on-demand creation of a node at the remote peer.
        """

        return self._impl.dynamic

    @dynamic.setter
    def dynamic(self, value):
        self._impl.dynamic = value

    @property
    def properties(self):
        """
        Control the properties of nodes created on demand.
        """

        return self._impl.properties

    @properties.setter
    def properties(self, value):
        self._impl.properties = value

    @property
    def timeout(self):
        """
        The period after which the source or target is discarded.
        """

        return self._impl.timeout

    @timeout.setter
    def timeout(self, value):
        self._impl.timeout = value

    @property
    def expiry_policy(self):
        """
        Control when the clock for expiration begins.
        """

        return self._impl.expiry_policy

    @expiry_policy.setter
    def expiry_policy(self, value):
        self._impl.expiry_policy = value

    @property
    def capabilities(self):
        """
        Extensions supported or desired.
        """

        return self._impl.capabilities

    @capabilities.setter
    def capabilities(self, value):
        self._impl.capabilities = value

    # End of class TerminusOptions

class DeliveryMode(object):
    pass

DeliveryMode.AT_MOST_ONCE = DeliveryMode()
DeliveryMode.AT_LEAST_ONCE = DeliveryMode()
DeliveryMode.EXACTLY_ONCE = DeliveryMode()

class DistributionMode(object):
    pass

DistributionMode.COPY = DistributionMode()
DistributionMode.MOVE = DistributionMode()

class DurabilityMode(object):
    pass

DurabilityMode.NONE = DurabilityMode()
DurabilityMode.CONFIGURATION = DurabilityMode()
DurabilityMode.UNSETTLED_STATE = DurabilityMode()

class ExpiryPolicy(object):
    pass

ExpiryPolicy.LINK_CLOSE = ExpiryPolicy()
ExpiryPolicy.SESSION_CLOSE = ExpiryPolicy()
ExpiryPolicy.CONNECTION_CLOSE = ExpiryPolicy()
ExpiryPolicy.NEVER = ExpiryPolicy()

# Event processing

class Event(object):
    """
    The Proton event object.  It is passed to the methods on
    handler.
    """

    def __init__(self):
        self._impl = _core.Event()

    @property
    def container(self):
        """
        Get the container.
        """

        return self._impl.container

    @property
    def connection(self):
        """
        Get the connection.
        """

        return self._impl.connection

    @property
    def session(self):
        """
        Get the session.
        """

        return self._impl.session

    @property
    def link(self):
        """
        Get the link.
        """

        return self._impl.link

    @property
    def sender(self):
        """
        Get the sender.
        """

        return self._impl.sender

    @property
    def receiver(self):
        """
        Get the receiver.
        """

        return self._impl.receiver

    @property
    def delivery(self):
        """
        Get the delivery.
        """

        return self._impl.delivery

    @property
    def transport(self):
        """
        Get the transport.
        """

        return self._impl.transport

    # End of class Event

class Handler(object):
    """
    The Proton event handler.  It allows users to intercept and
    change Proton behaviors.
    """

    def __init__(self):
        self._impl = _core.Handler()

    def on_start(self, event, container):
        """
        The event loop is started.

        :type event: Event
        :type container: Container
        """

        return self._impl.on_start(event, container)

    def on_stop(self, event, container):
        """
        The event loop is stopped.

        :type event: Event
        :type container: Container
        """

        return self._impl.on_stop(event, container)

    def on_message(self, event, message):
        """
        A message is received.

        :type event: Event
        :type message: Message
        """

        return self._impl.on_message(event, message)

    def on_sendable(self, event, sender):
        """
        A message can be sent.
        
        The sender has credit and messages can therefore be
        transferred.

        :type event: Event
        :type sender: Sender
        """

        return self._impl.on_sendable(event, sender)

    def on_unhandled(self, event):
        """
        Fallback event handling.
        
        Called if an event handler function is not overriden to
        handle an event.

        :type event: Event
        """

        return self._impl.on_unhandled(event)

    def on_unhandled_error(self, event, condition):
        """
        Fallback error handling.
        
        Called if an error handler function is not overriden to
        handle an error.

        :type event: Event
        :type condition: Condition
        """

        return self._impl.on_unhandled_error(event, condition)

    def on_connection_open(self, event, connection):
        """
        The remote peer opened the connection.

        :type event: Event
        :type connection: Connection
        """

        return self._impl.on_connection_open(event, connection)

    def on_connection_close(self, event, connection):
        """
        The remote peer closed the connection.

        :type event: Event
        :type connection: Connection
        """

        return self._impl.on_connection_close(event, connection)

    def on_connection_error(self, event, connection):
        """
        The remote peer closed the connection with an error
        condition.

        :type event: Event
        :type connection: Connection
        """

        return self._impl.on_connection_error(event, connection)

    def on_session_open(self, event, session):
        """
        The remote peer opened the session.

        :type event: Event
        :type session: Session
        """

        return self._impl.on_session_open(event, session)

    def on_session_close(self, event, session):
        """
        The remote peer closed the session.

        :type event: Event
        :type session: Session
        """

        return self._impl.on_session_close(event, session)

    def on_session_error(self, event, session):
        """
        The remote peer closed the session with an error
        condition.

        :type event: Event
        :type session: Session
        """

        return self._impl.on_session_error(event, session)

    def on_link_open(self, event, link):
        """
        The remote peer opened the link.

        :type event: Event
        :type link: Link
        """

        return self._impl.on_link_open(event, link)

    def on_link_detach(self, event, link):
        """
        The remote peer detached the link.

        :type event: Event
        :type link: Link
        """

        return self._impl.on_link_detach(event, link)

    def on_link_close(self, event, link):
        """
        The remote peer closed the link.

        :type event: Event
        :type link: Link
        """

        return self._impl.on_link_close(event, link)

    def on_link_error(self, event, link):
        """
        The remote peer closed the link with an error condition.

        :type event: Event
        :type link: Link
        """

        return self._impl.on_link_error(event, link)

    def on_sender_flush(self, event, sender):
        """
        The remote end of the sender requested flushing.

        :type event: Event
        :type sender: Sender
        """

        return self._impl.on_sender_flush(event, sender)

    def on_receiver_flush(self, event, receiver):
        """
        The remote end of the receiver finished flushing.

        :type event: Event
        :type receiver: Receiver
        """

        return self._impl.on_receiver_flush(event, receiver)

    def on_delivery_accept(self, event, delivery):
        """
        The remote peer accepted an outgoing message.

        :type event: Event
        :type delivery: Delivery
        """

        return self._impl.on_delivery_accept(event, delivery)

    def on_delivery_reject(self, event, delivery):
        """
        The remote peer rejected an outgoing message.
        
        XXX error condition

        :type event: Event
        :type delivery: Delivery
        """

        return self._impl.on_delivery_reject(event, delivery)

    def on_delivery_release(self, event, delivery):
        """
        The remote peer released an outgoing message.  Note that
        this may be in response to either the RELEASE or MODIFIED
        state as defined by the AMQP specification.

        :type event: Event
        :type delivery: Delivery
        """

        return self._impl.on_delivery_release(event, delivery)

    def on_delivery_settle(self, event, delivery):
        """
        The remote peer settled an outgoing message.  This is the
        point at which it should never be retransmitted.

        :type event: Event
        :type delivery: Delivery
        """

        return self._impl.on_delivery_settle(event, delivery)

    def on_transport_open(self, event, transport):
        """
        The underlying network channel opened.

        :type event: Event
        :type transport: Transport
        """

        return self._impl.on_transport_open(event, transport)

    def on_transport_close(self, event, transport):
        """
        The underlying network channel closed.

        :type event: Event
        :type transport: Transport
        """

        return self._impl.on_transport_close(event, transport)

    def on_transport_error(self, event, transport):
        """
        The underlying network channel closed with an error
        condition.

        :type event: Event
        :type transport: Transport
        """

        return self._impl.on_transport_error(event, transport)

    # End of class Handler

# Network

class Transport(object):
    """
    A network channel supporting an AMQP connection.
    """

    def __init__(self):
        self._impl = _core.Transport()

    @property
    def ssl(self):
        """
        Get SSL connection information.
        """

        return self._impl.ssl

    @property
    def sasl(self):
        """
        Get SASL connection information.
        """

        return self._impl.sasl

    @property
    def condition(self):
        """
        Get the error condition.
        """

        return self._impl.condition

    # End of class Transport

class Acceptor(object):
    """
    A context for accepting inbound connections.
    """

    def __init__(self):
        self._impl = _core.Acceptor()

    @property
    def connection_options(self):
        """
        Default options for new inbound connections.
        """

        return self._impl.connection_options

    @connection_options.setter
    def connection_options(self, value):
        self._impl.connection_options = value

    def close(self):
        """
        Close the acceptor.

        """

        return self._impl.close()

    # End of class Acceptor

class Sasl(object):
    """
    SASL properties for a connection.
    """

    pass

class Ssl(object):
    """
    SSL properties for a connection.
    """

    pass

# Error handling

class ProtonError(object):
    """
    The base class for Proton errors.
    """

    pass

class TimeoutError(ProtonError):
    """
    An operation timed out.
    """

    pass

class ConversionError(ProtonError):
    """
    A type conversion failed.
    """

    pass

# End of module core
