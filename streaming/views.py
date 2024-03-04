import asyncio
import random

from django.conf import settings
from django.http import StreamingHttpResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape


async def delayed_range(n: int, delay: float):
    """Simulates some slow operations."""
    indices = list(range(n))
    random.shuffle(indices)
    for i in indices:
        await asyncio.sleep(delay)
        yield i


async def content_generator():
    # Set up the Jinja2 environment. In reality, you'd probably just configure
    # Django to use Jinja2 as the template engine, but for this example, we'll
    # set it up manually.
    env = Environment(
        loader=FileSystemLoader(settings.BASE_DIR / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        enable_async=True,
    )

    template = env.get_template("streaming/index.html")
    # Render the template in chunks, passing the generator as a context variable In
    # an ideal world we'd use `template.stream_async` but that doesn't exist. The
    # difference between `generate` and `stream` is that `stream` returns a type
    # that, for network efficiency, buffers up a configurable number of "items" so
    # we're not yielding super tiny strings. How important this is in practice is
    # unknown.
    async for chunk in template.generate_async(delayed_range=delayed_range):
        yield chunk


async def shadow_dom_streaming_example(request):
    # Note that if you have nginx in front of your Django server, you may need to
    # add `proxy_buffering off;` either globally or for specific location blocks.
    #
    # Another option is to set the header `X-Accel-Buffering` header to `no` in your
    # view...maybe using a custom StreamingHttpResponse subclass or a middleware.
    return StreamingHttpResponse(content_generator())
