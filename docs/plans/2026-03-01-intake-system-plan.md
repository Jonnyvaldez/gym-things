# Client Intake System — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Python CLI intake tool that collects client info and generates a personalized Week 1 training program as both markdown and HTML files.

**Architecture:** Single entry point (`intake.py`) with supporting modules for the exercise database, program generation logic, and output formatting. All data is local files, no external dependencies. The exercise database is a Python dict of exercises tagged with metadata from Jonny's coaching framework (muscle group, resistance profile, strength curve bias, fatigue cost, complexity, equipment).

**Tech Stack:** Python 3.9+ standard library only (no pip installs). pytest for tests.

---

### Task 1: Project Setup & Exercise Database

**Files:**
- Create: `exercise_db.py`
- Create: `tests/test_exercise_db.py`

**Step 1: Write the failing test**

```python
# tests/test_exercise_db.py
from exercise_db import EXERCISES, get_exercises_for_muscle_group, filter_exercises

def test_exercises_exist():
    assert len(EXERCISES) > 0

def test_each_exercise_has_required_fields():
    required = {"name", "muscle_group", "secondary_muscles", "resistance_profile",
                "strength_curve_bias", "fatigue_cost", "complexity", "equipment",
                "hypertrophy_pillar", "default_sets", "default_reps", "default_rest",
                "coaching_cue"}
    for ex in EXERCISES:
        assert required.issubset(ex.keys()), f"{ex.get('name', 'unknown')} missing fields"

def test_get_exercises_for_muscle_group():
    glutes = get_exercises_for_muscle_group("glutes")
    assert len(glutes) > 0
    assert all(e["muscle_group"] == "glutes" for e in glutes)

def test_filter_exercises_by_complexity():
    beginner = filter_exercises(complexity="beginner")
    assert len(beginner) > 0
    assert all(e["complexity"] in ("beginner", "all") for e in beginner)

def test_filter_exercises_by_equipment():
    cable = filter_exercises(equipment="cable")
    assert len(cable) > 0
    assert all(e["equipment"] == "cable" for e in cable)
```

**Step 2: Run test to verify it fails**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_exercise_db.py -v`
Expected: FAIL — module not found

**Step 3: Write the exercise database**

Create `exercise_db.py` with:
- `EXERCISES` list — comprehensive exercise database covering:
  - **Glutes:** KAS glute bridge, hip thrust, glute medius kickback, cable kickback, cable pull-through
  - **Quads:** goblet squat, hack squat, leg press, leg extension, Bulgarian split squat, walking lunge, reverse lunge
  - **Hamstrings:** RDL, lying leg curl, seated leg curl, single-leg RDL
  - **Chest:** incline DB press, chest press machine, cable fly, push-up
  - **Back:** T-bar row, seated cable row, lat pulldown, chest-supported row, DB row
  - **Shoulders:** seated shoulder press, seated lateral raise, DB rear delt fly, cable lateral raise, face pull
  - **Arms:** cable curl, triceps pressdown, hammer curl, overhead triceps extension
  - **Calves:** standing calf raise, seated calf raise
  - **Core:** plank, pallof press, dead bug, cable crunch
- Each exercise tagged with all required metadata fields
- `get_exercises_for_muscle_group(group)` function
- `filter_exercises(**kwargs)` function that filters by any combination of fields

**Step 4: Run tests to verify they pass**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_exercise_db.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add exercise_db.py tests/test_exercise_db.py
git commit -m "feat: add exercise database with filtering"
```

---

### Task 2: Client Intake CLI

**Files:**
- Create: `intake_questions.py`
- Create: `tests/test_intake_questions.py`

**Step 1: Write the failing test**

