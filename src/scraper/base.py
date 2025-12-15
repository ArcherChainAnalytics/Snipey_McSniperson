class BaseScraper:
    def fetch(self):
        raise NotImplementedError("fetch() must be implemented by subclasses")

    def parse(self, raw):
        raise NotImplementedError("parse() must be implemented by subclasses")
