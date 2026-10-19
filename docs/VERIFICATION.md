# Verification

Verified in the build environment using Java 17 and Python 3.

- All Java source compiled successfully for Java 17.
- JavaScript syntax passed Node's syntax checker.
- API integration suite passed against a real Java server and temporary H2 database.
- Checks included unique accounts, role enforcement, CSRF rejection, hostile origin rejection, last-seat concurrency, duplicate registration prevention, cancellation, capacity validation, attendance persistence, event deletion restrictions, session invalidation, and database persistence after restart.
- The application serves HTML/CSS/JS with the expected Content Security Policy.
- ZIP integrity and required entries checked before delivery.

No browser automation capability was available. Responsive appearance, print output, calendar application imports, and Windows execution require manual checks on the target computer. Email delivery, recovery flows, load testing, multi-instance deployment, and independent security review are outside this version's scope.

Final branding check: selected navy/coral logo, header placement, developer credit, and byte-exact PNG serving passed. The compiled JAR includes the final CSS, HTML, and logo.
