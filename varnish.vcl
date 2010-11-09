backend default {
  .host = "127.0.0.1";
  .port = "8000";
}

sub vcl_fetch {
    if (req.url == "/esi") {
        esi;  /* Do ESI processing */
    }
}
