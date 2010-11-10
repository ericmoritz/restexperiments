Phase 1
===============

In phase on I need to present my family profile to the world

Solutions
----------

Conventional Design
~~~~~~~~~~~~~~~~~~~

Create one page located at /family that the world will use to
access my information at.  This solution will directly access the data
from the database and generate a response using a template.


RESTful Design
~~~~~~~~~~~~~~~

Direct Access
^^^^^^^^^^^^^^^^

Create one resource located at /family that the world will use to
access my information at.  This solution will directly access the data
from the database and generate a response using a template.

Indirect Access
^^^^^^^^^^^^^^^^^

Fetch a /spouse and /children resource independently and combine them
using a template.

ESI
^^^^

Use an ESI template and Varnish to combine the /spouse and /children
resources outside of the application.


Client Side
^^^^^^^^^^^^
Fetches code that describes how to fetch the needed data and combine
them on the client.  This is essentially the "AJAX" method.  In AJAX,
an HTML file is downloaded that includes the needed Javascript to
fetch the /spouse and /children and combine them into a single piece
of data.  This is essentially what the ESI implementation is doing.

Varnish is acting as the client.  It fetches the ESI template and
parses it, then fetches the two resources it's needs to generate the
final response.  In this experiment.  I am going to consider ESI the
same as client side rendering.


Hypothesis
-----------

Both the Conventional and RESTful direct access methods will perform
the best because they access the data directly.


Test Cases
-----------
Each implementation must produce the following response::

    Gina Moritz;Aiden Moritz,Ethan Moritz


/conventional/direct/family
     Uses direct access to the database to generate the response

/restful/direct/family
     Uses direct access to the database to generate the response

/restful/indirect/family
     Fetches the spouse and children resources behind the scenes and
     generates the response based on the resources

/restful/esi/family
     Returns an ESI template for varnish to use to generate a response


Methodology
------------

Benchmark the URIs using Apache Bench with a sample size of 10,000
requests::

    ab -n10000 -c1 $URI


Results
--------

[Present analyzed data]

Conclusion
-----------

[Present you conclusion]



