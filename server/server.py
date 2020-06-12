from pathlib import Path

from frost import FrostServer


class Server(FrostServer):

    def __init__(self, file: str) -> None:
        db = Path('pyfrost.sqlite3')
        if not db.exists():
            from server.utils import init_db
            init_db()

        super().__init__(file)