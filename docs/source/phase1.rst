Phase 1
===============

In phase 1 I need to present my family profile to the world

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
of data.  

To calculate the effort on the server I will use the following formula::

   control_tpr + (spouse_tpr + children_tpr) / 2

The time of /spouse and /children is averaged because the browser can 
asynchronously fetch the two resources.  From that value I can
extrapolate the requests per second throughput of the AJAX collation::

    1 / tpr * 1000 = rps


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

I had to disqualify the RESTful indirect method because I could not
test it using a single worker thread.  The implications of that is
that the number of concurrent requests is limited to (workers)/3. To
accomplish 250 concurrent requests, I would have to have 750 worker
processes for both nginx and uwsgi.  The resident memory would end up
being 12gigs.

.. raw:: html

  <script
    src="_static/highcharts.js"
    type="text/javascript"></script>
  <script
    src="_static/csvchart.js"
    type="text/javascript"></script>
  <script
    src="_static/phase1.js"
    type="text/javascript"></script>


  <div id="phase1-rps-chart"></div>

  <div id="phase1-tpr-chart"></div>

Conclusion
-----------

It is obvious that accessing the data directly would produce the
quickest result. It is the implementation with the fewest moving parts.

ESI's overhead was surprising.  If you subtract the mean time per
request for the spouse and children resource you will find that the
ESI collating added 1ms of overhead.  I'd be interested to see what
kind of overhead ESI adds for more complicated templates.

Comparing ESI to direct access is probably a bit unfair because ESI is
doing much more than the Python string format template does for the 
direct responses.  I would suspect that the values for AJAX would be 
a fairer comparison.

I think that it is safe for me to conclude that if server data needs
to be collated on the server, accessing the data directly would be
best.

That being said, you gain flexibility when using edge side and client
side collating.  If you ignore database limitations, you could
theoretically gain the throughput of the direct method by horizontally
scaling the servers but that would require more system resources
(which may be cheap enough to justify).
