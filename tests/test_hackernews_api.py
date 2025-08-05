import requests
import pytest

BASE_URL = "https://hacker-news.firebaseio.com/v0/"


# Test retrieving top stories with the Top Stories API
def test_get_top_stories():
    response = requests.get(f"{BASE_URL}topstories.json")
    assert response.status_code == 200, "Failed to retrieve top stories"
    top_stories = response.json()
    assert isinstance(top_stories, list), "Top stories should be a list"
    assert len(top_stories) > 0, "Top stories list should not be empty"

# Test retrieving the current top story from the Items API
def test_get_current_top_story():
    response = requests.get(f"{BASE_URL}topstories.json")
    assert response.status_code == 200, "Failed to retrieve top stories"
    top_stories = response.json()
    assert isinstance(top_stories, list) and len(top_stories) > 0, "Top stories should be a non-empty list"

    top_story_id = top_stories[0]
    response = requests.get(f"{BASE_URL}item/{top_story_id}.json")
    assert response.status_code == 200, "Failed to retrieve the current top story"
    
    top_story = response.json()
    assert isinstance(top_story, dict), "Top story should be a dictionary"
    assert 'title' in top_story, "Top story should have a title"
    assert 'type' in top_story, "Top story should have a type"
    assert top_story['type'] == 'story', "Top story type should be 'story'"
    assert top_story.get('id') == top_story_id, "Top story ID should match the requested ID"

# Test retrieving a top story, retrieving its first comment using the Items API
def test_get_top_story_first_comment():
    response = requests.get(f"{BASE_URL}topstories.json")
    assert response.status_code == 200, "Failed to retrieve top stories"
    top_stories = response.json()
    assert isinstance(top_stories, list) and len(top_stories) > 0, "Top stories should be a non-empty list"

    top_story_id = top_stories[0]
    response = requests.get(f"{BASE_URL}item/{top_story_id}.json")
    assert response.status_code == 200, "Failed to retrieve the current top story"
    
    top_story = response.json()
    assert isinstance(top_story, dict), "Top story should be a dictionary"
    assert 'kids' in top_story and len(top_story['kids']) > 0, "Top story should have comments"

    first_comment_id = top_story['kids'][0]
    response = requests.get(f"{BASE_URL}item/{first_comment_id}.json")
    assert response.status_code == 200, "Failed to retrieve the first comment"
    
    first_comment = response.json()
    assert isinstance(first_comment, dict), "First comment should be a dictionary"
    assert 'text' in first_comment, "First comment should have text"
    assert first_comment.get('id') == first_comment_id, "First comment ID should match the requested ID"
    assert first_comment.get('type') == 'comment', "First comment type should be 'comment'"