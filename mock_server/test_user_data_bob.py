import requests

def test_user_data_for_bob():
    """
    Tests that the /user/data endpoint returns correct details for username='bob' (pro plan).
    """
    # Assuming the server is running locally on port 8000
    base_url = "http://localhost:8000/user/data"
    params = {"username": "bob"}

    response = requests.get(base_url, params=params)
    assert response.status_code == 200, f"Unexpected status code {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data["username"] == "bob", f"Expected username 'bob', got {data.get('username')}"
    assert data["plan"] == "pro", f"Expected plan 'pro', got {data.get('plan')}"

    features = data["data"].get("features", [])
    # Pro plan includes "feature_a", "feature_b", and "priority_support"
    expected_features = {"feature_a", "feature_b", "priority_support"}
    for feature in expected_features:
        assert feature in features, f"Expected '{feature}' in features for pro plan"
    # Pro plan should NOT have "premium_support", "analytics", or "feature_c"
    forbidden_features = {"premium_support", "analytics", "feature_c"}
    assert not forbidden_features.intersection(features), "Pro plan should not contain enterprise-only features"

    msg = data["data"].get("message", "")
    assert "PRO" in msg and "bob" in msg, "Message should mention pro plan and user 'bob'"

    print("Test passed: /user/data?username=bob returns pro plan details as expected.")

if __name__ == "__main__":
    test_user_data_for_bob()
