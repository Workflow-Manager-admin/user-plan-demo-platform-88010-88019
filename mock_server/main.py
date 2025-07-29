from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Dict

app = FastAPI(
    title="Mock Server with User Plan Demo",
    description="API returns different data based on authenticated user's plan.",
    version="1.0.0",
    openapi_tags=[
        {"name": "user", "description": "User-specific API endpoints"}
    ]
)

# In-memory user-plan mapping for demo purposes
USER_PLANS: Dict[str, str] = {
    "alice": "free",
    "bob": "pro",
    "carol": "enterprise"
}


class AuthAndPlanMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts username from the 'X-Username' header,
    authenticates the user, and attaches the user's plan to the request.state.
    """
    async def dispatch(self, request: Request, call_next):
        username = request.headers.get('X-Username')
        if not username:
            return JSONResponse(status_code=401, content={"error": "X-Username header missing"})

        plan = USER_PLANS.get(username)
        if not plan:
            return JSONResponse(status_code=403, content={"error": f"User {username} does not exist or has no assigned plan."})
        # Attach user and plan to state
        request.state.username = username
        request.state.plan = plan
        response = await call_next(request)
        return response

# Add the middleware to the app
app.add_middleware(AuthAndPlanMiddleware)


def get_current_user_plan(request: Request) -> Dict[str, str]:
    """
    Dependency to extract the current username and plan from the request.
    """
    # PUBLIC_INTERFACE
    return {
        "username": getattr(request.state, "username", None),
        "plan": getattr(request.state, "plan", None)
    }


@app.get("/user/data", tags=["user"], summary="Get user data with plan-specific response")
async def get_user_data(user_info: dict = Depends(get_current_user_plan)):
    """
    Returns data tailored to the user's assigned plan. Demonstrates concept of differentiated API behaviour.

    - **Header**: X-Username: REQUIRED, one of 'alice', 'bob', 'carol'
    - **Returns:** JSON with plan-specific content
    """
    # PUBLIC_INTERFACE
    username = user_info["username"]
    plan = user_info["plan"]

    # Example: Change API results based on plan
    if plan == "free":
        data = {
            "message": f"Hello {username}, you are on the FREE plan! Limited access to features.",
            "features": ["feature_a"]
        }
    elif plan == "pro":
        data = {
            "message": f"Hi {username}, thanks for subscribing to the PRO plan. More features unlocked!",
            "features": ["feature_a", "feature_b", "priority_support"]
        }
    elif plan == "enterprise":
        data = {
            "message": f"Welcome {username}, ENTERPRISE customer! All features and premium support enabled.",
            "features": ["feature_a", "feature_b", "feature_c", "premium_support", "analytics"],
            "dedicated_manager": True
        }
    else:
        raise HTTPException(status_code=500, detail="Unrecognized plan for user.")

    return {"username": username, "plan": plan, "data": data}


@app.get("/", tags=["user"], summary="Basic health check endpoint")
async def root():
    """PUBLIC_INTERFACE
    Quick health check of the mock server.
    """
    return {"status": "ok", "message": "Mock server is running."}

