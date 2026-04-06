# Veniamin Velikoretskikh veniamin@pdx.edu
# CS302 Fall 2025 Karla Fant

# Core hierarchy implementation for Program #4
# Will have the base class SocialMediaProfile and the derived
# facebook, tiktok, instagram classes


# Social Media Base Class
#------------------------------------------------------
# representing a genric social media profile
# will have user ID, username, and list of posts
class SocialMediaProfile: 
    
    def __init__(self, user_id: str, username: str):
        if not user_id:
            raise ValueError("User ID cannot be empty")
        if not username: 
            raise ValueError("Username cannot be empty")
        
        self._user_id = user_id
        self._username = username
        self._posts = []  # all platforms store posts in a list

        # Getters
    def get_user_id(self):
        return self._user_id

    def get_username(self):
        return self._username

    def get_posts(self):
        return self._posts

    # Simple post behavior — works for base class but overridden in children
    def add_post(self, content: str):
        if not content:
            raise ValueError("Post content cannot be empty")
        self._posts.append({"content": content})


    # Display formatting
    def display(self):
        return f"User ID: {self._user_id}\nUsername: {self._username}"


    # Operator Overloading
    def __lt__(self, other):
        # if other object isn't a SocialMediaProfile, it won't compare
        if not isinstance(other, SocialMediaProfile):
            return NotImplemented
        return self._user_id < other._user_id

    def __eq__(self, other):
        # makes sure that the equality only works on profiles, not random types
        if not isinstance(other, SocialMediaProfile):
            return NotImplemented
        return self._user_id == other._user_id

    # allows two of the same profiles to merge
"""
    def __add__(self, other):
        # Dosen't allow merge if the two profiles are different 
        if type(self) is not type(other):
            raise TypeError("Cannot merge profiles of different platforms")

        # Creates a new profile of the same class type
        # _get_extra_fields_for_merge() is in every derived class. 
        merged = type(self)(self._user_id, self._username, *self._get_extra_fields_for_merge())
        merged._posts = self._posts + other._posts
        return merged

    def _get_extra_fields_for_merge(self):
        return []
"""
    

# Facebook Profile 
#---------------------------------------------------------------
# INherits everythign from base profile and adds friends count, group count
# And Facebook post with likes
class FacebookProfile(SocialMediaProfile):
    """Derived class representing a Facebook profile"""

    def __init__(self, user_id: str, username: str, friends: int, groups: int):
        super().__init__(user_id, username)
        # raises error if friends or groups are negative
        if friends < 0:
            raise ValueError("Friends count cannot be negative")
        if groups < 0:
            raise ValueError("Groups count cannot be negative")

        self._friends = friends
        self._groups = groups

    # Facebook-specific getters
    def get_friends(self):
        return self._friends

    def get_groups(self):
        return self._groups

    # Facebook posts have likes
    def add_facebook_post(self, content: str, likes: int = 0):
        if not content:
            raise ValueError("Facebook post content cannot be empty")
        if likes < 0:
            raise ValueError("Likes cannot be negative")
        self._posts.append({"content": content, "likes": likes})

    # Compute average likes
    def average_likes(self):
        liked_posts = [p["likes"] for p in self._posts if "likes" in p]
        return sum(liked_posts) / len(liked_posts) if liked_posts else 0

    # Find most liked post
    def most_liked_post(self):
        liked_posts = [p for p in self._posts if "likes" in p]
        return max(liked_posts, key=lambda post: post["likes"]) if liked_posts else None

    # Passes extra fields for merging
    def _get_extra_fields_for_merge(self):
        return [self._friends, self._groups]

    # over rides the + operator for the Facebook profiles
    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Cannot merge profiles of different platforms")
        
        merged = FacebookProfile(self._user_id, self._username, self._friends, self._groups)
        merged._posts = self._posts + other._posts
        return merged

    def display(self):
        base = super().display()
        return f"{base}\nFriends: {self._friends}\nGroups: {self._groups}"



# Instagram Profile
# ------------------------------------------------------------------------
# Inherits base profile and adds followers, following and instagram post
# each post has hearts
class InstagramProfile(SocialMediaProfile):
    """Derived class representing an Instagram profile"""

    def __init__(self, user_id: str, username: str, followers: int, following: int):
        super().__init__(user_id, username)
        # Error check for negative values
        if followers < 0:
            raise ValueError("Follower count cannot be negative")
        if following < 0:
            raise ValueError("Following count cannot be negative")

        self._followers = followers
        self._following = following

    # Instagram-specific getters
    def get_followers(self):
        return self._followers

    # Instagram posts have hearts and shares
    def add_instagram_post(self, content: str, hearts: int = 0, shares: int = 0):
        if not content:
            raise ValueError("Instagram post cannot be empty")
        if hearts < 0 or shares < 0:
            raise ValueError("Hearts/shares cannot be negative")

        post = {"content": content, "hearts": hearts, "shares": shares}
        self._posts.append(post)

    # Engagement rate based on hearts + shares
    def engagement_rate(self):
        if not self._posts:
            return 0
        total_engagement = sum(p.get("hearts", 0) + p.get("shares", 0) for p in self._posts)
        return total_engagement / self._followers if self._followers else 0

    # Most shared post
    def most_shared(self):
        shared_posts = [p for p in self._posts if "shares" in p]
        return max(shared_posts, key=lambda post: post["shares"]) if shared_posts else None

    # passes extra fields for merging Instagram profile
    def _get_extra_fields_for_merge(self):
        return [self._followers, self._following]

    # Over rides the + operator for the INstagram profile
    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Cannot merge profiles of different platforms")
        merged = InstagramProfile(self._user_id, self._username, self._followers, self._following)
        merged._posts = self._posts + other._posts
        return merged

    def display(self):
        base = super().display()
        return f"{base}\nFollowers: {self._followers}\nFollowing: {self._following}"



# TikTok Profile 
# -------------------------------------------------------------
# Inherits base profile adn adds watch time, and videos, each video has views. 
class TikTokProfile(SocialMediaProfile):
    """Derived class representing a TikTok profile"""

    def __init__(self, user_id: str, username: str, watch_time: int):
        super().__init__(user_id, username)
        # checks for negative value
        if watch_time < 0:
            raise ValueError("Watch time cannot be negative")

        self._watch_time = watch_time
        self._videos = []  # Internal video list (also stored to posts via add_video)

    # TikTok-specific getter
    def get_watch_time(self):
        return self._watch_time

    # Add video (also goes into posts list for consistency)
    def add_video(self, title: str, views: int = 0):
        if views < 0:
            raise ValueError("Views cannot be negative")
        video = {"title": title, "views": views}
        self._videos.append(video)
        self._posts.append(video)

    # Average views across videos
    def avg_views(self):
        view_counts = [v["views"] for v in self._videos]
        return sum(view_counts) / len(view_counts) if view_counts else 0

    # Top viewed video
    def top_video(self):
        return max(self._videos, key=lambda v: v["views"]) if self._videos else None

    # Passes extra fields for merging TikTok profiles
    def _get_extra_fields_for_merge(self):
        return [self._watch_time]

    # Over rides the + operator for the TikTok profile
    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Cannot merge profiles of different platforms")
        merged = TikTokProfile(self._user_id, self._username, self._watch_time)
        merged._videos = self._videos + other._videos
        merged._posts = self._posts + other._posts
        return merged

    def display(self):
        base = super().display()
        return f"{base}\nWatch Time: {self._watch_time}"