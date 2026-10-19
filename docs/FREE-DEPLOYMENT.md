# Free hosting: Render Free + Neon Free

Choose Free plans on both services and stay within their usage limits. This setup stores accounts, events, and registrations in PostgreSQL on Neon, independently of Render's temporary filesystem. It does not require a paid Render disk. Free plan availability/limits can change.

## 1. Create a Neon Free database

- Sign up at https://neon.com and choose Free (do not enable a paid plan).
- Create a project/database for CampusLoop, preferably near your Render service's region.
- Open Connect and obtain the hostname, database name, role/username, and password. You can use the direct endpoint for this single-instance college project.
- Configure the JDBC URL using the returned host and database. Example format only:

```text
jdbc:postgresql://YOUR-HOST.neon.tech/YOUR-DATABASE?sslmode=require
```

The real hostname and database come from your Neon project. Do not include a username or password in the URL; use the separate secret fields below. Do not paste secrets into chat or commit them to Git.

## 2. Upload the project to GitHub

Create a repository and upload the CONTENTS of the extracted `CampusLoop-Java` folder. `Dockerfile`, `render.yaml`, `src`, `web`, `build.sh`, and `lib` must be at the repository root. Do not upload a data folder, .env files, database backups, or credentials.

A GitHub account and connected repository are needed for the standard Render Git deployment flow.

## 3. Deploy the Free web service

In Render, create a Web Service from that repository. Use Docker and choose the **Free** instance type. Do not add a disk or paid database. Keep one service instance.

Set these environment variables/secrets:

| Name | Value |
| --- | --- |
| JDBC_DATABASE_URL | Your PostgreSQL JDBC URL from step 1 |
| DATABASE_USER | Your Neon database role/username |
| DATABASE_PASSWORD | Your Neon database password (secret) |
| ADMIN_EMAIL | Email you choose for the new admin account |
| ADMIN_PASSWORD | Unique password, at least 10 characters (secret) |
| REQUIRE_EXTERNAL_DB | true |
| BIND_ADDRESS | 0.0.0.0 |
| COOKIE_SECURE | true |

Set the health check path to `/api/health`. The Dockerfile provides the start command and honors Render's PORT. Alternatively, create a Blueprint using the included `render.yaml` (explicitly configured with `plan: free`) and fill in its required secret values.

The application refuses cloud startup without PostgreSQL settings instead of falling back to temporary H2 storage.

Deploy, wait until the service is live, and open its HTTPS URL. Sign in with the administrator credentials you configured. Create student accounts and test event registration.

## 4. Verify persistence

Create a student and registration, redeploy/restart Render, log in again, and confirm the records remain. Sessions are intentionally invalidated on restart; signing in again is expected. PostgreSQL data is independent of the Render application instance.

Your existing localhost database is not transferred automatically. This setup creates a new online database. Keep local data private; migration can be arranged separately if needed.

## Free-plan limitations

As checked on 19 October 2026:
- Render Free web services sleep after 15 minutes of inactivity. A returning request can take about a minute to wake the service.
- Render Free has monthly resource limits. A service can be suspended when limits are reached. Do not add a paid plan or payment method if your requirement is strictly no charges.
- Neon Free includes limited storage and compute. Check the current dashboard allowance and remain on Free. The published plan currently lists 1 GB storage and 100 CU-hours per project monthly.
- The health endpoint does not query the database, avoiding unnecessary PostgreSQL wake-ups from health polling.
- No credentials or accounts are created until you configure your own services. This package is not itself a completed deployment.

References: https://render.com/docs/free, https://neon.com/pricing, https://jdbc.postgresql.org/download/

## Local operation and testing

For local use, leave JDBC_DATABASE_URL, DATABASE_USER, DATABASE_PASSWORD, and REQUIRE_EXTERNAL_DB unset; run.bat/run.sh continue to use the on-disk H2 database.

For local Docker with H2, explicitly override `REQUIRE_EXTERNAL_DB=false` and `COOKIE_SECURE=false`; the image defaults are for hosted HTTPS plus external PostgreSQL.

Verification: the application compiles, local H2 API integration checks pass, and the PostgreSQL driver is bundled. Hosted PostgreSQL connectivity and the Docker build still require verification after your accounts are connected. No Docker engine or Neon credentials were available in the preparation environment.
