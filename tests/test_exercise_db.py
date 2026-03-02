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
