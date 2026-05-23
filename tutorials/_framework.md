# Studio Tutorial Framework

## Philosophy

These tutorials are not manual summaries. They are session guides — starting points for experimentation, built around one governing idea: **make a complete-sounding loop as fast as possible, then explore**.

Every tutorial establishes a minimum working system: a clock, something rhythmic, a voice, and a texture. From that foundation, everything else is optional exploration.

---

## The Four Layers

Each session builds through four layers, in order. You stop whenever the session feels complete.

| Layer | Role | Examples |
|---|---|---|
| **1. Clock** | Master tempo — everything follows this | Digitakt, Pamela's Pro Workout, KeyStep Pro, M32 sequencer |
| **2. Rhythm** | The pulse you hear — beat, gates, pattern | Digitakt audio tracks, BIA via Mutant Brain, clock divider |
| **3. Voice** | Something with pitch | Mother-32 bassline, Beehive melody, MicroBrute drone |
| **4. Texture** | Color, space, randomness | BeatFactory sample, Strymon reverb, Maths LFO into filter |

You do not need all four layers for a session to be worthwhile. A clock and one voice is a complete experiment.

---

## Clock Sources

These devices can serve as master tempo for the full rig. Each tutorial names which one is in charge.

| Device | What it clocks | How |
|---|---|---|
| **Digitakt** | Everything via MIDI | MIDI OUT → CME Thru5 → all MIDI devices; MIDI tracks → Mutant Brain → modular gates |
| **Pamela's Pro Workout** | Eurorack modular | Gate outputs → BIA TRIG, M32 TEMPO, clock divider, etc. |
| **KeyStep Pro** | MIDI + CV/gate | MIDI OUT + dedicated CV clock output |
| **Mother-32** | Itself + one other | ASSIGN output (clock mode) → another M32 TEMPO input |

---

## Tutorial Structure

Each tutorial follows this format:

1. **Overview** — one sentence on what you'll build
2. **Connections** — exactly what to plug in before you start
3. **Layer by layer** — step-by-step instructions with expected results
4. **Experiment prompts** — open questions to explore once the loop is running
5. **What this unlocks** — which next tutorial builds on this one

---

## Conventions

- **Bold text** = physical control label or patch point exactly as it appears on the device
- `Code text` = menu path (e.g., `SETTINGS > MIDI CONFIG > SYNC`)
- "Raise slowly" = turn clockwise from minimum
- "Fully CCW" / "Fully CW" = knob at its minimum / maximum stop
- An arrow (→) means patch cable or signal flow

---

## Tutorial Index

| # | Title | Clock | Voices | Focus |
|---|---|---|---|---|
| [01](01-digitakt-clock-bia-kick-m32-bass.md) | First Loop | Digitakt | BIA + M32 | Complete working loop from scratch |
| 02 | Pamela's Clocks Everything | Pamela's Pro Workout | BIA + M32 | Pure Eurorack timing, no MIDI clock |
| 03 | M32 as Sequencer and Voice | M32 internal | M32 + Beehive | Two voices, one sequences the other |
| 04 | Maths as Modulation | Digitakt | M32 + Maths | Adding slow movement to a static patch |
| 05 | Beehive First Sounds | Digitakt | Beehive models | Exploring all 16 synthesis models |
| 06 | BeatFactory + Modular | Digitakt | BIA + M32 + samples | Adding BeatFactory samples to a live patch |

*Tutorials are added as sessions happen.*
