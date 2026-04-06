
# Veniamin Velikoretskikh    veniamin@pdx.edu
# CS302 Fall 2025    Karla Fant
# GLASS-BOX TESTING for Program #4 Core Hierarchy
# ------------------------------------------------------------

import pytest

from CS302_Core_Hierarchy import FacebookProfile
from CS302_Core_Hierarchy import InstagramProfile
from CS302_Core_Hierarchy import TikTokProfile
from CS302_Core_Hierarchy import SocialMediaProfile


# SOCIAL MEDIA BASE CLASS TESTS
# ---------------------------------------------------------

def test_social_media_constructor_valid():
    profile = SocialMediaProfile("user123", "JohnDoe")
    assert profile.get_user_id() == "user123"
    assert profile.get_username() == "JohnDoe"
    assert isinstance(profile.get_posts(), list)

def test_social_media_constructor_invalid_userid():
    with pytest.raises(ValueError):
        SocialMediaProfile("", "John")

def test_social_media_constructor_invalid_username():
    with pytest.raises(ValueError):
        SocialMediaProfile("user123", "")

def test_social_media_add_post():
    p = SocialMediaProfile("u1", "Alice")
    p.add_post("Hello world")
    assert len(p.get_posts()) == 1

def test_social_media_display_format():
    p = SocialMediaProfile("u1", "Alice")
    result = p.display()
    assert "User ID:" in result
    assert "Username:" in result


# FACEBOOK PROFILE TESTS
# ---------------------------------------------------------

def test_facebook_constructor_valid():
    f = FacebookProfile("u1", "Alice", 10, 2)
    assert f.get_friends() == 10
    assert f.get_groups() == 2

def test_facebook_constructor_invalid():
    with pytest.raises(ValueError):
        FacebookProfile("u1", "Alice", -1, 5)

def test_facebook_add_post():
    f = FacebookProfile("u1", "Alice", 10, 2)
    f.add_facebook_post("Post1", likes=10)
    assert len(f.get_posts()) == 1

def test_facebook_average_likes():
    f = FacebookProfile("u1", "Alice", 10, 2)
    f.add_facebook_post("A", likes=10)
    f.add_facebook_post("B", likes=20)
    assert f.average_likes() == 15

def test_facebook_most_liked():
    f = FacebookProfile("u1", "Alice", 10, 2)
    f.add_facebook_post("A", likes=5)
    f.add_facebook_post("B", likes=50)
    assert f.most_liked_post()["likes"] == 50


def test_fb_internal_post_structure():
    fb = FacebookProfile("fb1", "Glass", 5, 1)
    fb.add_facebook_post("Test", likes=42)
    # Inspect internal list
    assert fb._posts[0]["likes"] == 42
    assert fb._posts[0]["content"] == "Test"

def test_fb_average_likes_internal_loop_forced():
    fb = FacebookProfile("fb2", "Glass", 5, 1)
    
    # Force branch where no liked posts
    fb._posts = []
    assert fb.average_likes() == 0

    # Force calculation loop branch
    fb._posts = [{"likes": 10}, {"likes": 20}, {"likes": 30}]
    assert fb.average_likes() == 20  # verifies sum/len path


# INSTAGRAM PROFILE TESTS
# ---------------------------------------------------------

def test_instagram_constructor_valid():
    ig = InstagramProfile("i1", "Zara", 100, 5)
    assert ig.get_followers() == 100

def test_instagram_constructor_invalid():
    with pytest.raises(ValueError):
        InstagramProfile("i1", "Zara", -5, 10)

def test_instagram_add_post():
    ig = InstagramProfile("i1", "Zara", 100, 5)
    ig.add_instagram_post("Pic", hearts=10, shares=2)
    assert len(ig.get_posts()) == 1

def test_instagram_engagement_rate():
    ig = InstagramProfile("i1", "Zara", 10, 5)
    ig.add_instagram_post("Pic", hearts=5, shares=5)
    assert ig.engagement_rate() == pytest.approx((5+5)/10)

