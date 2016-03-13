# Module core

# Core model

class Container(object):
    def __init__(self, handler=None, id=None):
        super().__init__()

        self._id = self._generate_id()
        self._client_connection_options = ConnectionOptions()
        self._server_connection_options = ConnectionOptions()
        self._session_options = SessionOptions()
        self._link_options = LinkOptions()

        self._handler = None

        if handler is not None:
            self._handler = handler

        if id is not None:
            self._id = id

    @property
    def id(self):
        return self._id

    @property
    def client_connection_options(self):
        return self._client_connection_options

    @property
    def server_connection_options(self):
        return self._server_connection_options

    @property
    def session_options(self):
        return self._session_options

    @property
    def link_options(self):
        return self._link_options

    def run(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def send(self, message, url):
        raise NotImplementedError()

    def send_request(self, message, url):
        raise NotImplementedError()

    def send_response(self, message, request):
        raise NotImplementedError()

    def connect(self, url, options=None):
        raise NotImplementedError()

    def listen(self, url, options=None):
        raise NotImplementedError()

    def open_receiver(self, url, options=None):
        raise NotImplementedError()

    def open_sender(self, url, options=None):
        raise NotImplementedError()

    def connections(self):
        raise NotImplementedError()

    # End of class Container

class Client(Container):
    def __init__(self, url, handler=None, id=None):
        super().__init__()


        self._url = url

        self._handler = None

        if handler is not None:
            self._handler = handler

        self._id = None

        if id is not None:
            self._id = id

    # End of class Client

class Server(Container):
    def __init__(self, url, handler=None, id=None):
        super().__init__()


        self._url = url

        self._handler = None

        if handler is not None:
            self._handler = handler

        self._id = None

        if id is not None:
            self._id = id

    # End of class Server

class Endpoint(object):
    def __init__(self):
        super().__init__()

        self._local_uninitialized = None # Discovered
        self._remote_uninitialized = None # Discovered
        self._local_active = None # Discovered
        self._remote_active = None # Discovered
        self._local_closed = None # Discovered
        self._remote_closed = None # Discovered
        self._remote_condition = None # Discovered
        self._remote_properties = map() # Discovered
        self._remote_offered_capabilities = list() # Discovered
        self._remote_desired_capabilities = list() # Discovered

    @property
    def local_uninitialized(self):
        return self._local_uninitialized

    @property
    def remote_uninitialized(self):
        return self._remote_uninitialized

    @property
    def local_active(self):
        return self._local_active

    @property
    def remote_active(self):
        return self._remote_active

    @property
    def local_closed(self):
        return self._local_closed

    @property
    def remote_closed(self):
        return self._remote_closed

    @property
    def remote_condition(self):
        return self._remote_condition

    @property
    def remote_properties(self):
        return self._remote_properties

    @property
    def remote_offered_capabilities(self):
        return self._remote_offered_capabilities

    @property
    def remote_desired_capabilities(self):
        return self._remote_desired_capabilities

    # End of class Endpoint

class Connection(Endpoint):
    def __init__(self):
        super().__init__()

        self._transport = Transport()
        self._default_session = Session()
        self._remote_container_id = None # Discovered
        self._remote_virtual_host = None # Discovered
        self._remote_user = None # Discovered
        self._remote_idle_timeout = None # Discovered
        self._remote_max_sessions = None # Discovered
        self._remote_max_frame_size = None # Discovered

    @property
    def transport(self):
        return self._transport

    @property
    def default_session(self):
        return self._default_session

    @property
    def remote_container_id(self):
        return self._remote_container_id

    @property
    def remote_virtual_host(self):
        return self._remote_virtual_host

    @property
    def remote_user(self):
        return self._remote_user

    @property
    def remote_idle_timeout(self):
        return self._remote_idle_timeout

    @property
    def remote_max_sessions(self):
        return self._remote_max_sessions

    @property
    def remote_max_frame_size(self):
        return self._remote_max_frame_size

    def open(self, options=None):
        raise NotImplementedError()

    def close(self, condition=None):
        raise NotImplementedError()

    def send(self, message):
        raise NotImplementedError()

    def send_request(self, message):
        raise NotImplementedError()

    def send_response(self, response_message, request_message):
        raise NotImplementedError()

    def open_sender(self, address, options=None):
        raise NotImplementedError()

    def open_receiver(self, address, options=None):
        raise NotImplementedError()

    def open_session(self, options=None):
        raise NotImplementedError()

    def sessions(self):
        raise NotImplementedError()

    def links(self):
        raise NotImplementedError()

    def deliveries(self):
        raise NotImplementedError()

    # End of class Connection

class Session(Endpoint):
    def __init__(self):
        super().__init__()

        self._connection = Connection()
        self._incoming_bytes = None # Discovered
        self._outgoing_bytes = None # Discovered
        self._remote_incoming_window = None # Discovered
        self._remote_outgoing_window = None # Discovered

    @property
    def connection(self):
        return self._connection

    @property
    def incoming_bytes(self):
        return self._incoming_bytes

    @property
    def outgoing_bytes(self):
        return self._outgoing_bytes

    @property
    def remote_incoming_window(self):
        return self._remote_incoming_window

    @property
    def remote_outgoing_window(self):
        return self._remote_outgoing_window

    def open(self, options=None):
        raise NotImplementedError()

    def close(self, condition=None):
        raise NotImplementedError()

    def send(self, message):
        raise NotImplementedError()

    def send_request(self, message):
        raise NotImplementedError()

    def send_response(self, response_message, request_message):
        raise NotImplementedError()

    def open_receiver(self, address, options=None):
        raise NotImplementedError()

    def open_sender(self, address, options=None):
        raise NotImplementedError()

    def links(self):
        raise NotImplementedError()

    def deliveries(self):
        raise NotImplementedError()

    # End of class Session

class Link(Endpoint):
    def __init__(self):
        super().__init__()

        self._type = None # Discovered
        self._session = Session()
        self._name = self._generate_name()
        self._credit = None # Discovered
        self._remote_source = None # Discovered
        self._remote_target = None # Discovered
        self._remote_delivery_mode = None # Discovered
        self._remote_max_message_size = None # Discovered

    @property
    def type(self):
        return self._type

    @property
    def session(self):
        return self._session

    @property
    def name(self):
        return self._name

    @property
    def credit(self):
        return self._credit

    @property
    def remote_source(self):
        return self._remote_source

    @property
    def remote_target(self):
        return self._remote_target

    @property
    def remote_delivery_mode(self):
        return self._remote_delivery_mode

    @property
    def remote_max_message_size(self):
        return self._remote_max_message_size

    def open(self, options=None):
        raise NotImplementedError()

    def close(self, condition=None):
        raise NotImplementedError()

    def detach(self, condition=None):
        raise NotImplementedError()

    def deliveries(self):
        raise NotImplementedError()

    # End of class Link

class Receiver(Link):
    def __init__(self):
        super().__init__()

    def add_credit(self, count):
        raise NotImplementedError()

    def flush(self):
        raise NotImplementedError()

    # End of class Receiver

class Sender(Link):
    def __init__(self):
        super().__init__()

    def send(self, message):
        raise NotImplementedError()

    def send_request(self, message):
        raise NotImplementedError()

    def send_response(self, response, request):
        raise NotImplementedError()

    # End of class Sender

class Terminus(object):
    def __init__(self):
        super().__init__()

        self._type = None # Discovered
        self._address = None # Discovered
        self._durability_mode = None # Discovered
        self._distribution_mode = None # Discovered
        self._filters = map() # Discovered
        self._dynamic = None # Discovered
        self._properties = map() # Discovered
        self._timeout = None # Discovered
        self._expiry_policy = None # Discovered
        self._capabilities = list() # Discovered

    @property
    def type(self):
        return self._type

    @property
    def address(self):
        return self._address

    @property
    def durability_mode(self):
        return self._durability_mode

    @property
    def distribution_mode(self):
        return self._distribution_mode

    @property
    def filters(self):
        return self._filters

    @property
    def dynamic(self):
        return self._dynamic

    @property
    def properties(self):
        return self._properties

    @property
    def timeout(self):
        return self._timeout

    @property
    def expiry_policy(self):
        return self._expiry_policy

    @property
    def capabilities(self):
        return self._capabilities

    # End of class Terminus

class Message(object):
    def __init__(self, body=None):
        super().__init__()

        self._id = None
        self._user = None
        self._to = None
        self._reply_to = None
        self._correlation_id = None
        self._subject = None
        self._body = None
        self._content_type = None
        self._content_encoding = None
        self._expiry_time = None
        self._creation_time = None
        self._inferred = False
        self._durable = False
        self._priority = 4
        self._ttl = None
        self._first_acquirer = True
        self._delivery_count = 0
        self._group_id = None
        self._group_sequence = None
        self._reply_to_group_id = None
        self._properties = map()
        self._delivery_annotations = map()
        self._message_annotations = map()
        self._footer = map()

        if body is not None:
            self._body = body

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, value):
        self._to = value

    @property
    def reply_to(self):
        return self._reply_to

    @reply_to.setter
    def reply_to(self, value):
        self._reply_to = value

    @property
    def correlation_id(self):
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, value):
        self._correlation_id = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        self._content_type = value

    @property
    def content_encoding(self):
        return self._content_encoding

    @content_encoding.setter
    def content_encoding(self, value):
        self._content_encoding = value

    @property
    def expiry_time(self):
        return self._expiry_time

    @expiry_time.setter
    def expiry_time(self, value):
        self._expiry_time = value

    @property
    def creation_time(self):
        return self._creation_time

    @creation_time.setter
    def creation_time(self, value):
        self._creation_time = value

    @property
    def inferred(self):
        return self._inferred

    @inferred.setter
    def inferred(self, value):
        self._inferred = value

    @property
    def durable(self):
        return self._durable

    @durable.setter
    def durable(self, value):
        self._durable = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def ttl(self):
        return self._ttl

    @ttl.setter
    def ttl(self, value):
        self._ttl = value

    @property
    def first_acquirer(self):
        return self._first_acquirer

    @first_acquirer.setter
    def first_acquirer(self, value):
        self._first_acquirer = value

    @property
    def delivery_count(self):
        return self._delivery_count

    @delivery_count.setter
    def delivery_count(self, value):
        self._delivery_count = value

    @property
    def group_id(self):
        return self._group_id

    @group_id.setter
    def group_id(self, value):
        self._group_id = value

    @property
    def group_sequence(self):
        return self._group_sequence

    @group_sequence.setter
    def group_sequence(self, value):
        self._group_sequence = value

    @property
    def reply_to_group_id(self):
        return self._reply_to_group_id

    @reply_to_group_id.setter
    def reply_to_group_id(self, value):
        self._reply_to_group_id = value

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value

    @property
    def delivery_annotations(self):
        return self._delivery_annotations

    @delivery_annotations.setter
    def delivery_annotations(self, value):
        self._delivery_annotations = value

    @property
    def message_annotations(self):
        return self._message_annotations

    @message_annotations.setter
    def message_annotations(self, value):
        self._message_annotations = value

    @property
    def footer(self):
        return self._footer

    @footer.setter
    def footer(self, value):
        self._footer = value

    def clear(self):
        raise NotImplementedError()

    def encode(self):
        raise NotImplementedError()

    def decode(self, bytes):
        raise NotImplementedError()

    # End of class Message

