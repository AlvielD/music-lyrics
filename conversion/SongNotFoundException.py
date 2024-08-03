class SongNotFoundException(Exception):
    def __init__(self, title, artist):
        super().__init__(f"Song '{title}' by '{artist}' not found.")
        self.title = title
        self.artist = artist