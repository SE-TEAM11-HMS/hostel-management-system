# HOSTEL-38 Security Review

Review scope: authentication, authorization, session handling, request validation, template output, and deployment security settings across the Django application.

## Controls confirmed in the current code

- Administrator views require authentication and check is_staff; student portal views require a student login and resolve the student from the authenticated user.
- Student portal queries use the linked student and active allocation. The portal does not accept a student ID from the request to select whose data is shown.
- Room, hostel, student, and allocation operations validate input through Django forms, model constraints, or allocation services. The application uses Django ORM queries; the source search found no raw SQL, csrf_exempt, or mark_safe usage.
- CsrfViewMiddleware is enabled. State-changing views use POST, and logout is POST-only.
- Authentication uses Django's authenticate and session APIs. User creation uses Django's password-hashing APIs; this project does not implement custom password storage.
- Django templates retain automatic HTML escaping. Login errors are generic and do not reveal whether a username exists.
- The existing tests cover role restrictions, denied writes, logout, and session termination. This change adds checks for security response headers and strict parsing of boolean security environment values.

## Configuration added

The settings now support environment-controlled HTTPS redirect, secure session and CSRF cookies, and HSTS. They also explicitly set HttpOnly and SameSite=Lax for session and CSRF cookies, X-Content-Type-Options: nosniff, Referrer-Policy: same-origin, and X-Frame-Options: DENY.

The .env.example values are for local HTTP development only. For deployment, set secure cookies and HTTPS redirect to match the actual TLS setup. Set HSTS only after HTTPS is live and verified for the hostname; HSTS can make browsers refuse HTTP for the configured duration.

## Decisions and deployment follow-up

- Failed-login throttling: No throttling or account lockout behavior was added. The security requirement asks for the approved SAD/security policy before changing this behavior. Confirm the policy with the faculty/team, then implement a shared, production-suitable rate limit if required. Avoid per-process memory counters for a multi-worker deployment.
- HTTPS/HSTS: The repository does not identify a verified deployment hostname or TLS termination/proxy configuration. HTTPS deployment and HSTS therefore remain deployment checks, not claims of completion. Do not enable HSTS preload or subdomain coverage until those hostnames are confirmed to support HTTPS.
- Security headers: Header tests exercise the Django response middleware. Reverse-proxy and hosting headers still need verification in the actual deployment environment.

## Verification

CI is the verification source for this pull request. No production deployment or external-host security scan is represented by this review.