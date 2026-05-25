# Krish's Spring 2026 Deadlines — Deploy Guide

This folder contains `index.html`, a single-file static site that shows all your CS 231, AFM 231, and CO 380 deadlines.

Pick **one** of the two paths below. Vercel is faster (one command, ~30 seconds). GitHub Pages takes a few more minutes but lives at a stable `github.io` URL.

---

## Option A — Vercel (recommended, fastest)

Open Terminal, then run:

```bash
cd "/Users/krishrai/Library/Application Support/Claude/local-agent-mode-sessions/57dad387-0bfc-4891-b0a0-6575244875ae/32fc6623-c154-4422-b210-787a2aead673/local_da193e12-8e4a-44cb-9cc4-a7b09b6e383d/outputs/deadlines-site"
npx vercel --yes
```

On first run, it will:
1. Ask you to log in (browser pops open) — use the same account you already have.
2. Ask "Set up and deploy?" → press Enter (yes).
3. Ask "Which scope?" → pick your personal account.
4. Ask "Link to existing project?" → No.
5. Ask "Project name?" → `deadlines` (or whatever you like).
6. Ask "Directory?" → press Enter (current dir).
7. Override settings? → No.

It prints a live URL like `https://deadlines-xxxx.vercel.app`. Send that to your mom.

To **update the site later** (e.g., after exam date is confirmed), run the same `npx vercel --yes` from this folder — takes ~5 seconds.

---

## Option B — GitHub Pages (stable URL, more steps)

In Terminal:

```bash
cd "/Users/krishrai/Library/Application Support/Claude/local-agent-mode-sessions/57dad387-0bfc-4891-b0a0-6575244875ae/32fc6623-c154-4422-b210-787a2aead673/local_da193e12-8e4a-44cb-9cc4-a7b09b6e383d/outputs/deadlines-site"
git init -b main
git add index.html
git commit -m "Initial deadlines site"
```

Then create the GitHub repo. Easiest with the GitHub CLI if you have it:

```bash
gh repo create deadlines --public --source=. --remote=origin --push
```

If you don't have `gh`, create the repo manually at https://github.com/new (name it `deadlines`, public, no README), then:

```bash
git remote add origin https://github.com/YOUR-USERNAME/deadlines.git
git push -u origin main
```

Then enable Pages:
1. Go to `https://github.com/YOUR-USERNAME/deadlines/settings/pages`
2. Under "Source", pick **Deploy from a branch**
3. Branch: `main`, folder: `/ (root)` → Save
4. Wait ~1 minute. The site goes live at `https://YOUR-USERNAME.github.io/deadlines/`

To update later: edit `index.html`, then `git add . && git commit -m "update" && git push`.

---

## Which should you pick?

- **Vercel** if you just want it live RIGHT NOW and don't care about the URL.
- **GitHub Pages** if you want a permanent, predictable URL like `krish-rai.github.io/deadlines` to bookmark.

You can also do both — the site is one file, it'll work anywhere.

<!-- watcher test 16:13:17 -->
