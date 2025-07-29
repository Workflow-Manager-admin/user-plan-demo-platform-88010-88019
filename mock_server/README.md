# Mock Server: User Plan Demo

This mock server demonstrates how the same API endpoint can produce different responses for different users based on their assigned "plan". It uses FastAPI and a simple middleware-based authentication and plan identification mechanism.

## Features

- Username-based login via custom header (`X-Username`)
- Plan identification (users: alice=free, bob=pro, carol=enterprise)
- API route (`/user/data`) reacts differently depending on user's plan

## How to Run

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

## How to Use

Send requests to `/user/data` with header `X-Username` set to one of:
- alice (free plan)
- bob (pro plan)
- carol (enterprise plan)

Example (with HTTPie):

```bash
http GET http://localhost:8000/user/data X-Username:alice
http GET http://localhost:8000/user/data X-Username:bob
http GET http://localhost:8000/user/data X-Username:carol
```

You should see different responses for each user, showing how APIs can provide differentiated behaviours per user plan.

## Health Check

`GET /` returns a simple status payload.
