from pathlib import Path

VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".m4v",
    ".wmv", ".mpg", ".mpeg", ".ts"
}

POSTER_NAMES = {
    "poster.jpg",
    "folder.jpg"
}

SUBTITLE_EXTENSIONS = {
    ".srt", ".ass", ".ssa", ".sub"
}


class LibraryScanner:

    def __init__(self, root):
        self.root = Path(root)

    def scan(self):

        stats = {
            "movies": 0,
            "categories": 0,
            "posters": 0,
            "nfo": 0,
            "subtitles": 0,
        }

        ignore = {
            ".Trash-1000",
            "System Volume Information"
        }

        for folder in self.root.iterdir():

            if not folder.is_dir():
                continue

            if folder.name in ignore:
                continue

            stats["categories"] += 1

            for file in folder.rglob("*"):

                if not file.is_file():
                    continue

                suffix = file.suffix.lower()

                if suffix in VIDEO_EXTENSIONS:
                    stats["movies"] += 1

                elif suffix == ".nfo":
                    stats["nfo"] += 1

                elif suffix in SUBTITLE_EXTENSIONS:
                    stats["subtitles"] += 1

                elif file.name.lower() in POSTER_NAMES:
                    stats["posters"] += 1

        return stats