class Delivery(object):
    def __init__(self):
        super().__init__()

        self._id = self._generate_id()
        self._link = Link()
        self._local_settled = False
        self._remote_settled = False
        self._local_state = DeliveryState.NONE
        self._remote_state = DeliveryState.NONE
        self._updated = bool()
        self._readable = bool()
        self._writable = bool()

    @property
    def id(self):
        return self._id

    @property
    def link(self):
        return self._link

    @property
    def local_settled(self):
        return self._local_settled

    @property
    def remote_settled(self):
        return self._remote_settled

    @property
    def local_state(self):
        return self._local_state

    @property
    def remote_state(self):
        return self._remote_state

    @property
    def updated(self):
        return self._updated

    @property
    def readable(self):
        return self._readable

    @property
    def writable(self):
        return self._writable

    def settle(self):
        raise NotImplementedError()

    def accept(self):
        raise NotImplementedError()

    def reject(self):
        raise NotImplementedError()

    def release(self):
        raise NotImplementedError()

    def modify(self):
        raise NotImplementedError()

    # End of class Delivery

class Condition(object):
    def __init__(self, name, description=None, properties=None):
        super().__init__()

        self._name = str()
        self._description = None
        self._properties = map()

        self._name = name

        if description is not None:
            self._description = description

        if properties is not None:
            self._properties = properties

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value

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
    def __init__(self):
        super().__init__()

        self._properties = map()
        self._offered_capabilities = list()
        self._desired_capabilities = list()
        self._handler = None

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value

    @property
    def offered_capabilities(self):
        return self._offered_capabilities

    @offered_capabilities.setter
    def offered_capabilities(self, value):
        self._offered_capabilities = value

    @property
    def desired_capabilities(self):
        return self._desired_capabilities

    @desired_capabilities.setter
    def desired_capabilities(self, value):
        self._desired_capabilities = value

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, value):
        self._handler = value

    # End of class EndpointOptions

