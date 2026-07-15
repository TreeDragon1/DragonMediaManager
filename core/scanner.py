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
    "television",
    "series",
    "shows",
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

        ignore = {

            ".Trash-1000",

            "System Volume Information",

            "$RECYCLE.BIN",

            "lost+found",

        }

        if not self.root.exists():
            return stats

        #
        # Categories
        #

        for folder in self.root.iterdir():

            if not folder.is_dir():
                continue

            if folder.name in ignore:
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