
# Veniamin Velikoretskikh  veniamin@pdx.edu
# CS302 Fall 2025 Karla Fant

# Black-Box testing for program #4

import pytest
import CS302_Core_Hierarchy

# SOCIAL MEDIA BASE CLASS
# -------------------------

def test_social_media_constructor_valid():
    profile = CS302_Core_Hierarchy.SocialMediaProfile("user123", "JohnDoe")
    assert profile.get_user_id() == "user123"
    assert profile.get_username() == "JohnDoe"
    assert isinstance(profile.get_posts(), list)

def test_social_media_constructor_invalid_userid():
    with pytest.raises(ValueError):
        CS302_Core_Hierarchy.SocialMediaProfile("", "John")

def test_social_media_constructor_invalid_username():
    with pytest.raises(ValueError):
        CS302_Core_Hierarchy.SocialMediaProfile("user123", "")

def test_social_media_add_post():
    p = CS302_Core_Hierarchy.SocialMediaProfile("u1", "Alice")
    p.add_post("Hello world")
    posts = p.get_posts()
    assert len(posts) == 1
    assert posts[0]["content"] == "Hello world"

def test_social_media_display_format():
    p = CS302_Core_Hierarchy.SocialMediaProfile("u1", "Alice")
    result = p.display()
    assert "User ID:" in result
    assert "Username:" in result

# FACEBOOK TESTS
# -------------------------

def test_facebook_constructor_valid():
    f = CS302_Core_Hierarchy.FacebookProfile("u1", "Alice", 10, 2)
    assert f.get_friends() == 10
    assert f.get_groups() == 2

def test_facebook_constructor_invalid():
    with pytest.raises(ValueError):
        CS302_Core_Hierarchy.FacebookProfile("u1", "Alice", -1, 5)

def test_facebook_add_post():
    f = CS302_Core_Hierarchy.FacebookProfile("u1", "Alice", 10, 2)
    f.add_facebook_post("Post1", likes=10)
    assert len(f.get_posts()) == 1

def test_facebook_average_likes():
    f = CS302_Core_Hierarchy.FacebookProfile("u1", "Alice", 10, 2)
    f.add_facebook_post("A", likes=10)
    f.add_facebook_post("B", likes=20)
    assert f.average_likes() == 15

def test_facebook_most_liked():
    f = CS302_Core_Hierarchy.FacebookProfile("u1", "Alice", 10, 2)
    f.add_facebook_post("A", likes=5)
    f.add_facebook_post("B", likes=50)
    assert f.most_liked_post()["likes"] == 50

# INSTAGRAM TESTS
# -------------------------

def test_instagram_constructor_valid():
    ig = CS302_Core_Hierarchy.InstagramProfile("i1", "Zara", 100, 5)
    assert ig.get_followers() == 100

def test_instagram_constructor_invalid():
    with pytest.raises(ValueError):
        CS302_Core_Hierarchy.InstagramProfile("i1", "Zara", -5, 10)

def test_instagram_add_post():
    ig = CS302_Core_Hierarchy.InstagramProfile("i1", "Zara", 100, 5)
    ig.add_instagram_post("Pic", hearts=10, shares=2)
    assert len(ig.get_posts()) == 1

def test_instagram_engagement_rate():
    ig = CS302_Core_Hierarchy.InstagramProfile("i1", "Zara", 10, 5)
    ig.add_instagram_post("Pic", hearts=5, shares=5)
    assert ig.engagement_rate() == pytest.approx((5+5)/10)

def test_instagram_most_shared():
    ig = CS302_Core_Hierarchy.InstagramProfile("i1", "Zara", 10, 5)
    ig.add_instagram_post("Pic1", hearts=2, shares=1)
    ig.add_instagram_post("Pic2", hearts=3, shares=20)
    assert ig.most_shared()["shares"] == 20

# TIKTOK TESTS
# -------------------------

def test_tiktok_constructor_valid():
    tk = CS302_Core_Hierarchy.TikTokProfile("t1", "Jess", 50)
    assert tk.get_user_id() == "t1"
    assert tk.get_username() == "Jess"
    assert tk.get_watch_time() == 50
    assert isinstance(tk.get_posts(), list)

def test_tiktok_constructor_invalid_watch_time():
    with pytest.raises(ValueError):
        CS302_Core_Hierarchy.TikTokProfile("t1", "Jess", -10)

def test_tiktok_add_video():
    tk = CS302_Core_Hierarchy.TikTokProfile("t1", "Jess", 50)
    tk.add_video("Vid1", views=100)
    assert len(tk.get_posts()) == 1

def test_tiktok_avg_views():
    tk = CS302_Core_Hierarchy.TikTokProfile("t1", "Jess", 50)
    tk.add_video("v1", views=10)
    tk.add_video("v2", views=30)
    assert tk.avg_views() == 20

def test_tiktok_top_video():
    tk = CS302_Core_Hierarchy.TikTokProfile("t1", "Jess", 50)
    tk.add_video("v1", views=10)
    tk.add_video("v2", views=300)
    assert tk.top_video()["views"] == 300

# OPERATOR OVERLOADING
# -------------------------

def test_less_than_by_userid():
    a = CS302_Core_Hierarchy.SocialMediaProfile("abc", "A")
    b = CS302_Core_Hierarchy.SocialMediaProfile("bcd", "B")
    assert (a < b) is True

def test_equals_same_userid():
    a = CS302_Core_Hierarchy.SocialMediaProfile("abc", "A")
    b = CS302_Core_Hierarchy.SocialMediaProfile("abc", "B")
    assert (a == b)

def test_add_same_type_posts_merged():
    ig1 = CS302_Core_Hierarchy.InstagramProfile("i1", "Zara", 10, 2)
    ig2 = CS302_Core_Hierarchy.InstagramProfile("i2", "Kyle", 10, 3)
    ig1.add_instagram_post("A", hearts=10, shares=1)
    ig2.add_instagram_post("B", hearts=20, shares=2)
    merged = ig1 + ig2
    assert len(merged.get_posts()) == 2

def test_add_different_types_error():
    f = CS302_Core_Hierarchy.FacebookProfile("u1", "Alice", 3, 1)
    i = CS302_Core_Hierarchy.InstagramProfile("i1", "Zara", 10, 5)
    with pytest.raises(TypeError):
        f + i
