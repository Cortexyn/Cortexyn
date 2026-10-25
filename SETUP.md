# Cortexyn command-center maintenance

This is the public profile repository for `@Cortexyn`. GitHub renders the root `README.md` on the profile.

## Content model

The profile is intentionally split into three layers:

- `README.md` controls section order, links, accessibility text, and the responsive table layout.
- `profile.json` is the editable source for focus cards, project cards, the technology matrix, and off-duty signals.
- `scripts/generate_assets.py` turns `profile.json` into self-contained SVG files in `assets/`.

Edit content in `profile.json`, then regenerate the static dashboard assets:

```bash
python3 scripts/generate_assets.py
```

Check that committed assets match the source without changing files:

```bash
python3 scripts/generate_assets.py --check
```

## Public telemetry

`scripts/update_profile.py` calls the public GitHub API and writes `assets/github-stats.svg`. It counts only public repositories returned by the API. Forks and original repositories are separated, and stars are counted only across original repositories.

```bash
python3 scripts/update_profile.py --username Cortexyn --output assets/github-stats.svg
```

The GitHub Actions workflow runs every Monday and can also be started manually. It regenerates static assets, refreshes public telemetry, and commits only when generated SVG files changed. It uses the repository-scoped `GITHUB_TOKEN`; no personal token is required.

## Project-card rules

- Link a project card to an existing public repository.
- Mark personal repositories as `OWN BUILD` and forks as `OPEN SOURCE`.
- Link the official upstream repository in `README.md` before describing a fork as a contribution.
- Never include private projects, private activity, placeholder metrics, or guessed counters.

## GitHub rendering constraints

- GitHub Flavored Markdown and GitHub-safe HTML only.
- No page-level CSS, JavaScript, `foreignObject`, or external SVG resources.
- Project links live in README HTML around each image; SVG-internal links are not relied upon.
- Every SVG has a title and description, and every README image has alt text.
- SVG animation is decorative and includes a reduced-motion fallback.
- Fonts use local system/monospace fallbacks, so no remote font request is needed.

## Layout notes

The five focus cards and four project cards are separate SVGs. This keeps the command-center look while allowing GitHub to reflow the tables on narrower screens. The original JPEG banner remains the only raster design asset.
