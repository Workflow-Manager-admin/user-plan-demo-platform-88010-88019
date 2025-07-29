import requests

def test_user_data_for_carol():
    """
    Tests that the /user/data endpoint returns correct details for username='carol' (enterprise plan).
    """
    # Assuming the server is running locally on port 8000
    base_url = "http://localhost:8000/user/data"
    params = {"username": "carol"}

    response = requests.get(base_url, params=params)
    assert response.status_code == 200, f"Unexpected status code {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data["username"] == "carol", f"Expected username 'carol', got {data.get('username')}"
    assert data["plan"] == "enterprise", f"Expected plan 'enterprise', got {data.get('plan')}"

    features = data["data"].get("features", [])
    # Enterprise plan includes all features and premium ones
    expected_features = {"feature_a", "feature_b", "feature_c", "premium_support", "analytics"}
    for feature in expected_features:
        assert feature in features, f"Expected '{feature}' in features for enterprise plan"
    # Should NOT lack any expected enterprise features
    forbidden_features = set()
    assert not forbidden_features.intersection(features), "Enterprise plan returned an unexpected feature restriction"

    # Dedicated manager flag
    assert data["data"].get("dedicated_manager") is True, "Enterprise plan should include a dedicated manager"

    msg = data["data"].get("message", "")
    assert "ENTERPRISE" in msg and "carol" in msg, "Message should mention enterprise plan and user 'carol'"

    print("Test passed: /user/data?username=carol returns enterprise plan details as expected.")

if __name__ == "__main__":
    test_user_data_for_carol()
