import requests

BASE_URL = "http://127.0.0.1:5000"  # The base URL for your Flask app


def register_user(email: str, password: str) -> None:
    """Register a user and assert response"""
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json() == {"email": email, "message": "user created"}
    print("register_user: OK")


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with the wrong password and assert response"""
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("log_in_wrong_password: OK")


def log_in(email: str, password: str) -> str:
    """Log in a user and return the session ID"""
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    session_id = response.cookies.get("session_id")
    assert session_id is not None, "Session ID not found"
    print("log_in: OK")
    return session_id


def profile_unlogged() -> None:
    """Access profile without logging in and assert response"""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    print("profile_unlogged: OK")


def profile_logged(session_id: str) -> None:
    """Access profile while logged in and assert response"""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "email" in response.json(), "Expected 'email' in response"
    print("profile_logged: OK")


def log_out(session_id: str) -> None:
    """Log out a user and assert response"""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 302, f"Expected 302, got {response.status_code}"
    print("log_out: OK")


def reset_password_token(email: str) -> str:
    """Get a password reset token and assert response"""
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    reset_token = response.json().get("reset_token")
    assert reset_token is not None, "Reset token not found"
    print("reset_password_token: OK")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password using the reset token and assert response"""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token, "new_password": new_password},
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json() == {"email": email, "message": "Password updated"}
    print("update_password: OK")


# Constants for testing
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
