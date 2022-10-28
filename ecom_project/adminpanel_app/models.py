from django.db import models

class Logo(models.Model):
    image = models.ImageField(upload_to ='static/media/Admin_panel')
    def __str__(self):
        return "{} -".format(self.image)

class Header(models.Model):
    navbar_data = models.CharField(max_length=250)
    def __str__(self):
        return "{} -".format(self.navbar_data)

class Banner(models.Model):
    title = models.CharField(max_length=350)
    description = models.TextField()
    button_text = models.CharField(max_length=300)
    image = models.ImageField(upload_to ='static/media/Admin_panel')
    def __str__(self):
        return "{}-{}-{}-{}".format(self.title, self.description, self.button_text,self.image)

class Services(models.Model):
    image = models.ImageField(upload_to ='static/media/Admin_panel')
    title = models.CharField(max_length=350)
    description = models.TextField()
    def __str__(self):
        return "{}-{}-{}".format(self.title, self.description,self.image)

class Carousel(models.Model):
    image = models.ImageField(upload_to ='static/media/Admin_panel')
    def __str__(self):
        return "{}".format(self.image)

class Testimonial(models.Model):
    title = models.CharField(max_length=350)
    description = models.TextField()
    def __str__(self):
        return "{}-{}-{}".format(self.title, self.description)

class HeadingCategory(models.Model):
    name = models.CharField(max_length=350)

    def __str__(self):
      return self.name

class Headings(models.Model):
    category = models.ForeignKey(HeadingCategory, on_delete=models.CASCADE)
    heading = models.CharField(max_length=350)
    def __str__(self):
        return "{}-{}-{}".format(self.category, self.heading)

