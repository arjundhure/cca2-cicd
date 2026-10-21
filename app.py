
import pandas as pd
import streamlit as st

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor


# -------------------- PAGE SETTINGS --------------------

st.set_page_config(
    page_title="Student Performance Study",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #f7f7f4;
        color: #202c3a;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #202c3a;
        font-weight: 600;
        letter-spacing: -0.4px;
    }

    p, label, .stMarkdown {
        color: #475467;
    }

    div[data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #e2e5e9;
        border-radius: 8px;
        padding: 1.5rem;
    }

    /* Bright blue prediction button */
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] button {
        background-color: #2563eb;
        color: #ffffff !important;
        border: 1px solid #2563eb;
        border-radius: 5px;
        padding: 0.65rem 1.2rem;
        font-weight: 600;
    }

    div.stButton > button p,
    div[data-testid="stFormSubmitButton"] button p {
        color: #ffffff !important;
    }

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #1d4ed8;
        color: #ffffff !important;
        border-color: #1d4ed8;
    }

    /* White text on a dark blue grade card */
    div[data-testid="stMetric"] {
        background-color: #263f5b;
        border: 1px solid #263f5b;
        border-radius: 8px;
        padding: 1.4rem;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] label p,
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] div,
    div[data-testid="stMetricValue"] p {
        color: #ffffff !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #ffffff !important;
    }

    hr {
        border-color: #e2e5e9;
    }

    .eyebrow {
        color: #65758b;
        text-transform: uppercase;
        font-size: 0.76rem;
        letter-spacing: 1.5px;
        font-weight: 600;
    }

    .small-note {
        font-size: 0.88rem;
        color: #667085;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- FRIENDLY LABELS --------------------

labels = {
    "school": "School",
    "sex": "Student sex",
    "age": "Age in years",
    "address": "Home location",
    "famsize": "Family size",
    "Pstatus": "Parents' living arrangement",

    "Medu": "Mother's education level (0–4)",
    "Fedu": "Father's education level (0–4)",
    "Mjob": "Mother's occupation",
    "Fjob": "Father's occupation",
    "guardian": "Main guardian",
    "famrel": "Family relationship quality (1–5)",

    "reason": "Reason for choosing school",
    "traveltime": "Travel time to school (1–4)",
    "studytime": "Weekly study time (1–4)",
    "failures": "Past class failures",
    "schoolsup": "Extra school support?",
    "famsup": "Family educational support?",
    "paid": "Extra paid classes?",
    "activities": "Extracurricular activities?",
    "nursery": "Attended nursery school?",
    "higher": "Wants higher education?",
    "internet": "Internet access at home?",
    "absences": "Number of school absences",

    "romantic": "In a romantic relationship?",
    "freetime": "Free time after school (1–5)",
    "goout": "Going out with friends (1–5)",
    "Dalc": "Workday alcohol consumption (1–5)",
    "Walc": "Weekend alcohol consumption (1–5)",
    "health": "Self-reported health (1–5)"
}


# -------------------- READABLE DROPDOWN OPTIONS --------------------

display_options = {
    "school": {
        "GP": "Gabriel Pereira (GP)",
        "MS": "Mousinho da Silveira (MS)"
    },
    "sex": {
        "F": "Female",
        "M": "Male"
    },
    "address": {
        "U": "Urban",
        "R": "Rural"
    },
    "famsize": {
        "LE3": "3 or fewer people",
        "GT3": "More than 3 people"
    },
    "Pstatus": {
        "T": "Living together",
        "A": "Living apart"
    },
    "Mjob": {
        "teacher": "Teacher",
        "health": "Health services",
        "services": "Services",
        "at_home": "At home",
        "other": "Other"
    },
    "Fjob": {
        "teacher": "Teacher",
        "health": "Health services",
        "services": "Services",
        "at_home": "At home",
        "other": "Other"
    },
    "guardian": {
        "mother": "Mother",
        "father": "Father",
        "other": "Other"
    },
    "reason": {
        "course": "Course preference",
        "home": "Close to home",
        "reputation": "School reputation",
        "other": "Other"
    },
    "schoolsup": {
        "yes": "Yes",
        "no": "No"
    },
    "famsup": {
        "yes": "Yes",
        "no": "No"
    },
    "paid": {
        "yes": "Yes",
        "no": "No"
    },
    "activities": {
        "yes": "Yes",
        "no": "No"
    },
    "nursery": {
        "yes": "Yes",
        "no": "No"
    },
    "higher": {
        "yes": "Yes",
        "no": "No"
    },
    "internet": {
        "yes": "Yes",
        "no": "No"
    },
    "romantic": {
        "yes": "Yes",
        "no": "No"
    }
}


# -------------------- HELPER TEXT --------------------

help_text = {
    "Medu": "0 = none; 1 = primary; 2 = grades 5–9; 3 = secondary; 4 = higher education.",
    "Fedu": "0 = none; 1 = primary; 2 = grades 5–9; 3 = secondary; 4 = higher education.",
    "famrel": "1 = very poor; 5 = excellent.",
    "traveltime": "1 = under 15 minutes; 2 = 15–30 minutes; 3 = 30–60 minutes; 4 = over 60 minutes.",
    "studytime": "1 = under 2 hours; 2 = 2–5 hours; 3 = 5–10 hours; 4 = over 10 hours per week.",
    "freetime": "1 = very low; 5 = very high.",
    "goout": "1 = very low; 5 = very high.",
    "Dalc": "1 = very low; 5 = very high.",
    "Walc": "1 = very low; 5 = very high.",
    "health": "1 = very poor; 5 = very good."
}


# -------------------- LOAD DATA AND TRAIN MODEL --------------------

@st.cache_resource
def prepare_model():
    data = pd.read_csv("data/student-mat.csv", sep=";")

    # Exclude G1 and G2 for early grade prediction
    X = data.drop(columns=["G1", "G2", "G3"])
    y = data["G3"]

    categorical_cols = X.select_dtypes(
        include=["object", "str"]
    ).columns.tolist()

    numerical_cols = X.select_dtypes(
        exclude=["object", "str"]
    ).columns.tolist()

    preprocessor = ColumnTransformer([
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_cols
        ),
        ("numerical", "passthrough", numerical_cols)
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=200,
            random_state=42
        ))
    ])

    model.fit(X, y)

    return data, X, model


