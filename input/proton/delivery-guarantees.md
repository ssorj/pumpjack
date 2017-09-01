# Delivery guarantees

The AMQP model for settlement is based on the lifecycle of a delivery
at an endpoint. At each end of a link, a delivery is created, it
exists for some period of time, and finally it is forgotten, that is
"settled".  Note that because this lifecycle happens independently at
both the sender and the receiver, there are four events of interest in
the combined lifecycle of a given delivery:

 - Created at sender
 - Created at receiver
 - Settled at sender
 - Settled at receiver

Because the sender and receiver are operating concurrently, these
events can occur in various orders, and the order of these events
impacts the types of failures that may occur when transferring a
delivery.  Eliminating scenarios where the receiver creates the
delivery first, we have the following possible sequences of interest.

## Sender presettles ("at most once" delivery)

 1. Created at sender
 2. Settled at sender
 3. Created at receiver
 4. Settled at receiver

In this configuration the sender settles (that is, forgets about) the
delivery before it even reaches the receiver, and if anything should
happen to the delivery in flight, there is no basis for resending,
hence the "at most once" semantics.

## Receiver settles first ("at least once" delivery)

 1. Created at sender
 2. Created at receiver
 3. Settled at receiver
 4. Settled at sender

In this configuration the receiver settles the delivery first, and the
sender settles once it sees the receiver has settled.  Should anything
happen to the delivery in flight, the sender can resend.  The
receiver, however, has already forgotten the delivery, and a resend
will be interpreted as a new delivery.

## Receiver settles second ("exactly once" delivery)

 1. Created at sender
 2. Created at receiver
 3. Settled at sender
 4. Settled at receiver

In this configuration the receiver settles only once it has seen that
the sender has settled. This provides the sender the option to
retransmit, and the receiver has the option to recognize (and discard)
duplicates, allowing for "exactly once" semantics.

Note that in the last scenario the sender needs some way to know when
it is safe to settle. This is where delivery state comes in.  In
addition to these lifecycle related events surrounding deliveries
there is also the notion of a delivery state that can change over the
lifetime of a delivery.

For example, it might start out as nothing, transition to RECEIVED,
and then transition to ACCEPTED.  In the first two scenarios the
delivery state isn't required.  In the last scenario, however, the
sender would trigger settlement based on seeing the delivery state
transition to a terminal state such as ACCEPTED or REJECTED.

In practice, settlement is controlled by application policy, so there
are more options for settlement behavior.  For example, a sender might
not settle strictly based on what has happened at the receiver.  It
might also choose to impose some time limit and settle after that
period has expired, or it could simply have a sliding window of the
last N deliveries and settle the oldest whenever a new one comes
along.
