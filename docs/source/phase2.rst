Phase 2
===============

Oh No! My database has started sucking.  It is now taking 10ms for
every query. What Am I to do?

Methodology
------------

Ran the same test as phase1 but with a time.sleep(0.01) before each
access to the spouse and children data.

Results
--------

This test establishes a baseline for optimizing access to slow queries

.. raw:: html

  <script
    src="_static/highcharts.js"
    type="text/javascript"></script>
  <script
    src="_static/csvchart.js"
    type="text/javascript"></script>
  <script
    src="_static/phase2.js"
    type="text/javascript"></script>


  <div id="phase2-rps-chart"></div>

  <div id="phase2-tpr-chart"></div>


Conclusion
-----------

When realistic load is applied the individual implementations end up
becomes normalized.  The sub-millisecond differences become
negligible.

There is bad news. When there is load, Varnish has trouble accepting
connections between the 750-1000 concurrency levels.  These are high
concurrency levels and it's likely you would load balance the servers
before you reach those levels.  I am not certain why this is the case.
