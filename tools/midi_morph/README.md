# midi_morph

Play any MIDI file on loop to your hardware, continuously transformed by a slowly evolving variable.

The idea: instead of programming from scratch, find a MIDI file with good musical content (even cheesy source material), put it on your devices, and use the transformations to make it breathe and evolve. Then turn knobs on the hardware to explore what the device can do with music already running through it.

## Setup

```bash
pip install mido python-rtmidi
```

## Quick start

```bash
# See what MIDI ports are available
python midi_morph.py --list-ports

# Play Bach Invention 1, default settings (slow breathing dynamics)
python midi_morph.py ~/Music/BeatFactory/midi/bach/bach-invention-01-BWV772.mid

# Route to Mother-32 specifically
python midi_morph.py ~/Music/BeatFactory/midi/bach/bach-invention-01-BWV772.mid --port "Mother-32"

# Force 90 BPM
python midi_morph.py midi/bach-invention-01-BWV772.mid --bpm 90
```

## The morph variable

Every transformation is driven by a single value that moves slowly between 0.0 and 1.0. Think of it as a CV signal feeding all the transformations at once.

```
morph = 0.0 ──────────────── 0.5 ──────────────── 1.0
         quiet               neutral               loud
         early               on-grid               late  
         shifted down        no drift              shifted up
         sparse              full                  full
```

**Shapes** (set with `--variable`):

| Shape | Description |
|---|---|
| `sine` | Smooth, predictable cycle. Good starting point. |
| `slow_sine` | Sine with added harmonics — less mechanical. |
| `walk` | Random walk. Never repeats. Most organic. |

**Rate** (`--rate`, cycles per minute):
- `0.1` = one full cycle every 10 minutes — glacial, nearly imperceptible
- `0.25` = one cycle every 4 minutes (default) — slow like a long LFO
- `1.0` = one cycle per minute — you can hear it moving
- `4.0` = four cycles per minute — obvious, rhythmic shaping

## Transformations

### `--velocity` (default 0.4)
Breathes the dynamics. Low morph = quieter notes, high morph = louder. At depth 0.4, notes swing between about 60% and 140% of their original velocity. Depth 0.0 = off.

### `--humanize` (default 0.15)
Moves notes slightly off the grid. Maximum ±20ms at depth 1.0. Makes quantized MIDI feel played rather than programmed. Depth 0.0 = locked to grid.

### `--drift` + `--scale`
Transposes pitch with the morph variable. `--drift 7` lets notes drift up to 7 semitones up or down. `--scale pentatonic` snaps all drift to pentatonic intervals — everything stays musical even at maximum shift.

```bash
# Drift ±5 semitones, snapped to minor scale
python midi_morph.py file.mid --drift 5 --scale minor

# Drift ±12 semitones (full octave), pentatonic — stays very musical
python midi_morph.py file.mid --drift 12 --scale pentatonic
```

### `--dropout` (default 0.0)
Removes notes probabilistically when morph is low. At depth 0.3 and morph=0, about 30% of notes drop; at morph=1, nothing drops. Creates sparse/dense breathing patterns.

```bash
# Notes thin out at the bottom of each morph cycle
python midi_morph.py file.mid --dropout 0.3
```

## Recipes for specific devices

### Mother-32 — evolving bassline
```bash
python midi_morph.py midi/bach-invention-01-BWV772.mid \
    --port "Mother-32" \
    --bpm 90 \
    --variable slow_sine \
    --velocity 0.5 \
    --humanize 0.2 \
    --channel 0
```
The M32 is monophonic — it will play the last note received per tick. Route Channel 1 (MIDI channel 0 in zero-indexed) for just the bass voice. Set M32 **VCA MODE → EG**, play with **CUTOFF** and **RESONANCE** while it runs.

### JUNO-DS88 — chord pad
```bash
python midi_morph.py midi/bach-invention-01-BWV772.mid \
    --port "JUNO" \
    --bpm 75 \
    --variable sine \
    --rate 0.1 \
    --velocity 0.6 \
    --humanize 0.3
```
Very slow morph (0.1 cycles/min = 10-minute cycle). The JUNO handles polyphony — both voices of the invention play. Use a pad or string sound. Explore the JUNO's reverb and chorus while it plays.

### Beehive — drifting melody
```bash
python midi_morph.py midi/bach-invention-01-BWV772.mid \
    --port "Mutant Brain" \
    --drift 7 \
    --scale pentatonic \
    --variable walk \
    --dropout 0.2
```
Random walk morph with pentatonic snapping — every loop is different. The Beehive's HARMONICS and TIMBRE knobs become interesting to explore when the pitch input is slowly drifting.

## MIDI file sources

| Source | What's there | URL |
|---|---|---|
| **Mutopia Project** | Classical (Bach, Beethoven, Chopin) — public domain | https://mutopiaproject.org |
| **BitMidi** | 113,000+ files, all genres, preview before download | https://bitmidi.com |
| **MIDIWORLD** | Jazz, blues, pop, rock, game themes | https://midiworld.com/files |
| **Internet Archive: Magic of MIDI** | 169,000+ files | https://archive.org/details/themagicofmidiv1 |

## Included MIDI files

| File | Description | Source |
|---|---|---|
| `midi/bach-invention-01-BWV772.mid` | Bach Two-Part Invention No. 1 in C major | Mutopia Project (CC) |
| `midi/bach-invention-02-BWV773.mid` | Bach Two-Part Invention No. 2 in C minor | Mutopia Project (CC) |
| `midi/bach-invention-04-BWV775.mid` | Bach Two-Part Invention No. 4 in D minor | Mutopia Project (CC) |
