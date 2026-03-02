# Client Intake System — Design Document

**Date:** 2026-03-01
**Author:** Jonny Valdez + Claude Code

---

## Overview

A Python CLI tool that guides Jonny through a structured client intake questionnaire, then generates a personalized Week 1 training program based on his coaching framework. Outputs both a markdown file (coach reference) and an HTML file (client-facing, trackable).

## Context

- **Business:** Personal training at Domain Athletics, 102 Stanton Ct, Folsom
- **Clientele:** General population — fat loss (10-20 lbs), body recomp, muscle gain. Event-driven timelines (summer, weddings). Max 7 clients.
- **Not:** Athletes, injury rehab
- **Training structure:** 2-3 coached days/week + optional homework day
- **Philosophy:** Mechanisms over exercises. Stimulus-driven programming based on strength curves, resistance profiles, fatigue cost, and desired adaptation.

---

## Intake Questions

### 1. Client Info
- Name
- Age
- Height
- Current weight
- Goal weight (or "not sure")

### 2. Goal & Timeline
- Primary goal: Fat loss / Body recomp / Muscle gain / General fitness
- Target event or deadline (free text, or "no deadline")
- How they want to feel: strong, lean, athletic, confident, etc.

### 3. Training History
- Experience level: Beginner (0-6 mo) / Intermediate (6 mo - 2 yr) / Experienced (2+ yr)
- Current training frequency (days/week)
- Current program (free text or "none")
- Exercises they enjoy (free text)
- Exercises they dislike or want to avoid (free text)

### 4. Schedule & Availability
- Days per week training with Jonny (2 or 3)
- Preferred days (e.g., Mon/Wed/Fri)
- Open to homework days? (yes/no)
- Session length preference (45 min / 60 min)

### 5. Lifestyle Factors
- Job type: Desk / Active / Mixed
- Hours per week working
- Sleep quality: Poor / Okay / Good
- Stress level: Low / Moderate / High
- Meal prep or nutrition tracking: Yes / Somewhat / No

### 6. Coach Notes
- Free text field for observations (posture, movement quality, attitude, etc.)

---

## Program Generation Logic

### Step 1 — Determine Split
- **2 days/week:** Full Body A / Full Body B
- **3 days/week:** Lower / Upper / Full Body (or Lower / Upper / Lower depending on goal)
- **Homework day (if opted in):** Light session — walking, core, mobility, or short isolation circuit (3-4 movements, 20-30 min, low fatigue)

### Step 2 — Exercise Selection (Framework Filters)
1. Does the resistance profile match the strength curve?
2. Is fatigue cost appropriate for the client?
3. Does it accelerate progress toward their goal?
4. Is complexity appropriate for their experience level?

Additional logic:
- Beginners: More skill-based, stable movements (machines, goblet variations)
- Intermediate/Experienced: Heavier output-based work (barbell compounds, free weights)
- Client preferences honored: enjoyed exercises prioritized, dislikes swapped for equivalents

### Step 3 — Volume & Loading
- **2-day clients:** ~12-16 sets per session
- **3-day clients:** ~10-14 sets per session
- Rep ranges by hypertrophy pillar:
  - Mechanical tension: 6-8 reps (heavy, mid-range emphasis)
  - Muscle damage: 8-10 reps (controlled eccentrics, lengthened bias)
  - Metabolic stress: 12-15 reps (shortened bias, higher volume)
- Rest periods: 2-4 min compounds, 1.5-2.5 min isolations

### Step 4 — Session Structure
1. Compound movement (output-based)
2. Secondary compound or accessory
3. Accessory work
4. Isolation finisher (shortened bias, low fatigue)

### Step 5 — Homework Day (if opted in)
- 3-4 movements, 20-30 min
- Low fatigue: bodyweight, bands, light dumbbells
- No supervision required

---

## Output Format

### File Structure
```
/Gym Things/
  clients/
    jane_doe.md          <- coach reference
    jane_doe.html        <- client-facing, trackable
  Jonny_Valdez_Coaching_Framework.md
  intake.py
  docs/plans/
```

### Markdown File (Coach Reference)
- Intake summary (all answers, organized)
- Lifestyle snapshot
- Preferences (enjoys/avoids)
- Coach notes
- Week 1 program tables (exercise, sets, reps, rest, coaching cues)

### HTML File (Client-Facing)
- Client profile summary at top
- Each training day as a formatted table
- Checkboxes next to each exercise for tracking completion
- Notes field per session for logging weights/observations
- Clean, dark/neutral styling with Jonny's branding
- Responsive — works on phone, tablet, laptop
- Standalone file — no server, no login, just open in browser

---

## Workflow

1. Run `python intake.py` in terminal
2. Walk through guided questions (during consult or after)
3. Tool generates client .md + .html files in clients/ folder
4. Review program, tweak by hand if needed
5. Share HTML with client (text, AirDrop, email)
6. Repeat for new training blocks

---

## Technical Notes

- Python 3 — no external dependencies (uses standard library only)
- All data stored as local files (no database)
- Exercise database embedded in the script, tagged with: muscle group, resistance profile, strength curve bias, fatigue cost, complexity level, equipment
- Program generation uses rule-based logic mapped to the coaching framework
