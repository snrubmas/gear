#!/usr/bin/env python3
"""
midi_morph.py — play a MIDI file on loop with evolving transformations.

A single "morph variable" changes slowly over time — like a CV signal —
and continuously shapes how notes are played: their dynamics, timing,
pitch, and density. Use this to put a MIDI file on your devices and then
explore what each transformation does to the sound.

Usage:
    python midi_morph.py <file.mid> [options]

Examples:
    # Play on first available port, slow breathing dynamics
    python midi_morph.py midi/bach-invention-01-BWV772.mid

    # Route to M32, add pitch drift within pentatonic scale
    python midi_morph.py ~/Music/BeatFactory/midi/bach/bach-invention-01-BWV772.mid \\
        --port "Mother-32" --drift 7 --scale pentatonic

    # Random walk morph, heavy humanization, some note dropout
    python midi_morph.py ~/Music/BeatFactory/midi/bach/bach-invention-01-BWV772.mid \\
        --variable walk --humanize 0.4 --dropout 0.2

    # Force 90 BPM, send to Digitakt auto channel
    python midi_morph.py ~/Music/BeatFactory/midi/bach/bach-invention-01-BWV772.mid \\
        --bpm 90 --port "Digitakt"

    # List available MIDI ports
    python midi_morph.py --list-ports

Requirements:
    pip install mido python-rtmidi
"""

import argparse
import math
import random
import sys
import time

import mido


# ── Scales (semitone intervals) ───────────────────────────────────────────────

SCALES = {
    "chromatic":  list(range(12)),
    "major":      [0, 2, 4, 5, 7, 9, 11],
    "minor":      [0, 2, 3, 5, 7, 8, 10],
    "pentatonic": [0, 2, 4, 7, 9],
    "blues":      [0, 3, 5, 6, 7, 10],
    "dorian":     [0, 2, 3, 5, 7, 9, 10],
}


# ── Morph variable ─────────────────────────────────────────────────────────────

class MorphVariable:
    """
    A slowly evolving value in [0.0, 1.0].

    Think of this as a CV signal that you're feeding into all the
    transformations at once. As it moves, the music breathes and shifts.

    Shapes:
      sine      — smooth predictable cycle, good starting point
      slow_sine — sine with added harmonics, less regular
      walk      — random walk, never repeats, more organic
    """

    def __init__(self, shape="sine", rate_cpm=0.25):
        self.shape = shape
        self.rate = rate_cpm / 60.0   # cycles per second
        self._walk_val = 0.5
        self._walk_last = 0.0

    def get(self, t):
        """Return morph value at elapsed time t (seconds)."""
        if self.shape == "sine":
            return 0.5 + 0.5 * math.sin(2 * math.pi * self.rate * t)

        elif self.shape == "slow_sine":
            # Primary wave plus two slower harmonics for organic movement
            v = 0.5 * math.sin(2 * math.pi * self.rate * t)
            v += 0.25 * math.sin(2 * math.pi * self.rate * 2.7 * t + 1.0)
            v += 0.1 * math.sin(2 * math.pi * self.rate * 5.1 * t + 2.3)
            return max(0.0, min(1.0, 0.5 + v))

        elif self.shape == "walk":
            now = time.time()
            if now - self._walk_last > 0.05:   # step every 50 ms
                self._walk_val += random.gauss(0, 0.025)
                self._walk_val = max(0.0, min(1.0, self._walk_val))
                self._walk_last = now
            return self._walk_val

        return 0.5


# ── Transformations ───────────────────────────────────────────────────────────

def xform_velocity(velocity, morph, depth):
    """
    Breathe the dynamics.
    morph → 0: quieter  |  morph → 1: louder
    depth 0.0 = no effect, 1.0 = full range (can silence or clip)
    """
    if depth == 0:
        return velocity
    factor = 1.0 + depth * (morph - 0.5) * 2.0
    return max(1, min(127, int(velocity * factor)))


def xform_timing(delta_s, morph, depth):
    """
    Humanize the grid.
    Adds up to ±20ms of timing offset — notes drift slightly early/late.
    depth 0.0 = locked to grid, 1.0 = maximum drift
    """
    if depth == 0 or delta_s == 0:
        return delta_s
    max_offset = 0.020 * depth
    offset = (morph - 0.5) * 2.0 * max_offset
    return max(0.0, delta_s + offset)


def snap_to_scale(note, intervals, root=0):
    """Snap a MIDI note number to the nearest degree of a scale."""
    octave = note // 12
    pc = (note % 12) - root
    closest = min(intervals, key=lambda s: min(abs(s - pc) % 12, abs(pc - s) % 12))
    return max(0, min(127, octave * 12 + closest + root))


def xform_pitch(note, morph, max_semitones, scale_intervals):
    """
    Drift pitch with the morph variable.
    morph → 0: shift down  |  morph → 1: shift up
    Snapped to scale_intervals if provided.
    """
    if max_semitones == 0:
        return note
    drift = int((morph - 0.5) * 2.0 * max_semitones)
    shifted = max(0, min(127, note + drift))
    if scale_intervals:
        shifted = snap_to_scale(shifted, scale_intervals)
    return shifted


def xform_dropout(morph, depth):
    """
    Drop notes out when morph is low.
    morph=0 + depth=1 → up to 100% dropout chance
    morph=1 → no dropout regardless of depth
    Returns True if the note should play.
    """
    if depth == 0:
        return True
    prob_drop = depth * (1.0 - morph)
    return random.random() > prob_drop


