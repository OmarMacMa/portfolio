# test_db.py

import unittest
from peewee import *
from app import TimeLinePost

MODELS = [TimeLinePost]
test_db = SqliteDatabase(':memory:') # use an in-memory SQLite for tests

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
    
    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()
    
    def test_timeline_post(self):
        #Create two timeline post
        first_post = TimeLinePost.create(name="John Doe" , email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1

        second_post = TimeLinePost.create(name="Jane Doe" , email='jane@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2

        posts = TimeLinePost.select()
        self.assertEqual(len(posts), 2)

        self.assertEqual(posts[0].name, "John Doe")
        self.assertEqual(posts[0].email, "john@example.com")
        self.assertEqual(posts[0].content, "Hello world, I'm John!")

        self.assertEqual(posts[1].name, "Jane Doe")
        self.assertEqual(posts[1].email, "jane@example.com")
        self.assertEqual(posts[1].content, "Hello world, I'm Jane!")