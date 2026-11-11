import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "service"))
os.environ.setdefault("AWS_ACCESS_KEY_ID", "AKIATESTONLY")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test-only")
import main  # noqa: E402


class T(unittest.TestCase):
    def test_announce(self):
        self.assertEqual(main.announce("title: A\ncloses: Friday\noptions: [x, y]"), "Poll 'A' is open until Friday (2 options)")

    def test_storage_target_does_not_leak_the_key(self):
        self.assertNotIn("test-only", main.storage_target())


if __name__ == "__main__":
    unittest.main()