def test_instagram_most_shared():
    ig = InstagramProfile("i1", "Zara", 10, 5)
    ig.add_instagram_post("Pic1", hearts=2, shares=1)
    ig.add_instagram_post("Pic2", hearts=3, shares=20)
    assert ig.most_shared()["shares"] == 20


def test_ig_internal_branch_followers_zero():
    ig = InstagramProfile("igZ", "GlassIG", 0, 5)
    ig._posts = []  # No posts + zero followers
    assert ig.engagement_rate() == 0  # hits empty+zero branch

def test_ig_internal_post_storage():
    ig = InstagramProfile("ig2", "GlassIG", 100, 10)
    ig.add_instagram_post("Photo", hearts=7, shares=9)
    assert ig._posts[0]["hearts"] == 7
    assert ig._posts[0]["shares"] == 9


# TIKTOK PROFILE TESTS
# ---------------------------------------------------------

def test_tiktok_constructor_valid():
    tk = TikTokProfile("t1", "Jess", 50)
    assert tk.get_user_id() == "t1"
    assert tk.get_username() == "Jess"
    assert tk.get_watch_time() == 50
    assert isinstance(tk.get_posts(), list)

def test_tiktok_constructor_invalid_watch_time():
    with pytest.raises(ValueError):
        TikTokProfile("t1", "Jess", -10)

def test_tiktok_add_video():
    tk = TikTokProfile("t1", "Jess", 50)
    tk.add_video("Vid1", views=100)
    assert len(tk.get_posts()) == 1

def test_tiktok_avg_views():
    tk = TikTokProfile("t1", "Jess", 50)
    tk.add_video("v1", views=10)
    tk.add_video("v2", views=30)
    assert tk.avg_views() == 20

def test_tiktok_top_video():
    tk = TikTokProfile("t1", "Jess", 50)
    tk.add_video("v1", views=10)
    tk.add_video("v2", views=300)
    assert tk.top_video()["views"] == 300


def test_tk_internal_video_storage():
    tk = TikTokProfile("glass1", "Tok", 60)
    tk.add_video("V", views=501)
    assert tk._videos[0]["views"] == 501
    assert tk._posts[0]["views"] == 501

def test_tk_avg_views_forced_branches():
    tk = TikTokProfile("glass2", "Tok", 60)

    # Force no videos branch
    tk._videos = []
    assert tk.avg_views() == 0

    # Force computation branch
    tk._videos = [{"views": 10}, {"views": 40}]
    assert tk.avg_views() == 25  # checks loop math


# OPERATOR OVERLOADING TESTS
# ---------------------------------------------------------

def test_less_than_by_userid():
    a = SocialMediaProfile("abc", "A")
    b = SocialMediaProfile("bcd", "B")
    assert (a < b) is True

def test_equals_same_userid():
    a = SocialMediaProfile("abc", "A")
    b = SocialMediaProfile("abc", "B")
    assert (a == b)

def test_add_same_type_posts_merged():
    ig1 = InstagramProfile("i1", "Zara", 10, 2)
    ig2 = InstagramProfile("i2", "Kyle", 10, 3)

    ig1.add_instagram_post("A", hearts=10, shares=1)
    ig2.add_instagram_post("B", hearts=20, shares=2)

    merged = ig1 + ig2
    assert len(merged.get_posts()) == 2

def test_add_different_types_error():
    f = FacebookProfile("u1", "Alice", 3, 1)
    i = InstagramProfile("i1", "Zara", 10, 5)
    with pytest.raises(TypeError):
        f + i


def test_merge_new_object_created_glassbox():
    fb1 = FacebookProfile("m1", "A", 1, 1)
    fb2 = FacebookProfile("m1", "B", 2, 2)
    fb1._posts = [{"content": "P1"}]
    fb2._posts = [{"content": "P2"}]
    
    merged = fb1 + fb2
    # Ensure new object created via operator path
    assert merged is not fb1
    assert merged is not fb2
    assert len(merged._posts) == 2

