# Tutorial 01 — First Loop
**Clock:** Digitakt | **Voices:** BIA (kick) + Mother-32 (bassline) | **Texture:** Digitakt sample track

You will build a complete working loop: a kick drum from the BIA, a bassline from one Mother-32, and a sample track from the Digitakt — all locked to the Digitakt's clock. By the end of this session you will have a groove that runs itself while you explore.

Estimated time to first sound: **10 minutes**.

---

## Connections

Do these before powering anything on.

### MIDI chain
```
Digitakt MIDI OUT → CME MIDI Thru5 IN
CME MIDI Thru5 OUT 1 → Mutant Brain MIDI IN
CME MIDI Thru5 OUT 2 → Mother-32 #1 MIDI IN (front panel, 5-pin DIN)
```

### Eurorack patch
```
Mutant Brain GATE A → BIA TRIG input
```

### Audio
```
BIA OUT → Erica Black Stereo Mixer (any open channel)
Mother-32 #1 VCA OUT → Erica Black Stereo Mixer (left channel, or existing patch)
Erica Black Stereo Mixer L/R OUT → Tascam Model 16
```
*If the M32 → Mixer → Tascam path is already your known-good patch, leave it.*

---

## Layer 1: Clock

**Goal:** Digitakt is running. Everything will follow it.

1. Power on the Digitakt.
2. Press **[SETTINGS]** (the gear icon).
3. Navigate to **MIDI CONFIG → SYNC**.
4. Turn on **CLOCK SEND** (press **[YES]** to toggle it on — it lights up).
5. Turn on **TRANSPORT SEND** (same).
6. Leave **CLOCK RECEIVE** off — the Digitakt is master, not a follower.
7. Back out to the main screen.
8. Press **[TEMPO]**. Turn the **LEVEL/DATA** knob to set BPM. Start at **90**. You can always change this later.

The Digitakt is now broadcasting clock. Every device downstream will follow it when you press **[PLAY]**.

---

## Layer 2: Rhythm — BIA Kick

**Goal:** A kick drum fires on beat 1 (and wherever you want it).

### Configure Mutant Brain
The Mutant Brain converts MIDI notes on a specific channel into gate signals. By default, GATE A fires when it receives a note on whatever channel it's configured to monitor. Confirm GATE A responds to incoming MIDI notes — tap the **HIT** button on the BIA to confirm the BIA is working first.

### Set up a Digitakt MIDI track for the BIA
The Digitakt has 8 MIDI tracks (tracks 9–16). You'll use one to send note triggers to the Mutant Brain.

1. Hold **[TRK]** and press **[TRIG 9]** to select MIDI Track 1 (shown as T9 on screen).
2. Press **[SRC]** to open the MIDI Source page.
3. Turn knob **A** (**CHAN**) to set the channel the Mutant Brain's GATE A is listening on. A common default is **channel 10** (the conventional MIDI drum channel) — use whatever your Mutant Brain is configured for.
4. Press **[RECORD]** to enter Grid Recording.
5. Press **[TRIG 1]** to place a note on step 1 (beat 1). This will fire GATE A → BIA TRIG.
6. Press **[PLAY]**.

You should hear the BIA fire on beat 1 of every bar. The BIA's default patch produces a percussive hit — don't worry about sound design yet.

### Add more kick hits
7. Stay in Grid Recording (**[RECORD]** is still lit).
8. Add **[TRIG 9]** for beat 3 (a half-time feel), or **[TRIG 1], [TRIG 5], [TRIG 9], [TRIG 13]** for four-on-the-floor.
9. Listen. Pick what feels right.

### Shape the BIA sound (optional, 2 minutes)
On the BIA panel:
- **DECAY** at roughly 12 o'clock — medium length hit.
- **ATTACK** at center — clean transient.
- **MORPH** fully CCW — sine waveform, clean thud.
- **SKIN/LIQUID/METAL** switch → **SKIN** — membrane-style, most kick-like.
- **BASS/ALTO/TREBLE** switch → **BASS** — lowest register.
- Adjust **PITCH** (the rotary encoder) down until it sits in kick territory. Press+turn for coarse steps.

You now have a kick. Let it loop.

---

## Layer 3: Voice — Mother-32 Bassline

**Goal:** M32 plays a simple repeating bassline locked to the Digitakt's clock.

### Configure Mother-32 #1 for MIDI
The M32 listens on MIDI channel 1 by default. The Digitakt MIDI track you assign to it should match.

