from django.db import models

# Create your models here.
owner = models.ForeignKey('authentication.CustomUser', on_delete = models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    class Meta:
        verbose_name_plural = "Catrgories"

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    def __unicode__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey('authentication.CustomUser', on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100, unique = True)
    tags = models.ManyToManyField(Tag)
    content = models.TextField()
    updated_on = models.DateField(auto_now=True)
    created_on = models.DateField(auto_now_add=True)
    publish_on = models.DateField()
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-publish_on']
        verbose_name_plural = "articles"

    def __unicode__(self):
        return self.title

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def next_article(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()

    def pre_article(self):
        return Article.objects.filter(id__lt=self.id).first()