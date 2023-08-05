import os
from baselib.json import JsonFile


class TestJsonFile(object):

    def test_json_file(self):
        if os.path.isfile("test.json"):
            os.remove("test.json")
        data = JsonFile.read("test.json")
        assert data == {}
        JsonFile.write("test.json", {"msg": "hello"})
        data = JsonFile.read("test.json")
        assert data == {"msg": "hello"}
        JsonFile.update("test.json", {"msg": "world"})
        data = JsonFile.read("test.json")
        assert data == {"msg": "world"}
        JsonFile.update("test.json", {"info": "hello"})
        data = JsonFile.read("test.json")
        assert data == {"info": "hello", "msg": "world"}
        os.remove("test.json")
