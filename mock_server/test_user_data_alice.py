import requests

def test_user_data_for_alice():
    """
    Tests that the /user/data endpoint returns correct details for username='alice' (free plan).
    """
    # Assuming the server is running locally on port 8000
    base_url = "http://localhost:8000/user/data"
    params = {"username": "alice"}

    response = requests.get(base_url, params=params)
    assert response.status_code == 200, f"Unexpected status code {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data["username"] == "alice", f"Expected username 'alice', got {data.get('username')}"
    assert data["plan"] == "free", f"Expected plan 'free', got {data.get('plan')}"

    features = data["data"].get("features", [])
    assert "feature_a" in features, "Expected 'feature_a' in features for free plan"
    # Free plan should not have premium/pro-only features
    forbidden_features = {"feature_b", "priority_support", "premium_support", "analytics", "feature_c"}
    assert not forbidden_features.intersection(features), "Free plan should not contain advanced features"

    msg = data["data"].get("message", "")
    assert "FREE" in msg and "alice" in msg, "Message should mention free plan and user 'alice'"

    print("Test passed: /user/data?username=alice returns free plan details as expected.")

if __name__ == "__main__":
    test_user_data_for_alice()
