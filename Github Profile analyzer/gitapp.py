import json
import sys
import requests

# Output file names
git_activity = "gitactivity.json"
git_details = "gitdetails.json"
git_repo_list = "gitrepolist.json"


class GitHub:
    """
    Simple GitHub client using the public GitHub REST API.
    - Fetches user details, events, and repositories.
    - Saves responses as JSON files.
    - Prints a small summary to the console.
    """

    BASE_URL = "https://api.github.com"

    def _get(self, path: str):
        """
        Internal helper to perform a GET request and return JSON data.

        :param path: API path, e.g. "users/octocat/repos"
        :return: Parsed JSON (dict or list) or None if error.
        """
        url = f"{self.BASE_URL}/{path}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            # Print error and return None instead of killing the program
            print(f"Error {response.status_code} for URL: {url}")
            try:
                # GitHub usually returns error message in JSON
                print("Message:", response.json().get("message"))
            except Exception:
                pass
            return None

    def _read_json(self, filename: str):
        """
        Internal helper to read JSON data from a file.

        :param filename: Path to JSON file
        :return: Parsed JSON or None if file not found / invalid
        """
        try:
            with open(filename, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print(f"File not found: {filename}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in: {filename}")
        return None

    def _save_json(self, data, filename: str):
        """
        Internal helper to save JSON data to a file.

        :param data: JSON-serializable data (dict or list)
        :param filename: Path to output file
        """
        if data is None:
            # Nothing to save (probably request failed)
            return

        try:
            with open(filename, "w") as json_file:
                json.dump(data, json_file, indent=4)
            # Optional: print confirmation
            # print(f"Saved {filename}")
        except OSError as e:
            print(f"Error writing to {filename}: {e}")

    # ---------------- API fetch methods ---------------- #

    def get_user_activity(self, username, file_name):
        """
        Fetch recent public events for a user and save to file.
        """
        data = self._get(f"users/{username}/events")
        self._save_json(data, file_name)

    def get_user_details(self, username, file_name):
        """
        Fetch basic user profile details and save to file.
        """
        data = self._get(f"users/{username}")
        self._save_json(data, file_name)

    def fetch_user_repositories(self, username, file_name):
        """
        Fetch public repositories for a user and save to file.
        """
        data = self._get(f"users/{username}/repos")
        self._save_json(data, file_name)

    # ---------------- Printing / analysis methods ---------------- #

    def print_details(self):
        """
        Print a short summary using the user details JSON.
        """
        data = self._read_json(git_details)
        if not data:
            return

        name = data.get("name") or data.get("login")
        followers = data.get("followers", 0)
        following = data.get("following", 0)
        bio = data.get("bio") or "No bio provided."
        twitter = data.get("twitter_username") or "Not linked"

        print("\n=== GitHub Profile Summary ===")
        print(f"My name is {name}")
        print(f"I have {followers} followers")
        print(f"I am following {following} people")
        print(f"Bio: {bio}")
        print(f"My Twitter username: {twitter}")

    def _load_repo_list(self):
        """
        Helper to load repo list once.
        """
        data = self._read_json(git_repo_list)
        if not data:
            return []
        return data

    def print_public_repo(self):
        """
        Print names of all public repositories.
        """
        repos = self._load_repo_list()
        if not repos:
            return

        print("\n=== My GitHub Public Repositories ===")
        for repo in repos:
            # 'private' is False for public repos
            if not repo.get("private", True):
                print(f"- {repo.get('name')}")

    def print_number_of_stars(self):
        """
        Print each public repo with its number of stars and language.
        """
        repos = self._load_repo_list()
        if not repos:
            return

        print("\n=== Repositories with Stars & Languages ===")
        for repo in repos:
            if not repo.get("private", True):
                name = repo.get("name")
                stars = repo.get("stargazers_count", 0)
                language = repo.get("language") or "Unknown"
                print(f"- {name}  ⭐ {stars}  ({language})")

    def printing_languages(self):
        """
        Count how many repos use each language and print the summary.
        """
        repos = self._load_repo_list()
        if not repos:
            return

        language_counts = {}
        for repo in repos:
            language = repo.get("language")
            if language is None:
                # Skip repos with no detected language
                continue
            language_counts[language] = language_counts.get(language, 0) + 1

        print("\n=== Language Usage in Repositories ===")
        if not language_counts:
            print("No languages found.")
        else:
            for lang, count in language_counts.items():
                print(f"- {lang}: {count} repo(s)")


def main():
    """
    Entry point: takes a GitHub username from the command line,
    fetches data from GitHub API, saves JSON files, and prints a summary.
    """
    if len(sys.argv) < 2:
        print("Usage: python gitapp.py <github-username>")
        sys.exit(1)

    username = sys.argv[1]
    print("This app lists only events from last 30 days (as per GitHub API).")

    github = GitHub()

    # Fetch and save data
    github.get_user_activity(username, git_activity)
    github.get_user_details(username, git_details)
    github.fetch_user_repositories(username, git_repo_list)

    # Print summary based on saved data
    github.print_details()
    github.print_public_repo()
    github.print_number_of_stars()
    github.printing_languages()


if __name__ == "__main__":
    main()
