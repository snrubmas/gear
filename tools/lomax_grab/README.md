# lomax_grab

Download Alan Lomax field recordings from archive.org as MP3 samples.

## Setup

```bash
pip install requests
```

## Usage

```bash
# See all available collections
python lomax_grab.py --list

# Download one collection
python lomax_grab.py sounds-of-the-south

# Download everything
python lomax_grab.py all

# Download to a custom location
python lomax_grab.py sounds-of-the-south --dest ~/Desktop/samples
```

## Collections

| Key | Contents | Good for |
|---|---|---|
| `sounds-of-the-south` | Blues, field hollers, spirituals, sea island song — Georgia to Mississippi Delta, 1959 | Sampling, textures, vocal atmospheres |
| `kentucky` | Old-time, Appalachian ballads, shape-note — 1937-42 | Drones, melodic loops, unusual timbres |
| `blues-songbook` | Country blues, prison recordings, Texas & Mississippi — 1935-78 | Guitar loops, vocal samples, rhythmic textures |
| `east-africa` | Drums, polyrhythmic percussion, vocal — East Africa (Lomax + Hugh Tracey) | Rhythm reference, percussion textures |
| `scotland` | Scots ballads, waulking songs, mouth music | Drone material, voice textures |

## Archive.org — much bigger picture

The Lomax collections are a fraction of what archive.org has. The full Audio Archive contains:

- **Etree.org live concert recordings** — thousands of legally recorded concerts (Grateful Dead, Phish, and hundreds of others who allow taping)
- **78rpm digitization project** — early blues, jazz, folk, gospel, world music from the 1920s-40s
- **Great 78 Project** — 400,000+ digitized 78rpm records, all pre-1928 (US public domain)
- **Old Time Radio** — tens of thousands of broadcasts
- **NASA audio** — space sounds, mission recordings
- **UCSB Cylinder Audio Archive** — Edison cylinder recordings, 1890s-1920s

For any of these, `lomax_grab.py` can be adapted — just change the archive ID and run.

### Finding downloadable audio on archive.org

Search: `archive.org/search?query=field+recordings&mediatype=audio`

Filter by: **Mediatype: Audio**, **Subject: field recordings / blues / african**

If a page shows "VBR MP3" in the download options, it's free to download.

### Quick curl download (no script needed)

For any archive.org item you find manually:

```bash
# List files in an item
curl -s "https://archive.org/metadata/sounds_south" | python3 -m json.tool | grep '"name"'

# Download a single file
curl -L "https://archive.org/download/sounds_south/LoSS01.mp3" -o sample.mp3

# Download all MP3s from an item (requires internetarchive CLI)
pip install internetarchive
ia download sounds_south --format="VBR MP3"
```