```python
# tests/test_intake_questions.py
from intake_questions import run_intake, INTAKE_SECTIONS
from unittest.mock import patch
from io import StringIO

def test_intake_sections_defined():
    assert len(INTAKE_SECTIONS) == 6
    names = [s["name"] for s in INTAKE_SECTIONS]
    assert "client_info" in names
    assert "goal_timeline" in names
    assert "training_history" in names
    assert "schedule" in names
    assert "lifestyle" in names
    assert "coach_notes" in names

def test_run_intake_collects_all_fields():
    # Simulate user input for every question
    inputs = [
        "Jane Doe",       # name
        "25",             # age
        "5'2\"",          # height
        "170",            # current weight
        "160",            # goal weight
        "2",              # goal: body recomp
        "summer 2026",    # timeline
        "strong, lean",   # how they want to feel
        "2",              # experience: intermediate
        "5",              # current frequency
        "Hourglass Aspect template", # current program
        "hip thrust, goblet squat, T-bar row, shoulder press", # enjoys
        "lunges, Bulgarian split squats", # dislikes
        "3",              # days with Jonny
        "Mon, Wed, Fri",  # preferred days
        "y",              # homework: yes
        "2",              # session length: 60 min
        "1",              # job: desk
        "40",             # hours/week
        "2",              # sleep: okay
        "2",              # stress: moderate
        "1",              # meal prep: yes
        "Good attitude, needs to reduce volume", # coach notes
    ]
    with patch("builtins.input", side_effect=inputs):
        data = run_intake()

    assert data["client_info"]["name"] == "Jane Doe"
    assert data["client_info"]["age"] == "25"
    assert data["goal_timeline"]["primary_goal"] == "Body recomp"
    assert data["schedule"]["days_per_week"] == 3
    assert data["schedule"]["homework"] is True
    assert data["lifestyle"]["job_type"] == "Desk"
```

**Step 2: Run test to verify it fails**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_intake_questions.py -v`
Expected: FAIL — module not found

**Step 3: Write the intake questions module**

Create `intake_questions.py` with:
- `INTAKE_SECTIONS` — list of section dicts, each with name, display title, and questions
- Each question has: key, prompt text, type (text/choice/number/boolean), and options (if choice)
- `run_intake()` function that:
  - Prints a welcome header ("Jonny Valdez Coaching — New Client Intake")
  - Iterates through sections, printing section headers
  - For each question: displays prompt, collects input, validates
  - Choice questions show numbered options (user picks a number)
  - Boolean questions accept y/n
  - Returns a nested dict with all answers organized by section

**Step 4: Run tests to verify they pass**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_intake_questions.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add intake_questions.py tests/test_intake_questions.py
git commit -m "feat: add client intake questionnaire CLI"
```

---

### Task 3: Program Generation Engine

**Files:**
- Create: `program_generator.py`
- Create: `tests/test_program_generator.py`

**Step 1: Write the failing tests**

```python
# tests/test_program_generator.py
from program_generator import generate_program, determine_split, select_exercises_for_session

def test_determine_split_2_days():
    split = determine_split(days_per_week=2, primary_goal="Body recomp", homework=False)
    assert len(split) == 2
    assert split[0]["name"] == "Full Body A"
    assert split[1]["name"] == "Full Body B"

def test_determine_split_3_days():
    split = determine_split(days_per_week=3, primary_goal="Body recomp", homework=False)
    assert len(split) == 3

def test_determine_split_with_homework():
    split = determine_split(days_per_week=3, primary_goal="Fat loss", homework=True)
    assert len(split) == 4
    assert split[3]["name"] == "Homework (Optional)"

def test_select_exercises_respects_session_structure():
    # Session should follow: compound -> secondary -> accessory -> isolation finisher
    exercises = select_exercises_for_session(
        session_type="lower",
        experience="intermediate",
        preferred=[],
        avoided=[],
        goal="Body recomp"
    )
    assert len(exercises) >= 3
    assert len(exercises) <= 5

def test_select_exercises_respects_preferences():
    exercises = select_exercises_for_session(
        session_type="lower",
        experience="intermediate",
        preferred=["hip thrust", "goblet squat"],
        avoided=["lunges"],
        goal="Body recomp"
    )
    names = [e["name"].lower() for e in exercises]
    assert not any("lunge" in n for n in names)

def test_generate_program_volume_3_day():
    intake_data = {
        "client_info": {"name": "Jane Doe"},
        "goal_timeline": {"primary_goal": "Body recomp"},
        "training_history": {
            "experience": "Intermediate",
            "preferred_exercises": "hip thrust, goblet squat",
            "avoided_exercises": "lunges"
        },
        "schedule": {"days_per_week": 3, "homework": True, "session_length": "60 min"},
    }
    program = generate_program(intake_data)
    assert "days" in program
    for day in program["days"]:
        if day["name"] != "Homework (Optional)":
            total_sets = sum(e["sets"] for e in day["exercises"])
            assert 10 <= total_sets <= 16, f"{day['name']} has {total_sets} sets"

def test_generate_program_volume_2_day():
    intake_data = {
        "client_info": {"name": "John Smith"},
        "goal_timeline": {"primary_goal": "Fat loss"},
        "training_history": {
            "experience": "Beginner",
            "preferred_exercises": "",
            "avoided_exercises": ""
        },
        "schedule": {"days_per_week": 2, "homework": False, "session_length": "45 min"},
    }
    program = generate_program(intake_data)
    assert len(program["days"]) == 2
    for day in program["days"]:
        total_sets = sum(e["sets"] for e in day["exercises"])
        assert 12 <= total_sets <= 18, f"{day['name']} has {total_sets} sets"

def test_homework_day_is_low_fatigue():
    intake_data = {
        "client_info": {"name": "Test"},
        "goal_timeline": {"primary_goal": "Body recomp"},
        "training_history": {
            "experience": "Intermediate",
            "preferred_exercises": "",
            "avoided_exercises": ""
        },
        "schedule": {"days_per_week": 2, "homework": True, "session_length": "60 min"},
    }
    program = generate_program(intake_data)
    homework = [d for d in program["days"] if "Homework" in d["name"]]
    assert len(homework) == 1
    assert len(homework[0]["exercises"]) <= 4
```

