A game about a lost crew of pirates exploring the ocean, trying to find their home port.

It is designed to be easily extendable, for use in a classroom context. The main extension points are 1) explorable islands and other locations and 2) events. When adding new islands and events, the student will most likely also want to add new 1) monsters and combats and/or 2) items.

To add an event:
1) Make a new .py file in the events/ folder with the handling for your event
2) Add the file name to __init__.py
3) Add the event to an event pool.
   Example: To add the event to the world event pool
   a) Import the event into world.py
   b) Append at least one instance of the event to the events list.
   See commit d580f65807d524dabbe84bf49ffd1de524f26e64 for an example

