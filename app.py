import streamlit as st
from PIL import Image

from utils.guidance_engine import generate_inspection_guidance
from utils.risk_engine import calculate_risk


CONDITIONS = [
    "Clear Flow",
    "Organic Debris",
    "Mud & Sediment",
    "Solid Waste / Plastic",
    "Standing Water",
    "Heavy Visible Occlusion",
]

st.set_page_config(
    page_title="DrainGuard",
    page_icon="🌧️",
    layout="wide"
)

st.title("🌧️ DrainGuard")

st.subheader(
    "Drainage Risk Screening & Maintenance Prioritization System"
)

st.write(
    "A software-based decision-support prototype for screening "
    "visible drainage-condition indicators and prioritizing human inspection."
)

st.divider()

st.sidebar.header("Drainage Information")

asset_id = st.sidebar.text_input(
    "Drain Asset ID",
    value="DR-001"
)

rainfall = st.sidebar.selectbox(
    "Rainfall Condition",
    [
        "Low/Nil",
        "Moderate",
        "Heavy",
        "Very Heavy"
    ]
)

history = st.sidebar.selectbox(
    "Historical Waterlogging",
    [
        "None",
        "Occasional",
        "Frequent Recurring"
    ]
)

location_type = st.sidebar.selectbox(
    "Location Type",
    [
        "Residential",
        "Market Area",
        "Main Road",
        "School Zone",
        "Industrial Area"
    ]
)

st.header("1. Upload Drainage Image")

uploaded_file = st.file_uploader(
    "Upload a drainage photograph",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Drainage Image",
        width=500
    )

    st.divider()

    st.header("2. Manual Drainage Assessment")
    st.info("Review the uploaded image and select the most visible condition.")
    selected_condition = st.selectbox(
        "Visible Drainage Condition",
        CONDITIONS,
    )

    if st.button("🔍 Analyze Drainage Condition"):
        image_condition = selected_condition

        result = calculate_risk(image_condition, rainfall, history)

        st.subheader("Assessment Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Priority Score",
                f"{result['total_score']}/100"
            )

        with col2:
            st.metric(
                "Inspection Priority",
                result["priority"]
            )

        with col3:
            st.metric(
                "Asset",
                asset_id
            )

        st.divider()

        st.write("### Detected Visible Condition")
        st.info(image_condition)

        st.write("### Score Breakdown")
        st.write(f"Visual condition: **{result['visual_score']} points**")
        st.write(f"Rainfall context: **{result['rainfall_score']} points**")
        st.write(f"Historical waterlogging: **{result['history_score']} points**")

        st.divider()

        st.write("### Recommended Action")

        if result["priority"] == "HIGH":
            st.error(
                "Elevated inspection priority. Physical inspection is recommended to verify the "
                "visible drainage condition and downstream flow."
            )
        elif result["priority"] == "MEDIUM":
            st.warning(
                "Moderate inspection priority. Field verification should be considered based on "
                "local conditions."
            )
        else:
            st.success(
                "Low inspection priority based on the prototype screening criteria."
            )

        st.write("### Maintenance Guidance & Field Checklist")
        with st.spinner("Retrieving SOPs and generating guidance..."):
            guidance = generate_inspection_guidance(
                image_condition,
                rainfall,
                history,
                result["priority"],
                result["total_score"],
            )
        st.info(guidance)

else:
    st.info(
        "Upload a drainage image to begin the assessment."
    )

st.divider()
st.caption(
    "Prototype / Demonstration System. "
    "The priority score is a heuristic and is not a validated "
    "flood prediction model. Image analysis evaluates visible "
    "surface conditions only. Human physical inspection remains "
    "the final verification step."
)
