<p align="center">
  <img src="web/logo.png" alt="CampusLoop — College Event Management" width="280">
</p>

<h1 align="center">CampusLoop</h1>
<p align="center"><strong>Your campus. Your events. Stay in the loop.</strong></p>
<p align="center">A Java-based College Event Management System connecting students and event organizers.</p>
<p align="center"><a href="https://campusloop-1b6y.onrender.com"><strong>Open CampusLoop — Live Website ↗</strong></a></p>

---

## About the project

CampusLoop brings event discovery, registration, participant management, and attendance into one website. Students can explore campus activities and reserve a place, while administrators can organize events and manage participation.

The project uses a **Java 17 backend**, a responsive **HTML/CSS/JavaScript frontend**, and **SQL storage**. It supports **H2 for local use** and **PostgreSQL for cloud deployment**. No Spring Boot, Maven, or Node.js installation is required to run the bundled local application.

The name combines **Campus**, representing college life, with **Loop**, representing a connected community that keeps everyone informed.

## Features

| For students | For administrators |
| --- | --- |
| Create an account with a unique email and student ID | Sign in with a separate administrator role |
| Search events and filter by category | Create and edit event details |
| View descriptions, venues, dates, and available seats | Set seat limits and view actual registrations |
| Register or cancel before an event starts | View participants and export CSV lists |
| View personal registrations and cancellation updates | Mark or undo attendance |
| Download event calendar files | Cancel events while preserving participant records |
| Print a participation certificate after attendance confirmation | Delete events that have no registrations |

Event categories: **Technical, Cultural, Sports, Workshop, and Community**.

## Technology stack

| Layer | Technology |
| --- | --- |
| Backend | Java 17, JDK HttpServer |
| Frontend | HTML5, CSS3, vanilla JavaScript |
| Database access | JDBC and prepared statements |
| Local database | H2 |
| Cloud database | PostgreSQL, compatible with Neon |
| Deployment | Docker; Render configuration included |
| API integration tests | Python 3 standard library |

## Run locally

### Requirements

- Java 17 or later; install a JDK if you want to rebuild the source.
- A modern browser.
- Git if you are cloning the repository.

Download the repository or clone it using its GitHub URL. Open the project folder containing `run.bat`, `run.sh`, and `campusloop.jar`.

For local H2 operation, leave the external database variables and `REQUIRE_EXTERNAL_DB` unset.

### Windows / VS Code

Open the project folder in VS Code, select **Terminal → New Terminal**, and run:

```powershell
java -version
.\run.bat
```

### macOS / Linux

```sh
java -version
sh run.sh
```

On the first startup, enter your chosen administrator email and a password of **10–128 characters** when prompted. There is no default administrator password.

Open **http://localhost:8080**. Keep the terminal running and press **Ctrl+C** to stop the application.

Use **Join campus** to create student accounts. Opening `web/index.html` directly or using VS Code Live Server does not start the Java backend.

### Rebuild after changes

Stop the server before rebuilding.

Windows:

```powershell
.\build.bat
.\run.bat
```

macOS / Linux:

```sh
sh build.sh
sh run.sh
```

The build includes the frontend and logo inside `campusloop.jar`.

## Deploy with Render and Neon

The repository includes a Dockerfile and a Render Blueprint configured for a **Free** web service. Use a separate Neon PostgreSQL database for persistent cloud data; do not rely on the web service's temporary filesystem.

1. Create a Neon database and obtain its connection details.
2. Create a Render Web Service from this repository using the **Docker** runtime and **Free** instance, or use `render.yaml` as a Blueprint.
3. Add the environment variables below in Render.
4. Set the health check path to **`/api/health`**.
5. Deploy and open the HTTPS URL provided by Render.

| Variable | Value / purpose |
| --- | --- |
| `JDBC_DATABASE_URL` | `jdbc:postgresql://YOUR-NEON-HOST/YOUR-DATABASE?sslmode=require` |
| `DATABASE_USER` | Your Neon database username |
| `DATABASE_PASSWORD` | Your Neon database password; store as a secret |
| `ADMIN_EMAIL` | Email for the administrator created on first startup |
| `ADMIN_PASSWORD` | Unique administrator password of at least 10 characters; store as a secret |
| `REQUIRE_EXTERNAL_DB` | `true` |
| `BIND_ADDRESS` | `0.0.0.0` |
| `COOKIE_SECURE` | `true` for hosted HTTPS |

