from pathlib import Path

VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".m4v",
    ".wmv", ".mpg", ".mpeg", ".ts"
}

POSTER_FILES = {
    "poster.jpg",
    "folder.jpg"
}

NFO_EXTENSION = ".nfo"

SUBTITLE_EXTENSIONS = {
    ".srt", ".ass", ".ssa", ".sub"
}


class LibraryScanner:

    def __init__(self, root_folder):
        self.root = Path(root_folder)

    def scan(self):

        stats = {
            "categories": 0,
            "movies": 0,
            "posters": 0,
            "nfo": 0,
            "subtitles": 0
        }

        ignore = {
            ".Trash-1000",
            "System Volume Information"
        }

        for category in self.root.iterdir():

            if not category.is_dir():
                continue

            if category.name in ignore:
                continue

            stats["categories"] += 1

            for item in category.rglob("*"):

                if item.is_file():

                    suffix = item.suffix.lower()

                    if suffix in VIDEO_EXTENSIONS:
                        stats["movies"] += 1

                    elif suffix == NFO_EXTENSION:
                        stats["nfo"] += 1

                    elif suffix in SUBTITLE_EXTENSIONS:
                        stats["subtitles"] += 1

                    elif item.name.lower() in POSTER_FILES:
                        stats["posters"] += 1

        return stats