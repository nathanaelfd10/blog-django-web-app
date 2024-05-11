from django.db import models
from django.utils import timezone
from django.conf import settings
# from django.contrib.auth import get_user_model
# from wagtail.models import Page
# from wagtail.fields import RichTextField
# from wagtail.admin.panels import FieldPanel
# from wagtail.search import index

# class HomePage(Page):
#     intro = RichTextField(blank=True)

#     content_panels = Page.content_panels + [
#         FieldPanel('intro')
#     ]

# class BlogPage(Page):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     date = models.DateField("post_date")
#     intro = models.CharField(max_length=250)
#     text = RichTextField(blank=True)

#     search_fields = Page.search_fields + [
#         index.SearchField('intro'),
#         index.SearchField('text'),
#     ]

#     content_panels = Page.content_panels + [
#         FieldPanel('date'),
#         FieldPanel('intro'),
#         FieldPanel('text'),
#     ]

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class Vote(models.Model):
    comment = models.ForeignKey('blog.Comment', on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    def upvote(self):
        self.is_upvote = True
        self.save()

    def downvote(self):
        self.save()

    def __str__(self):
        return self.is_upvote
    
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def get_vote(self):
        vote_count = self.votes.count()
        downvote_count = self.votes.filter(is_upvote=False).count()
        upvote_count = vote_count - downvote_count       

        # print(self.author)
        # print(self.text)
        # print("Vote count:" + str(vote_count))
        # print("Downvote count: " + str(downvote_count))
        # print("Result: " + str(upvote_count - downvote_count))
        # print("=============")

        return str(upvote_count - downvote_count)

    def approve(self):
        self.approved_comment = True
        self.save()
    
    def __str__(self):
        return self.text