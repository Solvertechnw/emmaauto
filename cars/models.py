from django.db import models

class Dealer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=400, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Car(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="cars", null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    make = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(null=True, blank=True)
    mileage = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="cars/")
    alt = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.car.title} image {self.order}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)
