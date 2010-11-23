Transclusion
===============

I need to the user to have access to a single URI that will have my
wife's name and my children's name.  We need to accomplish this
utilizing the method that produces the shortest stack time.

.. raw:: html

  <script
    src="../_static/highcharts.js"
    type="text/javascript"></script>
  <script
    src="../_static/csvchart.js"
    type="text/javascript"></script>
  <script
    src="../_static/transclusion.js"
    type="text/javascript"></script>


Resources
----------

There are three resources that will be used for transclusion.  They
will expose the three pieces of data I want to make accessible to a user.

/spouse
  This is my wife's name

/children
  This is a comma separated list of my children's names sorted by
  birth date.

/family
  This is a semi-comma separated list of my wife's name and the
  children resource.

Definitions
------------

Let me start by defining terms I am going to use in this document.

Direct Access
    The way internal data is accessed by talking directly to the
    service providing the data.  Most often this is accomplished using
    a database or file system.

Indirect Access
    The way internal data is accessed by accessing data as a resource
    identified by a URI and served by HTTP.

Perceived Time
    The total time all resources are download and compiled

Stack Time
    The total time all resources are downloaded prior to compilation
   
Solutions
----------

Server Side
~~~~~~~~~~~~~~~~~~~

Direct Access
   The most common way of transcluding data into a single response on the
   server side is by direct access.  

Indirect Access
    Transcluding data is by internally fetching
    resources and transcluding the responses in a server side
    application

SSI
    Off-loading the transcluding of resources to the webserver by the
    means of a SSI template and the two resources   

Edge Side
~~~~~~~~~~

ESI
   There really is only one standard way of doing transclusion at the
   edge and that is ESI.  There will be three resources needed for
   ESI, an ESI template and the two resources.

Client Side
~~~~~~~~~~~~

AJAX
   Javascript is used to insert resources into a template.  There will
   be three resources needed for AJAX, an HTML with inline Javascript,
   and the two resources

iframe
   An iframe is used to transclude the two resources into a single
   document. There will be three resources needed for the iframe
   technique. An HTML document containing iframes and the two resources.


Test Cases
------------

It is hard to fairly compare the perceived time because of variations
speeds in templating systems.  For my tests I am going to test the
stack time.

If we look at individual solutions we will find the need for the
following resources

* Direct
  * /direct/family  
* Indirect
  * /indirect/family
* SSI
  * /family.ssi.html
  * /spouse
  * /children
* ESI
  * /family.esi.html
  * /spouse
  * /children
* AJAX
  * /family.ajax.html
  * /spouse
  * /children
* iframe
  * /family.iframe.html
  * /spouse
  * /children

From the servers point of view we can distill the implementations into
the following

* Direct
  /direct/family
* Indirect
  /indirect/family
* Externally Templated
  /template
  /spouse
  /children

Indirect cannot be included in the externally templated class because
the responsibility of compiling items lands on the application.

Experiments
-------------

Phase 1
~~~~~~~~

In phase 1 we will test the overhead of each implementation based on
stack time.

Hypothesis
~~~~~~~~~~~~

Direct Access will be the fastest because it has the fewest layers
between data and response.

Methodology
~~~~~~~~~~~~
A new Rackspace Cloud VPS running Ubuntu 10.10 was created for a clean
room environment.  I ran the following to initialize the server::

    git clone git://github.com/ericmoritz/restexperiments.git
    cd restexperiments
    git checkout simplified
    ./bin/ubuntu-10-10-build.sh    

NGINX and UWSGI are configured using one worker each to serve a WSGI
application that provides each implementation mounted at the URIs
described above.  This HTTP/WSGI stack was chosen based on the
conclusions made by
`Nicholas Piël <http://nichol.as/benchmark-of-python-web-servers>`_
in his benchmarks of HTTP/WSGI solutions.  I do not need to recreate
his tests so I chose the setup from the three winners from his tests.

Varnish is used in front of the HTTP/WSGI stack to add the overhead
that would exist if a request was fetched through Varnish.

The ./bin/startservers.sh script is used to configure the server for
high concurrency as described by 
`Nicholas Piël <http://nichol.as/benchmark-of-python-web-servers>`_
and to launch the needed servers.

I will make 10,000 requests to each resource needed to compile the
family document are increasing concurrency levels using Apache Bench::

    ab -n10000 -c1    $URI
    ab -n10000 -c250  $URI
    ab -n10000 -c500  $URI
    ab -n10000 -c1000 $URI


I will calculate the total stack time for the externally templated
method by summing the mean request time of each resource using the
follow formula (trp = Time per Request)::

   template.tpr + spouse.tpr + children.tpr

Because a external templating system could fetch the resources
asynchronously, the actual time needed for the spouse and children
resources would be between::

    (spouse.tpr + children.tpr) / 2 < x < (spouse.tpr + children.tpr)

For sake of argument, I am going to err on the side of caution and use
the worse case of (spouse.tpr + children.tpr)

Results
~~~~~~~~

I had to disqualify the indirect method because I could not test it using
a single worker thread.  The implications of that is that the number
of concurrent requests is limited to (workers)/3.

This makes a concurrency level of 1 require 3 workers; a concurrency
level of 2 require 6 workers, and so on.

To accomplish the second tier of testing at 250 concurrent requests, I
would have to have 750 worker processes for both nginx and uwsgi.  The
resident memory would end up being 12gigs.

Without further adieu:

.. raw:: html

  <div id="phase1-rps-chart"></div>
  <div id="phase1-tpr-chart"></div>
