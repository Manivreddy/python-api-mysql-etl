from etl_pipeline.transform import transform_posts, transform_users

def test_transform_users_cleans_and_deduplicates():
    records = [
        {"id": 1, "name": " Alice ", "email": " alice@example.com "},
        {"id": 1, "name": "Alice Updated", "email": "a@example.com"},
        {"id": "invalid", "name": "Bad"},
        {"id": 0, "name": "Zero"},
    ]
    result = transform_users(records)
    assert len(result) == 1
    assert result.iloc[0]["id"] == 1
    assert result.iloc[0]["name"] == "Alice Updated"

def test_transform_posts_removes_invalid_and_orphan_records():
    records = [
        {"id": 10, "userId": 1, "title": " First ", "body": " body "},
        {"id": 11, "userId": 99, "title": "Orphan", "body": "x"},
        {"id": 12, "userId": "bad", "title": "Invalid", "body": "x"},
        {"id": 13, "userId": 1, "title": "   ", "body": "x"},
    ]
    result = transform_posts(records, valid_user_ids={1})
    assert len(result) == 1
    assert result.iloc[0]["id"] == 10
    assert result.iloc[0]["title"] == "First"
    assert result.iloc[0]["body"] == "body"

def test_empty_inputs_return_expected_columns():
    assert list(transform_users([]).columns) == [
        "id", "name", "username", "email", "phone", "website"
    ]
    assert list(transform_posts([]).columns) == ["id", "user_id", "title", "body"]
