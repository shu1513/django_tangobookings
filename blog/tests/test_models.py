# blog/tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post
from django.utils import timezone
from django.db import IntegrityError, transaction, connection

class PostModelTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_post_with_valid_author(self):
        # Create a Post object with a valid author
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            date_posted=timezone.now(),
            author=self.user
        )
        # Assert the post was created successfully
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post.')
        self.assertEqual(post.author.username, 'testuser')

    def test_create_post_with_author_id(self):
        # Create a Post object using author_id
        post = Post.objects.create(
            title='Another Test Post',
            content='This is another test post.',
            date_posted=timezone.now(),
            author_id=self.user.id
        )
        # Assert the post was created successfully
        self.assertEqual(post.title, 'Another Test Post')
        self.assertEqual(post.content, 'This is another test post.')
        self.assertEqual(post.author.username, 'testuser')

    def test_create_post_without_author(self):
        # Attempt to create a Post object without an author
        with self.assertRaises(IntegrityError):
            Post.objects.create(
                title='Post without author',
                content='This post has no author.',
                date_posted=timezone.now()
            )

    def test_create_post_with_nonexistent_author(self):
        # Attempt to create a Post object with a nonexistent author
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                post = Post(
                    title='Post with nonexistent author',
                    content='This post references a nonexistent author.',
                    date_posted=timezone.now(),
                    author_id=999
                )
                post.save()
                connection.cursor().execute('PRAGMA foreign_keys = ON;')
                connection.check_constraints()


