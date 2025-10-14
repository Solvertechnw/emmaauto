Deploying this project to Fly.io (free tier) and attaching a free domain

This document will walk you through:
- Pushing your code to GitHub
- Creating a Fly app and deploying via flyctl or GitHub Actions
- (Optional) Registering a free domain (Freenom or similar) and pointing it at Fly

Prerequisites
- A GitHub account and an empty repository where you'll push this project
- Local git installed and working
- WSL or bash on Windows (commands below assume bash)

1) Prepare and push repository to GitHub

# create repo locally and push (replace USER/REPO)
git init
git add .
git commit -m "Initial commit for Fly deploy"
git branch -M main
# create GitHub repo (you can create via web UI or use gh CLI)
# Replace the URL below with your repository URL
git remote add origin git@github.com:YOUR_GITHUB_USER/YOUR_REPO.git
git push -u origin main

2) Install flyctl locally

curl -L https://fly.io/install.sh | sh
# ensure $HOME/.fly/bin is on your PATH

3) Create a Fly app (run in your project folder)

fly launch --name autocar --region fra --no-deploy

This generates a `fly.toml` file. Use `--no-deploy` so you can set secrets first.

4) Add secrets to Fly

# example - set your Django secret and turn off DEBUG
fly secrets set DJANGO_SECRET='pick-a-strong-secret' DJANGO_DEBUG='False'

5) (Optional) Create managed Postgres (recommended for production)

fly postgres create --name autocar-db --region fra
# follow interactive prompts; after creation, set DATABASE_URL secret with the provided URL

6) Deploy locally first time

fly deploy

7) (Optional) Configure GitHub Actions auto-deploy

- Create a Fly API token (from https://fly.io/user/personal_access_tokens)
- Add it to your GitHub repo secrets as `FLY_API_TOKEN`
- On push to `main`, the workflow `.github/workflows/fly-deploy.yml` will trigger and deploy.

8) (Optional) Free domain via Freenom or alternative

- Register a free domain at Freenom (e.g., example.ga). Freenom availability varies.
- In Freenom DNS, add an A/AAAA or CNAME as Fly docs instruct (Fly supports automatic certificate provisioning and custom domains). Follow Fly docs: https://fly.io/docs/app-guides/custom-domains/

Notes and troubleshooting
- If you use SQLite (default `db.sqlite3`) it will be ephemeral on containerized hosts; use Postgres for persistent DB.
- Static/media: Fly apps are ephemeral; you should store media on an external object store (S3/R2) or use Fly Volumes for persistent storage.

If you want, I can:
- Create the GitHub repo commands for you (give me your GitHub username and repo name)
- Add a `fly.toml` (I can generate a basic one) and push the workflow; you will still need to run `fly auth login` locally to complete setup.
