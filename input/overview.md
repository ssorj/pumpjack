# Overview

Proton sends and receives **messages**.  Messages are transferred
between connected peers over **links**.  At the sending peer the link
is called a **sender**.  At the receiving peer it is called a
**receiver**.  Messages are sent by senders and received by receivers.
Links may have named **source** and **target addresses**, which can be
used to identify the queue messages are sent to or received from.

Links are established over **sessions**.  Sessions are established
over **connections**.  Connections are generally established between
two uniquely identified **containers**.  Though a connection can have
multiple sessions, often this is not needed.  The container API allows
you to ignore sessions unless you require them.

;; XXX Mention endpoint in the above

A connection operates using a **transport**.  A transport is a network
communication channel, such as a TCP connection.

The sending of a message over a link is called a **delivery**.  The
message is the content sent, including all metadata such as headers
and annotations.  The delivery is the protocol exchange associated
with the transfer of that content.

To indicate that a delivery is complete, either the sender or the
receiver **settles** it.  When the other side learns that it has been
settled, it will no longer communicate about that delivery.  The
receiver can also indicate whether they accept or reject the message.

- [AMQP conceptual model](http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-transport-v1.0-os.html#doc-idp2176)

<!--

## Containers

## Endpoints

- Lifecycle
- Local and remote state
- Options
- Error conditions

## Deliveries

- Lifecycle
- Local and remote state
- Settlement state versus delivery state

Three different levels of **delivery guarantee** can be achieved:
at-most-once, at-least-once, or exactly-once.

- [Delivery guarantees](delivery-guarantees.html)

## Sources and targets

## Messages

- Addresses: to and reply-to, correspondence to source and target
- Content parts: body, headers, and other properties

## Events and handlers

## Flow control

- Flow control

## Network

- Transport lifecycle, coincidence of transport and connection start
- Connect, listen, acceptor
- SASL and SSL
- [Protocol engines](protocol-engines.html)

## More topics

- Threading model, locking
- Type system
- Codec
- IO
- [Implementation guide](implementation-guide.html)

-->
