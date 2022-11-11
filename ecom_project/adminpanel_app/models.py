from django.db import models

class Logo(models.Model):
    image = models.ImageField(upload_to ='Logo')
    def __str__(self):
        return "{} -".format(self.image)

class Header(models.Model):
    menu = models.CharField(max_length=250)
    url = models.URLField(max_length = 300)
    def __str__(self):
        return "{} -{}".format(self.menu, self.url)

class Banner(models.Model):
    title = models.CharField(max_length=350)
    description = models.TextField()
    button_text = models.CharField(max_length=300)
    def __str__(self):
        return "{}-{}-{}".format(self.title, self.description, self.button_text)

class Services(models.Model):
    image = models.ImageField(upload_to ='Services_images')
    title = models.CharField(max_length=350)
    description = models.TextField()
    def __str__(self):
        return "{}-{}-{}".format(self.title, self.description,self.image)

class FAQ(models.Model):
    title = models.CharField(max_length=350)
    description = models.TextField()
    def __str__(self):
        return "{}-{}".format(self.title, self.description)