class ConnectionOptions(EndpointOptions):
    def __init__(self):
        self._container_id = self._generate_container_id()
        self._virtual_host = None
        self._user = None
        self._password = None
        self._sasl_enabled = True
        self._sasl_allow_insecure_mechs = False
        self._sasl_allowed_mechs = None
        self._idle_timeout = None
        self._max_sessions = None
        self._max_frame_size = None

    @property
    def container_id(self):
        return self._container_id

    @container_id.setter
    def container_id(self, value):
        self._container_id = value

    @property
    def virtual_host(self):
        return self._virtual_host

    @virtual_host.setter
    def virtual_host(self, value):
        self._virtual_host = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def sasl_enabled(self):
        return self._sasl_enabled

    @sasl_enabled.setter
    def sasl_enabled(self, value):
        self._sasl_enabled = value

    @property
    def sasl_allow_insecure_mechs(self):
        return self._sasl_allow_insecure_mechs

    @sasl_allow_insecure_mechs.setter
    def sasl_allow_insecure_mechs(self, value):
        self._sasl_allow_insecure_mechs = value

    @property
    def sasl_allowed_mechs(self):
        return self._sasl_allowed_mechs

    @sasl_allowed_mechs.setter
    def sasl_allowed_mechs(self, value):
        self._sasl_allowed_mechs = value

    @property
    def idle_timeout(self):
        return self._idle_timeout

    @idle_timeout.setter
    def idle_timeout(self, value):
        self._idle_timeout = value

    @property
    def max_sessions(self):
        return self._max_sessions

    @max_sessions.setter
    def max_sessions(self, value):
        self._max_sessions = value

    @property
    def max_frame_size(self):
        return self._max_frame_size

    @max_frame_size.setter
    def max_frame_size(self, value):
        self._max_frame_size = value

    # End of class ConnectionOptions

