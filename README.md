Authors: Dr. Delbert Hart, Professor of Computer Science, SUNY Plattsburgh and Dr. Christopher Morales, Assistant Professor of Computer Science, SUNY Plattsburgh.

A game about a lost crew of pirates exploring the ocean, trying to find their home port.

It is designed to be easily extendable, for use in a classroom context. The main extension points are 1) explorable islands and other locations and 2) events. When adding new islands and events, the student will most likely also want to add new 1) monsters and combats and/or 2) items.

To add an event:
1) Make a new .py file in the events/ folder with the handling for your event
2) Add the file name to \_\_init__.py
4) Add the event to an event pool.
   Example: To add the event to the world event pool
   1) Import the event into world.py
   2) Append at least one instance of the event to the events list.
   See commit d580f65807d524dabbe84bf49ffd1de524f26e64 for an example

To add an explorable location:
1) Make a new .py file in the locations/ folder with the handling for your island
   1) Since islands are more complicated than events, you will likely need a template to work from. You can make a copy of the provided example island to get started (make sure to choose a good file and class name!).
2) Add the file name to \_\_init__.py
4) Add the island to the island_list list.
5) You will also need to regularly test your island, I suggest adjusting the test island (testland) in world.py to be an instance of your island. The testland is always directly south of the starting point. 

Each sublocation in an explorable location like an island has its own event pool, so you will also likely want to add events. See island.py and its history for an example.
