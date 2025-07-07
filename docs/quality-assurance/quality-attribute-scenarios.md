## Performance Efficiency
### Time Behavior
#### Why is it important?
Users expect fast, responsive access to the course catalog and learning content. If the platform is slow, especially when filtering courses or navigating between pages, it creates frustration and reduces trust.
#### QAS test
| Attribute            | Value                                                                           |
| -------------------- | --------------------------------------------------------------------------------|
| **Stimulus**         | A user submits a query during peak load.                                        |
| **Environment**      | Production VPS with async FastAPI and PostgreSQL under 100 concurrent users.    |
| **Artifact**         | `/courses` endpoint.                                                            |
| **Response**         | Returns a list of courses within 500 milliseconds.                              |
| **Response Measure** | 95th percentile response time ≤ 500ms under 100 concurrent users.               |
#### Actual test implementation
- Use Locust framework to simulate 100 users sending GET requests to `/courses`.
- Measure response times and ensure they meet the target.
- Monitor CPU/memory usage via `htop` to ensure system remains stable under load.
  
## Reliability
### Fault Tolerance
#### Why is it important?
Fault tolerance ensures that occasional backend problems don't result in a broken or inaccessible product. Customers appreciate systems that “fail gracefully” rather than unexpectedly.
#### QAS test
| Attribute            | Value                                                                                |
| -------------------- | ------------------------------------------------------------------------------------ |
| **Stimulus**         | A user sends a request while the database is temporarily unavailable.                |
| **Environment**      | VPS-hosted production environment with PostgreSQL offline or restarting.             |
| **Artifact**         | FastAPI backend using async SQLAlchemy.                                              |
| **Response**         | System returns an error message, logs the issue, and remains operational.            |
| **Response Measure** | Returns error within 2 seconds; service stays online; logs contain full error trace. |
#### Actual test implementation
- Intentionally stop the PostgreSQL service.
- Send a request to the /courses endpoint.
- Verify:
  - HTTP 500 or custom error response is returned within 2 seconds.
  - Server remains up and responds to other requests (e.g., health check).
  - Logs include meaningful diagnostic information.

## Compatibility
### Interoperability
#### Why is it important?
Users expect seamless access to the platform using tools they already trust and use (like Telegram). Interoperability ensures that external systems like Telegram can reliably communicate with Daha without breaking or needing workarounds.
#### QAS test
| Attribute            | Value                                                                                                                |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Stimulus**         | A user attempts to log in using the Telegram login widget.                                                           |
| **Environment**      | Staging environment with Telegram authentication integration.                                                        |
| **Artifact**         | Telegram login module and FastAPI route for authentication.                                                          |
| **Response**         | The system receives and correctly parses Telegram-signed data, then logs in the user.                                |
| **Response Measure** | Login works reliably across different Telegram clients (mobile, desktop); 100% compliance with Telegram’s login API. |
#### Actual test implementation
- Prepare Telegram login test payload (simulate from client).
- Send payload to backend login route.
- Verify Backend Behavior:
  - Response is 200 OK if hash is correct.
  - Response is 401 Unauthorized if tampered hash is sent.
  - Logged-in user data matches Telegram profile.
