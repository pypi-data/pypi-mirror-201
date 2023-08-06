from gen_markdown.smoke import five


class TestSmoke:
    def test_smoke(self):
        assert 5 == five()
