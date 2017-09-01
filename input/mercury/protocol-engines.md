# Protocol Engines

The Proton toolkit is built around the concept of a protocol engine.
The idea behind a protocol engine is to capture all the complex
details of implementing a given protocol in a way that is as decoupled
as possible from OS details such as IO and threading models.  The
result is a highly portable and easily embedded component that
provides a full protocol implementation.  To see how this works in the
general case, it helps to start out with some simple examples of
engines and build up to the full model used by Proton.

We'll begin with something very basic, the "echo" protocol.  Anything
sent to an echo server will be copied back to the client.  The details
of implementing an echo server will vary depending on what kind of IO
framework you are using, but somewhere in the heart of every echo
server there is some kind of data structure serving as a byte queue or
circular buffer.  If you define an abstract interface around this data
structure, you have something that captures the trivial semantics of
the echo protocol.  It does this in a way that has no necessary
interaction with the OS at all.

We now have the echo engine depicted below, a simple circular buffer
or byte queue, but with a fancier title.  With this abstract
interface, we can start changing the implementation of our engine
independently from the rest of our server.

<object type="image/svg+xml" data="images/echo-engine.svg">
  Your browser does not support SVG
</object>
 
Let's start by making our example do something more interesting. We
can add a query interface to our engine as depicted below.  The IO
portion of our application still views the engine as an ordinary
circular buffer, but we can now add application logic that uses the
query interface to take action.  The exact nature of the query
interface depends on the protocol and on the engine internals.  A
simplistic query interface might just provide a byte count of data
passing through, whereas a more sophisticated engine could decode and
make available semantic content embedded within the byte stream.
While a little bit more capable than a simple echo engine, this kind
of engine is still just a simple data structure with some added
interrogatives, and so retains the desired decoupling and portability.

<object type="image/svg+xml" data="images/echo-engine-with-query-interface.svg">
  Your browser does not support SVG
</object>
 
Now consider modifying our example to be a simple request-response
protocol where every response is a predefined function (F) of each
request.  We can provide an engine for this kind of protocol by
modifying our echo engine to detect requests and replace them with
responses.  With the transformation function entirely encapsulated
inside the engine, the interface presented is identical to our
original echo engine, but we now have the ability to capture a larger
class of protocols.

<object type="image/svg+xml" data="images/simple-request-response-engine.svg">
  Your browser does not support SVG
</object>

As we did with the echo server, we can extend the simple
request-response scenario with a query interface.  As before, our
engine is just a data structure with well defined interfaces that keep
it decoupled and portable.

<object type="image/svg+xml" data="images/simple-request-response-engine-with-query-interface.svg">
  Your browser does not support SVG
</object>
 
Despite being able to capture a large class of protocols, the simple
request-response engine has some significant limitations.  For
example, if the response transformation requires accessing a file, as
is the case with a classic HTTP implementation, our engine is no
longer decoupled from the OS and could in fact block on file IO.
Also, if the request is actually invoking application logic, such as
with an RPC protocol or with most modern usage of HTTP, we simply
can't predefine the result within the confines of our library. To
accommodate these scenarios, we need to modify our engine a little
further to allow the application to control aspects of the
response. To do this we add a control interface that can be used in
conjunction with the query interface to inspect a request and modify
the response.

As we do this we begin to see two distinct facets of the engine
emerge.  We have the interface presented to the IO portion of our
server which remains identical to our original echo engine, that is a
simple circular buffer.  Independent of this we have a higher level
API emerging that presents the semantics of the protocol to the part
of the server dealing with application logic.  As we've seen, the
latter interface can evolve and change depending on the nature of the
protocol without any impact on the former. The IO portion of our
server need not know what kind of processing happens to the byte
stream as it passes through the engine.

<object type="image/svg+xml" data="images/request-response-engine.svg">
  Your browser does not support SVG
</object>
 
While the above design captures a fairly general class of protocol, it
is limited to those that use request-response interactions.  The
output bytes are always a function of the input bytes, even though the
nature of that function may be influenced by the control interface.
The final step to a fully general-purpose protocol engine is to define
the output bytes as a function of both the input bytes and the control
interface. This allows for fully general protocols that are not
limited to the request-response pattern.

It is important to note that with the general purpose engine depicted
below, while the IO portion of the application is almost identical to
our original echo server, there is one important difference.  In the
echo engine, pushing bytes into the engine is the only thing that will
cause them to be produced.  In the general-purpose engine, any use of
the control interface can cause bytes to be produced.
 
<object type="image/svg+xml" data="images/general-engine.svg">
  Your browser does not support SVG
</object>
 
A further refinement of the general purpose engine is to separate the
control interface into a distinct entity with its own lifecycle. This
entity can be bound to a given transport and then unbound. This
separation formalizes the two facets of the engine interface discussed
above into a bottom half that can keep a very simple IO-oriented view
of the world, and a top half that reflects the high-level application
interface to the protocol. The distinct lifecycle also permits the
control interface to carry state across multiple physical connections,
which can allow for a much more sophisticated control entity that can
provide a simpler interface, for example automatically recovering
state from a previous connection as is done with HTTP sessions.

<object type="image/svg+xml" data="images/separate-control-interface-lifecycle.svg">
  Your browser does not support SVG
</object>