# ── MIDI file preparation ──────────────────────────────────────────────────────

def flatten(mid, bpm_override=None):
    """
    Merge all tracks and return a list of (delta_seconds, message).
    Handles tempo changes unless bpm_override is set.
    """
    tempo = 500_000  # 120 BPM default
    if bpm_override:
        tempo = int(60_000_000 / bpm_override)

    events = []
    for msg in mido.merge_tracks(mid.tracks):
        delta_s = mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
        if msg.type == "set_tempo" and not bpm_override:
            tempo = msg.tempo
        events.append((delta_s, msg))

    return events


# ── Port helpers ───────────────────────────────────────────────────────────────

def list_ports():
    ports = mido.get_output_names()
    if ports:
        print("Available MIDI output ports:")
        for p in ports:
            print(f"  {p}")
    else:
        print("No MIDI output ports found. Is a MIDI interface connected?")


def resolve_port(fragment):
    ports = mido.get_output_names()
    if not ports:
        print("No MIDI output ports available.")
        sys.exit(1)
    if fragment is None:
        return ports[0]
    matches = [p for p in ports if fragment.lower() in p.lower()]
    if not matches:
        print(f"No port matching '{fragment}'. Run --list-ports to see options.")
        sys.exit(1)
    return matches[0]


# ── Main playback loop ─────────────────────────────────────────────────────────

def run(args):
    mid = mido.MidiFile(args.file)
    events = flatten(mid, args.bpm)

    port_name = resolve_port(args.port)
    scale = SCALES.get(args.scale) if args.drift > 0 else None
    morph = MorphVariable(shape=args.variable, rate_cpm=args.rate)

    print(f"File     : {args.file}  ({mid.length:.1f}s per loop)")
    print(f"Port     : {port_name}")
    print(f"Morph    : {args.variable}  rate={args.rate} cycles/min")
    print(f"Velocity : depth={args.velocity}")
    print(f"Humanize : depth={args.humanize}")
    print(f"Drift    : {args.drift} semitones  scale={args.scale}")
    print(f"Dropout  : depth={args.dropout}")
    print()
    print("Playing. Ctrl-C to stop.\n")

    start = time.time()
    loop = 0

    with mido.open_output(port_name) as port:
        try:
            while True:
                loop += 1

                for delta_s, msg in events:
                    t = time.time() - start
                    m = morph.get(t)

                    # Sleep for this event's delta (with humanization)
                    sleep = xform_timing(delta_s, m, args.humanize)
                    if sleep > 0:
                        time.sleep(sleep)

                    # Refresh morph after sleep
                    t = time.time() - start
                    m = morph.get(t)

                    if msg.type == "note_on" and msg.velocity > 0:
                        # Skip channels we're not processing
                        if args.channel is not None and msg.channel != args.channel:
                            port.send(msg)
                            continue

                        if not xform_dropout(m, args.dropout):
                            # Drop this note — send note_off so nothing hangs
                            port.send(msg.copy(velocity=0))
                            continue

                        note = xform_pitch(msg.note, m, args.drift, scale)
                        vel  = xform_velocity(msg.velocity, m, args.velocity)
                        port.send(msg.copy(note=note, velocity=vel))

                        # Status line
                        bar = "▓" * int(m * 20) + "░" * (20 - int(m * 20))
                        print(
                            f"  loop {loop:03d}  t={t:6.1f}s  morph [{bar}] {m:.2f}",
                            end="\r"
                        )

                    elif msg.type in ("note_off", "note_on"):
                        port.send(msg)

                    elif msg.type == "end_of_track":
                        pass  # loop continues

                    else:
                        port.send(msg)

        except KeyboardInterrupt:
            print("\n\nStopping — sending all-notes-off...")
            for ch in range(16):
                port.send(mido.Message("control_change", channel=ch, control=123, value=0))
            print("Done.")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("file", nargs="?", help="MIDI file to play")
    p.add_argument("--port",       default=None,        help="MIDI output port (partial name OK)")
    p.add_argument("--bpm",        type=float,          help="Override file tempo")
    p.add_argument("--variable",   default="sine",      choices=["sine", "slow_sine", "walk"],
                                                        help="Morph variable shape (default: sine)")
    p.add_argument("--rate",       type=float, default=0.25,
                                                        help="Morph rate in cycles/minute (default: 0.25 = 4 min cycle)")
    p.add_argument("--velocity",   type=float, default=0.4,
                                                        help="Velocity modulation depth 0-1 (default: 0.4)")
    p.add_argument("--humanize",   type=float, default=0.15,
                                                        help="Timing humanization depth 0-1 (default: 0.15)")
    p.add_argument("--drift",      type=int,   default=0,
                                                        help="Max pitch drift in semitones (default: 0 = off)")
    p.add_argument("--scale",      default="chromatic", choices=list(SCALES.keys()),
                                                        help="Scale to snap pitch drift to (default: chromatic)")
    p.add_argument("--dropout",    type=float, default=0.0,
                                                        help="Note dropout depth 0-1 (default: 0 = off)")
    p.add_argument("--channel",    type=int,   default=None,
                                                        help="Only transform notes on this channel 0-15 (default: all)")
    p.add_argument("--list-ports", action="store_true", help="List MIDI output ports and exit")

    args = p.parse_args()

    if args.list_ports:
        list_ports()
        return

    if not args.file:
        p.print_help()
        sys.exit(1)

    run(args)


if __name__ == "__main__":
    main()
