# API reference

All paths start with `/api/`. GET returns JSON. POST consumes `application/x-www-form-urlencoded` and returns JSON. Errors use `{"error":"message"}` with an appropriate 4xx/5xx status. Cookies identify the session. Obtain the CSRF value from `GET /api/me` and send `X-CSRF-Token` for authenticated POST requests.

| Method | Path | Permission / request fields |
| --- | --- | --- |
| GET | /health | Public process health; no database query |
| GET | /me | Anyone; user and csrf, or null |
| POST | /signup | Anyone; name, email, studentId, department, password; creates student and session |
| POST | /login | Anyone; email, password |
| POST | /logout | Signed-in user + CSRF |
| GET | /events | Anyone; event details and actual booked counts |
| GET | /registrations | Signed-in user; only own registrations |
| POST | /register | Student + CSRF; eventId |
| POST | /unregister | Student + CSRF; eventId |
| GET | /admin/participants?eventId=ID | Admin; participant records |
| POST | /admin/save-event | Admin + CSRF; optional id; name, category, description, startsAt, venue, capacity |
| POST | /admin/cancel-event | Admin + CSRF; eventId |
| POST | /admin/delete-event | Admin + CSRF; eventId; must have no registrations |
| POST | /admin/attendance | Admin + CSRF; registrationId, attended (true/false) |

Times use an ISO local datetime such as `2026-11-06T09:00`. Invalid, duplicate, expired, unauthorized, or full-event operations are rejected by the server even if the frontend is bypassed.
