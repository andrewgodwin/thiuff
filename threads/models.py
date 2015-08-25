from __future__ import unicode_literals

import urlman

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_pgjson.fields import JsonBField


class Group(models.Model):
    """
    A grouping of topics, generally under some overarching subject like
    "Django" or "Kittens".
    """

    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class urls(urlman.Urls):
        view = "/g/{self.name}/"

    def get_absolute_url(self):
        return self.urls.view

    def __unicode__(self):
        return self.name


class GroupMember(models.Model):
    """
    Ties users into being members of Groups - that is, they see stuff from the
    groups on their homepage more often. This model also captures permissions
    that users can have on groups (admin, moderator, that kind of stuff).
    """

    PERMISSIONS = [
        "edit",
    ]

    group = models.ForeignKey(Group, related_name="members")
    user = models.ForeignKey("users.User", related_name="memberships")

    admin = models.BooleanField(default=False)
    moderator = models.BooleanField(default=False)

    def has_permission(self, permission):
        if permission not in self.PERMISSIONS:
            raise ValueError("Unknown permission %s" % permission)
        if self.admin:
            return True
        return False


class Topic(models.Model):
    """
    A topic is an overarching point of discussion. It could be a link, an image,
    or just a question or statement. They're highly moderated and selective; while
    users can suggest topics to a group, only a select group of users can
    actually approve them to appear in the main flow.

    Topics present as a sort of meld of chatroom and forum; there's single-level
    threading and longer form replies are encouraged, but at the same time
    replies appear instantly and can be composed inline.

    Whether this is a good idea remains to be seen.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    group = models.ForeignKey(Group, related_name="topics")
    author = models.ForeignKey("users.User", related_name="topics")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, db_index=True)

    score = models.FloatField(default=0, db_index=True)

    # A topic has at least a title, and might also have a link, text or
    # some other thing.
    title = models.TextField()
    url = models.URLField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)


class TopicInteraction(models.Model):
    """
    When a topic is visited (the link clicked or the discussion page opened),
    entries are written into this model. A periodic task goes round and uses
    this to update the topic's current "score", along with inputs like
    "how much discussion is happening" and "how old is it?".

    This model isn't for permanent archival storage; old entries can be dropped
    after a while.
    """

    topic = models.ForeignKey(Topic, related_name="interactions")
    user = models.ForeignKey("users.User", related_name="interactions")
    view_content = models.BooleanField(default=False)
    view_discussion = models.BooleanField(default=False)
    when = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """
    A message on a Topic. Can be either top-level or one level down;
    we disallow more nesting in the code, but the schema would technically
    allow full nesting.
    """

    topic = models.ForeignKey(Topic, related_name="messages", db_index=True)
    parent = models.ForeignKey("self", related_name="children", null=True, blank=True)

    author = models.ForeignKey("users.User", related_name="messages")

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    edited = models.DateTimeField(null=True, blank=True)

    score = models.FloatField(default=0, db_index=True)


class Reaction(models.Model):
    """
    A response to a message - either something positive, like a thanks or like,
    or something negative, like a spam or abuse report.
    """

    TYPE_CHOICES = [
        ("like", "Like"),
        ("informative", "Informative"),
        ("surprising", "Surprising"),
        ("confusing", "Confusing"),
        ("spam", "Spam"),
        ("abuse", "Abuse"),
    ]

    message = models.ForeignKey(Message, db_index=True)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    user = models.ForeignKey("users.User", related_name="reactions")

    class Meta:
        unique_together = [
            ["message", "user"],
        ]
