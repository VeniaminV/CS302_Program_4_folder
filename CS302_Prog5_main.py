# Veniamin Velikoretskikh   veniamin@pdx.edu
# CS302 - Program #5
# Main application for Social Media Analytics Tool
# Uses BST implementation and core hierarchy classes

from CS302_Core_Hierarchy import (
    FacebookProfile,
    InstagramProfile,
    TikTokProfile,
    SocialMediaProfile
)
from CS302_BST import BST


class main:
    def __init__(self):
        self._tree = BST()      # store all profiles in one BST

    # ---------------------------------------------------------
    def run(self):
        print("\nWelcome to the Social Media Analytics Tool!")
        print("This program allows you to manage and analyze multiple social media profiles.\n")

        while True:
            self._display_menu()

            try:
                choice = input("Enter choice: ").strip()
                if not choice:
                    raise ValueError("Input cannot be empty.")

                if choice == "1":
                    profile = self._create_profile_menu()
                    if profile is not None:
                        self._tree.insert(profile)
                        print("Profile added successfully!\n")

                elif choice == "2":
                    self._display_all()

                elif choice == "3":
                    self._find_profile()

                elif choice == "4":
                    self._remove_profile()

                elif choice == "5":
                    self._add_content_to_profile()

                elif choice == "6":
                    self._show_profile_metrics()

                elif choice == "7":
                    print("Exiting program... Goodbye!")
                    break

                else:
                    print("Invalid choice. Try again.\n")

            except Exception as error:
                print(f"Error: {error}\n")

    # ---------------------------------------------------------
    def _display_menu(self):
        print("------- MAIN MENU -------")
        print("1. Add a new social media profile")
        print("2. Display all profiles (in order)")
        print("3. Search for a profile")
        print("4. Remove a profile")
        print("5. Add post/video to a profile")
        print("6. Show profile metrics (likes, engagement, views)")
        print("7. Exit")
        print("---------------------------")

    # ---------------------------------------------------------
    # gets the right profile and adds the necessary attributes and returns the right profile
    def _create_profile_menu(self):
        print("\nSelect the type of social media profile to create:")
        print("1. Facebook")
        print("2. Instagram")
        print("3. TikTok")

        choice = input("Enter choice: ").strip()

        user_id = input("Enter user ID: ").strip()
        username = input("Enter username: ").strip()

        if choice == "1":
            friends = int(input("Enter number of friends: "))
            groups = int(input("Enter number of groups: "))
            return FacebookProfile(user_id, username, friends, groups)

        elif choice == "2":
            followers = int(input("Enter number of followers: "))
            following = int(input("Enter number of accounts you follow: "))
            return InstagramProfile(user_id, username, followers, following)

        elif choice == "3":
            watch_time = float(input("Enter total watch time (hours): "))
            return TikTokProfile(user_id, username, watch_time)

        else:
            print("Invalid choice.")
            return None

    # ---------------------------------------------------------
    def _display_all(self):
        print("\n----- DISPLAYING ALL PROFILES (inorder traversal) -----")
        profile_list = self._tree.display_inorder()

        if not profile_list:
            print("No profiles stored.\n")
            return

        for p in profile_list:
            print(p.display())
            print("--------------------------------------------------")

    # ---------------------------------------------------------
    def _find_profile(self):
        user_id = input("\nEnter the user ID to search for: ").strip()
        if not user_id:
            raise ValueError("User ID cannot be empty.")

        profile = self._tree.retrieve(user_id)

        if profile:
            print("\nProfile found:")
            print(profile.display(), "\n")
        else:
            print("Profile not found.\n")

    # ---------------------------------------------------------
    def _remove_profile(self):
        user_id = input("\nEnter user ID to remove: ").strip()
        if not user_id:
            raise ValueError("User ID cannot be empty.")

        removed = self._tree.remove(user_id)

        if removed:
            print(f"Profile '{user_id}' removed successfully.\n")
        else:
            print("User ID not found. Nothing removed.\n")

    # -----------------------------------------------------------
    # Add post/video to a profile
    def _add_content_to_profile(self):
        user_id = input("Enter user ID to add content to: ").strip()
        profile = self._tree.retrieve(user_id)
        if not profile:
            print("Profile not found.\n")
            return

        if isinstance(profile, FacebookProfile):
            content = input("Enter Facebook post content: ").strip()
            likes = int(input("Enter number of likes: "))
            profile.add_facebook_post(content, likes)
            print("Facebook post added!\n")

        elif isinstance(profile, InstagramProfile):
            content = input("Enter Instagram post content: ").strip()
            hearts = int(input("Enter hearts count: "))
            shares = int(input("Enter shares count: "))
            profile.add_instagram_post(content, hearts, shares)
            print("Instagram post added!\n")

        elif isinstance(profile, TikTokProfile):
            title = input("Enter TikTok video title: ").strip()
            views = int(input("Enter number of views: "))
            profile.add_video(title, views)
            print("TikTok video added!\n")


    # Show metrics for a profile
    def _show_profile_metrics(self):
        user_id = input("Enter user ID to view metrics: ").strip()
        profile = self._tree.retrieve(user_id)
        if not profile:
            print("Profile not found.\n")
            return

        print(f"\nMetrics for {profile.get_username()}:")

        if isinstance(profile, FacebookProfile):
            print(f"Average Likes: {profile.average_likes()}")
            most = profile.most_liked_post()
            if most:
                print(f"Most Liked Post: {most['content']} ({most['likes']} likes)")

        elif isinstance(profile, InstagramProfile):
            print(f"Engagement Rate: {profile.engagement_rate():.2f}")
            most = profile.most_shared()
            if most:
                print(f"Most Shared Post: {most['content']} ({most['shares']} shares)")

        elif isinstance(profile, TikTokProfile):
            print(f"Average Views: {profile.avg_views():.2f}")
            top = profile.top_video()
            if top:
                print(f"Top Video: {top['title']} ({top['views']} views)")

        print()

# ---------------------------------------------------------
# RUN MAIN
if __name__ == "__main__":
    main = main()
    main.run()
