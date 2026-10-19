# Architecture and viva notes

## Request flow

Browser -> Java HttpServer -> session/CSRF/role validation -> prepared JDBC statement -> H2 database -> JSON response -> frontend rendering.

The frontend is served by the same Java process as the API, so no cross-origin API configuration is required. Assets are embedded in the compiled application.

## Java classes

| Class | Responsibility |
| --- | --- |
| App | Startup, admin bootstrap, routing, sessions, validation, API authorization, HTTP responses |
| Database | Schema initialization, sample events, JDBC connections, reusable prepared queries |
| Security | Secure random session tokens and PBKDF2 password hashes |
| Json | Output-only JSON serialization, including escaped strings |

Core Java concepts demonstrated: classes, encapsulation, records, collections, exceptions, threads, synchronization, JDBC, prepared statements, I/O, and HTTP request processing.

## Tables

- users: id, name, email (unique), student_id (unique), department, password_hash, role.
- events: id, name, category, description, starts_at, venue, capacity, status.
- registrations: id, event_id (foreign key), user_id (foreign key), registered_at, attended. Unique pair (event_id, user_id).

A student has many registrations, an event has many registrations, and each registration belongs to exactly one student and one event. This resolves the many-to-many relationship.

## Seat integrity

The application serializes all write operations through one monitor. Registration begins a JDBC transaction, checks that the event is open and in the future, checks for a duplicate registration, counts occupied seats, inserts the row, and commits. A unique constraint provides an additional duplicate guard. This model targets one application instance; it is not a multi-instance distributed locking design.

## Lifecycle rules

- Registration and cancellation close at the event start.
- Cancelled events retain registrations and display a cancellation update.
- Cancelled events cannot be edited or receive attendance changes.
- Events with registrations cannot be deleted.
- Capacity cannot be reduced below current registration count.
- Administrators cannot register as students; create a separate student account for that use.
- Certificates become available only for attendance-confirmed, non-cancelled events.

## Authentication

The administrator is created during the first startup. Student signup cannot set the role. Login uses a generic credential error, a salted password hash, an eight-hour random server-side session, and a cookie inaccessible to frontend JavaScript. A separate session CSRF token is required on authenticated mutations. Sign-out removes the session. Restart invalidates all sessions.

## Classroom demonstration

1. Start the Java server and create an administrator.
2. Create a student in a normal browser window.
3. Sign into the administrator in a private window; create an event with one seat.
4. Register as the student and observe the shared count in the administrator window (or reload).
5. Try registering another student; the server rejects overbooking.
6. Mark the participant present and print the student's certificate.
7. Export participants as CSV.
8. Cancel the event; the student sees the update.
9. Restart the server, log in again, and show that data persists.
