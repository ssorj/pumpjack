# Implementation guide

## Overview

| Namespace                  | Content                                       | Depends on                                 |
|----------------------------|-----------------------------------------------|--------------------------------------------|
| [proton/core][1]           | AMQP model, event processing                  | proton/types, proton/codec, proton/io      |
| [proton/types][2]          | AMQP data types                               | -                                          |
| [proton/codec][3]          | AMQP data encoding and decoding               | proton/types                               |
| [proton/io][4]             | An SPI for IO integration                     | -                                          |
| [proton/internal][5]       | API internals and language extensions         | -                                          |
| [proton/messenger][6]      | Home of the Messenger API                     | proton/core                                |

[1]: #namespace-protoncore
[2]: #namespace-protontypes
[3]: #namespace-protoncodec
[4]: #namespace-protonio
[5]: #namespace-protoninternal
[6]: #namespace-protonmessenger

## Entity names

The entity names in this document take the form 'some-entity', lower
case and hyphenated.  Implementers are meant to translate them into
language-conventional variants.

 - value remains `value` or becomes `Value`
 - event-type becomes `event_type` or `EventType`
 - url-error becomes `url_error` or `UrlError`

## Data types

The API should operate in terms of language-native data types whenever
possible.  If a type is not available in the language or its standard
library, the implementer should introduce it in the 'proton/types' (or
optionally 'proton') namespace.

## Namespace 'proton/core'

This is the primary user entry point for the event-driven API.  Most
programs will import only this namespace.

Because of their centrality, the APIs here may be placed directly in
the 'proton' namespace instead.

### AMQP model entities

<div class="four-column" markdown="1">

 - container
 - endpoint
 - connection
 - session
 - link
 - receiver
 - sender
 - terminus
 - condition
 - delivery
 - message

</div>

### Event processing

 - event
 - handler

### Network and security

<div class="four-column" markdown="1">

 - transport
 - acceptor
 - ssl
 - ssl-client-options
 - ssl-server-options
 - sasl

</div>

### Error handling
 
 - proton-error or -exception
 - timeout-error or -exception
 - conversion-error or -exception

## Namespace 'proton/types'

Because of their centrality, the APIs here may be placed directly in
the 'proton' namespace instead.

<div class="four-column" markdown="1">

 - binary
 - boolean
 - byte
 - char
 - decimal32
 - decimal64
 - decimal128
 - double
 - duration
 - float
 - int
 - list
 - long
 - map
 - null
 - short
 - string
 - symbol
 - timestamp
 - ubyte
 - uint
 - ulong
 - url 
 - ushort
 - uuid

</div>

## Namespace 'proton/codec'

AMQP data encoding and decoding.  These interfaces are available to
the user but won't typically be necessary when building a Proton-based
application.

 - encoder
 - decoder

## Namespace 'proton/io'

An SPI for IO integration and a place for standard IO implementations.
Like 'proton/codec', it is available but not primary.

 - connection-engine
 - io-adapter

## Namespace 'proton/internal'

A place for anything that you happen to need in your implementation,
but which you cannot make private.

These interfaces are by definition *not* central to the API.  They
should not be rendered into standard API documentation.

 - API internals
 - Language utilities

## Namespace 'proton/messenger'

A home for the legacy Messenger API.

 - messenger
 - messenger-error or -exception
 - tracker
 - subscription

