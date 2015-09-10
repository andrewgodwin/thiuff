from __future__ import unicode_literals

import channels
import htmlmin
import json
import markdown
import urlman

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

from django.db import models
from django.utils.functional import cached_property
from django.template.loader import get_template
from django.contrib.postgres.fields import ArrayField
from django_pgjson.fields import JsonBField


class Group(models.Model):
    """
    A grouping of threads, generally under some overarching subject like
    "Django" or "Kittens".

    And yes, colour is spelt the British way. It's my own little troll.
    """

    PERMISSIONS = [
        "view",
        "edit",
        "member",
        "create_thread",
        "create_message",
        "approve_thread",
        "approve_member",
        "view_reports",
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    intro = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    colour = models.CharField(max_length=30, blank=True, null=True)
    frontpage = models.BooleanField(default=False)
    background = models.ForeignKey("images.Image", blank=True, null=True, related_name="+")
    logo = models.ForeignKey("images.Image", blank=True, null=True, related_name="+")

    private = models.BooleanField(default=False)
    approve_members = models.BooleanField(default=False)
    approve_threads = models.BooleanField(default=False)
    approve_messages = models.BooleanField(default=False)

    # Cached numbers of members and threads
    num_members = models.IntegerField(default=0)
    num_threads = models.IntegerField(default=0)

    class urls(urlman.Urls):
        view = "/g/{self.name}/"
        edit = "{view}edit/"
        join = "{view}join/"
        leave = "{view}leave/"
        create_thread = "{view}t/create/"

    def get_absolute_url(self):
        return self.urls.view

    def __unicode__(self):
        return self.name

    @property
    def icon_colour(self):
        for char in self.colour.lower():
            if char not in "#1234567890abcdef":
                raise ValueError("Colour incorrect")
        return self.colour or "#369"

    def has_permission(self, user, permission):
        if permission not in self.PERMISSIONS:
            raise ValueError("Unknown permission %s" % permission)
        member = self.membership(user)
        # Banned members get nothing
        if member and member.status == "banned":
            return False
        # Pending members are the same as non members
        if member and member.status == "pending":
            member = None
        # Non-members can only view if not hidden
        if member is None:
            return (permission == "view") and (not self.private)
        # Admins get all
        if member.status == "admin":
            return True
        # Mods get all but edit
        if member.status == "moderator" and permission != "edit":
            return True
        # Members can view and make threads
        if permission in ["view", "create_thread", "create_message", "member"]:
            return True
        return False

    def membership(self, user):
        if user is None or user.is_anonymous():
            return None
        return self.members.filter(user=user).first()

    def update_stats(self, commit=True):
        """
        Updates denormalised stats
        """
        self.num_members = self.members.exclude(status__in=["banned", "pending"]).count()
        self.num_threads = self.threads.filter(status="approved").count()
        if commit:
            self.save()


class GroupMember(models.Model):
    """
    Ties users into being members of Groups - that is, they see stuff from the
    groups on their homepage more often. This model also captures permissions
    that users can have on groups (admin, moderator, that kind of stuff).
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("member", "Member"),
        ("moderator", "Moderator"),
        ("admin", "Admin"),
        ("banned", "Banned"),
    ]

    group = models.ForeignKey(Group, related_name="members")
    user = models.ForeignKey("users.User", related_name="memberships")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, db_index=True)


class Thread(models.Model):
    """
    A thread is an overarching point of discussion. It could be a link, an image,
    or just a question or statement. They're highly moderated and selective; while
    users can suggest threads to a group, only a select group of users can
    actually approve them to appear in the main flow.

    Threads present as a sort of meld of chatroom and forum; there's single-level
    threading and longer form replies are encouraged, but at the same time
    replies appear instantly and can be composed inline.

    Whether this is a good idea remains to be seen.
    """

    PERMISSIONS = [
        "view",
        "edit",
        "delete",
        "undelete",
        "create_message",
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    group = models.ForeignKey(Group, related_name="threads")
    author = models.ForeignKey("users.User", related_name="threads")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, db_index=True)

    score = models.FloatField(default=0, db_index=True)

    # Cached numbers of replies and discussions
    num_top_level_messages = models.IntegerField(default=0)
    num_messages = models.IntegerField(default=0)

    # A thread has at least a title, and might also have a link, text or
    # some other thing.
    title = models.TextField()
    url = models.URLField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    class urls(urlman.Urls):
        view = "{self.group.urls.view}t/{self.id}/"
        content = "{self.content_url}"
        create_top_level_message = "{view}m/create/"
        report = "{view}report/"

    def get_absolute_url(self):
        return self.urls.view

    def __unicode__(self):
        return self.title

    def has_permission(self, user, permission):
        """
        Permission checking.
        """
        if permission not in self.PERMISSIONS:
            raise ValueError("Unknown permission %s" % permission)
        # Author can do everything
        if user == self.author:
            return True
        # Delegate rest to group for now
        if permission in ["view", "create_message"]:
            return self.group.has_permission(user, permission)
        else:
            return False

    @property
    def content_url(self):
        """
        Returns the primary "content" url - an external URL if one provided,
        or the thread page if it's just text or other embedded content.
        """
        if self.url:
            return self.url
        return self.urls.view

    @property
    def content_domain(self):
        if self.url:
            try:
                bits = urlparse.urlparse(self.url)
                domain = bits.netloc
                if domain.startswith("www."):
                    domain = domain[4:]
                return domain
            except ValueError:
                pass
        return None

    @property
    def formatted_body(self):
        """
        Formats the body to HTML.
        """
        output = markdown.markdown(self.body, safe_mode=True, enable_attributes=False)
        # I'm really paranoid.
        if "<script" in output:
            raise ValueError("XSS attempt detected")
        return output

    @property
    def top_level_messages(self):
        """
        Returns all top-level (non-parented) messages
        """
        return self.messages.filter(
            parent__isnull=True
        ).annotate(
            num_children=models.Count('children')
        ).filter(
            models.Q(num_children__gt=0) | models.Q(deleted__isnull=True)
        ).order_by("created")

    def update_stats(self, commit=True):
        """
        Updates denormalised stats
        """
        self.num_messages = self.messages.filter(deleted__isnull=True).count()
        self.num_top_level_messages = self.top_level_messages.count()
        if commit:
            self.save(update_stats=False)
            self.send_stream_group()

    def save(self, update_stats=True, *args, **kwargs):
        """
        Notifies channels and updates stats on save.
        """
        super(Thread, self).save(*args, **kwargs)
        # Update parent group stats
        if update_stats:
            self.group.update_stats()

    def send_stream_group(self):
        """
        Sends a notification of us to our groups's stream.
        """
        data = {
            "id": str(self.id),
            "type": "thread",
            "num_messages": self.num_messages,
            "num_top_level_messages": self.num_top_level_messages,
        }
        channels.Group("stream-group-%s" % self.group.id).send({
            "content": json.dumps(data),
        })


class ThreadInteraction(models.Model):
    """
    When a thread is visited (the link clicked or the discussion page opened),
    entries are written into this model. A periodic task goes round and uses
    this to update the thread's current "score", along with inputs like
    "how much discussion is happening" and "how old is it?".

    This model isn't for permanent archival storage; old entries can be dropped
    after a while.
    """

    thread = models.ForeignKey(Thread, related_name="interactions")
    user = models.ForeignKey("users.User", related_name="interactions")
    view_content = models.BooleanField(default=False)
    view_discussion = models.BooleanField(default=False)
    when = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """
    A message on a Thread. Can be either top-level or one level down;
    we disallow more nesting in the code, but the schema would technically
    allow full nesting.
    """

    PERMISSIONS = [
        "view",
        "edit",
        "delete",
        "undelete",
        "create_message",
    ]

    thread = models.ForeignKey(Thread, related_name="messages", db_index=True)
    parent = models.ForeignKey("self", related_name="children", null=True, blank=True)

    author = models.ForeignKey("users.User", related_name="messages")

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    edited = models.DateTimeField(null=True, blank=True)
    deleted = models.DateTimeField(null=True, blank=True)

    score = models.FloatField(default=0, db_index=True)

    class urls(urlman.Urls):
        view = "{self.thread.urls.view}m/{self.id}/"
        reply = "{view}reply/"
        edit = "{view}edit/"
        delete = "{view}delete/"
        report = "{view}report/"

    @property
    def formatted_body(self):
        """
        Formats the body to HTML.
        """
        output = markdown.markdown(self.body, safe_mode=True, enable_attributes=False)
        # I'm really paranoid.
        if "<script" in output:
            raise ValueError("XSS attempt detected")
        return output

    @cached_property
    def replies(self):
        """
        Returns replies in date order.
        """
        return list(self.children.order_by("created"))

    def save(self, update_stats=True, *args, **kwargs):
        """
        Notifies channels on save.
        """
        super(Message, self).save(*args, **kwargs)
        # Update parent thread stats
        if update_stats:
            self.thread.update_stats()
        # Always send notification to thread
        self.send_stream_thread()

    def __unicode__(self):
        return self.body[:50] + ("..." if len(self.body) > 50 else "")

    def send_stream_thread(self):
        """
        Sends a notification of us to our thread's stream.
        """
        data = {
            "id": str(self.id),
            "thread_id": str(self.thread_id),
        }
        if self.parent:
            data['type'] = "reply"
            data['discussion_id'] = str(self.parent_id)
            data['html'] = htmlmin.minify(self.reply_html())
        else:
            data['type'] = "discussion"
            data['html'] = htmlmin.minify(self.discussion_html())
        channels.Group("stream-thread-%s" % self.thread.id).send({
            "content": json.dumps(data),
        })

    def discussion_html(self):
        """
        Renders the HTML for this as a reply chunk.
        """
        template = get_template("threads/_discussion.html")
        return template.render({
            "message": self,
            "thread": self.thread,
        })

    def reply_html(self):
        """
        Renders the HTML for this as a reply chunk.
        """
        template = get_template("threads/_reply.html")
        return template.render({"reply": self})

    def has_permission(self, user, permission):
        """
        Returns if the user has a certain permission.
        """
        # Check the permission is valid
        if permission not in self.PERMISSIONS:
            raise ValueError("Invalid permission %s" % permission)
        # Admins get all
        if user.is_superuser:
            return True
        # Owners get most
        if user == self.author and permission != "undelete":
            return True
        # View is handled by thread
        if permission in ["view", "create_message"]:
            return self.thread.has_permission(user, permission)
        return False


class Report(models.Model):
    """
    A record that a message or thread is against site rules.
    """

    TYPE_CHOICES = [
        ("spam", "Spam"),
        ("abuse", "Abuse"),
        ("offensive", "Offensive"),
        ("personal", "Personal Information"),
        ("hack", "Malware / Hack"),
        ("illegal", "Illegal content"),
        ("other", "Other (provide reason)"),
    ]

    thread = models.ForeignKey(Thread, null=True, blank=True, related_name="reports")
    message = models.ForeignKey(Message, null=True, blank=True, related_name="reports")
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    comment = models.TextField(null=True, blank=True)

    reporter = models.ForeignKey("users.User", related_name="submitted_reports")
    accused = models.ForeignKey("users.User", related_name="reports")

    class Meta:
        unique_together = [
            ["message", "thread", "reporter"],
        ]