**Step 2: Run tests to verify they fail**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_program_generator.py -v`
Expected: FAIL — module not found

**Step 3: Write the program generator**

Create `program_generator.py` with:

- `determine_split(days_per_week, primary_goal, homework)` — returns list of session dicts with name and session_type
  - 2 days: Full Body A / Full Body B
  - 3 days + recomp/muscle gain: Lower / Upper / Full Body
  - 3 days + fat loss: Full Body A / Full Body B / Full Body C
  - Homework appended if opted in

- `select_exercises_for_session(session_type, experience, preferred, avoided, goal)` — returns ordered exercise list
  - Uses `exercise_db.py` to pull candidates
  - Filters by session_type muscle groups
  - Prioritizes preferred exercises
  - Removes avoided exercises (substitutes equivalents)
  - Orders: compound → secondary → accessory → isolation finisher
  - Adjusts complexity based on experience level

- `generate_program(intake_data)` — main function
  - Calls determine_split
  - For each session, calls select_exercises_for_session
  - Sets volume: 10-14 sets/session (3-day), 12-16 sets/session (2-day)
  - Assigns rep ranges per hypertrophy pillar:
    - Compounds: 6-8 reps (mechanical tension)
    - Accessories: 8-10 reps (muscle damage)
    - Isolation finishers: 12-15 reps (metabolic stress)
  - Rest: 2-4 min compounds, 1.5-2.5 min isolations
  - Returns full program dict

**Step 4: Run tests to verify they pass**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_program_generator.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add program_generator.py tests/test_program_generator.py
git commit -m "feat: add program generation engine with framework logic"
```

---

### Task 4: Markdown Output Generator

**Files:**
- Create: `output_generators.py`
- Create: `tests/test_output_generators.py`

**Step 1: Write the failing test**

```python
# tests/test_output_generators.py
from output_generators import generate_markdown, generate_html

def test_generate_markdown_has_all_sections():
    intake_data = {
        "client_info": {"name": "Jane Doe", "age": "25", "height": "5'2\"",
                        "current_weight": "170", "goal_weight": "160"},
        "goal_timeline": {"primary_goal": "Body recomp", "timeline": "summer 2026",
                          "desired_feeling": "strong, lean"},
        "training_history": {"experience": "Intermediate", "current_frequency": "5",
                             "current_program": "template", "preferred_exercises": "hip thrust",
                             "avoided_exercises": "lunges"},
        "schedule": {"days_per_week": 3, "preferred_days": "Mon, Wed, Fri",
                     "homework": True, "session_length": "60 min"},
        "lifestyle": {"job_type": "Desk", "hours_per_week": "40", "sleep": "Okay",
                      "stress": "Moderate", "nutrition": "Yes"},
        "coach_notes": {"notes": "Good attitude"},
    }
    program = {
        "days": [
            {"name": "Day 1 — Lower Body", "exercises": [
                {"name": "KAS Glute Bridge", "sets": 3, "reps": "6-8",
                 "rest": "3 min", "coaching_cue": "Full hip extension, pause at top"}
            ]}
        ]
    }
    md = generate_markdown(intake_data, program)
    assert "# Jane Doe — Client Profile" in md
    assert "## Intake Summary" in md
    assert "## Lifestyle" in md
    assert "## Preferences" in md
    assert "## Coach Notes" in md
    assert "## Week 1 Program" in md
    assert "KAS Glute Bridge" in md
    assert "| Exercise |" in md
```

