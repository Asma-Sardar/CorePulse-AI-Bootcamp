import json
import chromadb
from chromadb.utils import embedding_functions


def get_collection():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    client = chromadb.PersistentClient(path=os.path.join(BASE_DIR, "rag", "vectorstore"))
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_collection(
        name="corepulse_protocols",
        embedding_function=embedding_fn
    )


def build_query(readiness_score: float, workout_type: str, experience_level: int) -> str:
    if readiness_score < 40:
        readiness_label = "low readiness full rest recovery"
    elif readiness_score < 70:
        readiness_label = "moderate readiness light training"
    else:
        readiness_label = "high readiness ready to train"

    experience_map = {1: "beginner", 2: "intermediate", 3: "advanced"}
    experience_label = experience_map.get(experience_level, "intermediate")

    return f"{readiness_label} {workout_type} athlete {experience_label}"


def retrieve_protocols(
    readiness_score: float,
    workout_type: str,
    experience_level: int,
    n_results: int = 3
) -> list:
    collection = get_collection()
    query = build_query(readiness_score, workout_type, experience_level)

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    protocols = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        protocols.append({
            "title": meta["title"],
            "actions": json.loads(meta["actions"]),
            "warning": meta["warning"],
            "return_to_training": meta["return_to_training"],
            "readiness_range": meta["readiness_range"],
            "workout_type": meta["workout_type"],
            "experience_level": meta["experience_level"],
            "sources": meta.get("sources", "")
        })

    return protocols


def get_contributing_factors(
    readiness_score: float,
    avg_bpm: float,
    resting_bpm: float,
    sleep_hours: float,
    weekly_load: float,
    intensity: float,
    user_avg_sleep: float = 7.5,
    user_avg_resting_bpm: float = 65.0,
    user_avg_weekly_load: float = None
) -> list:
    factors = []

    # Sleep factor
    sleep_diff = sleep_hours - user_avg_sleep
    if sleep_diff < -1.5:
        impact = -18
        desc = f"Significant sleep deficit ({sleep_hours:.1f}h vs your avg {user_avg_sleep:.1f}h)"
    elif sleep_diff < -0.5:
        impact = -8
        desc = f"Slight sleep deficit ({sleep_hours:.1f}h vs your avg {user_avg_sleep:.1f}h)"
    elif sleep_diff > 0.5:
        impact = +8
        desc = f"Good sleep ({sleep_hours:.1f}h — above your average)"
    else:
        impact = 0
        desc = f"Normal sleep ({sleep_hours:.1f}h)"
    factors.append({"factor": "Sleep", "impact": impact, "description": desc})

    # Heart rate factor
    bpm_diff = resting_bpm - user_avg_resting_bpm
    if bpm_diff > 8:
        impact = -15
        desc = f"Elevated resting HR ({resting_bpm} BPM — {bpm_diff:.0f} above your baseline)"
    elif bpm_diff > 4:
        impact = -7
        desc = f"Slightly elevated resting HR ({resting_bpm} BPM)"
    elif bpm_diff < -4:
        impact = +8
        desc = f"Low resting HR ({resting_bpm} BPM — well recovered)"
    else:
        impact = 0
        desc = f"Normal resting HR ({resting_bpm} BPM)"
    factors.append({"factor": "Heart Rate", "impact": impact, "description": desc})

    # Intensity factor
    if intensity > 0.9:
        impact = -15
        desc = f"Very high session intensity ({intensity*100:.0f}% of max HR)"
    elif intensity > 0.8:
        impact = -8
        desc = f"High session intensity ({intensity*100:.0f}% of max HR)"
    elif intensity > 0.7:
        impact = -3
        desc = f"Moderate session intensity ({intensity*100:.0f}% of max HR)"
    else:
        impact = +5
        desc = "Low session intensity — manageable load"
    factors.append({"factor": "Session Intensity", "impact": impact, "description": desc})

    # Weekly load factor
    if user_avg_weekly_load and weekly_load > user_avg_weekly_load * 1.3:
        spike_pct = ((weekly_load / user_avg_weekly_load) - 1) * 100
        impact = -12
        desc = f"Weekly load spiked {spike_pct:.0f}% above your average"
    elif user_avg_weekly_load and weekly_load < user_avg_weekly_load * 0.7:
        impact = +6
        desc = "Weekly load is below your average — well within capacity"
    else:
        impact = 0
        desc = "Weekly training load is within your normal range"
    factors.append({"factor": "Weekly Load", "impact": impact, "description": desc})

    return factors


if __name__ == "__main__":
    # Test with sample data — no database needed
    print("=== Testing Retrieval ===\n")

    protocols = retrieve_protocols(
        readiness_score=35,
        workout_type="HIIT",
        experience_level=1
    )

    print(f"Retrieved {len(protocols)} protocols:\n")
    for p in protocols:
        print(f"Title: {p['title']}")
        print(f"Return to training: {p['return_to_training']}")
        print(f"Warning: {p['warning']}")
        print(f"Sources: {p['sources']}")
        print(f"Actions:")
        for a in p["actions"]:
            print(f"  - {a}")
        print()

    print("=== Contributing Factors ===\n")
    factors = get_contributing_factors(
        readiness_score=35,
        avg_bpm=165,
        resting_bpm=75,
        sleep_hours=5.5,
        weekly_load=12000,
        intensity=0.88,
        user_avg_sleep=7.5,
        user_avg_resting_bpm=65,
        user_avg_weekly_load=9000
    )

    for f in factors:
        sign = "+" if f["impact"] > 0 else ""
        print(f"{f['factor']}: {sign}{f['impact']} — {f['description']}")