try:
    data, X, model = prepare_model()
except FileNotFoundError:
    st.error(
        "Dataset not found. Check that data/student-mat.csv "
        "exists inside your StudentAi folder."
    )
    st.stop()


# -------------------- HEADER --------------------

st.markdown(
    '<div class="eyebrow">Academic research project</div>',
    unsafe_allow_html=True
)

st.title("Student Performance Study")

st.markdown(
    "An exploratory tool for estimating final mathematics grades "
    "from student background, study habits and school-related factors."
)

st.divider()


# -------------------- STUDENT INPUT FORM --------------------

st.subheader("Student information")

st.write(
    "Enter the available details below. The prediction is an estimate, "
    "not a guaranteed final grade."
)

sections = {
    "Personal details": [
        "school", "sex", "age", "address", "famsize", "Pstatus"
    ],
    "Family background": [
        "Medu", "Fedu", "Mjob", "Fjob", "guardian", "famrel"
    ],
    "School and study": [
        "reason", "traveltime", "studytime", "failures",
        "schoolsup", "famsup", "paid", "activities",
        "nursery", "higher", "internet", "absences"
    ],
    "Lifestyle and wellbeing": [
        "romantic", "freetime", "goout", "Dalc", "Walc", "health"
    ]
}

student = {}

with st.form("student_form"):

    for section_name, fields in sections.items():
        st.markdown(f"### {section_name}")

        left, right = st.columns(2)

        for i, field in enumerate(fields):
            container = left if i % 2 == 0 else right

            with container:
                column_data = X[field]

                if field in display_options:
                    options = sorted(
                        column_data.dropna().astype(str).unique().tolist()
                    )

                    default_value = str(column_data.mode().iloc[0])

                    default_index = (
                        options.index(default_value)
                        if default_value in options else 0
                    )

                    student[field] = st.selectbox(
                        labels[field],
                        options=options,
                        index=default_index,
                        format_func=lambda value, f=field: (
                            display_options.get(f, {}).get(value, value)
                        ),
                        help=help_text.get(field)
                    )

                else:
                    minimum = int(column_data.min())
                    maximum = int(column_data.max())
                    default_value = int(column_data.median())

                    student[field] = st.number_input(
                        labels[field],
                        min_value=minimum,
                        max_value=maximum,
                        value=default_value,
                        step=1,
                        help=help_text.get(field)
                    )

    submitted = st.form_submit_button(
        "Estimate final grade",
        use_container_width=True
    )


# -------------------- PREDICTION RESULT --------------------

if submitted:
    input_data = pd.DataFrame([student], columns=X.columns)

    prediction = float(model.predict(input_data)[0])
    prediction = max(0.0, min(20.0, prediction))

    st.divider()
    st.subheader("Prediction result")

    result_col, explanation_col = st.columns([1, 2])

    with result_col:
        st.metric(
            label="Estimated final grade",
            value=f"{prediction:.1f} / 20"
        )

    with explanation_col:
        st.markdown("#### Interpretation")

        st.write(
            "This estimate was produced by a Random Forest regression "
            "model using student background, study habits and other "
            "school-related information."
        )

        st.write(
            "The model excludes first-period and second-period grades. "
            "Because those grades can be informative, this early prediction "
            "may be less accurate."
        )

    st.caption(
        "This is a research demonstration, not an official assessment. "
        "The estimate may be inaccurate and should not be used to make "
        "important decisions about an individual student."
    )


# -------------------- ABOUT THE PROJECT --------------------

st.divider()

with st.expander("About this study"):
    st.write(
        "**Dataset:** UCI Student Performance dataset, mathematics records."
    )

    st.write(
        "**Target:** G3, the final mathematics grade on a scale from 0 to 20."
    )

    st.write("**Algorithm:** Random Forest Regressor.")

    st.write(
        "**Preprocessing:** One-hot encoding converts categorical inputs "
        "into a numerical representation that the model can use."
    )

    st.write(
        "**Early prediction:** G1 and G2 are excluded to investigate "
        "prediction before those grades are known."
    )

    st.write(
        "**Limitation:** The dataset is relatively small, and the model's "
        "predictions are estimates rather than certain outcomes."
    )

st.markdown(
    '<p class="small-note">Student Performance Study · Machine Learning Project</p>',
    unsafe_allow_html=True
)