**Step 2: Run test to verify it fails**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_output_generators.py::test_generate_markdown_has_all_sections -v`
Expected: FAIL — module not found

**Step 3: Write the markdown generator**

Add to `output_generators.py`:
- `generate_markdown(intake_data, program)` — returns a string of formatted markdown
  - Header with client name
  - Intake Summary section (all key data points)
  - Lifestyle section
  - Preferences section (enjoys/avoids)
  - Coach Notes section
  - Week 1 Program section with markdown tables per day
  - Each table: Exercise | Sets | Reps | Rest | Notes columns
  - Footer: "Program by Jonny Valdez — Domain Athletics, Folsom"

**Step 4: Run test to verify it passes**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_output_generators.py::test_generate_markdown_has_all_sections -v`
Expected: PASS

**Step 5: Commit**

```bash
git add output_generators.py tests/test_output_generators.py
git commit -m "feat: add markdown output generator"
```

---

### Task 5: HTML Output Generator

**Files:**
- Modify: `output_generators.py`
- Modify: `tests/test_output_generators.py`

**Step 1: Write the failing test**

```python
# Add to tests/test_output_generators.py

def test_generate_html_is_valid():
    intake_data = {
        "client_info": {"name": "Jane Doe", "age": "25", "height": "5'2\"",
                        "current_weight": "170", "goal_weight": "160"},
        "goal_timeline": {"primary_goal": "Body recomp", "timeline": "summer 2026",
                          "desired_feeling": "strong, lean"},
        "training_history": {"experience": "Intermediate", "current_frequency": "5",
                             "current_program": "template", "preferred_exercises": "hip thrust",
                             "avoided_exercises": "lunges"},
        "schedule": {"days_per_week": 3, "preferred_days": "Mon, Wed, Fri",
                     "homework": True, "session_length": "60 min"},
        "lifestyle": {"job_type": "Desk", "hours_per_week": "40", "sleep": "Okay",
                      "stress": "Moderate", "nutrition": "Yes"},
        "coach_notes": {"notes": "Good attitude"},
    }
    program = {
        "days": [
            {"name": "Day 1 — Lower Body", "exercises": [
                {"name": "KAS Glute Bridge", "sets": 3, "reps": "6-8",
                 "rest": "3 min", "coaching_cue": "Full hip extension, pause at top"}
            ]}
        ]
    }
    html = generate_html(intake_data, program)
    assert "<!DOCTYPE html>" in html
    assert "Jane Doe" in html
    assert "KAS Glute Bridge" in html
    assert 'type="checkbox"' in html
    assert "Jonny Valdez" in html
    assert "Domain Athletics" in html
    # Responsive meta tag
    assert "viewport" in html

def test_html_has_tracking_checkboxes():
    intake_data = {
        "client_info": {"name": "Test"},
        "goal_timeline": {}, "training_history": {}, "schedule": {},
        "lifestyle": {}, "coach_notes": {},
    }
    program = {
        "days": [{"name": "Day 1", "exercises": [
            {"name": "Ex1", "sets": 3, "reps": "8", "rest": "2 min", "coaching_cue": "cue"},
            {"name": "Ex2", "sets": 2, "reps": "10", "rest": "2 min", "coaching_cue": "cue"},
        ]}]
    }
    html = generate_html(intake_data, program)
    assert html.count('type="checkbox"') >= 2
```

