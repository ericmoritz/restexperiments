.. REST vs The World documentation master file, created by
   sphinx-quickstart on Wed Nov 10 19:09:47 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

REST vs The World
====================

Modern web applications have a number of requirements that both
developers need and users need.  These experiments will compare
solutions presented by REST proponents versus current solutions.

Whenever the status quo is challenged, the burden of proof is on the
challenger.


Hypothetical Web Application
-----------------------------

I am creating a hypothetical web application that is basically a
service for getting information about myself.  This application will
in the end have all the functionality of a modern web application
should have.

I will solve the problem in each phase of the development using as
many solutions that I can come up with using both conventional
solutions and RESTful solutions.

Data
~~~~~

My web application needs to expose three pieces of data.  My wife's
name, my children's names and a family profile with is the combination
of those two items.

These data elements set up the most common need of web applications
and that is collating related content into compound documents.

In the hypertext world, this is called, "`transclusion`_".
Transclusion is the inclusion of a document or part of a document into
another document by reference.

.. _transclusion: http://en.wikipedia.org/wiki/Transclusion

Transclusion
--------------

Let's explore how transclusion is typically done in HTML.

Server-Side
~~~~~~~~~~~~

There are two ways of doing transclusion on the server side.

The most common way of transcluding content on the server is by
accessing a hidden service such as a database and at the server level
the pieces of data are compiled into a single response.

Another way to do server side transclusion is by the use of SSI.
SSI is a way of a origin server to transclude resources into a single
response.  The benefit of SSI is you can significantly reduce the
complexity of your application's response rendering and off load it to
the HTTP server layer.  The disadvantage to SSI is it adds load on the
web server layer.

Edge-Side
~~~~~~~~~~

Edge side transclusion occurs somewhere between the origin server and
the user-agent.  The most popular technology used to accomplish this
is called ESI.  ESI has all the benefits of SSI but corrects the
disadvantage in that it off loads the transclusion of content on to a
specialized application who's only responsibility could be
transclusion.  Putting the transclusion on the edge allows you to more
easily horizontally scale the transclusion process if it proves to be
a bottleneck.

Another benefit of ESI is it's supported by major CDNs such as Akamai
and proxy servers such as Varnish.  Having the transclusion
responsibility in the edge allows you to exchange solutions
transparently to the user-agent or origin server.


Client-Side
~~~~~~~~~~~~

Client side transclusion occurs in the user-agent.  The benefits of
doing the transclusion is much my flexible and dynamic transclusion of
content. You have basically have a URI to some content and you can
place the content inside a page in the fly using client side
scripting.

An addition benefit is the user-agent can take advantage of client
side caching to eliminate network traffic all together.

Ideally you would take advantage of at a minimum, two layers
of caching.  Edge Side caching and Client Side caching.  You would
want these two layers for two reasons.  First, you can't trust
client's to cache.  Second, once the client hits the origin server and
a response has to be dynamically generated, throughput takes a
hit.  Whenever you can eliminate network traffic you win and whenever
you can eliminate application access, you win.

There are two ways to accomplish transclusion in HTML.  The simpliest
method of transclusion is an iframe.  It mimics the SSI and ESI
techniques but has two added benefits.  First, iframes takes advantage
of client side caching. Secondly the intent to include the content
explicit in the markup. The disadvantages to iframes are that you are
bound by a box on the page and they are cumbersome to make the feel
seamless [#].

.. [#] iframe's seamless attribute in HTML5 fixes the box bounding
.. problem, but it isn't implemented in even the most advanced HTML5
.. browsers at this time.

The second way to accomplish client-side transclusion is by using
AJAX.  The benefit to AJAX is that transclusion of partial content can
be accomplished by DOM transversial and manipulation.  The
jQuery.load() function makes this incredibily easy::

    // Insert the #header tag from the /static/base-template resource
    // into the #site-header tag of the current document
    jQuery("h1#site-header").load("/static/base-template #header")

Unfortunately it is incredibly hard use the HTML markup to determine
that the #header tag will be filled in with part of an external
document. Whereas an iframe would make that explicitly clear::

    <!-- include the header resource here -->
    <iframe src="/static/header/" />


Testing
--------

In the :ref:`Transclusion testing <testing/transclusion>`_ document
describes how the different methods of transclusion are testing.


Contents
===========

.. toctree::
   :maxdepth: 2
   
   testing/transclusion

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