### Set M32 panel for bassline
Set these controls on Mother-32 #1:
- **VCA MODE** → **EG** (switch toward EG). Each MIDI note will trigger the envelope.
- **VCO WAVE** → **SAW** (switch down). Bright, cutting bass tone.
- **CUTOFF** → 10–11 o'clock. Filter partially open.
- **RESONANCE** → fully CCW (no resonance to start).
- **VCF MOD SOURCE** → **EG**. The envelope will open the filter on each note.
- **VCF MOD AMOUNT** → 9–10 o'clock. Subtle filter punch on each note.
- **VCF MOD POLARITY** → **+** (up).
- **ATTACK** → fully CCW (fast attack — immediate).
- **DECAY** → 9 o'clock (medium-short — punchy).
- **SUSTAIN** → **OFF** (switch down). Note dies after decay — no sustain.
- **VOLUME** → 12 o'clock.
- **VCO MOD AMOUNT** → fully CCW (no pitch mod).

### Set up a Digitakt MIDI track for M32
1. Hold **[TRK]** + press **[TRIG 10]** to select MIDI Track 2.
2. Press **[SRC]**. Set **CHAN** (knob A) to **1** (M32's default MIDI channel).
3. Press **[RECORD]** to enter Grid Recording.
4. Press **[TRIG 1]** — a note is placed on step 1.
   - The default note is C3. You can change it: hold **[TRIG 1]** and turn knob **A** (NOTE) on the TRIG page.
5. Add a few more notes. A simple starting bassline:
   - **Step 1**: C (root)
   - **Step 5**: C (root, beat 2)
   - **Step 9**: G (fifth) or F (fourth)
   - **Step 13**: C (root)
6. Press **[PLAY]** if not already running. You should hear the M32 bassline locked to the kick.

### Adjust until it grooves
- Change **CUTOFF** on the M32 while it plays. Listen to how the filter shapes the bass character.
- Try raising **RESONANCE** slightly (7–8 o'clock) for a more aggressive tone.
- Try changing note pitches: hold a lit **[TRIG]** key and turn knob **A** on the TRIG page.

---

## Layer 4: Texture — A Sample from Digitakt

**Goal:** Add one Digitakt audio track — a hi-hat, loop, or BeatFactory sample — to fill space.

### Load and program a hi-hat or texture sample
1. Hold **[TRK]** + press **[TRIG 3]** to select Audio Track 3.
2. Press **[SRC]**.
3. Turn knob **D** (SAMP) to browse samples. If you have BeatFactory samples loaded in the project, scroll to find one — a hi-hat, shaker, or ambient texture works well here.
4. Press **[YES]** to confirm.
5. Press **[RECORD]**.
6. For a straight hi-hat feel: press **[TRIG 1], [TRIG 3], [TRIG 5], [TRIG 7], [TRIG 9], [TRIG 11], [TRIG 13], [TRIG 15]** (every 8th note).
7. Or for something more rhythmically interesting, play with odd placements — steps 3, 7, 11, 14.

### Blend it in
- Press **[AMP]** and lower the **VOL** parameter (knob G) to mix the sample behind the kick and bass.
- Add a touch of reverb: press **[FUNC]** + **[AMP]** to open the Reverb send. Turn knob **B** (REV) up slightly.

---

## The Loop Is Running

You now have:
- Digitakt as MIDI clock master
- BIA kick, locked via Mutant Brain gate
- M32 bassline, sequenced from a Digitakt MIDI track
- A texture sample from the Digitakt audio tracks

Let it run for a few minutes. Listen.

---

## Experiment Prompts

These are questions to explore without instructions — no right answer.

1. **Change the BIA decay.** Turn **DECAY** slowly clockwise while the kick plays. Where does it stop sounding like a kick and start sounding like something else?

2. **Change one bassline note.** Hold a lit **[TRIG]** on Track 10 and turn the NOTE knob. What happens to the groove when you move just one note?

3. **Add swing.** Press **[TEMPO]** on the Digitakt. Turn knob **E** (SWING) from 50% up to 58%. Does the groove feel looser?

4. **Mute a layer.** Hold **[FUNC]** + **[BANK]** on the Digitakt to enter Mute mode. Mute the sample track (press its trig button). Does the loop feel different with fewer elements?

5. **Filter the bass.** Turn the M32's **CUTOFF** down slowly while the loop plays. Where does the bass disappear into the low end? Where does it open up?

6. **Try the LIQUID algorithm on BIA.** Flip the SKIN/LIQUID/METAL switch to **LIQUID**. The kick becomes something else. Try it with **ALTO** register. Is it usable?

7. **Change BPM.** Press **[TEMPO]** on the Digitakt and lower the BPM to 75. Does the groove change character? Try 110. What feels right for your ear today?

---

## What This Unlocks

- **Tutorial 02** replaces the Digitakt clock with Pamela's Pro Workout — the same loop, but the modular drives the tempo.
- **Tutorial 04** adds Maths as a modulation source — a slow-moving LFO into the M32 filter that evolves the bassline without any programming.
- **Tutorial 06** digs into BeatFactory — loading and performing your own samples alongside the live patch.
