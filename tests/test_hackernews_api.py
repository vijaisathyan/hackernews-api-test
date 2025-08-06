import requests
import pytest

BASE_URL = "https://hacker-news.firebaseio.com/v0/"

def get_top_stories():
    response = requests.get(f"{BASE_URL}topstories.json")
    assert response.status_code == 200, "Failed to retrieve top stories"
    top_stories = response.json()
    assert isinstance(top_stories, list) and len(top_stories) > 0, "Top stories should be a non-empty list"
    return top_stories

def get_item(item_id):
    response = requests.get(f"{BASE_URL}item/{item_id}.json")
    assert response.status_code == 200, f"Failed to retrieve item {item_id}"
    item = response.json()
    assert isinstance(item, dict), f"Item {item_id} should be a dictionary"
    return item

def get_first_comment(story):
    assert 'kids' in story and len(story['kids']) > 0, "Story should have comments"
    first_comment_id = story['kids'][0]
    return get_item(first_comment_id)

def test_get_top_stories():
    """Test retrieving top stories with the Top Stories API."""
    top_stories = get_top_stories()
    # Additional assertions can go here if needed

def test_get_current_top_story():
    """Test retrieving the current top story from the Items API."""
    top_stories = get_top_stories()
    top_story = get_item(top_stories[0])
    assert 'title' in top_story, "Top story should have a title"
    assert 'type' in top_story, "Top story should have a type"
    assert top_story['type'] == 'story', "Top story type should be 'story'"
    assert top_story.get('id') == top_stories[0], "Top story ID should match the requested ID"

def test_get_top_story_first_comment():
    """Test retrieving a top story and its first comment using the Items API."""
    top_stories = get_top_stories()
    top_story = get_item(top_stories[0])
    first_comment = get_first_comment(top_story)
    assert 'text' in first_comment, "First comment should have text"
    assert first_comment.get('id') == top_story['kids'][0], "First comment ID should match the requested ID"
    assert first_comment.get('type') == 'comment', "First comment type should be 'comment'"