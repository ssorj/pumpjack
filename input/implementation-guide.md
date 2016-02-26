# Implementation guide

## Overview

| Namespace                  | Content                                       | Depends on                   |
|----------------------------|-----------------------------------------------|------------------------------|
| [proton/core][1]           | AMQP model, event processing, error handling  | proton/amqp, proton/io       |
| [proton/amqp][2]           | AMQP data encoding and decoding               | proton/internal if needed    |
| [proton/io][3]             | IO integration                                | proton/internal if needed    |
| [proton/internal][4]       | API internals and language extensions         | -                            |
| [proton/messenger][5]      | Home of the Messenger API                     | proton/core                  |

[1]: #namespace-protoncore
[2]: #namespace-protonamqp
[3]: #namespace-protonio
[4]: #namespace-protonmessenger
[5]: #namespace-protoninternal

## Entity names

The entity names in this document take the form 'some-entity', lower
case and hyphenated.  Implementers are meant to translate them into
language-conventional variants.

 - value remains `value` or becomes `Value`
 - event-type becomes `event_type` or `EventType`
 - url-error becomes `url_error` or `UrlError`

## Root namespace

In general, prefer simply 'proton' as the root namespace.  If your
language uses fully qualified package names a la Java, it should
include 'qpid', as in org.apache.qpid.proton.

## Data types

The API should operate in terms of language-native data types whenever
possible.  If a type is not available in the language or its standard
library, the implementer should introduce it in either 'proton/core'
namespace or the 'proton/amqp' namespace.

**API data types.** Data types that are featured in elements of the
core API should go in the 'proton/core' namespace.

**Codec data types.** Data types that will find their principle use in
low-level codec operations should reside in the 'proton/amqp'
namespace.

## Namespace 'proton/core'

This is the primary user entry point for the event-driven API.  Most
programs will import only this namespace.

Because of their centrality, the APIs here may sometimes be placed
instead directly in the 'proton' namespace.

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

### API data types

<div class="four-column" markdown="1">

 - binary
 - boolean
 - duration
 - float (float, double)
 - integer (short, int, long)
 - list
 - map
 - null
 - string
 - symbol
 - timestamp
 - url 
 - uuid

</div>

## Namespace 'proton/amqp'

AMQP data encoding and decoding.  These interfaces are available to
the user but won't typically be necessary when building a Proton-based
application.

### Codec data types

<div class="four-column" markdown="1">

 - byte
 - char
 - decimal128
 - decimal32
 - decimal64
 - ubyte
 - uint
 - ulong
 - ushort

</div>

## Namespace 'proton/io'

An SPI for IO integration and a place for standard IO implementations.
Like 'proton/amqp', it is available but not primary.

 - connection-engine
 - io-adapter
 - windows-io
 - posix-io

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

