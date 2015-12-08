# Overview

Messages are transferred between connected peers over "links".  At the
sending peer the link is called a sender.  At the receiving peer it is
called a receiver.  Messages are sent by senders and received by
receivers.  Links may have named "source" and "target" addresses,
which can be used to identify the queue messages are sent to or
received from.

Links are established over sessions.  Sessions are established over
connections.  Connections are generally established between two
uniquely identified containers.  Though a connection can have multiple
sessions, often this is not needed.  The container API allows you to
ignore sessions unless you require them.

The sending of a message over a link is called a delivery.  The
message is the content sent, including all metadata such as headers
and annotations.  The delivery is the protocol exchange associated
with the transfer of that content.

To indicate that a delivery is complete, either the sender or the
receiver "settles" it.  When the other side learns that it has been
settled, it will no longer communicate about that delivery.  The
receiver can also indicate whether they accept or reject the message.

Three different delivery levels or "guarantees" can be achieved:
at-most-once, at-least-once, or exactly-once.

 - [Delivery guarantees](delivery-guarantees.html)
 - [Protocol engines](protocol-engines.html)
 - [API layout](api-layout.html)

;; XXX add an engine-oriented section
