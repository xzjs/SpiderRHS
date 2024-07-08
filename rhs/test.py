import re

urls = [
    "background-image:url('https://apps.rhs.org.uk/plantselectorimages/d_(e)_tail/visi46517.jpg');",
    "background-image:url('https://apps.rhs.org.uk/plantselectorimages/detail/WSY0020456_9867.jpg');",
    "background-image:url('https://apps.rhs.org.uk/plantselectorimages/detail/visi31159.jpg');",
    "background-image:url('https://apps.rhs.org.uk/plantselectorimages/detail/visi46517.jpg');",
    "background-image:url('https://apps.rhs.org.uk/plantselectorimages/detail/WSY0020456_9867.jpg');",
    "background-image:url('https://apps.rhs.org.uk/plantselectorimages/detail/visi31159.jpg');",
    'background-image:url(https://apps.rhs.org.uk/plantselectorimages/detail/WSY0020456_9867.jpg);',
    "background-image:url('https://apps.rhs.org.uk/plantselectorimages/detail/RHS_RHS-0001436_1125.JPG');"
]

pattern = re.compile(r"url\s*\(['\"]?(https?://[^'\")]+)['\"]?\)")
image_urls = [pattern.findall(url) for url in urls]
print(image_urls)
