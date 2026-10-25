#!/usr/bin/env python3
"""Generate a self-contained GitHub statistics card from public API data."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request


API_ROOT = "https://api.github.com"


def request_json(path: str, token: str | None) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "cortexyn-profile-readme",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(f"{API_ROOT}{path}", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")
        raise RuntimeError(f"GitHub API returned HTTP {error.code}: {detail}") from error


def public_repositories(username: str, token: str | None) -> list[dict[str, object]]:
    repositories: list[dict[str, object]] = []
    encoded_username = urllib.parse.quote(username, safe="")

    for page in range(1, 11):
        payload = request_json(
            f"/users/{encoded_username}/repos?type=owner&sort=updated&per_page=100&page={page}",
            token,
        )
        if not isinstance(payload, list):
            raise RuntimeError("Unexpected repository response from GitHub API")
        repositories.extend(item for item in payload if isinstance(item, dict))
        if len(payload) < 100:
            break

    return repositories


def metric(value: int) -> str:
    return f"{value:,}"


def build_svg(username: str, profile: dict[str, object], repositories: list[dict[str, object]]) -> str:
    original_repositories = [repo for repo in repositories if not bool(repo.get("fork"))]
    working_forks = [repo for repo in repositories if bool(repo.get("fork"))]
    total_stars = sum(int(repo.get("stargazers_count") or 0) for repo in original_repositories)
    public_repo_count = int(profile.get("public_repos") or len(repositories))
    updated_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    safe_username = html.escape(username)

    cards = (
        ("PUBLIC REPOS", metric(public_repo_count), 54),
        ("ORIGINAL BUILDS", metric(len(original_repositories)), 332),
        ("WORKING FORKS", metric(len(working_forks)), 610),
        ("STARS EARNED", metric(total_stars), 888),
    )
    card_markup = "\n".join(
        f'''    <g transform="translate({x} 84)">
      <rect width="258" height="105" rx="12" fill="#0b2427" stroke="#2de0d1" stroke-opacity=".42"/>
      <text x="20" y="34" class="label" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" font-size="14" font-weight="600">{label}</text>
      <text x="20" y="79" class="value" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" font-size="34" font-weight="700">{value}</text>
    </g>'''
        for label, value, x in cards
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="250" viewBox="0 0 1200 250" role="img" aria-labelledby="title desc">
  <title id="title">Public GitHub repository statistics for {safe_username}</title>
  <desc id="desc">{public_repo_count} public repositories: {len(original_repositories)} original builds, {len(working_forks)} working forks, and {total_stars} stars earned across original builds.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#061719"/><stop offset="1" stop-color="#111b20"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#22d3c5"/><stop offset="1" stop-color="#ff9f43"/></linearGradient>
  </defs>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .label {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 14px; font-weight: 600; fill: #82aaa8; letter-spacing: 1.1px; }}
    .value {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 34px; font-weight: 700; fill: #e4fffc; }}
  </style>
  <rect x="1" y="1" width="1198" height="248" rx="16" fill="url(#bg)" stroke="url(#edge)" stroke-width="2"/>
  <text x="36" y="48" class="mono" fill="#ffad5c" font-size="20">PUBLIC SIGNAL // @{safe_username}</text>
  <text x="1164" y="48" text-anchor="end" class="mono" fill="#789c9a" font-size="14">PUBLIC API // VERIFIED</text>
{card_markup}
  <text x="36" y="224" class="mono" fill="#6e9391" font-size="13">LAST SYNC // {updated_at}</text>
  <circle cx="1158" cy="219" r="5" fill="#36d399"/>
</svg>
'''


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="Cortexyn")
    parser.add_argument("--output", type=Path, default=Path("assets/github-stats.svg"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    encoded_username = urllib.parse.quote(args.username, safe="")
    profile_payload = request_json(f"/users/{encoded_username}", token)
    if not isinstance(profile_payload, dict):
        raise RuntimeError("Unexpected profile response from GitHub API")

    repositories = public_repositories(args.username, token)
    svg = build_svg(args.username, profile_payload, repositories)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    print(f"Updated {args.output} from public GitHub data for @{args.username}.")


if __name__ == "__main__":
    main()