class SessionOptions(EndpointOptions):
    def __init__(self):
        self._incoming_capacity = None
        self._max_links = None
        self._incoming_window = None
        self._outgoing_window = None

    @property
    def incoming_capacity(self):
        return self._incoming_capacity

    @incoming_capacity.setter
    def incoming_capacity(self, value):
        self._incoming_capacity = value

    @property
    def max_links(self):
        return self._max_links

    @max_links.setter
    def max_links(self, value):
        self._max_links = value

    @property
    def incoming_window(self):
        return self._incoming_window

    @incoming_window.setter
    def incoming_window(self, value):
        self._incoming_window = value

    @property
    def outgoing_window(self):
        return self._outgoing_window

    @outgoing_window.setter
    def outgoing_window(self, value):
        self._outgoing_window = value

    # End of class SessionOptions

class LinkOptions(EndpointOptions):
    def __init__(self):
        self._source = TerminusOptions()
        self._target = TerminusOptions()
        self._delivery_mode = DeliveryMode.AT_LEAST_ONCE
        self._name = self._generate_name()
        self._message_window = 10
        self._max_message_size = None

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def delivery_mode(self):
        return self._delivery_mode

    @delivery_mode.setter
    def delivery_mode(self, value):
        self._delivery_mode = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def message_window(self):
        return self._message_window

    @message_window.setter
    def message_window(self, value):
        self._message_window = value

    @property
    def max_message_size(self):
        return self._max_message_size

    @max_message_size.setter
    def max_message_size(self, value):
        self._max_message_size = value

    # End of class LinkOptions

