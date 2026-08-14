from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from .models import Post


class BlogViewsTests(TestCase):
    def test_homepage_shows_latest_posts(self):
        Post.objects.create(title="My first post", content="Hello world")

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My first post")

    def test_post_detail_page_works(self):
        post = Post.objects.create(title="A detailed post", content="Detailed content")

        response = self.client.get(reverse("post_detail", args=[post.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A detailed post")
        self.assertContains(response, "Detailed content")
