"""Entry points for local play and Vercel's Python scanner.

Run this file directly to start the Pygame prototype. Vercel imports top-level
``main.py`` files looking for an ``app`` object, so this module also provides a
tiny WSGI app that serves the static project page.
"""

from pathlib import Path


def app(environ, start_response):
    """Minimal WSGI app so Vercel shows the project page at the root URL."""

    index_path = Path(__file__).with_name("public") / "index.html"
    body = index_path.read_bytes()
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]


if __name__ == "__main__":
    from underloam.game import Game

    Game().run()
