from html.parser import HTMLParser


class Supee(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.recording += 1

    def handle_endtag(self, tag):
        if tag == 'div':
            self.recording -= 1

    def handle_data(self, data):
        if self.recording == 0:
            self.data.append(data.strip())


def get_string_after_div(html):
    parser = Supee()
    parser.feed(html)
    return parser.data[0] if parser.data else None
