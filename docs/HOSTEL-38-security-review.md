# HOSTEL-38 Security Review

Review scope: authentication, authorization, session handling, CSRF, cache controls, request validation, template output, login throttling, and deployment security settings across the Django application.

## Controls reviewed

- Administrator views require authentication and check is_staff. Student portal views require student authentication and resolve the student from the authenticated user.
- Student portal queries use the linked student and active allocation. The portal does not accept a student ID from the request to select whose data is shown.
- Room, hostel, student, and allocation operations validate input through Django forms, model constraints, or allocation services. Queries use the Django ORM; source review found no raw SQL, csrf_exempt, or mark_safe usage.
- CsrfViewMiddleware is enabled. State-changing views use POST, logout is POST-only, and the tests verify a POST without a CSRF token is rejected.
- Authentication uses Django's authentication and session APIs. Django hashes stored passwords; a test checks that the stored password differs from the submitted plaintext and still verifies correctly.
- Login failures use django-axes with its database handler. The configurable default blocks a username/IP pair after five failures in a rolling 15-minute window, returns HTTP 429, and clears the failure state after a successful login.
- Authenticated responses receive no-store/no-cache headers through middleware. The existing login and student portal views also use never_cache.
- Django templates retain automatic HTML escaping. Login errors are generic and do not reveal whether a username exists.

## Deployment security settings

Settings support environment-controlled HTTPS redirect, secure session and CSRF cookies, and HSTS. They also set HttpOnly and SameSite=Lax for session and CSRF cookies, X-Content-Type-Options: nosniff, Referrer-Policy: same-origin, and X-Frame-Options: DENY.

The .env.example values are for local HTTP development only. For deployment, set secure cookies and HTTPS redirect to match the actual TLS setup. Set HSTS only after HTTPS is live and verified for the hostname; HSTS can make browsers refuse HTTP for the configured duration.

## Policy and deployment notes

- The HOSTEL-38 description requires repeated-login protection but gives no numeric threshold. This PR uses five failures per username/IP pair in a rolling 15-minute window as its configurable default. Set AXES_FAILURE_LIMIT and AXES_COOLOFF_MINUTES to the team's chosen values if its policy differs.
- Login attempts are tracked in the database so throttling is shared across application processes. The Axes request records include the username/IP needed for enforcement; the optional detailed failure log is not enabled.
- The repository does not identify a verified deployment hostname or TLS termination/proxy configuration. HTTPS deployment and HSTS therefore remain deployment checks, not claims of completion. Do not enable HSTS preload or subdomain coverage until those hostnames are confirmed to support HTTPS.
- Header tests exercise Django response middleware. Reverse-proxy and hosting headers still need verification in the actual deployment environment.

## Verification

GitHub Actions passed Django checks, database migrations, and the full automated test suite for this pull request. No production deployment or external-host security scan is represented by this review.
