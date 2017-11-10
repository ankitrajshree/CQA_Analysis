from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        if ("code" in  self.get_starttag_text()):
            return
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

