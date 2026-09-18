def calculate_risk(image_condition, rainfall, history):

    image_scores = {
        "Clear Flow": 0,
        "Organic Debris": 15,
        "Mud & Sediment": 20,
        "Solid Waste / Plastic": 25,
        "Standing Water": 30,
        "Heavy Visible Occlusion": 40
    }

    rainfall_scores = {
        "Low/Nil": 0,
        "Moderate": 10,
        "Heavy": 20,
        "Very Heavy": 30
    }

    history_scores = {
        "None": 0,
        "Occasional": 15,
        "Frequent Recurring": 30
    }

    visual_score = image_scores.get(image_condition, 0)
    rainfall_score = rainfall_scores.get(rainfall, 0)
    history_score = history_scores.get(history, 0)

    total_score = visual_score + rainfall_score + history_score

    if total_score <= 30:
        priority = "LOW"
    elif total_score <= 60:
        priority = "MEDIUM"
    else:
        priority = "HIGH"

    return {
        "visual_score": visual_score,
        "rainfall_score": rainfall_score,
        "history_score": history_score,
        "total_score": total_score,
        "priority": priority
    }
