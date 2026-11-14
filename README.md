# My Approach to Web Application and Infrastructure Enumeration

Lab files behind the write-up of the same name. Covers subdomain enumeration,
virtual host discovery, directory/content discovery, DNS investigation
(including a zone transfer), service enumeration, and reading unexpected HTTP
response codes — all run for real against a small local lab, not simulated.

## What's running

- A custom Python HTTP server (`vhost_server.py`) that answers differently
  depending on the `Host` header it receives — `blog.corp.local`,
  `admin-panel.corp.local`, and a default vhost — so `ffuf`'s vhost-discovery
  mode has something real to distinguish.
- A plain webroot (`webroot/`) with `admin/`, `backup/`, `.git/`, and
  `uploads/` directories, for directory/content discovery with `ffuf`.
- A local authoritative BIND9 zone for `corp.local` (listening on
  `127.0.0.1:5353`) that allows AXFR, so the zone-transfer step in the post is
  a real transfer, not a canned example.

## Reproducing it

```bash
# BIND zone (adjust paths for your system's bind config layout)
cp lab/bind/db.corp.local /etc/bind/zones/
cp lab/bind/named-local.conf /etc/
named -c /etc/named-local.conf -u bind

# vhost server
python3 lab/vhost_server.py   # serves lab/vhostroot/{blog,admin-panel,main}

# plain webroot for directory brute-forcing
cd lab/webroot && python3 -m http.server 8889
```

Then run the real `nmap`, `ffuf`, and `dig` commands from the write-up against
these.

## Contents

- `lab/vhost_server.py` — Host-header-aware HTTP server.
- `lab/vhostroot/` — the three vhosts it serves.
- `lab/webroot/` — target directory tree for content discovery.
- `lab/bind/` — the zone file and named config used for the AXFR demo.
- `lab/render_term2.py` — the terminal-screenshot renderer (handles ANSI stripping and `ffuf`'s `\r`-joined progress-line noise).
- `screenshots/` — the real screenshots embedded in the post (nmap, AXFR, NS/A record lookups, ffuf vhost discovery, ffuf directory discovery, curl status codes).
- `terminal-output/` — the raw captured command output behind each screenshot.
