.. REST vs The World documentation master file, created by
   sphinx-quickstart on Wed Nov 10 19:09:47 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

REST vs The World
=============================================

Modern web applications have a number of requirements that both
developers need and users need.  These experiments will compare
solutions presented by REST proponents versus current solutions.

Whenever the status quo is challenged, the burden of proof is on the
challenger.

Each solution presented effects the entire system.  I will start with
small tests and create new tests based of the results

Hypothetical Web Application
-----------------------------

I am creating a hypothetical web application that is basically a
service for getting information about myself.  This application will
in the end have all the functionality of a modern web application
should have.  I will solve the problem in each phase of the
development using as many solutions that I can come up with using both
conventional solutions and RESTful solutions.

Data
~~~~~

I have two pieces of data inside my "database". The first piece is
information the name of my wife, the second piece of information is a
list of the names of my two sons.

I will need to create a compound piece of data which I will call my
"family profile".  That compound piece of data is the combination of
the name of my wife and the names of my two sons.

This profile is the homepage of my application.

Phase One
---------

I need to present my family profile to the world.

Phase Two
---------

Oh no! my database has started sucking.  It's now taking 10ms per db record
Let's see how my application has faired.

Contents:

.. toctree::
   :maxdepth: 2
   
   phase1
   phase2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

