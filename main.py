"""Entry points for local play and Vercel's Python scanner.

Run this file directly to start the Pygame prototype. Vercel imports top-level
``main.py`` files looking for an ``app`` object, so this module also provides a
tiny WSGI app that points users to the static project page.
"""


def app(environ, start_response):
    """Minimal WSGI app so Vercel does not mistake the game for a broken API."""

    body = (
        "Underloam is a local Python/Pygame desktop game. "
        "Open the Vercel static page or run `python main.py` locally."
    ).encode("utf-8")
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]


if __name__ == "__main__":
    from underloam.game import Game

    Game().run()
