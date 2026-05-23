#!/usr/bin/env python3
"""
lomax_grab.py — download Alan Lomax field recordings from archive.org as MP3 samples.

The Internet Archive hosts the complete Lomax collection as free, downloadable MP3s.
This script downloads specific collections into your samples directory,
organized by region and style — ready to drag into Digitakt or BeatFactory.

Usage:
    python lomax_grab.py [collection] [--dest DIR] [--list]

Collections:
    sounds-of-the-south     Georgia Sea Islands to Mississippi Delta, 1959-60
                            Blues, spirituals, field hollers, work songs, ballads
    kentucky                Rural Kentucky, 1937-42
                            Old-time, ballads, shape-note singing
    blues-songbook          Blues recordings, 1935-78
    east-africa             British East Africa (Hugh Tracey) — drums, song, dance
    all                     Download all of the above

Examples:
    python lomax_grab.py sounds-of-the-south
    python lomax_grab.py all --dest ~/Documents/GitHub/gear/samples/lomax
    python lomax_grab.py --list

Requirements:
    pip install internetarchive requests
    (or: pip install requests   for the manual curl-based fallback)
"""

import argparse
import os
import sys
import json

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

# ── Collection definitions ────────────────────────────────────────────────────

COLLECTIONS = {
    "sounds-of-the-south": {
        "id": "sounds_south",
        "desc": "Sounds of the South — Georgia Sea Islands to Mississippi Delta, 1959-60",
        "notes": "Blues, field hollers, spirituals, work songs, sea island song, shape-note. 105 tracks.",
        "tags": ["blues", "hollers", "spirituals", "work songs", "sea islands"],
    },
    "sounds-of-the-south-alt": {
        "id": "lomax-alan-1960-sounds-of-the-south-intro",
        "desc": "Sounds of the South (alternate upload)",
        "notes": "Another digitization of the same 1960 Atlantic Records LP set.",
        "tags": ["blues", "hollers", "spirituals"],
    },
    "kentucky": {
        "id": "lomaxky",
        "desc": "Kentucky Recordings, 1937-42",
        "notes": "Rural Kentucky — old-time fiddle, ballads, shape-note, jack tales. Deep Appalachian recordings.",
        "tags": ["old-time", "ballads", "appalachian"],
    },
    "blues-songbook": {
        "id": "alanlomaxbluessongbook",
        "desc": "Blues Songbook — field recordings 1935-78",
        "notes": "Blues from Texas, Mississippi, the South. Includes prison recordings, country blues, urban blues.",
        "tags": ["blues", "texas blues", "mississippi blues", "prison songs"],
    },
    "east-africa": {
        "id": "lp_british-east-africa_alan-lomax-hugh-tracey",
        "desc": "British East Africa — Alan Lomax & Hugh Tracey",
        "notes": "Drums, song, dance from East Africa. Polyrhythm, percussion ensembles, vocal music.",
        "tags": ["african", "drums", "polyrhythm", "vocal"],
    },
    "scotland": {
        "id": "lp_scotland_alan-lomax",
        "desc": "Scotland — Alan Lomax field recordings",
        "notes": "Scots folk song, ballads, waulking songs, mouth music.",
        "tags": ["folk", "celtic", "ballads"],
    },
    "caribbean": {
        "id": "mbid-9582326a-5a8d-4cb8-a517-346bec15320b",
        "desc": "Sounds of the South — alternate (includes Caribbean field recordings)",
        "notes": "Field recordings including Caribbean-influenced Southern music.",
        "tags": ["caribbean", "blues", "folk"],
    },
}

# ── Archive.org API ───────────────────────────────────────────────────────────

def get_mp3_files(archive_id):
    """Return list of (filename, url) for all MP3 files in an archive.org item."""
    url = f"https://archive.org/metadata/{archive_id}"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        print(f"  Could not fetch metadata for {archive_id} (HTTP {r.status_code})")
        return []

    meta = r.json()
    files = meta.get("files", [])
    base = f"https://archive.org/download/{archive_id}/"

    mp3s = []
    for f in files:
        name = f.get("name", "")
        fmt = f.get("format", "").lower()
        if fmt in ("vbr mp3", "mp3") or name.lower().endswith(".mp3"):
            mp3s.append((name, base + requests.utils.quote(name, safe="/")))

    return mp3s


def download_file(url, dest_path):
    """Download a single file with progress indication."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    if os.path.exists(dest_path):
        size = os.path.getsize(dest_path)
        if size > 1000:
            print(f"  ↷ {os.path.basename(dest_path)} (exists)")
            return True

    r = requests.get(url, stream=True, timeout=60)
    if r.status_code != 200:
        print(f"  ✗ {os.path.basename(dest_path)} (HTTP {r.status_code})")
        return False

    total = int(r.headers.get("content-length", 0))
    downloaded = 0

    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)

    mb = downloaded / 1_000_000
    print(f"  ✓ {os.path.basename(dest_path)} ({mb:.1f} MB)")
    return True


def grab_collection(key, dest_root):
    col = COLLECTIONS[key]
    archive_id = col["id"]
    dest_dir = os.path.join(dest_root, key)

    print(f"\n{'─' * 60}")
    print(f"Collection : {col['desc']}")
    print(f"Archive ID : {archive_id}")
    print(f"Dest       : {dest_dir}")
    print(f"Notes      : {col['notes']}")
    print()

    mp3s = get_mp3_files(archive_id)
    if not mp3s:
        print("  No MP3 files found.")
        return

    print(f"  Found {len(mp3s)} MP3 files.\n")
    for name, url in mp3s:
        dest_path = os.path.join(dest_dir, name)
        download_file(url, dest_path)

    # Write a README for the collection
    readme = os.path.join(dest_dir, "_collection.md")
    with open(readme, "w") as f:
        f.write(f"# {col['desc']}\n\n")
        f.write(f"**Source:** https://archive.org/details/{archive_id}\n\n")
        f.write(f"{col['notes']}\n\n")
        f.write(f"**Tags:** {', '.join(col['tags'])}\n\n")
        f.write(f"**Files:** {len(mp3s)} MP3 recordings\n\n")
        f.write("These recordings are in the public domain or made available by the\n")
        f.write("Association for Cultural Equity and the Library of Congress.\n")

    print(f"\n  Done. {len(mp3s)} files in {dest_dir}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("collection", nargs="?", help="Collection name (or 'all')")
    p.add_argument("--dest", default=os.path.expanduser("~/Documents/GitHub/gear/samples/lomax"),
                   help="Destination directory (default: ~/Documents/GitHub/gear/samples/lomax)")
    p.add_argument("--list", action="store_true", help="List available collections")
    args = p.parse_args()

    if args.list or not args.collection:
        print("\nAvailable Lomax collections:\n")
        for key, col in COLLECTIONS.items():
            print(f"  {key}")
            print(f"    {col['desc']}")
            print(f"    {col['notes']}")
            print()
        print(f"Usage: python lomax_grab.py <collection>  --dest <dir>")
        print(f"       python lomax_grab.py all")
        return

    os.makedirs(args.dest, exist_ok=True)

    if args.collection == "all":
        for key in COLLECTIONS:
            grab_collection(key, args.dest)
    elif args.collection in COLLECTIONS:
        grab_collection(args.collection, args.dest)
    else:
        print(f"Unknown collection '{args.collection}'. Run --list to see options.")
        sys.exit(1)


if __name__ == "__main__":
    main()
