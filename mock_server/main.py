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

# Plan storage backend abstraction for demonstration
class UserPlanStore:
    """
    Demonstrates storing/retrieving user plan info.
    Currently uses an in-memory dictionary but could swap for environment-based or DB-backed storage.
    """
    _store: Dict[str, str] = {
        "alice": "free",
        "bob": "pro",
        "carol": "enterprise"
    }

    # PUBLIC_INTERFACE
    @classmethod
    def get_plan_for_user(cls, username: str) -> str:
        """
        Retrieves the plan for the given username.
        Currently from in-memory store.
        """
        return cls._store.get(username)

    # PUBLIC_INTERFACE
    @classmethod
    def set_plan_for_user(cls, username: str, plan: str):
        """
        Sets/overrides the plan for a user (for demonstration/testing).
        """
        cls._store[username] = plan

    # PUBLIC_INTERFACE
    @classmethod
    def load_from_env(cls, env_var="USER_PLANS"):
        """
        Load user plans from an environment variable (if demonstration requires it).
        Env var format: 'alice=free,bob=pro,carol=enterprise'
        """
        import os
        val = os.environ.get(env_var)
        if val:
            new_store = {}
            for entry in val.split(","):
                if "=" in entry:
                    user, plan = entry.split("=", 1)
                    new_store[user.strip()] = plan.strip()
            if new_store:
                cls._store = new_store

    # PUBLIC_INTERFACE
    @classmethod
    def all_user_plans(cls) -> Dict[str, str]:
        """
        Returns all current user-plan mappings (for demonstration).
        """
        return dict(cls._store)



# Note: Removed AuthAndPlanMiddleware. Username will be supplied as input parameter to route rather than header based.
from fastapi import Query

# PUBLIC_INTERFACE
@app.get("/user/data", tags=["user"], summary="Get user data with plan-specific response", responses={
    200: {
        "description": "User plan-specific data response",
        "content": {
            "application/json": {
                "example": {
                    "username": "alice",
                    "plan": "free",
                    "data": {
                        "message": "Hello alice, you are on the FREE plan! Limited access to features.",
                        "features": ["feature_a"]
                    }
                }
            }
        }
    },
    400: {"description": "Missing required parameter or user not found"},
})
async def get_user_data(
    username: str = Query(..., description="Username to fetch plan-based data for (e.g., alice, bob, carol)")
):
    """
    PUBLIC_INTERFACE

    Returns data tailored to the given user's assigned plan.

    - **Query Parameter**: username (required) - one of 'alice', 'bob', 'carol'
    - **Returns:** JSON with plan-specific content
    - **No header-based authentication required**
    """
    plan = UserPlanStore.get_plan_for_user(username)
    if not plan:
        raise HTTPException(status_code=404, detail=f"User '{username}' does not exist or has no assigned plan.")

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

# PUBLIC_INTERFACE
@app.get("/user/plan", tags=["user"], summary="View all user plan assignments")
async def get_all_user_plans():
    """
    Returns the current mapping of usernames to assigned plans.
    Demonstrates how plan mapping could be retrieved from backend storage.
    """
    return UserPlanStore.all_user_plans()

# PUBLIC_INTERFACE
@app.post("/user/plan", tags=["user"], summary="Assign or update a user's plan")
async def update_user_plan(username: str, plan: str):
    """
    Assign or update a specific user's plan for demonstration/testing purposes.
    In a real system, such changes would be restricted to admin only.
    """
    UserPlanStore.set_plan_for_user(username, plan)
    return {"message": f"Plan for user '{username}' set to '{plan}'."}

@app.get("/", tags=["user"], summary="Basic health check endpoint")
async def root():
    """PUBLIC_INTERFACE
    Quick health check of the mock server.
    """
    return {"status": "ok", "message": "Mock server is running."}

