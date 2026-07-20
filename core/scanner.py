"""
Dragon Media Manager
Dragon Scanner Engine

Version: v0.1.3-alpha
Build 9.1 Phoenix
"""

from pathlib import Path

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".m4v",
    ".wmv",
    ".mpg",
    ".mpeg",
    ".ts",
}

POSTER_NAMES = {
    "poster.jpg",
    "folder.jpg",
    "cover.jpg",
    "fanart.jpg",
}

SUBTITLE_EXTENSIONS = {
    ".srt",
    ".ass",
    ".ssa",
    ".sub",
}

TV_FOLDERS = {
    "tv",
    "tv shows",
    "tv series",
    "television",
    "series",
    "shows",
}

IGNORE_FOLDERS = {
    ".Trash-1000",
    "System Volume Information",
    "$RECYCLE.BIN",
    "lost+found",
}


class LibraryScanner:

    def __init__(self, root):

        self.root = Path(root)

    def scan(self):

        stats = {

            "movies": 0,

            "tv": 0,

            "categories": 0,

            "posters": 0,

            "nfo": 0,

            "subtitles": 0,

            "video_files": 0,

            "folders": 0,

            "size_gb": 0.0,

        }

        if not self.root.exists():
            return stats

        #
        # Categories
        #

        for folder in self.root.iterdir():

            if not folder.is_dir():
                continue

            if folder.name in IGNORE_FOLDERS:
                continue

            stats["categories"] += 1

        #
        # Scan everything
        #

        for file in self.root.rglob("*"):

            try:

                if not file.is_file():
                    continue

                suffix = file.suffix.lower()

                parent = str(file.parent).lower()

                stats["size_gb"] += file.stat().st_size / (
                    1024 ** 3
                )

                #
                # Videos
                #

                if suffix in VIDEO_EXTENSIONS:

                    stats["video_files"] += 1

                    if any(
                        tv in parent
                        for tv in TV_FOLDERS
                    ):
                        stats["tv"] += 1

                    else:
                        stats["movies"] += 1

                #
                # Posters
                #

                elif file.name.lower() in POSTER_NAMES:

                    stats["posters"] += 1

                #
                # NFO
                #

                elif suffix == ".nfo":

                    stats["nfo"] += 1

                #
                # Subtitles
                #

                elif suffix in SUBTITLE_EXTENSIONS:

                    stats["subtitles"] += 1

            except Exception:
                continue

        #
        # Round values
        #

        stats["size_gb"] = round(
            stats["size_gb"],
            2,
        )

        return stats

    @staticmethod
    def scan_tv_library(tv_path):
        """
        Return real TV series and episode counts for a TV library root.
        """

        root = Path(tv_path)

        result = {
            "tv_shows": 0,
            "episodes": 0,
        }

        if not root.exists() or not root.is_dir():
            return result

        try:
            children = [
                path
                for path in root.iterdir()
                if path.is_dir() and path.name not in IGNORE_FOLDERS
            ]
        except Exception:
            return result

        shows_root = root

        for child in children:
            if child.name.lower() in TV_FOLDERS:
                shows_root = child
                break

        try:
            show_folders = [
                path
                for path in shows_root.iterdir()
                if path.is_dir() and path.name not in IGNORE_FOLDERS
            ]
            result["tv_shows"] = len(show_folders)
        except Exception:
            result["tv_shows"] = 0

        try:
            for file in root.rglob("*"):
                try:
                    if (
                        file.is_file()
                        and file.suffix.lower() in VIDEO_EXTENSIONS
                    ):
                        result["episodes"] += 1
                except Exception:
                    continue
        except Exception:
            result["episodes"] = 0

        return result

    @classmethod
    def scan_libraries(cls, movies_path, tv_path):
        """
        Scan movie and TV libraries and return dashboard statistics.
        """

        movie_stats = cls(movies_path).scan()
        tv_stats = cls.scan_tv_library(tv_path)

        return {
            "movies": movie_stats.get("movies", 0),
            "tv_shows": tv_stats.get("tv_shows", 0),
            "episodes": tv_stats.get("episodes", 0),
            "categories": movie_stats.get("categories", 0),
            "posters": movie_stats.get("posters", 0),
            "nfo": movie_stats.get("nfo", 0),
            "size_gb": movie_stats.get("size_gb", 0.0),
        }
