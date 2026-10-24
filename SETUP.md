# Cortexyn profile setup

This folder is ready to become the public profile repository for `@Cortexyn`.

## 1. Create the special repository

On GitHub, create a new repository with these exact settings:

- **Owner:** `Cortexyn`
- **Repository name:** `Cortexyn`
- **Visibility:** Public

The repository must be public, its name must match the account name, and `README.md` must live in the repository root. GitHub then displays it on the account profile automatically.

If `Cortexyn/Cortexyn` already exists, use that repository instead of creating another one.

## 2. Upload this folder

Copy the contents of `Cortexyn-profile` into the repository root, preserving the hidden `.github` directory. The finished repository should look like this:

```text
Cortexyn/
├── .github/
│   └── workflows/
│       └── update-profile.yml
├── assets/
│   ├── circuit-divider.svg
│   ├── cortex-banner.jpeg
│   ├── github-stats.svg
│   ├── tech-stack.svg
│   └── terminal.svg
├── scripts/
│   └── update_profile.py
├── README.md
└── SETUP.md
```

You can also publish from a terminal after creating the empty GitHub repository:

```bash
git init
git add .
git commit -m "feat: launch Cortexyn command center"
git branch -M main
git remote add origin https://github.com/Cortexyn/Cortexyn.git
git push -u origin main
```

## 3. Start live telemetry

The initial `assets/github-stats.svg` contains a real public API snapshot taken during setup. A scheduled GitHub Actions workflow refreshes it every Monday and can also be run manually:

1. Open the repository's **Actions** tab.
2. Select **Update public profile telemetry**.
3. Choose **Run workflow**.

The workflow uses GitHub's repository-scoped `GITHUB_TOKEN`; no personal access token or extra secret is required. If a repository or organization policy blocks the commit, open **Settings → Actions → General → Workflow permissions** and allow read and write permissions for workflows.

## 4. Maintain the profile

- Update the short introduction directly in `README.md`.
- Keep the featured projects list selective and link only existing public repositories.
- For collaborative projects, link the official upstream first and describe the contribution precisely; use the personal fork only as the working-fork link.
- Edit `assets/tech-stack.svg` when the public stack changes.
- Keep the banner filename unchanged, or update its path in `README.md` when replacing it.
- The animation is contained entirely in `assets/terminal.svg`; it uses no JavaScript or external stylesheet.

## GitHub README constraints respected

- GitHub Flavored Markdown and basic HTML only.
- No custom page-level CSS or JavaScript.
- Relative, repository-local asset paths.
- SVG animation has a reduced-motion fallback.
- Statistics come from the public GitHub API and are never manually fabricated.