**The JDBC URL must not contain the username, password, or `@`.** Enter credentials only in their separate variables. Never commit passwords, `.env` files, connection strings containing credentials, or database backups.

The Docker image honors the host's `PORT` and uses the `Asia/Kolkata` timezone. Cloud mode refuses to start without PostgreSQL configuration, preventing accidental use of temporary local storage.

Choose the providers' Free plans and stay within their current usage limits. Free services may sleep or suspend when limits are reached. This repository does not guarantee unlimited hosting or fixed provider pricing.

Online deployment creates a separate database; local accounts and registrations are not automatically migrated. Keep the service at **one instance**, matching the application's write-lock design.

Detailed setup: [Free deployment guide](docs/FREE-DEPLOYMENT.md). Provider documentation: [Render](https://render.com/docs/free) and [Neon](https://neon.com/docs).

## Data and registration rules

- Local records are stored in `data/campusloop.mv.db`; cloud records use the configured PostgreSQL database.
- Emails, student IDs, and student/event registration pairs have uniqueness constraints.
- Registration changes close when an event starts.
- Seat checks and registration inserts run within a transaction under a shared application write lock.
- Capacity cannot be reduced below the existing registration count.
- Cancelled events retain participant records and appear as cancelled in students' dashboards.
- Attendance-confirmed students can print certificates for non-cancelled events.
- Sessions expire after eight hours and are invalidated by a server restart.
- Bootstrap admin variables create the first administrator; changing those variables later does not reset an existing password.

For local backups, stop the server before copying the `data` directory. Keep database files private and out of Git.

## Security controls

- Salted PBKDF2-HMAC-SHA256 password hashes.
- Server-side role checks and prepared SQL statements.
- HttpOnly, SameSite session cookies; Secure cookies for hosted HTTPS.
- CSRF tokens and request-origin validation for authenticated changes.
- Sign-in rate limiting, input validation, and request size limits.
- Escaped output and a Content Security Policy.

## Project structure

| Path | Purpose |
| --- | --- |
| `src/campusloop/` | Java HTTP server, authentication, database access, and JSON encoding |
| `web/` | Frontend HTML, CSS, JavaScript, and logo |
| `lib/` | Bundled database drivers and license notices |
| `docs/` | Architecture, API, deployment, and verification notes |
| `tests/integration.py` | Automated API integration checks |
| `campusloop.jar` | Compiled application with embedded frontend |
| `run.bat` / `run.sh` | Local startup scripts |
| `build.bat` / `build.sh` | Rebuild scripts |
| `Dockerfile` / `render.yaml` | Cloud build and service configuration |

## Testing

With Java and Python 3 installed, run from the project folder **with cloud database environment variables unset**:

```sh
python tests/integration.py
```

The suite starts an isolated Java server using temporary local H2 storage. It covers account creation, login, duplicate prevention, permissions, CSRF checks, last-seat concurrency, event cancellation, attendance, capacity validation, deletion restrictions, logo delivery, and persistence after restart.

Local integration checks passed during development. Hosted PostgreSQL connectivity and deployment must be verified in the target environment. Browser appearance, print output, and Windows execution require checks on the target computer.

## Branding

| Element | Colour |
| --- | --- |
| Primary | Navy `#1C3068` |
| Accent | Coral `#FF5757` |
| Background | Cool white `#F5F7FC` |
| Main text | Dark navy `#17213B` |

The community-circle logo represents students coming together through campus events.

## Current limitations

This is an academic project. Email/student ID ownership is not independently verified. Email/SMS notifications, account recovery, payments, and digitally signed certificates are not included. Certificates are printable participation acknowledgements based on administrator-recorded attendance. Sessions and sign-in rate limits are held in memory, and the application targets one running instance.

## Documentation

- [Architecture and viva notes](docs/ARCHITECTURE.md)
- [API reference](docs/API.md)
- [Free deployment guide](docs/FREE-DEPLOYMENT.md)
- [Verification notes](docs/VERIFICATION.md)

Bundled H2 and PostgreSQL drivers retain their respective license notices in `lib/`.

---

<p align="center"><strong>Designed and developed by Sheikh Sameer Ali</strong></p>
