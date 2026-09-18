import os


KNOWLEDGE_BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "knowledge_base")
)


def retrieve_guidance_context(condition, priority):
    """Retrieve relevant municipal guidance from local text and Markdown files."""
    context_docs = []
    search_terms = [condition.lower(), priority.lower()]

    if os.path.isdir(KNOWLEDGE_BASE_DIR):
        for filename in sorted(os.listdir(KNOWLEDGE_BASE_DIR)):
            if not filename.lower().endswith((".txt", ".md")):
                continue
            filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            if any(term in content.lower() for term in search_terms):
                context_docs.append(content)

    if not context_docs:
        context_docs.append(
            "Municipal Stormwater SOP: Confirm grate and curb opening clearance. "
            "Remove silt, sediment, and organic buildup within a 3-meter perimeter. "
            "If standing water is observed, inspect downstream outfall and culvert "
            "connectivity. Wear appropriate PPE and log clearance verification with "
            "a timestamped photo."
        )

    return "\n---\n".join(context_docs)


def _offline_guidance(condition, rainfall, history, priority, score):
    condition_guidance = {
        "Clear Flow": [
            "Confirm water is entering and leaving the inlet without pooling.",
            "Check the grate, curb opening, and nearby channel for early debris buildup.",
            "Record the clear-flow condition with a timestamped photo for routine monitoring.",
        ],
        "Organic Debris": [
            "Remove leaves, branches, and organic buildup from the grate and inlet perimeter.",
            "Check whether wet debris is restricting the opening or being carried downstream.",
            "Bag removed material and recheck flow after clearing the accessible surface area.",
        ],
        "Mud & Sediment": [
            "Inspect sediment depth at the grate and along the first accessible channel section.",
            "Clear accessible silt with appropriate tools and PPE; do not enter the drain.",
            "Check whether sediment is being deposited again from an upstream erosion source.",
        ],
        "Solid Waste / Plastic": [
            "Remove accessible plastic and solid waste using gloves and appropriate PPE.",
            "Inspect the grate bars and curb opening for lodged material that restricts flow.",
            "Document the waste type and location so recurring dumping can be reported.",
        ],
        "Standing Water": [
            "Check grate clearance and look for visible sediment or debris around the inlet.",
            "Inspect the downstream outlet or channel for flow restriction without entering it.",
            "Record water depth and duration if known, then escalate recurring ponding for field review.",
        ],
        "Heavy Visible Occlusion": [
            "Treat the location as a priority field inspection and keep people away from unsafe areas.",
            "Clear only loose, accessible obstruction with appropriate PPE; do not force material underground.",
            "Check upstream runoff and downstream discharge after safe surface clearance.",
        ],
    }
    rainfall_tip = {
        "Low/Nil": "Schedule follow-up during the next rainfall event to confirm drainage performance.",
        "Moderate": "Recheck flow during rainfall and note whether the opening handles incoming runoff.",
        "Heavy": "Prioritize verification while conditions are safe and monitor nearby pooling or overflow.",
        "Very Heavy": "Use high caution during inspection; keep clear of fast flow and postpone entry into flooded areas.",
    }.get(rainfall, "Confirm drainage performance under representative rainfall conditions.")
    history_tip = {
        "None": "No reported waterlogging history; retain the inspection record for future comparison.",
        "Occasional": "Compare this condition with previous reports and look for a repeat location pattern.",
        "Frequent Recurring": "Escalate recurring waterlogging for a broader catchment and downstream capacity review.",
    }.get(history, "Review available maintenance and waterlogging records.")

    lines = [
        f"**Assessment:** {condition} | **Priority:** {priority} ({score}/100)",
        "",
        "**Condition-specific maintenance**",
        *[f"- {tip}" for tip in condition_guidance.get(condition, ["Verify the visible condition in the field."])],
        "",
        "**Weather and history checks**",
        f"- {rainfall_tip}",
        f"- {history_tip}",
        "",
        "**Safety and close-out**",
        "- Never enter the drain or remove a secured cover as part of this screening.",
        "- Photograph the condition before and after safe surface maintenance, and log the time and asset ID.",
        "- Physical inspection is required before ordering maintenance; this checklist does not confirm underground blockage.",
    ]
    return "\n".join(lines)


def generate_inspection_guidance(condition, rainfall, history, priority, score):
    retrieve_guidance_context(condition, priority)
    return _offline_guidance(condition, rainfall, history, priority, score)