**Step 2: Run test to verify it fails**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_output_generators.py::test_generate_html_is_valid -v`
Expected: FAIL — generate_html not found

**Step 3: Write the HTML generator**

Add `generate_html(intake_data, program)` to `output_generators.py`:
- Full standalone HTML document (no external CSS/JS)
- Embedded CSS with dark/neutral theme:
  - Dark background (#1a1a2e or similar), light text
  - Clean sans-serif font
  - Responsive tables
  - Styled checkboxes
- Header: "Jonny Valdez Coaching" + client name
- Client summary card (key stats)
- Each training day as a styled table:
  - Checkbox column for tracking
  - Exercise | Sets | Reps | Rest | Notes columns
  - Notes field below each table (textarea) for logging weights
- Footer: "Domain Athletics — 102 Stanton Ct, Folsom"
- Mobile-responsive (viewport meta, fluid widths)
- Optional: localStorage JS snippet to persist checkbox state between sessions

**Step 4: Run tests to verify they pass**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/test_output_generators.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add output_generators.py tests/test_output_generators.py
git commit -m "feat: add HTML output with tracking checkboxes and dark theme"
```

---

### Task 6: Main Entry Point — intake.py

**Files:**
- Create: `intake.py`
- Create: `clients/` directory

**Step 1: Write intake.py**

Wire everything together:

```python
#!/usr/bin/env python3
"""Jonny Valdez Coaching — Client Intake System"""

import os
from intake_questions import run_intake
from program_generator import generate_program
from output_generators import generate_markdown, generate_html

def main():
    print("\n" + "=" * 50)
    print("  JONNY VALDEZ COACHING")
    print("  Domain Athletics — Folsom, CA")
    print("  New Client Intake")
    print("=" * 50 + "\n")

    # Run intake
    intake_data = run_intake()

    # Generate program
    print("\nGenerating program based on your coaching framework...")
    program = generate_program(intake_data)

    # Create output directory
    os.makedirs("clients", exist_ok=True)

    # Generate filename from client name
    name = intake_data["client_info"]["name"]
    filename = name.lower().replace(" ", "_")

    # Write markdown
    md = generate_markdown(intake_data, program)
    md_path = os.path.join("clients", f"{filename}.md")
    with open(md_path, "w") as f:
        f.write(md)
    print(f"  Coach reference saved: {md_path}")

    # Write HTML
    html = generate_html(intake_data, program)
    html_path = os.path.join("clients", f"{filename}.html")
    with open(html_path, "w") as f:
        f.write(html)
    print(f"  Client program saved: {html_path}")

    print(f"\nDone! Program generated for {name}.")
    print(f"Open {html_path} in a browser to view the trackable program.\n")

if __name__ == "__main__":
    main()
```

**Step 2: Create clients directory**

Run: `mkdir -p "/Users/jonnyvaldez/Claude Code/Gym Things/clients"`

**Step 3: Run full test suite**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 -m pytest tests/ -v`
Expected: All PASS

**Step 4: Manual smoke test**

Run: `cd "/Users/jonnyvaldez/Claude Code/Gym Things" && python3 intake.py`
Walk through with sample data to verify end-to-end flow.

**Step 5: Commit**

```bash
git add intake.py clients/.gitkeep
git commit -m "feat: add main intake.py entry point, complete intake system"
```

---

### Task 7: Girlfriend Test Run

**Files:**
- Creates: `clients/[girlfriend_name].md`
- Creates: `clients/[girlfriend_name].html`

**Step 1: Run the intake with her data**

Use the info Jonny provided:
- 25 years old, ~5'1"-5'2", 165-175 lbs, goal: lose ~10 lbs / body recomp
- Wants to feel strong, not skinny or weak
- Intermediate experience (currently running 5-day template program)
- Enjoys: T-bar row, hip thrust, glute bridge, goblet squat, shoulder press, incline press
- Tolerates: lunges (quads), Bulgarian split squats (occasional)
- 3 days/week coached, open to homework
- Desk job, 40 hrs/week, meal preps
- Current program is way too much volume (75 sets/week across 5 days)

**Step 2: Review generated program**

Verify it aligns with Jonny's framework:
- ~10-14 sets per coached session (not 75/week)
- Proper session structure (compound → accessory → finisher)
- Her preferred exercises prioritized
- Controlled volume, quality > quantity

**Step 3: Show Jonny the output for review and tweaks**

**Step 4: Commit the client files**

```bash
git add clients/
git commit -m "feat: first client program generated via intake system"
```
