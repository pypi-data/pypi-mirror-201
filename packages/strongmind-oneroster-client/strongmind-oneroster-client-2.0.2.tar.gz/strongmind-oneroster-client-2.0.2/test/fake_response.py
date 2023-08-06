import json


class FakeResponse:
    data: str

    def json(self):
        return json.loads(self.data)