class TerminusOptions(object):
    def __init__(self):
        super().__init__()

        self._address = None
        self._durability_mode = DurabilityMode.NONE
        self._distribution_mode = DistributionMode.MOVE
        self._filters = map()
        self._dynamic = False
        self._properties = map()
        self._timeout = None
        self._expiry_policy = ExpiryPolicy.SESSION_CLOSE
        self._capabilities = list()

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def durability_mode(self):
        return self._durability_mode

    @durability_mode.setter
    def durability_mode(self, value):
        self._durability_mode = value

    @property
    def distribution_mode(self):
        return self._distribution_mode

    @distribution_mode.setter
    def distribution_mode(self, value):
        self._distribution_mode = value

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        self._filters = value

    @property
    def dynamic(self):
        return self._dynamic

    @dynamic.setter
    def dynamic(self, value):
        self._dynamic = value

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @property
    def expiry_policy(self):
        return self._expiry_policy

    @expiry_policy.setter
    def expiry_policy(self, value):
        self._expiry_policy = value

    @property
    def capabilities(self):
        return self._capabilities

    @capabilities.setter
    def capabilities(self, value):
        self._capabilities = value

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
    def __init__(self):
        super().__init__()

        self._container = Container()
        self._connection = Connection()
        self._session = Session()
        self._link = Link()
        self._sender = Sender()
        self._receiver = Receiver()
        self._delivery = Delivery()
        self._transport = Transport()

    @property
    def container(self):
        return self._container

    @property
    def connection(self):
        return self._connection

    @property
    def session(self):
        return self._session

    @property
    def link(self):
        return self._link

    @property
    def sender(self):
        return self._sender

    @property
    def receiver(self):
        return self._receiver

    @property
    def delivery(self):
        return self._delivery

    @property
    def transport(self):
        return self._transport

    # End of class Event

class Handler(object):
    def __init__(self):
        super().__init__()

    def on_start(self, event, container):
        raise NotImplementedError()

    def on_stop(self, event, container):
        raise NotImplementedError()

    def on_message(self, event, message):
        raise NotImplementedError()

    def on_sendable(self, event, sender):
        raise NotImplementedError()

    def on_unhandled(self, event):
        raise NotImplementedError()

    def on_unhandled_error(self, event, condition):
        raise NotImplementedError()

    def on_connection_open(self, event, connection):
        raise NotImplementedError()

    def on_connection_close(self, event, connection):
        raise NotImplementedError()

    def on_connection_error(self, event, connection):
        raise NotImplementedError()

    def on_session_open(self, event, session):
        raise NotImplementedError()

    def on_session_close(self, event, session):
        raise NotImplementedError()

    def on_session_error(self, event, session):
        raise NotImplementedError()

    def on_link_open(self, event, link):
        raise NotImplementedError()

    def on_link_detach(self, event, link):
        raise NotImplementedError()

    def on_link_close(self, event, link):
        raise NotImplementedError()

    def on_link_error(self, event, link):
        raise NotImplementedError()

    def on_sender_flush(self, event, sender):
        raise NotImplementedError()

    def on_receiver_flush(self, event, receiver):
        raise NotImplementedError()

    def on_delivery_accept(self, event, delivery):
        raise NotImplementedError()

    def on_delivery_reject(self, event, delivery):
        raise NotImplementedError()

    def on_delivery_release(self, event, delivery):
        raise NotImplementedError()

    def on_delivery_settle(self, event, delivery):
        raise NotImplementedError()

    def on_transport_open(self, event, transport):
        raise NotImplementedError()

    def on_transport_close(self, event, transport):
        raise NotImplementedError()

    def on_transport_error(self, event, transport):
        raise NotImplementedError()

    # End of class Handler

# Network

class Transport(object):
    def __init__(self):
        super().__init__()

        self._ssl = Ssl()
        self._sasl = Sasl()
        self._condition = Condition()

    @property
    def ssl(self):
        return self._ssl

    @property
    def sasl(self):
        return self._sasl

    @property
    def condition(self):
        return self._condition

    # End of class Transport

class Acceptor(object):
    def __init__(self):
        super().__init__()

        self._connection_options = ConnectionOptions()

    @property
    def connection_options(self):
        return self._connection_options

    @connection_options.setter
    def connection_options(self, value):
        self._connection_options = value

    def close(self):
        raise NotImplementedError()

    # End of class Acceptor

class Sasl(object):
    pass

class Ssl(object):
    pass

# Error handling

class ProtonError(object):
    pass

class TimeoutError(ProtonError):
    pass

class ConversionError(ProtonError):
    pass

# End of module core
