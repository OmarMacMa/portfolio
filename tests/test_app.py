#tests/test_app.py - Intergration testing for Flask and DB

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code,200)
        
        html = response.get_data(as_text=True)
        #Check header
        assert "<title>Me</title>" in html 
        #Check nav-bar
        assert "</i> Experience</a>" in html 
        #Check Hello section
        assert "Hi, I'm Omar" in html
        #Check Skills section
        assert "<i class=\"fas fa-code\"></i> Skills</p>" in html
        #Check Education section
        assert "Computer Science and Technologies" in html
        #Check footer
        assert "<footer class=\"text-center\">" in html
       
    def test_timeline_page(self):
        # GET /timeline
        response = self.client.get("/timeline")
        self.assertEqual(response.status_code,200)
        html = response.get_data(as_text=True)

        self.assertIn("<title>Timeline</title>", html)
        self.assertIn("Upload a timeline post", html)
        self.assertIn("Name", html)
        self.assertIn("Email", html)
        self.assertIn("Content", html)
        self.assertIn("Post timeline", html)  

    def test_timeline_api_get(self):
        # GET /api/timeline_post
        response = self.client.get("/api/time_line_post")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        json = response.get_json()
        self.assertIn("time_line_posts", json)

    def test_timeline_api_post(self):        
        test_data = {
            'timeline-name': "John Test",
            'timeline-email': "john@testing.com",
            'timeline-content': "Testing timeline post API"
        }
        response = self.client.post("/api/time_line_post", data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        postJSON = response.get_json()
        
        self.assertIn("id", postJSON)
        self.assertEqual(postJSON["name"], test_data["timeline-name"])
        self.assertEqual(postJSON["email"], test_data["timeline-email"])
        self.assertEqual(postJSON["content"], test_data["timeline-content"])
    
    def test_timeline_api_post_then_get(self):
        post_data = {
            'timeline-name': "John Test",
            'timeline-email': "john@testing.com",
            'timeline-content': "Testing timeline API post -> get"
        }
        postResponse = self.client.post("/api/time_line_post", data=post_data)
        self.assertEqual(postResponse.status_code, 200)
        
        getResponse = self.client.get("/api/time_line_post")
        self.assertEqual(getResponse.status_code, 200)
        
        self.assertTrue(getResponse.is_json)
        getJSON = getResponse.get_json()
       
        self.assertIn("time_line_posts", getJSON)
        self.assertGreater(len(getJSON['time_line_posts']), 0)
        self.assertEqual(getJSON["time_line_posts"][0]["name"], post_data["timeline-name"])
        self.assertEqual(getJSON["time_line_posts"][0]["email"], post_data["timeline-email"])
        self.assertEqual(getJSON["time_line_posts"][0]["content"], post_data["timeline-content"])

    def test_timeline_api_post_then_delete(self):
        post_data = {
            'timeline-name': "John Test",
            'timeline-email': "john@testing.com",
            'timeline-content': "Testing timeline API post -> delete"
        }
        postResponse = self.client.post("/api/time_line_post", data=post_data)
        self.assertEqual(postResponse.status_code, 200)
        self.assertTrue(postResponse.is_json)
        postJSON = postResponse.get_json()
        postID = postJSON["id"]
        
        deleteResponse = self.client.delete("/api/time_line_post", data={"id": postID})
        self.assertEqual(deleteResponse.status_code, 200)
        self.assertTrue(deleteResponse.is_json)
        deleteJSON = deleteResponse.get_json()

        self.assertEqual(deleteJSON["name"], post_data["timeline-name"])
        self.assertEqual(deleteJSON["email"], post_data["timeline-email"])
        self.assertEqual(deleteJSON["content"], post_data["timeline-content"])
    
   
    def test_malformed_timeline_api_post(self):
        # POST : Missing name
        no_name_data = {
            "timeline-email": "john@example.com",
            "timeline-content": "Testing No Name"
        }
        no_name_response = self.client.post("/api/time_line_post", data=no_name_data)
        self.assertEqual(no_name_response.status_code, 400)
        no_name_html = no_name_response.get_data(as_text=True)
        self.assertIn("Invalid name", no_name_html)

        # POST: Malformed email
        malformed_email_data = {
            "timeline-name": "John Doe",
            "timeline-email": "not-an-email",
            "timeline-content": "Incorrect email format"
        }
        malformed_email_response = self.client.post("/api/time_line_post", data=malformed_email_data)
        self.assertEqual(malformed_email_response.status_code, 400)
        malformed_email_html = malformed_email_response.get_data(as_text=True)
        self.assertIn("Invalid email", malformed_email_html)

        # POST: Empty content
        empty_content_data = {
            "timeline-name": "John Doe",
            "timeline-email": "jonh@testing.com",
            "timeline-content": ""
        }
        empty_content_response = self.client.post("/api/time_line_post", data=empty_content_data)
        self.assertEqual(empty_content_response.status_code, 400)
        empty_content_html = empty_content_response.get_data(as_text=True)
        self.assertIn("Invalid content", empty_content_html)