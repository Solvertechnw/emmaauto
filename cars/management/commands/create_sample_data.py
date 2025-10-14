from django.core.management.base import BaseCommand
from cars.models import Dealer, Car, CarImage
from django.utils.text import slugify
import random

SAMPLE = [
    {'title':'2018 Toyota Camry SE','make':'Toyota','model':'Camry','year':2018,'price':3500000,'mileage':'70,000 km','description':'Well maintained Camry with full service history.'},
    {'title':'2016 Honda Accord LX','make':'Honda','model':'Accord','year':2016,'price':2800000,'mileage':'90,000 km','description':'Comfortable sedan, fuel efficient.'},
    {'title':'2020 Lexus RX 350','make':'Lexus','model':'RX 350','year':2020,'price':12500000,'mileage':'40,000 km','description':'Luxury SUV with premium features.'},
    {'title':'2017 Ford Ranger','make':'Ford','model':'Ranger','year':2017,'price':4500000,'mileage':'120,000 km','description':'Rugged pickup in good condition.'},
]

class Command(BaseCommand):
    help = 'Create sample cars and dealer for demo'

    def handle(self, *args, **options):
        dealer, _ = Dealer.objects.get_or_create(name='Demo Dealer', defaults={'website':'https://example.com'})
        for item in SAMPLE:
            slug = slugify(item['title'])[:50]
            car, created = Car.objects.get_or_create(slug=slug, defaults={
                'title': item['title'],
                'make': item['make'],
                'model': item['model'],
                'year': item['year'],
                'price': item['price'],
                'mileage': item['mileage'],
                'description': item['description'],
                'dealer': dealer
            })
            if created:
                self.stdout.write(f'Created {car.title}')
            else:
                self.stdout.write(f'Exists {car.title}')
        self.stdout.write('Sample data creation complete.')
