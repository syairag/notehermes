def test_list_emails(client):
    response = client.get("/api/v1/emails/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
