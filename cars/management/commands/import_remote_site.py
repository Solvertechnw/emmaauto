import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from bs4 import BeautifulSoup
from cars.models import Car, CarImage, Dealer
from django.conf import settings

REMOTE_SITE = "https://mgx-zd474yr8ons.mgx.world"

class Command(BaseCommand):
    help = "Import cars and images from remote site (basic scraper)"

    def handle(self, *args, **options):
        self.stdout.write(f"Fetching {REMOTE_SITE} ...")
        r = requests.get(REMOTE_SITE, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

        listings = soup.select(".card, .listing, .vehicle, .car-item")
        dealer, _ = Dealer.objects.get_or_create(name="Remote Dealer", defaults={"website": REMOTE_SITE})
        for idx, el in enumerate(listings):
            title_el = el.select_one("h3, h2, .title")
            title_text = title_el.get_text(strip=True) if title_el else f"Car {idx}"
            slug = slugify(title_text)[:50]
            description_el = el.select_one("p, .description")
            desc_text = description_el.get_text(strip=True) if description_el else ""
            price_el = el.select_one(".price")
            price_val = None
            if price_el:
                txt = price_el.get_text(strip=True).replace(',', '')
                try:
                    price_val = float(''.join(c for c in txt if (c.isdigit() or c=='.')))
                except:
                    price_val = None

            car, created = Car.objects.get_or_create(slug=slug, defaults={
                "title": title_text,
                "description": desc_text,
                "price": price_val,
                "dealer": dealer
            })
            img_tags = el.select("img")
            for order, img_tag in enumerate(img_tags):
                src = img_tag.get("src")
                if not src:
                    continue
                if src.startswith("//"):
                    src = "https:" + src
                if src.startswith("/"):
                    src = REMOTE_SITE.rstrip("/") + src
                try:
                    img_resp = requests.get(src, timeout=20)
                    if img_resp.status_code == 200:
                        fname = os.path.basename(src.split("?")[0])
                        car_img = CarImage(car=car, order=order)
                        car_img.image.save(fname, ContentFile(img_resp.content), save=True)
                except Exception as e:
                    self.stdout.write(f"Failed image {src}: {e}")

            self.stdout.write(f"Imported {car.title}")
