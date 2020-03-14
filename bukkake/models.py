from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class Bukkake(models.Model):
    NORMAL = 'no'
    CLARENDON = 'cl'
    GINGHAM = 'gi'
    MOON = 'mo'
    LARK = 'la'
    REYES = 're'
    JUNO = 'ju'
    SLUMBER = 'sl'
    ADEN = 'ad'
    PERPETUA = 'pe'
    MAYFAIR = 'ma'
    RISE = 'ri'
    HUDSON = 'hu'
    FILTER_IMAGES = (
        (NORMAL, 'normal'),
        (CLARENDON, 'clarendon'),
        (GINGHAM, 'gingham'),
        (MOON, 'moon'),
        (LARK, 'lark'),
        (REYES, 'reyes'),
        (JUNO, 'juno'),
        (SLUMBER, 'slumber'),
        (ADEN, 'aden'),
        (PERPETUA, 'perpetua'),
        (MAYFAIR, 'mayfair'),
        (RISE, 'rise'),
        (HUDSON, 'hudson'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bukkakes_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    description= models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bukkakes_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    filters = models.CharField(
        max_length=2,
        choices=FILTER_IMAGES,
        default=NORMAL
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Bukkake, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('bukkakes:detail', args=[self.id, self.slug])


class Comment(models.Model):
    body = models.TextField()
    commented_on = models.ForeignKey(Bukkake, on_delete=models.CASCADE)
    in_reply_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '{}. {}'.format(self.commented_on, self.commented_by)


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created= models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    message_html = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


# add to User models dynamically
User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))
