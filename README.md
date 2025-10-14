# AutoHub Clone (Django) — Complete Package

This package contains:
- Django app `cars` with models, admin, templates, and static layout.
- Filters/search on the listing page (by make, year, price, and free-text q).
- Django REST Framework API endpoint: `/api/cars/` (read-only).
- Two importers: `import_remote_site` (requests) and `import_remote_site_selenium` (Selenium).
- Management command `create_sample_data` to seed demo data.
- Fixture file `cars/fixtures/sample_fixtures.json` you can load with `loaddata`.

## Quick setup (local)

1. Create a virtualenv and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations and create superuser:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Create sample data (choose one):

   - Using management command:
     ```bash
     python manage.py create_sample_data
     ```
   - OR load fixture:
     ```bash
     python manage.py loaddata cars/fixtures/sample_fixtures.json
     ```

5. Run the dev server and visit the site:

   ```bash
   python manage.py runserver
   # Visit http://127.0.0.1:8000/
   # API: http://127.0.0.1:8000/api/cars/
   ```

6. (Optional) Import from remote site:

   - If the site is static: `python manage.py import_remote_site`
   - If the site is JS-rendered: ensure Chrome/Chromium is installed then:
     `python manage.py import_remote_site_selenium`

## Notes and next steps

- To make images work immediately, upload images in Django admin or attach them to CarImage rows.
- Customize templates in `cars/templates/cars/` to match exact branding.
- For production, switch `DEBUG=False`, configure allowed hosts, static/media storage, and a production DB.
