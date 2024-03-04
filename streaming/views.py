import random
import time

from django.conf import settings
from django.http import StreamingHttpResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape


def delayed_range(n, delay):
    # This generator simulates the server taking its time to generate the template items
    indices = list(range(n))
    random.shuffle(indices)  # Shuffle the list to randomize the order
    for i in indices:
        time.sleep(delay)
        yield i


def content_generator():
    # Set up the Jinja2 environment. In reality, you'd probably just configure
    # Django to use Jinja2 as the template engine, but for this example, we'll
    # set it up manually.
    env = Environment(
        loader=FileSystemLoader(settings.BASE_DIR / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    # Prepare the delayed_range generator with desired arguments
    delayed_iterable = delayed_range(5, 1)

    # Load and render the template, passing the generator as a context variable
    template = env.get_template("streaming/index.html")
    stream = template.stream(
        delayed_range=delayed_iterable
    )  # Pass the generator object

    # Stream the rendered content
    for chunk in stream:
        yield chunk


def shadow_dom_streaming_example(request):
    # Note that if you have nginx in front of your Django server, you may need to
    # add `proxy_buffering off;` either globally or for specific location blocks.
    #
    # Another option is to set the header `X-Accel-Buffering` header to `no` in your
    # view...maybe using a custom StreamingHttpResponse subclass or a middleware.
    return StreamingHttpResponse(content_generator())
