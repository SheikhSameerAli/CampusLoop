# Free deployment edition

For free hosting use **Render Free + Neon Free**. Start with `docs/FREE-DEPLOYMENT.md`. This edition supports PostgreSQL in the cloud and retains H2 for local use.

# CampusLoop — College Event Management System (Java Edition)

A runnable college project with a Java 17 backend, H2 relational database, and responsive HTML/CSS/JavaScript interface. Unlike the earlier static preview, accounts and registrations are stored on the server and survive browser changes and server restarts.

## Start on Windows

1. Install **Java 17 or later** (a JDK is needed if you want to rebuild the source).
2. Extract the complete ZIP into a folder such as `C:\CampusLoop-Java`. Keep `campusloop.jar`, `run.bat`, and the `lib` folder together.
3. Double-click **run.bat**. On the first run, enter the administrator email and a password of 10–128 characters. The password input is hidden. There is no default admin password.
4. Leave the terminal open. Visit **http://localhost:8080** in your browser.
5. Use **Join campus** to create student accounts, or sign in with your administrator credentials.
6. Stop the server using Ctrl+C. Start it again with run.bat; your database is retained.

The supplied compiled JAR and H2 driver allow the app to run without Maven or an internet connection. Opening `web/index.html` directly will not work: the Java server provides the API and frontend together.

## macOS / Linux

With Java 17+ installed, open a terminal in the extracted folder:

```sh
sh run.sh
```

To rebuild after changing source or web files:

```sh
sh build.sh
sh run.sh
```

On Windows, run `build.bat`, then `run.bat`. Stop the running server before rebuilding.

## Features

### Students
- Account creation with unique email and student ID; sign in and sign out.
- Browse, search, and filter events by category.
- Read event descriptions, times, venues, and actual available seat counts.
- Register and cancel before an event starts.
- View personal registrations, event cancellation updates, and attendance status.
- Download a calendar file for an event.
- Print or save a participation certificate as PDF after an admin confirms attendance.

### Administrators
- Server-enforced administrator access.
- Create and edit events, with future-date and seat-capacity validation.
- Participant lists containing student IDs, departments, and contact details.
- Mark or undo attendance after verifying student presence.
- Export participant CSV files (with spreadsheet formula escaping).
- Cancel events while preserving participant records.
- Delete events only when they have no registrations.
- Dashboard totals calculated from the actual database.

### Data and security
- H2 SQL database with primary keys, foreign keys, and uniqueness constraints.
- Prepared SQL statements; no SQL string interpolation of user input.
- Salted PBKDF2-HMAC-SHA256 password hashes (210,000 iterations).
- HttpOnly, SameSite=Strict session cookies with eight-hour expiry.
- CSRF tokens, request origin checks, request size limits, and sign-in rate limits.
- API authorization independent of whether a button is visible.
- Registration transactions and a shared write lock: two requests cannot take the last seat.
- Registration counts start at zero; sample events have no invented participants.
- Output escaping and a restrictive Content Security Policy.

## Database and backups

The database is created in `data/campusloop.mv.db`. Keep this file private. Back it up by stopping the server and copying the `data` folder. Restore with the server stopped. Do not delete the folder unless you intend to reset all accounts, events, and registrations. Do not run two app instances against the same folder.

Sample events are scheduled relative to the server's first run. Dates and displayed times use the college server's local timezone. Configure the operating system to the intended college timezone (for example, Asia/Kolkata).

Sessions are in memory and are intentionally invalidated when the server restarts. Password hashes and account details remain in the database. There is no password reset screen; retain the administrator credentials securely.

## Project structure

```text
CampusLoop-Java/
  src/campusloop/    Java source: HTTP routing, auth, database, JSON
  web/              HTML, CSS, JavaScript frontend
  lib/              H2 driver and license
  tests/            Automated API integration checks
  docs/             Architecture, API, and verification notes
  campusloop.jar    Compiled application with embedded frontend
  run.bat / run.sh  Start scripts
  build.bat / build.sh  Rebuild scripts
  data/             Created at first run; not included in the ZIP
```

## Automated verification

Requires Python 3, in addition to Java. Run from the project folder:

```sh
python tests/integration.py
```

The tests launch an isolated server with a temporary database and check signup, duplicate IDs/emails, login, permissions, CSRF, hostile origins, a race for the last seat, cancellation, attendance, capacity validation, deletion rules, and persistence across restart. Test data is removed afterward. Tests do not alter your real database.

## Optional configuration

Environment variables:

| Variable | Default / purpose |
| --- | --- |
| `PORT` | `8080` |
| `BIND_ADDRESS` | `127.0.0.1` (local computer only) |
| `DATA_DIR` | `data` relative to project directory |
| `ADMIN_EMAIL` | First-run bootstrap email; otherwise prompted |
| `ADMIN_PASSWORD` | First-run bootstrap password; otherwise prompted |
| `COOKIE_SECURE` | `false`; set to `true` when deployed behind HTTPS |

For a classroom demonstration across your LAN, set BIND_ADDRESS to `0.0.0.0`, allow the chosen port through your firewall, and use the host computer's LAN IP. Accounts and registrations will then be shared by all connected browsers. Use test accounts on plain HTTP. For internet hosting, use a Java-capable host, HTTPS reverse proxy, `COOKIE_SECURE=true`, backups, and additional operational hardening.

## Scope and honest limitations

This is a complete **college demonstration project**, not a production-audited service. Student IDs/emails are unique but not independently verified; a college roster or email delivery provider is not integrated. There are no email/SMS messages, password recovery, payments, or digitally signed certificates. Cancellation updates appear in the student's dashboard. Printable certificates are attendance acknowledgements, not independently verifiable credentials. Attendance depends on an administrator checking identity. Calendar files use floating local times; confirm the college timezone when importing.

Browser appearance and print layout were not visually tested in this environment. Automated API tests passed; Windows scripts were supplied but execution was verified on Linux only.

The Sites-hosted URL remains an explicitly labelled interactive preview and download page. Sites does not host this Java process. Run this package locally or deploy it to a Java-capable server for the real authenticated application.

## Dependency

H2 2.3.232 is distributed unchanged in `lib`. Its EPL 1.0 / MPL 2.0 license text is included as `lib/H2-LICENSE.txt`. Original project: https://h2database.com. No framework dependency is needed; the HTTP server is provided by the JDK.

## Final branding

Community-circle CampusLoop logo beside the header wordmark. Navy `#1C3068` and coral `#FF5757` with cool white backgrounds. Footer credit: Designed and developed by Sheikh Sameer Ali. The selected full-resolution logo artwork is included as `web/logo.png`; the header uses CSS framing to show its emblem without duplicating its wordmark.

PostgreSQL driver 42.7.14 is included in lib with its license. Hosted PostgreSQL uses JDBC_DATABASE_URL plus DATABASE_USER and DATABASE_PASSWORD. See docs/FREE-DEPLOYMENT.md.
