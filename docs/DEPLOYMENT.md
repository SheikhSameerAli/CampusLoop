# Free hosting is the selected setup

Use `FREE-DEPLOYMENT.md` and the included free Render Blueprint. The older H2-on-disk instructions below are an alternative for paid hosting only. With the current cloud Docker defaults, external PostgreSQL is required. To use the older disk-based setup, explicitly set REQUIRE_EXTERNAL_DB=false.

# Deploy the complete Java application

The root Dockerfile builds the Java application and packages the frontend. The image binds to 0.0.0.0 and honors the hosting platform's PORT environment variable. No passwords are embedded in the image.

## Render setup

1. Create a Git repository containing the CONTENTS of CampusLoop-Java, with Dockerfile at the repository root. Do not upload data, .env files, credentials, or personal database backups.
2. In Render create a Web Service from that repository. Choose Docker as its language/runtime. Use Dockerfile at the root; do not specify a custom start command.
3. Set the following environment variables in the hosting dashboard:

| Name | Value |
| --- | --- |
| ADMIN_EMAIL | Your chosen administrator email |
| ADMIN_PASSWORD | A unique password of at least 10 characters; save as a secret |
| BIND_ADDRESS | 0.0.0.0 |
| DATA_DIR | /var/data |
| COOKIE_SECURE | true |

PORT is supplied by the host. The Dockerfile sets the other defaults already, but they may also be configured in the dashboard. Keep the password private; do not put it in a repository or send it in chat.

4. For durable accounts and registrations, choose a paid web service and attach a persistent disk at `/var/data`. Review the host's current pricing before confirming a paid service. Keep a single service instance because this application uses an embedded H2 database.
5. Set the health check path to `/api/events`.
6. Deploy and wait for the healthy/live result. Open the provided HTTPS URL, sign in as admin, and create a student in a separate browser session.
7. Test creating an event, registering a student, marking attendance, and restarting/redeploying the service. Confirm that accounts and registrations remain available after signing in again.

The first deployment creates a NEW database and admin account. It does not automatically copy your localhost data. If you need existing data migrated, stop the local Java process and arrange a private transfer of the database folder before launching against it.

Free Render web services do not support persistent disks. A free deployment without external database integration is only a temporary demo: its accounts, event changes, and registrations can be lost on restart/redeploy. Do not present that configuration as durable hosting.

## Local Docker check (requires Docker)

Build from the project directory:

```sh
docker build -t campusloop .
```

Set ADMIN_EMAIL and ADMIN_PASSWORD in your local environment, then run:

```sh
docker run --rm -p 8080:8080 -v campusloop-data:/var/data -e ADMIN_EMAIL -e ADMIN_PASSWORD -e COOKIE_SECURE=false campusloop
```

Open http://localhost:8080. COOKIE_SECURE=false is for this local HTTP test only; leave it true on the hosted HTTPS site. The volume keeps database data when the container is replaced.

## Operational limits

This remains a college project: before broad production use, add verified student identity, account recovery, audited backups, and independent security review. The current login rate limit is keyed by the remote network address; behind a hosting reverse proxy, requests may share that address and its sign-in limit. Never trust forwarded IP headers without configuring and validating a trusted proxy.

Credentials are only used to create the first admin on an empty database. Changing ADMIN_PASSWORD later does not reset the stored account password. Retain your credentials securely.

## Verification status

The Java application and API integration suite passed. The Dockerfile and build inputs were checked, but a Docker engine was not available in the preparation environment. A container build and hosted health check must pass before deployment is considered verified.

References: https://render.com/docs/docker and https://render.com/docs/disks
