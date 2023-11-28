from django.db import models

LEVEL = [
    ('1a', '1A'),
    ('1b', '1Б'),
    ('2a', '2А'),
    ('2b', '2Б'),
    ('3a', '3А'),
    ('3b', '3Б'),
    ('4a', '4А'),
    ('4b', '4Б'),
    ('5a', '5А'),
    ('5b', '5Б'),
]


class Users(models.Model):
    email = models.EmailField(max_length=128, unique=True)
    fam = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    otc = models.CharField(max_length=128)
    phone = models.IntegerField(unique=True)


class Coord(models.Model):
    latitude = models.FloatField(max_length=50, verbose_name='Широта')
    longitude = models.FloatField(max_length=50, verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')


class Level(models.Model):
    winter = models.CharField(max_length=2, choices=LEVEL, null=True, blank=True)
    summer = models.CharField(max_length=2, choices=LEVEL, null=True, blank=True)
    autumn = models.CharField(max_length=2, choices=LEVEL, null=True, blank=True)
    spring = models.CharField(max_length=2, choices=LEVEL, null=True, blank=True)


class PerevalAdded(models.Model):
    NEW = 'NW'
    PENDING = 'PN'
    ACCEPTED = 'AC'
    REJECTED = 'RJ'
    STATUS_CHOICES = (
        ('NW', 'New'),
        ('AC', 'Accepted'),
        ('PN', 'Pending'),
        ('RJ', 'Rejected'),
    )
    beauty_title = models.CharField(max_length=128, default=None)
    title = models.CharField(max_length=128)
    other_titles = models.CharField(max_length=128)
    connect = models.TextField(max_length=128)
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=NEW)
    coord_id = models.OneToOneField(Coord, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE)


class Images(models.Model):
    title = models.CharField(max_length=128)
    data = models.URLField(null=True, blank=True)
    pereval_id = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE, related_name='images')
