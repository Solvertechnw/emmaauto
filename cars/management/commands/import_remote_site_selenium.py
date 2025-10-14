import os
import time
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from cars.models import Car, CarImage, Dealer
from django.conf import settings
from urllib.parse import urljoin, urlparse

REMOTE_SITE = "https://mgx-zd474yr8ons.mgx.world"

class Command(BaseCommand):
    help = "Import cars and images from remote site using Selenium (for JS-rendered sites)."

    def handle(self, *args, **options):
        self.stdout.write("Starting Selenium headless browser...")
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        try:
            driver.get(REMOTE_SITE)
            time.sleep(3)  # wait for JS to render; increase if needed
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            listings = soup.select(".card, .listing, .vehicle, .car-item, .product, .listing-item")
            if not listings:
                # fallback: take any link to detail pages
                listings = []
                for a in soup.select("a"):
                    href = a.get("href", "")
                    if "/car" in href or "vehicle" in href or "product" in href:
                        listings.append(a)

            dealer, _ = Dealer.objects.get_or_create(name="Remote Dealer", defaults={"website": REMOTE_SITE})

            for idx, el in enumerate(listings):
                # Try to extract title
                title_el = el.select_one("h3, h2, .title, .name") or el
                title_text = title_el.get_text(strip=True) if getattr(title_el, "get_text", None) else str(title_el)[:60]
                slug = slugify(title_text)[:50]
                description_el = el.select_one("p, .description, .desc")
                desc_text = description_el.get_text(strip=True) if description_el else ""
                price_el = el.select_one(".price, .amount")
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

                # Images: try to resolve absolute URLs
                img_tags = el.select("img")
                for order, img_tag in enumerate(img_tags):
                    src = img_tag.get("src") or img_tag.get("data-src") or img_tag.get("data-lazy")
                    if not src:
                        continue
                    src = urljoin(REMOTE_SITE, src)
                    try:
                        img_resp = requests.get(src, timeout=20)
                        if img_resp.status_code == 200:
                            fname = os.path.basename(urlparse(src).path) or f'image_{idx}_{order}.jpg'
                            car_img = CarImage(car=car, order=order)
                            car_img.image.save(fname, ContentFile(img_resp.content), save=True)
                    except Exception as e:
                        self.stdout.write(f"Failed image {src}: {e}")

                self.stdout.write(f"Imported {car.title}")

        finally:
            driver.quit()
