import math
from datetime import date, datetime, timedelta

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


MODEL_NAME = "SBI NRI Relationship Intelligence Platform"
APP_VERSION = "lho-nri-service-administration-mananchira-v2"
FOCUS_BRANCH = "SBI Mananchira Branch, Calicut"
LHO_UNIT = "LHO NRI Service Administration Department, Thiruvananthapuram"
ADMIN_ROLE = "LHO NRI Cell Administrator (Thiruvananthapuram)"


st.set_page_config(
    page_title=MODEL_NAME,
    page_icon="SBI",
    layout="wide",
    initial_sidebar_state="expanded",
)


ROLE_CONFIG = {
    ADMIN_ROLE: {
        "employee": "Aparna Rao",
        "unit": "LHO NRI Cell, Thiruvananthapuram",
        "permissions": [
            "View everything",
            "Edit everything",
            "View all customers",
            "View all scores",
            "Manage users",
            "Configure scoring model",
            "Publish model versions",
            "View audit logs",
            "Export reports",
            "View analytics dashboard",
        ],
        "modules": [
            "Executive Command Center",
            "Management Insights Center",
            "Relationship Intelligence Assessment Center",
            "Score Approval Workbench",
            "Customer 360 View",
            "Customer Reactivation Tracker",
            "Team Performance Dashboard",
            "Country Intelligence Module",
            "RM Workload Balancer",
            "Management Alert Center",
            "Scoring Methodology",
            "Platform Administration & Model Configuration",
            "PDF Report Generator",
            "Audit Trail",
            "User Administration",
        ],
    },
    "Branch Manager": {
        "employee": "Vikram Menon",
        "unit": "SBI Mananchira Branch, Calicut",
        "permissions": [
            "View branch-level customers",
            "View relationship scores",
            "View action recommendations",
            "Track reactivation progress",
            "View performance dashboards",
            "Approve branch actions",
            "Assign branch RMs and Wealth Managers",
            "Cannot change scoring methodology",
        ],
        "modules": [
            "Executive Command Center",
            "Management Insights Center",
            "Branch Operations Center",
            "Score Approval Workbench",
            "Customer 360 View",
            "Customer Reactivation Tracker",
            "Team Performance Dashboard",
            "Country Intelligence Module",
            "RM Workload Balancer",
            "Management Alert Center",
            "PDF Report Generator",
        ],
    },
    "NRI Wealth Manager": {
        "employee": "Neha Iyer",
        "unit": "SBI Mananchira Branch, Calicut",
        "permissions": [
            "View Platinum customers",
            "View High Priority / Gold Customers",
            "View deposit potential",
            "Update engagement status",
            "Add meeting notes",
            "Cannot assign relationship score",
        ],
        "modules": [
            "Management Insights Center",
            "Customer 360 View",
            "Customer Reactivation Tracker",
            "Team Performance Dashboard",
            "Country Intelligence Module",
            "PDF Report Generator",
        ],
    },
    "NRI Relationship Manager": {
        "employee": "Rahul Nair",
        "unit": "SBI Mananchira Branch, Calicut",
        "permissions": [
            "View assigned customers",
            "Update interaction records",
            "Add call outcomes",
            "Update reactivation progress",
            "Update customer feedback",
            "Cannot change relationship score",
        ],
        "modules": [
            "Customer 360 View",
            "Customer Reactivation Tracker",
            "RM Workload Balancer",
            "Management Alert Center",
            "PDF Report Generator",
        ],
    },
    "NRI Service Officer": {
        "employee": "Fatima Khan",
        "unit": "SBI Mananchira Branch, Calicut",
        "permissions": [
            "View KYC-related customers",
            "Documentation pending customers",
            "Service request customers",
            "Update service status",
            "Cannot change relationship score",
        ],
        "modules": [
            "Customer 360 View",
            "Customer Reactivation Tracker",
            "Management Alert Center",
            "PDF Report Generator",
        ],
    },
    "NRI Portfolio Analyst": {
        "employee": "Ankit Sharma",
        "unit": "LHO NRI Intelligence Cell, Thiruvananthapuram",
        "permissions": [
            "Create customer assessments",
            "Enter scoring factors",
            "Assign preliminary scores",
            "Save assessment drafts",
            "Cannot approve final score",
        ],
        "modules": [
            "Relationship Intelligence Assessment Center",
            "Customer 360 View",
            "Scoring Methodology",
        ],
    },
    "NRI Portfolio Supervisor": {
        "employee": "Meera Subramanian",
        "unit": "LHO NRI Intelligence Cell, Thiruvananthapuram",
        "permissions": [
            "Review submitted assessments",
            "Approve scores",
            "Reject scores",
            "Modify scores",
            "Finalize relationship score",
            "Publish score to SBI teams",
        ],
        "modules": [
            "Executive Command Center",
            "Relationship Intelligence Assessment Center",
            "Score Approval Workbench",
            "Customer 360 View",
            "Team Performance Dashboard",
            "Management Alert Center",
            "Scoring Methodology",
            "Audit Trail",
            "PDF Report Generator",
        ],
    },
}


BRANCHES = [
    "SBI Mananchira Branch, Calicut",
    "SBI Kannur Main Branch",
    "SBI Kochi NRI Branch",
    "SBI Malappuram Branch",
    "SBI Kozhikode Main Branch",
    "SBI Thiruvananthapuram Main Branch",
    "SBI Kollam Branch",
    "SBI Thrissur Branch",
    "SBI Palakkad Branch",
    "SBI Kottayam Branch",
    "SBI Alappuzha Branch",
    "SBI Pathanamthitta Branch",
    "SBI Kasaragod Branch",
    "SBI Ernakulam Broadway Branch",
    "SBI Vadakara Branch",
]
COUNTRIES = ["UAE", "Saudi Arabia", "Qatar", "Oman", "USA", "UK", "Kuwait", "Singapore"]
ACCOUNT_TYPES = ["NRE Savings", "NRO Savings", "NRO Current", "FCNR Deposit"]
DORMANCY_REASONS = [
    "KYC Expired",
    "Documentation Pending",
    "No Recent Remittance",
    "Service Issue",
    "Shifted to Other Bank",
    "Returned to India",
    "Closed Account",
    "No Longer Employed Abroad",
]
RISK_LEVELS = ["Low", "Medium", "High"]
REMITTANCE_LEVELS = ["High", "Medium", "Low"]
PIPELINE_STAGES = ["Scored", "Assigned", "Contacted", "Interested", "KYC Updated", "Funded", "Reactivated"]
RMS = ["Rahul Nair", "Sonia Das", "Dev Patel", "Amrita Bose", "Karthik Rao"]
WEALTH_MANAGERS = ["Neha Iyer", "Karan Sethi", "Nisha Shah", "Rohan Dutta"]


def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --sbi-blue: #163f8f;
            --sbi-cyan: #00a3c8;
            --ink: #142033;
            --muted: #64748b;
            --line: #dbe4ef;
            --page: #f5f8fc;
        }
        .stApp { background: #f5f8fc; color: #142033; }
        [data-testid="stSidebar"] { background: #10284f; }
        [data-testid="stSidebar"] * { color: white; }
        [data-testid="stSidebar"] button {
            background: #ffffff !important;
            color: #163f8f !important;
            border: 1px solid #dbe4ef !important;
            font-weight: 800 !important;
        }
        [data-testid="stSidebar"] button p {
            color: #163f8f !important;
        }
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #dbe4ef;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 12px 30px rgba(22,63,143,.07);
        }
        .login-hero {
            padding: 28px;
            border-radius: 8px;
            background: linear-gradient(135deg, #10284f, #163f8f 55%, #007fa5);
            color: white;
            margin-bottom: 18px;
        }
        .login-hero h1 {
            margin: 0 0 10px;
            font-size: 38px;
            letter-spacing: 0;
            line-height: 1.08;
        }
        .login-hero p { color: rgba(255,255,255,.86); font-size: 16px; line-height: 1.55; }
        .brand-row {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }
        .sbi-logo {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: #1d68d8;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 24px rgba(0,0,0,.18);
            position: relative;
            flex: 0 0 auto;
        }
        .sbi-logo:before {
            content: "";
            width: 16px;
            height: 16px;
            background: white;
            border-radius: 50%;
            position: absolute;
            top: 17px;
            left: 16px;
        }
        .sbi-logo:after {
            content: "";
            width: 12px;
            height: 22px;
            background: white;
            border-radius: 0;
            position: absolute;
            bottom: 0;
            left: 18px;
        }
        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        .sidebar-brand .sbi-logo {
            width: 36px;
            height: 36px;
            box-shadow: none;
        }
        .sidebar-brand .sbi-logo:before { width: 12px; height: 12px; top: 13px; left: 12px; }
        .sidebar-brand .sbi-logo:after { width: 8px; height: 17px; left: 14px; }
        .role-card, .info-card, .alert-card, .report-card {
            background: #ffffff;
            border: 1px solid #dbe4ef;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 12px 30px rgba(22,63,143,.07);
            margin-bottom: 12px;
        }
        .role-card h3, .info-card h3, .alert-card h3 { margin-top: 0; }
        .badge {
            display: inline-block;
            padding: 5px 9px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            color: #163f8f;
            background: #eaf3ff;
            margin: 2px 4px 2px 0;
        }
        .badge-red { color: #bd2f2f; background: #fff0f0; }
        .badge-green { color: #177245; background: #eaf8f0; }
        .badge-amber { color: #9a6417; background: #fff5df; }
        .badge-purple { color: #6851a5; background: #f1ecff; }
        .section-title {
            padding: 4px 0 14px;
        }
        .section-title h2 { margin-bottom: 2px; }
        .section-title p { color: #64748b; margin-top: 0; }
        .pipeline-grid {
            display: grid;
            grid-template-columns: repeat(7, minmax(100px, 1fr));
            gap: 10px;
        }
        .pipe-step {
            border-top: 4px solid #0b63b6;
            background: white;
            border-radius: 8px;
            border-left: 1px solid #dbe4ef;
            border-right: 1px solid #dbe4ef;
            border-bottom: 1px solid #dbe4ef;
            padding: 14px;
        }
        .pipe-step b { font-size: 26px; display: block; }
        .pipe-step span { color: #64748b; font-weight: 800; font-size: 12px; }
        .small-muted { color: #64748b; font-size: 13px; }
        .big-score {
            background: linear-gradient(140deg, #163f8f, #0b63b6);
            color: white;
            border-radius: 8px;
            text-align: center;
            padding: 24px;
        }
        .big-score b { display: block; font-size: 54px; }
        .timeline-row {
            border-left: 4px solid #cfe7f4;
            padding: 4px 0 12px 14px;
            margin-bottom: 8px;
        }
        .last-updated {
            color: #64748b;
            font-size: 12px;
            text-align: right;
            margin-top: -12px;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .notification-card {
            background: #ffffff;
            border: 1px solid #dbe4ef;
            border-left: 4px solid #00a3c8;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            box-shadow: 0 8px 22px rgba(22,63,143,.06);
        }
        .notification-card b { color: #163f8f; }
        [data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 6px;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label {
            align-items: center;
            background: rgba(255,255,255,.08) !important;
            border: 1px solid rgba(219,228,239,.20) !important;
            border-radius: 6px;
            padding: 8px 10px;
            margin: 4px 0;
            width: 100%;
            transition: background .15s ease, border-color .15s ease, box-shadow .15s ease;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(255,255,255,.14) !important;
            border-color: rgba(0,163,200,.70) !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background: #f8fbff !important;
            border-color: #00a3c8 !important;
            box-shadow: inset 3px 0 0 #00a3c8, 0 6px 18px rgba(0,0,0,.16);
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label span,
        [data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: #eef6ff !important;
            font-weight: 700;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span,
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
            color: #10284f !important;
        }
        [data-testid="stSidebar"] input[type="radio"] {
            accent-color: #00a3c8 !important;
        }
        @media (max-width: 900px) {
            .pipeline-grid { grid-template-columns: repeat(2, minmax(100px, 1fr)); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def money(value):
    value = float(value)
    if abs(value) >= 10_000_000:
        return f"₹{value / 10_000_000:.2f} Cr"
    return f"₹{value / 100_000:.1f} L"


def is_lho_admin():
    return st.session_state.role == ADMIN_ROLE


def is_branch_manager():
    return st.session_state.role == "Branch Manager"


def branch_scope():
    return st.session_state.selected_branch


def priority_from_segment(segment):
    mapping = {
        "Platinum Customers": "P1",
        "High Priority / Gold Customers": "P2",
        "Moderate Priority / Silver Customers": "P3",
        "Low Priority / Bronze Customers": "P4",
    }
    return mapping.get(segment, "P4")


def priority_level_from_score(score):
    return priority_from_segment(segment_from_score(score))


def last_updated_stamp():
    st.markdown(
        f'<div class="last-updated">Last updated: {datetime.now().strftime("%d %b %Y, %I:%M %p")}</div>',
        unsafe_allow_html=True,
    )


def sbi_brand_html(compact=False):
    class_name = "sidebar-brand" if compact else "brand-row"
    return f'<div class="{class_name}"><div class="sbi-logo"></div><div><b>State Bank of India</b></div></div>'

def score_breakdown(row):
    balance = row["Average Balance"]
    remittance_text = row["Historical Remittance Activity"]
    products = row["Number of SBI Products"]
    duration = row["Relationship Duration"]
    dormancy = row["Dormancy Reason"]

    balance_score = 100 if balance >= 2_500_000 else 85 if balance >= 1_500_000 else 70 if balance >= 800_000 else 48 if balance >= 400_000 else 30
    remittance_score = {"High": 100, "Medium": 70, "Low": 42}.get(remittance_text, 42)
    product_score = min(100, products * 15)
    if "KYC" in dormancy:
        dormancy_score = 88
    elif "Documentation" in dormancy:
        dormancy_score = 78
    elif "No Recent" in dormancy:
        dormancy_score = 65
    elif "Service" in dormancy:
        dormancy_score = 58
    elif "Shifted" in dormancy:
        dormancy_score = 35
    else:
        dormancy_score = 30
    duration_score = 100 if duration >= 12 else 84 if duration >= 8 else 68 if duration >= 5 else 45
    relationship_score = round(
        balance_score * 0.40
        + remittance_score * 0.25
        + dormancy_score * 0.15
        + product_score * 0.15
        + duration_score * 0.05
    )
    return {
        "Balance Score": balance_score,
        "Remittance Score": remittance_score,
        "Product Score": product_score,
        "Dormancy Score": dormancy_score,
        "Relationship Duration Score": duration_score,
        "Relationship Intelligence Score": relationship_score,
    }


def reactivation_probability(row):
    score = score_breakdown(row)["Relationship Intelligence Score"]
    probability = score / 100
    if row["Customer Risk Level"] == "High":
        probability -= 0.25
    elif row["Customer Risk Level"] == "Medium":
        probability -= 0.10
    if row["Dormancy Reason"] in ["KYC Expired", "Documentation Pending"]:
        probability += 0.08
    if row.get("Rejection Reason", "None") != "None":
        probability -= 0.14
    return max(0.18, min(0.90, probability))


def expected_recovery(row):
    return round(row["Expected Deposit Potential"] * reactivation_probability(row))


def segment_from_score(score):
    if score >= 80:
        return "Platinum Customers"
    if score >= 60:
        return "High Priority / Gold Customers"
    if score >= 40:
        return "Moderate Priority / Silver Customers"
    return "Low Priority / Bronze Customers"


def recommendations(row):
    recs = []
    if row["Segment"] == "Platinum Customers":
        recs.append("Assign Wealth Manager")
    if row["KYC Status"] != "Valid":
        recs.append("KYC Re-engagement Campaign")
    if row["Number of SBI Products"] >= 4:
        recs.append("Investment Product Discussion")
    if row["Expected Deposit Potential"] >= 2_000_000:
        recs.append("Premium NRI Banking Offer")
    if row["Dormancy Reason"] == "Documentation Pending":
        recs.append("Documentation Assistance Program")
    if row["Priority Level"] == "P1":
        recs.append("Priority Reactivation Campaign")
    return recs or ["Dedicated Relationship Manager Follow-up"]


@st.cache_data
def build_sample_customers():
    first_names = [
        "Arjun", "Priya", "Mohammed", "Rhea", "Sanjay", "Aisha", "George", "Irfan", "Maya", "Karthik",
        "Sara", "Biju", "Nikhil", "Ananya", "Sameer", "Divya", "Joseph", "Farhan", "Meera", "Rohan",
        "Lina", "Ajay", "Nadia", "Pranav", "Sofia", "Hari", "Zara", "Manoj", "Leena", "Kabir",
        "Nisha", "Thomas", "Amit", "Pooja", "Rehan", "Sneha", "Alan", "Veena", "Imran", "Tara",
        "Varun", "Fathima", "Joel", "Meghna", "Adil", "Ritu", "Dinesh", "Hema", "Yusuf", "Lakshmi",
    ]
    last_names = [
        "Krishnan", "Raman", "Haneef", "Mathew", "Pillai", "Thomas", "Varghese", "Ali", "Nambiar", "Balan",
        "Joseph", "Antony", "Menon", "Iyer", "Kapoor", "Nair", "D'Souza", "Khan", "Rao", "Sethi",
        "Shah", "Das", "Mirza", "Reddy", "Fernandes", "Patel", "Rahman", "Kulkarni", "Bose", "Shetty",
        "Mohan", "Chacko", "Malik", "Verma", "Ansari", "Gopal", "Mathew", "Prasad", "Qureshi", "Sen",
        "Bhat", "Hussain", "Paul", "Naidu", "Syed", "Raj", "Kumar", "Menon", "Shaikh", "Warrier",
    ]
    rows = []
    for i in range(50):
        country = COUNTRIES[i % len(COUNTRIES)]
        branch = FOCUS_BRANCH
        remittance = REMITTANCE_LEVELS[(i + (i // 4)) % 3]
        risk = RISK_LEVELS[(i * 2 + 1) % 3]
        dormancy = DORMANCY_REASONS[(i * 5 + 2) % len(DORMANCY_REASONS)]
        account_type = ACCOUNT_TYPES[(i * 7) % len(ACCOUNT_TYPES)]
        products = 1 + ((i * 2) % 7)
        duration = 2 + ((i * 3) % 18)
        balance = 250_000 + ((i * 173_000) % 4_400_000)
        if i in [0, 6, 10, 17, 25, 31, 42]:
            balance += 1_100_000
            remittance = "High"
            risk = "Low"
        if i in [7, 14, 22, 29, 36, 43]:
            balance = 120_000 + (i % 3) * 35_000
            remittance = "Low"
            products = 1
            duration = 2
            dormancy = "Closed Account"
            risk = "High"
        potential = int(balance * (1.25 + ((i % 6) * 0.14)) + 250_000)
        kyc = "Expired" if "KYC" in dormancy else "Pending" if "Documentation" in dormancy or i % 9 == 0 else "Valid"
        stage = PIPELINE_STAGES[(i * 2) % len(PIPELINE_STAGES)]
        rejection_reason = "None"
        if dormancy == "Shifted to Other Bank":
            rejection_reason = "Shifted to competitor bank"
        elif dormancy == "Returned to India":
            rejection_reason = "Returned to India"
        elif dormancy == "Closed Account":
            rejection_reason = "Closed account"
        elif dormancy == "No Longer Employed Abroad":
            rejection_reason = "No longer employed abroad"
        elif dormancy == "Service Issue" and i % 2 == 0:
            rejection_reason = "Poor service experience"
        customer = {
            "Customer ID": f"NRI-{1001 + i}",
            "Customer Name": f"{first_names[i]} {last_names[i]}",
            "Country": country,
            "Branch": branch,
            "Account Type": account_type,
            "Average Balance": balance,
            "Historical Remittance Activity": remittance,
            "Number of SBI Products": products,
            "Relationship Duration": duration,
            "Dormancy Reason": dormancy,
            "KYC Status": kyc,
            "Expected Deposit Potential": potential,
            "Customer Risk Level": risk,
            "Additional Analyst Comments": "Relationship shows measurable NRI recovery potential based on banking behavior.",
            "Relationship Notes": "Prior balances, product holdings and remittance patterns indicate targeted engagement value.",
            "Special Circumstances": "Coordinate outreach with time zone and documentation requirements.",
            "Segment": "Pending Score Segment",
            "Assigned RM": RMS[i % len(RMS)],
            "Assigned Wealth Manager": WEALTH_MANAGERS[i % len(WEALTH_MANAGERS)],
            "Pipeline Stage": stage,
            "Call Status": "Completed" if stage in ["Contacted", "Interested", "KYC Updated", "Funded", "Reactivated"] else "Pending",
            "Email Sent": "Yes" if i % 3 != 0 else "No",
            "Meeting Conducted": "Yes" if stage in ["Interested", "Funded", "Reactivated"] else "No",
            "Customer Interested": "Yes" if stage in ["Interested", "KYC Updated", "Funded", "Reactivated"] else "Undecided",
            "KYC Completed": "Yes" if stage in ["KYC Updated", "Funded", "Reactivated"] else "No",
            "Funds Added": "Yes" if stage in ["Funded", "Reactivated"] else "No",
            "Account Reactivated": "Yes" if stage == "Reactivated" else "No",
            "Actual Deposit Amount": int(potential * (0.55 if stage in ["Funded", "Reactivated"] else 0)),
            "Follow-up Date": date.today() + timedelta(days=(i % 14) - 3),
            "Follow-up Type": ["Call", "Email", "WhatsApp", "Video Meeting"][i % 4],
            "Follow-up Status": ["Pending", "Completed", "Missed"][i % 3],
            "Rejection Reason": rejection_reason,
            "Last Contact Days": (i * 7) % 61,
        }
        scores = score_breakdown(customer)
        customer.update(scores)
        customer["Segment"] = segment_from_score(scores["Relationship Intelligence Score"])
        customer["Reactivation Probability"] = reactivation_probability(customer)
        customer["Expected Deposit Recovery"] = expected_recovery(customer)
        customer["Priority Level"] = priority_level_from_score(scores["Relationship Intelligence Score"])
        customer["Recommended Action"] = recommendations(customer)[0]
        rows.append(customer)
    return pd.DataFrame(rows)


def init_state():
    if st.session_state.get("app_version") != APP_VERSION:
        st.session_state.clear()
        st.session_state.app_version = APP_VERSION
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = ADMIN_ROLE
    if "selected_branch" not in st.session_state:
        st.session_state.selected_branch = FOCUS_BRANCH
    if "customers" not in st.session_state:
        st.session_state.customers = build_sample_customers()
    if "assessments" not in st.session_state:
        st.session_state.assessments = seed_assessments(st.session_state.customers)
    if "audit_logs" not in st.session_state:
        st.session_state.audit_logs = seed_audit_logs()
    if "selected_customer_id" not in st.session_state:
        st.session_state.selected_customer_id = st.session_state.customers.iloc[0]["Customer ID"]
    if "model_factors" not in st.session_state:
        st.session_state.model_factors = pd.DataFrame(
            [
                ["Account Balance", 40, True],
                ["Historical Remittance Activity", 25, True],
                ["Dormancy Reason", 15, True],
                ["Number of SBI Products", 15, True],
                ["Relationship Duration", 5, True],
            ],
            columns=["Factor", "Weightage", "Enabled"],
        )
    if "segments" not in st.session_state:
        st.session_state.segments = pd.DataFrame(
            [
                ["Platinum Customers", 80, 100],
                ["High Priority / Gold Customers", 60, 79],
                ["Moderate Priority / Silver Customers", 40, 59],
                ["Low Priority / Bronze Customers", 0, 39],
            ],
            columns=["Segment", "Minimum Score", "Maximum Score"],
        )
    if "priorities" not in st.session_state:
        st.session_state.priorities = pd.DataFrame(
            [["P1", 80, 100], ["P2", 60, 79], ["P3", 40, 59], ["P4", 0, 39]],
            columns=["Priority", "Minimum Score", "Maximum Score"],
        )
    if "model_versions" not in st.session_state:
        st.session_state.model_versions = pd.DataFrame(
            [
                ["RIS-2.0", "Aparna Rao", "2026-06-18", "Current"],
                ["RIS-1.9", "Meera Subramanian", "2026-05-24", "Archived"],
                ["RIS-1.8", "Aparna Rao", "2026-05-01", "Archived"],
            ],
            columns=["Current Version", "Published By", "Published Date", "Status"],
        )


def seed_assessments(df):
    rows = []
    statuses = ["Published", "Approved", "Pending Review", "Draft", "Rejected"]
    assessors = ["Ankit Sharma", "Ravi Kumar", "Isha Verma", "Ankit Sharma", "Ravi Kumar"]
    for i, row in df.head(18).iterrows():
        rows.append(
            {
                "Assessment ID": f"AST-{9001 + i}",
                "Customer ID": row["Customer ID"],
                "Assessor Name": assessors[i % len(assessors)],
                "Reviewer Name": "Meera Subramanian" if statuses[i % len(statuses)] != "Draft" else "-",
                "Assessment Date": str(date.today() - timedelta(days=18 - i)),
                "Score": int(row["Relationship Intelligence Score"]),
                "Status": statuses[i % len(statuses)],
                "Comments": "Assessment created through Relationship Intelligence workflow.",
            }
        )
    return pd.DataFrame(rows)


def seed_audit_logs():
    return pd.DataFrame(
        [
            ["AUD-701", "Ankit Sharma", "NRI Portfolio Analyst", "LHO NRI Intelligence Cell, Thiruvananthapuram", "Created preliminary score", "NRI-1001", "-", 89, "New assessment submitted", "2026-05-21 10:20"],
            ["AUD-702", "Meera Subramanian", "NRI Portfolio Supervisor", "LHO NRI Intelligence Cell, Thiruvananthapuram", "Approved score", "NRI-1001", 84, 89, "KYC issue with strong deposit potential", "2026-05-21 10:35"],
            ["AUD-703", "Meera Subramanian", "NRI Portfolio Supervisor", "LHO NRI Intelligence Cell, Thiruvananthapuram", "Modified score", "NRI-1003", 82, 76, "Competitor shift lowers feasibility", "2026-05-23 11:24"],
            ["AUD-704", "Aparna Rao", ADMIN_ROLE, "LHO NRI Cell, Thiruvananthapuram", "Published score", "NRI-1007", 93, 93, "Published to SBI teams", "2026-05-24 15:10"],
        ],
        columns=["Audit ID", "Employee Name", "Role", "Branch", "Action", "Customer ID", "Old Value", "New Value", "Reason", "Date and Time"],
    )


def section(title, subtitle):
    st.markdown(
        f"""
        <div class="section-title">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(text, tone=""):
    class_name = f"badge {tone}".strip()
    return f'<span class="{class_name}">{text}</span>'


def visible_customers():
    df = st.session_state.customers.copy()
    if is_branch_manager():
        df = df[df["Branch"] == branch_scope()]
    return df


def login_page():
    hero_html = (
        f'<div class="login-hero">{sbi_brand_html()}'
        f"<h1>{MODEL_NAME}</h1>"
        "<p>Internal SBI workflow platform for dormant NRI relationship scoring, score governance, reactivation tracking, deposit recovery analytics and executive decision support.</p>"
        "<p><b>Segment criteria:</b> 100-80 Platinum Customers | 79-60 High Priority / Gold Customers | 59-40 Moderate Priority / Silver Customers | Below 40 Low Priority / Bronze Customers</p>"
        "</div>"
    )
    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )
    left, center, right = st.columns([0.7, 1.1, 0.7], gap="large")
    with center:
        st.subheader("Employee Login Access")
        role = st.selectbox("Employee Role", list(ROLE_CONFIG.keys()), index=list(ROLE_CONFIG.keys()).index(st.session_state.role))
        st.session_state.role = role
        branch = st.selectbox("Branch name", BRANCHES, index=BRANCHES.index(st.session_state.selected_branch))
        st.session_state.selected_branch = branch
        st.text_input("Employee Access ID", value=f"SBI-NRI-{role.upper().replace(' ', '-')}-001")
        st.text_input("Password", value="prototype-access", type="password")
        if st.button("Enter Platform", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()

def sidebar():
    role = st.session_state.role
    config = ROLE_CONFIG[role]
    st.sidebar.markdown(sbi_brand_html(compact=True), unsafe_allow_html=True)
    st.sidebar.markdown(f"## {MODEL_NAME}")
    st.sidebar.markdown("**LHO NRI Service Administration, Thiruvananthapuram**")
    st.sidebar.markdown(f"**Branch Name:**  \n{st.session_state.selected_branch}")
    st.sidebar.markdown(f"**{config['employee']}**  \n{role}  \n{config['unit']}")
    st.sidebar.divider()
    module = st.sidebar.radio("Modules", config["modules"])
    st.sidebar.divider()
    st.sidebar.markdown("**Permissions**")
    for permission in config["permissions"]:
        st.sidebar.markdown(f"- {permission}")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    return module


def kpi_row(df):
    total_recovery = df["Expected Deposit Recovery"].sum()
    total_potential = df["Expected Deposit Potential"].sum()
    avg_score = round(df["Relationship Intelligence Score"].mean())
    cols = st.columns(4)
    cols[0].metric("Total Dormant Accounts", f"{len(df):,}", "Portfolio under scoring")
    cols[1].metric("Potential Deposit Recovery", money(total_potential), "Gross opportunity")
    cols[2].metric("Expected Deposit Recovery", money(total_recovery), "Probability adjusted")
    cols[3].metric("Average Relationship Score", avg_score, "Portfolio average")
    cols = st.columns(4)
    cols[0].metric("Platinum Customers", int((df["Segment"] == "Platinum Customers").sum()), "Score 80 to 100")
    cols[1].metric("Pending Assessment", int((st.session_state.assessments["Status"] == "Draft").sum()), "Draft queue")
    cols[2].metric("Pending Approval", int((st.session_state.assessments["Status"] == "Pending Review").sum()), "Leader review")
    cols[3].metric("Reactivated Customers", int((df["Account Reactivated"] == "Yes").sum()), "Recovered accounts")


def notification_panel():
    assessments = st.session_state.assessments.copy()
    pending = assessments[assessments["Status"] == "Pending Review"]
    drafts = assessments[assessments["Status"] == "Draft"]
    recent = assessments.head(3)
    with st.expander("Notifications - New Assessments & Pending Approvals", expanded=False):
        c1, c2, c3 = st.columns(3)
        c1.metric("Pending Approvals", len(pending))
        c2.metric("Draft Assessments", len(drafts))
        c3.metric("New Assessment Alerts", len(recent))
        if pending.empty:
            st.success("No pending approvals waiting right now.")
        else:
            for _, row in pending.head(5).iterrows():
                st.markdown(
                    f"""
                    <div class="notification-card">
                        <b>{row['Assessment ID']}</b> requires approval for {row['Customer ID']}<br>
                        <span class="small-muted">Submitted by {row['Assessor Name']} on {row['Assessment Date']} | Score {row['Score']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def bar_chart(df, x, y, title, color="#163f8f", width=460, height=250):
    label_angle = -40 if len(df) > 2 else 0
    bars = (
        alt.Chart(df)
        .mark_bar(color=color, cornerRadiusTopLeft=3, cornerRadiusTopRight=3, size=28)
        .encode(
            x=alt.X(
                x,
                sort="-y",
                axis=alt.Axis(
                    labelAngle=label_angle,
                    labelAlign="right" if label_angle else "center",
                    labelBaseline="middle" if label_angle else "top",
                    labelLimit=240,
                    labelOverlap=False,
                    labelPadding=10,
                ),
            ),
            y=alt.Y(y, axis=alt.Axis(labelLimit=120)),
            tooltip=list(df.columns),
        )
    )
    labels = (
        alt.Chart(df)
        .mark_text(dy=-6, color="#142033", fontSize=11)
        .encode(
            x=alt.X(x, sort="-y"),
            y=alt.Y(y),
            text=alt.Text(y, format=".2s"),
        )
    )
    chart = (bars + labels).properties(width=width, height=height, title=title).configure_view(strokeWidth=0)
    st.altair_chart(chart, use_container_width=False)


def pie_chart(df, names, values, title, color_domain=None, color_range=None):
    palette = color_range or ["#163f8f", "#00a3c8", "#177245", "#b7791f", "#6851a5", "#bd2f2f", "#52677f"]
    color_scale = alt.Scale(domain=color_domain, range=palette) if color_domain else alt.Scale(range=palette)
    chart = (
        alt.Chart(df)
        .mark_arc(innerRadius=60)
        .encode(
            theta=alt.Theta(values, type="quantitative"),
            color=alt.Color(names, scale=color_scale, legend=alt.Legend(orient="right")),
            tooltip=[names, values],
        )
        .properties(width=420, height=280, title=title)
    )
    st.altair_chart(chart, use_container_width=False)


def pipeline_view(df):
    counts = df["Pipeline Stage"].value_counts().to_dict()
    html = '<div class="pipeline-grid">'
    for stage in PIPELINE_STAGES:
        html += f'<div class="pipe-step"><b>{counts.get(stage, 0)}</b><span>{stage}</span></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def opportunity_table(df, limit=10):
    view = (
        df.sort_values(["Priority Level", "Expected Deposit Recovery"], ascending=[True, False])
        .head(limit)[
            [
                "Customer ID",
                "Customer Name",
                "Country",
                "Segment",
                "Relationship Intelligence Score",
                "Priority Level",
                "Expected Deposit Recovery",
                "Recommended Action",
            ]
        ]
        .copy()
    )
    view["Expected Deposit Recovery"] = view["Expected Deposit Recovery"].map(money)
    st.dataframe(view, use_container_width=True, hide_index=True)


def executive_command_center():
    df = visible_customers()
    section("NRI Service Administration Center", "Premium operating view for the Mananchira branch dormant NRI portfolio, reactivation pipeline, pending governance and top opportunities.")
    last_updated_stamp()
    notification_panel()
    kpi_row(df)
    st.subheader("Reactivation Pipeline")
    pipeline_view(df)
    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        st.subheader("NRI Opportunity Radar")
        opportunity_table(df, 10)
    with right:
        country = df.groupby("Country", as_index=False)["Expected Deposit Recovery"].sum()
        bar_chart(country, "Country", "Expected Deposit Recovery", "Country Expected Recovery", "#163f8f")
    left, right = st.columns(2, gap="large")
    with left:
        branch = df.groupby("Branch", as_index=False)["Expected Deposit Recovery"].sum()
        st.markdown("**Branch Recovery Opportunity**")
        bar_chart(branch, "Branch", "Expected Deposit Recovery", "", "#00a3c8", height=270)
    with right:
        segment = df.groupby("Segment", as_index=False).size()
        pie_chart(
            segment,
            "Segment",
            "size",
            "Portfolio Composition",
            color_domain=[
                "Platinum Customers",
                "High Priority / Gold Customers",
                "Moderate Priority / Silver Customers",
                "Low Priority / Bronze Customers",
            ],
            color_range=["#b03a48", "#d4af37", "#aeb4bd", "#a97142"],
        )


def management_insights():
    df = visible_customers()
    section("Management Insights Center", "Rule-based scoring model insights and action recommendations for the LHO NRI service administration workflow.")
    last_updated_stamp()
    p1 = df[df["Priority Level"] == "P1"]
    cols = st.columns(4)
    cols[0].metric("P1 Immediate Action", len(p1), "Highest urgency")
    cols[1].metric("Projected Deposit Recovery", money(df["Expected Deposit Recovery"].sum()), "Expected model")
    cols[2].metric("Customers Under Reactivation", int(df["Pipeline Stage"].isin(["Contacted", "Interested", "KYC Updated", "Funded"]).sum()), "Active RM work")
    cols[3].metric("Revenue Opportunity", money(df["Expected Deposit Recovery"].sum() * 0.035), "Indicative margin")
    st.subheader("Scoring Model Insights")
    insights = [
        "Mananchira branch NRI customers with balance above Rs 10 lakh and dormant due to KYC issues show high reactivation potential.",
        "Long-tenure NRI customers with multiple SBI products should be prioritized for relationship-led reactivation.",
        "Shifted-to-other-bank customers show lower recovery probability and require targeted win-back offers.",
        "Documentation-pending customers convert faster when NRI service officers assist before relationship manager outreach.",
    ]
    for item in insights:
        st.markdown(f'<div class="alert-card">{item}</div>', unsafe_allow_html=True)
    st.subheader("Priority Action Recommendations")
    opportunity_table(df[df["Priority Level"].isin(["P1", "P2"])], 12)


def assessment_center():
    section("Relationship Intelligence Assessment Center", "Separate score assignment workbench for LHO NRI portfolio analysts, intelligence supervisors and the LHO NRI cell administrator.")
    df = st.session_state.customers
    customers = [f"{row['Customer ID']} - {row['Customer Name']}" for _, row in df.iterrows()]
    selected = st.selectbox("Load Existing Customer", customers)
    selected_id = selected.split(" - ")[0]
    row = df[df["Customer ID"] == selected_id].iloc[0].to_dict()
    with st.form("assessment_form"):
        st.subheader("Customer Assessment Form")
        c1, c2, c3 = st.columns(3)
        customer_id = c1.text_input("Customer ID", row["Customer ID"])
        customer_name = c2.text_input("Customer Name", row["Customer Name"])
        country = c3.selectbox("Country", COUNTRIES, index=COUNTRIES.index(row["Country"]))
        c1, c2, c3 = st.columns(3)
        account_type = c1.selectbox("Account Type", ACCOUNT_TYPES, index=ACCOUNT_TYPES.index(row["Account Type"]))
        balance = c2.number_input("Average Balance", min_value=0, value=int(row["Average Balance"]), step=50_000)
        remittance = c3.selectbox("Historical Remittance Activity", REMITTANCE_LEVELS, index=REMITTANCE_LEVELS.index(row["Historical Remittance Activity"]))
        c1, c2, c3 = st.columns(3)
        products = c1.number_input("Number of SBI Products", min_value=0, max_value=12, value=int(row["Number of SBI Products"]))
        duration = c2.number_input("Relationship Duration", min_value=0, max_value=40, value=int(row["Relationship Duration"]))
        dormancy = c3.selectbox("Dormancy Reason", DORMANCY_REASONS, index=DORMANCY_REASONS.index(row["Dormancy Reason"]))
        c1, c2, c3 = st.columns(3)
        kyc = c1.selectbox("KYC Status", ["Valid", "Pending", "Expired"], index=["Valid", "Pending", "Expired"].index(row["KYC Status"]))
        potential = c2.number_input("Expected Deposit Potential", min_value=0, value=int(row["Expected Deposit Potential"]), step=50_000)
        risk = c3.selectbox("Customer Risk Level", RISK_LEVELS, index=RISK_LEVELS.index(row["Customer Risk Level"]))
        comments = st.text_area("Additional Analyst Comments", row["Additional Analyst Comments"])
        notes = st.text_area("Relationship Notes", row["Relationship Notes"])
        special = st.text_area("Special Circumstances", row["Special Circumstances"])
        draft_row = row.copy()
        draft_row.update(
            {
                "Customer ID": customer_id,
                "Customer Name": customer_name,
                "Country": country,
                "Account Type": account_type,
                "Average Balance": balance,
                "Historical Remittance Activity": remittance,
                "Number of SBI Products": products,
                "Relationship Duration": duration,
                "Dormancy Reason": dormancy,
                "KYC Status": kyc,
                "Expected Deposit Potential": potential,
                "Customer Risk Level": risk,
                "Additional Analyst Comments": comments,
                "Relationship Notes": notes,
                "Special Circumstances": special,
            }
        )
        scores = score_breakdown(draft_row)
        p_level = priority_level_from_score(scores["Relationship Intelligence Score"])
        c1, c2 = st.columns([0.7, 0.3], gap="large")
        with c1:
            st.subheader("Automatic Score Calculation")
            score_df = pd.DataFrame(scores.items(), columns=["Factor", "Score"])
            bar_chart(score_df[score_df["Factor"] != "Relationship Intelligence Score"], "Factor", "Score", "Score Breakdown", "#163f8f")
        with c2:
            st.markdown(
                f"""
                <div class="big-score">
                    Relationship Intelligence Score
                    <b>{scores['Relationship Intelligence Score']}</b>
                    Priority Level {p_level}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.metric("Expected Recovery", money(expected_recovery(draft_row)), f"{reactivation_probability(draft_row) * 100:.0f}% probability")
        c1, c2 = st.columns(2)
        save = c1.form_submit_button("Save Assessment Draft", use_container_width=True)
        submit = c2.form_submit_button("Submit Assessment", type="primary", use_container_width=True)
    if save or submit:
        status = "Draft" if save else "Pending Review"
        add_assessment(draft_row, scores["Relationship Intelligence Score"], status, comments)
        st.success(f"Assessment saved as {status}.")
        st.rerun()
    st.subheader("Assessment History")
    st.dataframe(st.session_state.assessments, hide_index=True, use_container_width=True)


def add_assessment(row, score, status, comments):
    assessment_id = f"AST-{9200 + len(st.session_state.assessments)}"
    new_row = pd.DataFrame(
        [
            {
                "Assessment ID": assessment_id,
                "Customer ID": row["Customer ID"],
                "Assessor Name": ROLE_CONFIG[st.session_state.role]["employee"],
                "Reviewer Name": "Pending" if status == "Pending Review" else "-",
                "Assessment Date": str(date.today()),
                "Score": int(score),
                "Status": status,
                "Comments": comments,
            }
        ]
    )
    st.session_state.assessments = pd.concat([new_row, st.session_state.assessments], ignore_index=True)
    add_audit(row["Customer ID"], "Created score assessment", "-", score, status)


def add_audit(customer_id, action, old_score, new_score, reason):
    new_log = pd.DataFrame(
        [
            {
                "Audit ID": f"AUD-{800 + len(st.session_state.audit_logs)}",
                "Employee Name": ROLE_CONFIG[st.session_state.role]["employee"],
                "Role": st.session_state.role,
                "Branch": st.session_state.selected_branch if is_branch_manager() else ROLE_CONFIG[st.session_state.role]["unit"],
                "Action": action,
                "Customer ID": customer_id,
                "Old Value": old_score,
                "New Value": new_score,
                "Reason": reason,
                "Date and Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        ]
    )
    st.session_state.audit_logs = pd.concat([new_log, st.session_state.audit_logs], ignore_index=True)


def approval_workbench():
    section("Score Approval Workbench", "Team leader review, score modification, approval, rejection and publication workflow.")
    last_updated_stamp()
    notification_panel()
    workflow_statuses = [
        "Pending Review",
        "Approved",
        "Rejected",
        "Published",
        "Reassessment Requested",
        "Returned to Analyst",
        "Escalated to LHO",
    ]
    pending = st.session_state.assessments[st.session_state.assessments["Status"].isin(workflow_statuses)].copy()
    st.dataframe(pending, hide_index=True, use_container_width=True)
    review_ids = pending["Assessment ID"].tolist()
    if not review_ids:
        st.info("No submitted assessments available for review.")
        return
    selected = st.selectbox("Select Assessment for Workflow Action", review_ids)
    record = st.session_state.assessments[st.session_state.assessments["Assessment ID"] == selected].iloc[0]
    if is_branch_manager():
        st.info("Branch Manager access is limited to branch-level review actions. Scores and scoring methodology cannot be modified.")
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Request Reassessment", use_container_width=True):
            update_assessment_status(selected, "Reassessment Requested", record)
        if c2.button("Return to Analyst", use_container_width=True):
            update_assessment_status(selected, "Returned to Analyst", record)
        if c3.button("Recommend Priority Change", use_container_width=True):
            add_audit(record["Customer ID"], "Recommended priority review", record["Score"], record["Score"], "Branch Manager recommendation without score modification")
            st.success("Priority review recommendation recorded.")
        if c4.button("Escalate Dispute", type="primary", use_container_width=True):
            update_assessment_status(selected, "Escalated to LHO", record)
        remarks = st.text_area("Managerial Remarks", "Branch Manager reviewed the customer assessment and branch action status.")
        if st.button("Save Managerial Remarks", use_container_width=True):
            add_audit(record["Customer ID"], "Added managerial remarks", "-", "-", remarks)
            st.success("Managerial remarks saved and audit trail updated.")
        return
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Approve", use_container_width=True):
        update_assessment_status(selected, "Approved", record)
    if c2.button("Reject", use_container_width=True):
        update_assessment_status(selected, "Rejected", record)
    if c3.button("Publish", type="primary", use_container_width=True):
        update_assessment_status(selected, "Published", record)
    modified_score = c4.number_input("Modify Score", min_value=0, max_value=100, value=int(record["Score"]))
    if st.button("Save Modified Score"):
        idx = st.session_state.assessments.index[st.session_state.assessments["Assessment ID"] == selected][0]
        old = st.session_state.assessments.at[idx, "Score"]
        st.session_state.assessments.at[idx, "Score"] = modified_score
        add_audit(record["Customer ID"], "Modified score", old, modified_score, "Leader modification before final decision")
        st.success("Score modified and audit log updated.")
        st.rerun()


def update_assessment_status(assessment_id, status, record):
    idx = st.session_state.assessments.index[st.session_state.assessments["Assessment ID"] == assessment_id][0]
    st.session_state.assessments.at[idx, "Status"] = status
    st.session_state.assessments.at[idx, "Reviewer Name"] = ROLE_CONFIG[st.session_state.role]["employee"]
    add_audit(record["Customer ID"], f"{status} assessment", record["Status"], status, "Score approval workflow action")
    st.success(f"Assessment {assessment_id} marked as {status}.")
    st.rerun()


def customer_360():
    df = visible_customers()
    section("Customer 360 View", "Private banking CRM style customer intelligence with relationship metrics, scoring, history, recommendations and reactivation status.")
    if df.empty:
        st.warning("No customers visible for this role.")
        return
    options = [f"{r['Customer ID']} - {r['Customer Name']}" for _, r in df.iterrows()]
    selected = st.selectbox("Select Customer", options)
    cid = selected.split(" - ")[0]
    st.session_state.selected_customer_id = cid
    row = df[df["Customer ID"] == cid].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Relationship Score", int(row["Relationship Intelligence Score"]))
    c2.metric("Priority Level", row["Priority Level"], row["Segment"])
    c3.metric("Expected Recovery", money(row["Expected Deposit Recovery"]))
    c4.metric("Reactivation Probability", f"{row['Reactivation Probability'] * 100:.0f}%")
    st.markdown(
        f"""
        <div class="info-card">
            <h3>{row['Customer Name']} • {row['Customer ID']}</h3>
            {badge(row['Country'])}{badge(row['Segment'], 'badge-purple')}{badge(row['Pipeline Stage'], 'badge-green')}{badge(row['Priority Level'], 'badge-red' if row['Priority Level'] == 'P1' else 'badge-amber')}
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns([0.9, 1.1], gap="large")
    with left:
        st.subheader("Relationship Profile")
        profile = pd.DataFrame(
            [
                ["Country", row["Country"]],
                ["Branch", row["Branch"]],
                ["Account Type", row["Account Type"]],
                ["Average Balance", money(row["Average Balance"])],
                ["Deposit Potential", money(row["Expected Deposit Potential"])],
                ["Risk Level", row["Customer Risk Level"]],
                ["Assigned RM", row["Assigned RM"]],
                ["Assigned Wealth Manager", row["Assigned Wealth Manager"]],
                ["Dormancy Reason", row["Dormancy Reason"]],
                ["KYC Status", row["KYC Status"]],
            ],
            columns=["Metric", "Value"],
        )
        st.dataframe(profile, hide_index=True, use_container_width=True)
    with right:
        st.subheader("Relationship Score Breakdown")
        score_df = pd.DataFrame(
            [
                ["Balance Score", row["Balance Score"]],
                ["Remittance Score", row["Remittance Score"]],
                ["Product Score", row["Product Score"]],
                ["Dormancy Score", row["Dormancy Score"]],
                ["Relationship Duration Score", row["Relationship Duration Score"]],
            ],
            columns=["Factor", "Score"],
        )
        bar_chart(score_df, "Factor", "Score", "Customer Score Factors", "#163f8f")
    if is_branch_manager():
        st.subheader("Branch Manager Operational Controls")
        with st.form("branch_manager_customer_controls"):
            c1, c2, c3 = st.columns(3)
            new_rm = c1.selectbox("Assign / Reassign Relationship Manager", RMS, index=RMS.index(row["Assigned RM"]))
            new_wm = c2.selectbox("Assign Wealth Manager", WEALTH_MANAGERS, index=WEALTH_MANAGERS.index(row["Assigned Wealth Manager"]))
            new_kyc = c3.selectbox("Update KYC Status", ["Valid", "Pending", "Expired"], index=["Valid", "Pending", "Expired"].index(row["KYC Status"]))
            remarks = st.text_area("Manager Remarks", "Branch-level customer profile reviewed and operational action updated.")
            if st.form_submit_button("Save Branch Updates", type="primary"):
                idx = st.session_state.customers.index[st.session_state.customers["Customer ID"] == cid][0]
                st.session_state.customers.at[idx, "Assigned RM"] = new_rm
                st.session_state.customers.at[idx, "Assigned Wealth Manager"] = new_wm
                st.session_state.customers.at[idx, "KYC Status"] = new_kyc
                add_audit(cid, "Branch Manager updated customer profile", "-", "-", remarks)
                st.success("Customer information, assignments and managerial remarks saved for this branch.")
                st.rerun()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Recommended Strategy")
        for rec in recommendations(row):
            st.markdown(badge(rec, "badge"), unsafe_allow_html=True)
    with c2:
        st.subheader("Assessment History")
        st.dataframe(st.session_state.assessments[st.session_state.assessments["Customer ID"] == cid], hide_index=True, use_container_width=True)
    with c3:
        st.subheader("NRI Customer Timeline")
        timeline = [
            ("Account Opening", f"{2010 + (int(cid[-2:]) % 10)} • {row['Account Type']} opened"),
            ("Last Transaction", f"{row['Historical Remittance Activity']} remittance pattern"),
            ("Dormancy Date", row["Dormancy Reason"]),
            ("Score Assignment", f"Relationship score {row['Relationship Intelligence Score']}"),
            ("Contact Attempts", f"Last contacted {row['Last Contact Days']} days ago"),
            ("Reactivation Status", row["Pipeline Stage"]),
        ]
        for label, value in timeline:
            st.markdown(f'<div class="timeline-row"><b>{label}</b><br><span class="small-muted">{value}</span></div>', unsafe_allow_html=True)


def reactivation_tracker():
    df = visible_customers()
    section("Customer Reactivation Tracker", "Relationship manager workflow for contact outcomes, KYC completion, funding and refusal reason tracking.")
    pipeline_view(visible_customers())
    st.subheader("Update Reactivation Record")
    selected = st.selectbox("Customer", [f"{r['Customer ID']} - {r['Customer Name']}" for _, r in visible_customers().iterrows()])
    cid = selected.split(" - ")[0]
    idx = st.session_state.customers.index[st.session_state.customers["Customer ID"] == cid][0]
    row = st.session_state.customers.loc[idx]
    with st.form("reactivation_form"):
        c1, c2, c3 = st.columns(3)
        call_status = c1.selectbox("Call Status", ["Pending", "Completed", "Not Reachable"], index=["Pending", "Completed", "Not Reachable"].index(row["Call Status"]) if row["Call Status"] in ["Pending", "Completed", "Not Reachable"] else 0)
        email_sent = c2.selectbox("Email Sent", ["Yes", "No"], index=0 if row["Email Sent"] == "Yes" else 1)
        meeting = c3.selectbox("Meeting Conducted", ["Yes", "No"], index=0 if row["Meeting Conducted"] == "Yes" else 1)
        c1, c2, c3 = st.columns(3)
        interested = c1.selectbox("Customer Interested", ["Yes", "No", "Undecided"], index=["Yes", "No", "Undecided"].index(row["Customer Interested"]))
        kyc_completed = c2.selectbox("KYC Completed", ["Yes", "No"], index=0 if row["KYC Completed"] == "Yes" else 1)
        funds_added = c3.selectbox("Funds Added", ["Yes", "No"], index=0 if row["Funds Added"] == "Yes" else 1)
        c1, c2, c3 = st.columns(3)
        reactivated = c1.selectbox("Account Reactivated", ["Yes", "No"], index=0 if row["Account Reactivated"] == "Yes" else 1)
        expected_amount = c2.number_input("Expected Deposit Amount", value=int(row["Expected Deposit Potential"]), step=50_000)
        actual_amount = c3.number_input("Actual Deposit Amount", value=int(row["Actual Deposit Amount"]), step=50_000)
        c1, c2, c3 = st.columns(3)
        followup_date = c1.date_input("Follow-up Date", value=row["Follow-up Date"])
        followup_type = c2.selectbox("Follow-up Type", ["Call", "Email", "WhatsApp", "Video Meeting"], index=["Call", "Email", "WhatsApp", "Video Meeting"].index(row["Follow-up Type"]))
        followup_status = c3.selectbox("Follow-up Status", ["Pending", "Completed", "Missed"], index=["Pending", "Completed", "Missed"].index(row["Follow-up Status"]))
        rejection_reason = st.selectbox(
            "Reason for Rejection",
            ["None", "Shifted to competitor bank", "Returned to India", "Closed account", "No longer employed abroad", "Poor service experience", "Not interested"],
            index=["None", "Shifted to competitor bank", "Returned to India", "Closed account", "No longer employed abroad", "Poor service experience", "Not interested"].index(row["Rejection Reason"]),
        )
        submitted = st.form_submit_button("Update Reactivation Record", type="primary")
    if submitted:
        updates = {
            "Call Status": call_status,
            "Email Sent": email_sent,
            "Meeting Conducted": meeting,
            "Customer Interested": interested,
            "KYC Completed": kyc_completed,
            "Funds Added": funds_added,
            "Account Reactivated": reactivated,
            "Expected Deposit Potential": expected_amount,
            "Actual Deposit Amount": actual_amount,
            "Follow-up Date": followup_date,
            "Follow-up Type": followup_type,
            "Follow-up Status": followup_status,
            "Rejection Reason": rejection_reason,
        }
        for key, value in updates.items():
            st.session_state.customers.at[idx, key] = value
        add_audit(cid, "Updated reactivation tracker", "-", "-", "RM/service workflow update")
        st.success("Reactivation record updated.")
        st.rerun()
    left, right = st.columns(2)
    with left:
        st.subheader("Follow-up Reminders")
        reminders = visible_customers()[["Customer ID", "Customer Name", "Follow-up Date", "Follow-up Type", "Follow-up Status"]].sort_values("Follow-up Date")
        st.dataframe(reminders, hide_index=True, use_container_width=True)
    with right:
        st.subheader("Reason for Rejection Analytics")
        reject = df[df["Rejection Reason"] != "None"].groupby("Rejection Reason", as_index=False).size()
        if reject.empty:
            st.info("No rejection reasons captured yet.")
        else:
            bar_chart(reject, "Rejection Reason", "size", "Refusal Reason Counts", "#bd2f2f")


def team_performance():
    df = visible_customers()
    section("Team Performance Dashboard", "Assessor, relationship manager, wealth manager and deposit recovery performance.")
    last_updated_stamp()
    c1, c2 = st.columns(2, gap="large")
    with c1:
        assessors = st.session_state.assessments.groupby("Assessor Name", as_index=False).size()
        bar_chart(assessors, "Assessor Name", "size", "Top Assessors", "#163f8f")
    with c2:
        rm_perf = df.groupby("Assigned RM", as_index=False).agg(
            Reactivated=("Account Reactivated", lambda x: (x == "Yes").sum()),
            Recovery=("Expected Deposit Recovery", "sum"),
        )
        bar_chart(rm_perf, "Assigned RM", "Reactivated", "Most Reactivated Customers", "#177245")
    st.subheader("Performance Ranking")
    ranking = df.groupby("Assigned RM", as_index=False).agg(
        Assigned_Customers=("Customer ID", "count"),
        High_Value_Customers=("Segment", lambda x: x.isin(["Platinum Customers", "High Priority / Gold Customers"]).sum()),
        Expected_Recovery=("Expected Deposit Recovery", "sum"),
        Reactivated=("Account Reactivated", lambda x: (x == "Yes").sum()),
    )
    ranking["Expected_Recovery"] = ranking["Expected_Recovery"].map(money)
    st.dataframe(ranking, hide_index=True, use_container_width=True)


def country_intelligence():
    df = visible_customers()
    section("Country Intelligence Module", "Dormant NRI market ranking by account count, relationship score, deposit potential and recovery opportunity.")
    last_updated_stamp()
    stats = df.groupby("Country", as_index=False).agg(
        Dormant_Accounts=("Customer ID", "count"),
        Average_Relationship_Score=("Relationship Intelligence Score", "mean"),
        Average_Deposit_Potential=("Expected Deposit Potential", "mean"),
        Reactivation_Opportunity=("Expected Deposit Recovery", "sum"),
    )
    stats["Average_Relationship_Score"] = stats["Average_Relationship_Score"].round(0).astype(int)
    left, right = st.columns([1, 1], gap="large")
    with left:
        bar_chart(stats, "Country", "Reactivation_Opportunity", "Top NRI Markets", "#163f8f")
    with right:
        display = stats.copy()
        display["Average_Deposit_Potential"] = display["Average_Deposit_Potential"].map(money)
        display["Reactivation_Opportunity"] = display["Reactivation_Opportunity"].map(money)
        st.dataframe(display.sort_values("Dormant_Accounts", ascending=False), hide_index=True, use_container_width=True)


def workload_balancer():
    df = visible_customers()
    section("Relationship Manager Workload Balancer", "Automatic distribution view for high-value customers, assigned accounts and pending follow-ups.")
    last_updated_stamp()
    workload = df.groupby("Assigned RM", as_index=False).agg(
        Assigned_Customers=("Customer ID", "count"),
        High_Value_Customers=("Segment", lambda x: x.isin(["Platinum Customers", "High Priority / Gold Customers"]).sum()),
        Pending_Followups=("Follow-up Status", lambda x: (x != "Completed").sum()),
        Expected_Recovery=("Expected Deposit Recovery", "sum"),
    )
    display = workload.copy()
    display["Expected_Recovery"] = display["Expected_Recovery"].map(money)
    st.dataframe(display, hide_index=True, use_container_width=True)


def alert_center():
    df = visible_customers()
    section("Management Alert Center", "Operational alerts for high-value customers, KYC risk, stale contact and missed recovery opportunities.")
    last_updated_stamp()
    alerts = []
    for _, row in df.iterrows():
        if row["Last Contact Days"] > 30 and row["Priority Level"] in ["P1", "P2"]:
            alerts.append(["High", "High-value customer not contacted in 30 days", row["Customer ID"], row["Customer Name"], money(row["Expected Deposit Recovery"])])
        if row["Segment"] == "Platinum Customers" and row["Pipeline Stage"] == "Scored":
            alerts.append(["Medium", "Platinum customer pending assignment", row["Customer ID"], row["Customer Name"], money(row["Expected Deposit Recovery"])])
        if row["KYC Status"] == "Expired" and row["Priority Level"] == "P1":
            alerts.append(["High", "KYC-expired high-value customer", row["Customer ID"], row["Customer Name"], money(row["Expected Deposit Recovery"])])
        if row["Expected Deposit Recovery"] > 2_000_000 and row["Pipeline Stage"] in ["Scored", "Assigned"]:
            alerts.append(["High", "High recovery opportunity not pursued", row["Customer ID"], row["Customer Name"], money(row["Expected Deposit Recovery"])])
    if alerts:
        alert_df = pd.DataFrame(alerts, columns=["Severity", "Alert", "Customer ID", "Customer Name", "Expected Recovery"])
        st.dataframe(alert_df, hide_index=True, use_container_width=True)
        counts = alert_df.groupby("Alert", as_index=False).size()
        st.subheader("Alert Distribution")
        alert_distribution = counts.rename(columns={"size": "Count"}).sort_values("Count", ascending=False)
        st.dataframe(alert_distribution, hide_index=True, use_container_width=True)
    else:
        st.success("No management alerts for the visible portfolio.")


def branch_operations_center():
    df = visible_customers()
    section("Branch Operations Center", "Branch-level command view for assignments, follow-ups, meetings, reactivation actions and LHO escalations.")
    last_updated_stamp()
    if not is_branch_manager():
        st.error("This module is available only to Branch Managers.")
        return
    notification_panel()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pending Customer Assignments", int((df["Pipeline Stage"] == "Scored").sum()))
    c2.metric("Pending Follow-ups", int((df["Follow-up Status"] != "Completed").sum()))
    c3.metric("Upcoming Meetings", int((df["Follow-up Type"] == "Video Meeting").sum()))
    c4.metric("Escalation Requests", int((df["Customer Risk Level"] == "High").sum()))
    tabs = st.tabs(
        [
            "Assignments",
            "Allocations",
            "Follow-ups",
            "Activities",
            "Reactivated",
            "Branch Actions",
            "Escalations",
        ]
    )
    with tabs[0]:
        st.subheader("Pending Customer Assignments")
        pending = df[df["Pipeline Stage"].isin(["Scored", "Assigned"])][
            ["Customer ID", "Customer Name", "Segment", "Priority Level", "Assigned RM", "Assigned Wealth Manager", "Expected Deposit Recovery"]
        ].copy()
        pending["Expected Deposit Recovery"] = pending["Expected Deposit Recovery"].map(money)
        st.dataframe(pending, hide_index=True, use_container_width=True)
    with tabs[1]:
        st.subheader("RM and Wealth Manager Allocation")
        selected = st.selectbox("Select Customer for Allocation", [f"{r['Customer ID']} - {r['Customer Name']}" for _, r in df.iterrows()])
        cid = selected.split(" - ")[0]
        idx = st.session_state.customers.index[st.session_state.customers["Customer ID"] == cid][0]
        c1, c2, c3 = st.columns(3)
        rm = c1.selectbox("Relationship Manager", RMS, key="ops_rm")
        wm = c2.selectbox("Wealth Manager", WEALTH_MANAGERS, key="ops_wm")
        reason = c3.text_input("Reason", "Branch workload balancing")
        c1, c2, c3 = st.columns(3)
        if c1.button("Assign RM", use_container_width=True):
            st.session_state.customers.at[idx, "Assigned RM"] = rm
            add_audit(cid, "Assigned RM", "-", rm, reason)
            st.success("Relationship Manager assigned successfully.")
        if c2.button("Assign Wealth Manager", use_container_width=True):
            st.session_state.customers.at[idx, "Assigned Wealth Manager"] = wm
            add_audit(cid, "Assigned Wealth Manager", "-", wm, reason)
            st.success("Wealth Manager assigned successfully.")
        if c3.button("Reassign Customer", type="primary", use_container_width=True):
            st.session_state.customers.at[idx, "Assigned RM"] = rm
            st.session_state.customers.at[idx, "Assigned Wealth Manager"] = wm
            add_audit(cid, "Reassigned customer", "-", f"{rm} / {wm}", reason)
            st.success("Customer reassignment completed.")
    with tabs[2]:
        st.subheader("Pending Follow-ups")
        followups = df[df["Follow-up Status"] != "Completed"][
            ["Customer ID", "Customer Name", "Assigned RM", "Follow-up Date", "Follow-up Type", "Follow-up Status", "Priority Level"]
        ].sort_values("Follow-up Date")
        st.dataframe(followups, hide_index=True, use_container_width=True)
    with tabs[3]:
        st.subheader("Today's Branch Activities")
        activities = pd.DataFrame(
            [
                ["RM Calling Window", "12 pending calls", "In Progress"],
                ["KYC Documentation Desk", "8 documentation cases", "Open"],
                ["Wealth Review Meetings", "4 premium customer meetings", "Scheduled"],
                ["Deposit Recovery Follow-up", "6 high-value opportunities", "In Progress"],
            ],
            columns=["Activity", "Volume", "Status"],
        )
        st.dataframe(activities, hide_index=True, use_container_width=True)
    with tabs[4]:
        st.subheader("Recently Reactivated Customers")
        reactivated = df[df["Account Reactivated"] == "Yes"][
            ["Customer ID", "Customer Name", "Assigned RM", "Actual Deposit Amount", "Pipeline Stage"]
        ].copy()
        reactivated["Actual Deposit Amount"] = reactivated["Actual Deposit Amount"].map(money)
        st.dataframe(reactivated, hide_index=True, use_container_width=True)
    with tabs[5]:
        st.subheader("Pending Branch Actions")
        action_df = df[df["Priority Level"].isin(["P1", "P2"])][
            ["Customer ID", "Customer Name", "Priority Level", "Recommended Action", "Assigned RM", "Follow-up Status"]
        ]
        st.dataframe(action_df, hide_index=True, use_container_width=True)
        selected_action = st.selectbox("Action Customer", [f"{r['Customer ID']} - {r['Customer Name']}" for _, r in df.iterrows()], key="branch_action_customer")
        action_cid = selected_action.split(" - ")[0]
        c1, c2 = st.columns(2)
        if c1.button("Approve Branch Action", use_container_width=True):
            add_audit(action_cid, "Approved branch action", "-", "-", "Branch Manager approved operational action")
            st.success("Branch action approved.")
        if c2.button("Close Case", use_container_width=True):
            idx = st.session_state.customers.index[st.session_state.customers["Customer ID"] == action_cid][0]
            st.session_state.customers.at[idx, "Follow-up Status"] = "Completed"
            add_audit(action_cid, "Closed branch case", "-", "Completed", "Branch Manager closed completed case")
            st.success("Case closed successfully.")
    with tabs[6]:
        st.subheader("Escalation Requests")
        escalation_df = df[(df["Customer Risk Level"] == "High") | (df["Last Contact Days"] > 30)][
            ["Customer ID", "Customer Name", "Customer Risk Level", "Last Contact Days", "Priority Level", "Assigned RM"]
        ]
        st.dataframe(escalation_df, hide_index=True, use_container_width=True)
        selected_escalation = st.selectbox("Escalate Customer", [f"{r['Customer ID']} - {r['Customer Name']}" for _, r in df.iterrows()], key="lho_escalation_customer")
        reason = st.text_area("Escalation Reason", "Unresolved branch case requiring LHO guidance.")
        if st.button("Escalate to LHO", type="primary", use_container_width=True):
            add_audit(selected_escalation.split(" - ")[0], "Escalated to LHO", "-", "-", reason)
            st.success("Escalation request sent to LHO NRI Cell Administrator.")


def methodology():
    section("Scoring Methodology", "Transparent model governance page showing factor weights, scoring logic, normalization and workflow controls.")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Factor Weights")
        weights = pd.DataFrame(
            [
                ["Account Balance", "40%", "Existing relationship value"],
                ["Historical Remittance Activity", "25%", "Recurring NRI banking behavior"],
                ["Dormancy Reason Category", "15%", "Win-back feasibility"],
                ["Number of SBI Products Used", "15%", "Relationship depth"],
                ["Relationship Duration", "5%", "Loyalty and tenure"],
            ],
            columns=["Factor", "Weight", "Purpose"],
        )
        st.dataframe(weights, hide_index=True, use_container_width=True)
    with c2:
        st.subheader("Approval Workflow")
        workflow = pd.DataFrame(
            [
                ["Draft", "Team member saves assessment"],
                ["Pending Review", "Submitted to team leader"],
                ["Approved", "Leader validates score"],
                ["Rejected", "Returned with reason"],
                ["Published", "Visible to SBI teams"],
            ],
            columns=["Status", "Meaning"],
        )
        st.dataframe(workflow, hide_index=True, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Relationship Intelligence Priority Mapping")
        st.write("Priority level is derived directly from the Relationship Intelligence Score and customer segment.")
        st.dataframe(
            pd.DataFrame(
                [["P1", "Immediate Action"], ["P2", "High Priority"], ["P3", "Medium Priority"], ["P4", "Low Priority"]],
                columns=["Priority Level", "Meaning"],
            ),
            hide_index=True,
            use_container_width=True,
        )
    with c2:
        st.subheader("Expected Deposit Recovery Model")
        st.write("Expected Deposit Recovery = Expected Deposit Potential x Reactivation Probability.")
        st.write("Probability is adjusted by relationship score, risk, dormancy reason and refusal indicators.")


def admin_action(message, reason="Administrative configuration action"):
    add_audit("PLATFORM", message, "-", "-", reason)
    st.success(f"{message} completed successfully.")


def platform_administration():
    section("Platform Administration & Model Configuration", "LHO-only administration console for scoring model, rules, workflows, users, dashboards, versions, monitoring and governance.")
    last_updated_stamp()
    if not is_lho_admin():
        st.error("Access denied. This module is available only to the LHO NRI Cell Administrator, Thiruvananthapuram.")
        return
    tabs = st.tabs(
        [
            "Scoring Model",
            "Segments",
            "Priorities",
            "Business Rules",
            "Workflows",
            "Users & Roles",
            "Dashboards",
            "Versions",
            "System Config",
            "Monitoring",
            "Audit & Actions",
        ]
    )
    with tabs[0]:
        st.subheader("Scoring Model Configuration")
        edited = st.data_editor(
            st.session_state.model_factors,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Weightage": st.column_config.NumberColumn("Weightage (%)", min_value=0, max_value=100, step=1),
                "Enabled": st.column_config.CheckboxColumn("Enabled"),
            },
            key="model_factor_editor",
        )
        for idx, row in edited.iterrows():
            edited.at[idx, "Weightage"] = st.slider(
                f"{row['Factor']} weightage",
                0,
                100,
                int(row["Weightage"]),
                key=f"factor_slider_{idx}_{row['Factor']}",
            )
        total = int(edited[edited["Enabled"]]["Weightage"].sum())
        st.metric("Total Enabled Weightage", f"{total}%")
        if total != 100:
            st.warning("Total enabled factor weightage must equal 100% before publishing.")
        else:
            st.success("Total enabled factor weightage equals 100%.")
        c1, c2, c3 = st.columns(3)
        if c1.button("Save Draft", use_container_width=True, key="admin_model_save_draft"):
            st.session_state.model_factors = edited
            admin_action("Scoring model draft saved")
        if c2.button("Publish Model", type="primary", use_container_width=True, disabled=total != 100, key="admin_model_publish"):
            st.session_state.model_factors = edited
            admin_action("Scoring model published", "Published active scoring model version")
        if c3.button("Reset to Default", use_container_width=True, key="admin_model_reset_default"):
            st.session_state.model_factors = pd.DataFrame(
                [["Account Balance", 40, True], ["Historical Remittance Activity", 25, True], ["Dormancy Reason", 15, True], ["Number of SBI Products", 15, True], ["Relationship Duration", 5, True]],
                columns=["Factor", "Weightage", "Enabled"],
            )
            admin_action("Scoring model reset to default")
            st.rerun()
    with tabs[1]:
        st.subheader("Customer Segmentation")
        st.session_state.segments = st.data_editor(
            st.session_state.segments,
            use_container_width=True,
            column_config={
                "Minimum Score": st.column_config.NumberColumn(min_value=0, max_value=100),
                "Maximum Score": st.column_config.NumberColumn(min_value=0, max_value=100),
            },
            key="segment_editor",
        )
        if st.button("Save Segment Configuration", type="primary", key="admin_save_segments"):
            admin_action("Customer segmentation configuration saved")
    with tabs[2]:
        st.subheader("Priority Configuration")
        st.session_state.priorities = st.data_editor(
            st.session_state.priorities,
            use_container_width=True,
            column_config={
                "Minimum Score": st.column_config.NumberColumn(min_value=0, max_value=100),
                "Maximum Score": st.column_config.NumberColumn(min_value=0, max_value=100),
            },
            key="priority_editor",
        )
        if st.button("Save Priority Configuration", type="primary", key="admin_save_priorities"):
            admin_action("Priority configuration saved")
    with tabs[3]:
        st.subheader("Business Rule Configuration")
        c1, c2, c3 = st.columns(3)
        c1.slider("Reactivation Probability Logic", 0, 100, 72)
        c2.slider("Deposit Recovery Logic", 0, 100, 68)
        c3.slider("Recommendation Rules", 0, 100, 81)
        c1, c2, c3 = st.columns(3)
        c1.number_input("High Value Customer Threshold", min_value=0, value=2_500_000, step=50_000)
        c2.number_input("Risk Threshold", min_value=0, max_value=100, value=70)
        c3.number_input("Alert Threshold", min_value=0, max_value=100, value=80)
        c1, c2, c3 = st.columns(3)
        c1.toggle("Auto Recommendation Engine", value=True)
        c2.toggle("High Risk Escalation", value=True)
        c3.toggle("Deposit Recovery Alerts", value=True)
        if st.button("Save Business Rules", type="primary", key="admin_save_business_rules"):
            admin_action("Business rules saved")
    with tabs[4]:
        st.subheader("Workflow Configuration")
        workflows = [
            "Score Approval",
            "Supervisor Review",
            "RM Assignment",
            "Wealth Manager Assignment",
            "Audit Trail",
            "PDF Report Generation",
            "Management Alerts",
            "Notification Engine",
        ]
        cols = st.columns(2)
        for i, item in enumerate(workflows):
            cols[i % 2].toggle(item, value=True, key=f"workflow_{item}")
        if st.button("Save Workflow Configuration", type="primary", key="admin_save_workflows"):
            admin_action("Workflow configuration saved")
    with tabs[5]:
        st.subheader("User & Role Management")
        users = pd.DataFrame(
            [
                ["Aparna Rao", "SBI-LHO-001", ADMIN_ROLE, "LHO NRI Cell, Thiruvananthapuram", "Active", "2026-07-02 09:20"],
                ["Vikram Menon", "SBI-BM-014", "Branch Manager", FOCUS_BRANCH, "Active", "2026-07-02 09:04"],
                ["Rahul Nair", "SBI-RM-118", "NRI Relationship Manager", FOCUS_BRANCH, "Active", "2026-07-01 18:10"],
                ["Neha Iyer", "SBI-WM-044", "NRI Wealth Manager", FOCUS_BRANCH, "Active", "2026-07-01 17:45"],
                ["Ankit Sharma", "SBI-PA-022", "NRI Portfolio Analyst", "LHO NRI Intelligence Cell, Thiruvananthapuram", "Active", "2026-07-02 08:50"],
            ],
            columns=["Employee Name", "Employee ID", "Role", "Branch", "Status", "Last Login"],
        )
        st.dataframe(users, hide_index=True, use_container_width=True)
        actions = ["Create User", "Disable User", "Reset Password", "Assign Role", "Edit Permissions", "Delete User"]
        cols = st.columns(3)
        for i, action in enumerate(actions):
            if cols[i % 3].button(action, use_container_width=True, key=f"admin_user_action_{i}"):
                admin_action(action)
    with tabs[6]:
        st.subheader("Dashboard Configuration")
        dashboards = ["Executive Dashboard", "Management Dashboard", "Team Dashboard", "Country Intelligence", "Management Alerts"]
        kpis = ["Dormant Accounts", "Relationship Intelligence Score", "Expected Recovery", "Pending Approvals", "Reactivated Customers", "P1 Customers", "Follow-ups", "Alerts"]
        for dashboard in dashboards:
            st.multiselect(dashboard, kpis, default=kpis[:5], key=f"kpi_{dashboard}")
        if st.button("Save Dashboard Configuration", type="primary", key="admin_save_dashboard_config"):
            admin_action("Dashboard KPI configuration saved")
    with tabs[7]:
        st.subheader("Model Version Control")
        st.dataframe(st.session_state.model_versions, hide_index=True, use_container_width=True)
        cols = st.columns(5)
        for i, action in enumerate(["Create Version", "Clone Version", "Publish Version", "Rollback Version", "Archive Version"]):
            if cols[i].button(action, use_container_width=True, key=f"admin_version_action_{i}"):
                admin_action(action)
        st.subheader("Version History")
        st.dataframe(st.session_state.model_versions.sort_values("Published Date", ascending=False), hide_index=True, use_container_width=True)
    with tabs[8]:
        st.subheader("System Configuration")
        config_sets = {
            "Branch List": BRANCHES,
            "Countries": COUNTRIES,
            "Dormancy Reasons": DORMANCY_REASONS,
            "Risk Categories": RISK_LEVELS,
            "Remittance Categories": REMITTANCE_LEVELS,
            "Relationship Managers": RMS,
            "Wealth Managers": WEALTH_MANAGERS,
        }
        selected_config = st.selectbox("Configuration List", list(config_sets.keys()))
        edited_values = st.data_editor(pd.DataFrame({"Value": config_sets[selected_config]}), num_rows="dynamic", use_container_width=True, key="system_config_editor")
        if st.button("Save System Configuration", type="primary", key="admin_save_system_config"):
            admin_action(f"{selected_config} configuration saved", f"{len(edited_values)} records maintained")
    with tabs[9]:
        st.subheader("System Monitoring")
        metrics = [
            ("Total Users", 28, "Statewide platform users"),
            ("Users Online", 11, "Active sessions"),
            ("Today's Logins", 42, "Successful logins"),
            ("Today's Assessments", 9, "New or updated"),
            ("Pending Approvals", int((st.session_state.assessments["Status"] == "Pending Review").sum()), "Approval queue"),
            ("Published Scores", int((st.session_state.assessments["Status"] == "Published").sum()), "Visible to teams"),
            ("Rejected Scores", int((st.session_state.assessments["Status"] == "Rejected").sum()), "Returned cases"),
            ("Platform Health", "99.8%", "Operational"),
            ("Database Status", "Online", "Healthy"),
            ("System Status", "Operational", "Normal"),
            ("API Status", "Connected", "Prototype API"),
            ("Prototype Mode", "Enabled", "Demo environment"),
        ]
        for row in range(0, len(metrics), 4):
            cols = st.columns(4)
            for col, metric in zip(cols, metrics[row : row + 4]):
                col.metric(metric[0], metric[1], metric[2])
    with tabs[10]:
        st.subheader("Audit & Governance")
        st.dataframe(st.session_state.audit_logs, hide_index=True, use_container_width=True)
        st.subheader("Administrative Actions")
        cols = st.columns(5)
        for i, action in enumerate(["Save Configuration", "Publish Configuration", "Reset to Default", "Export Configuration", "Import Configuration"]):
            if cols[i].button(action, use_container_width=True, key=f"admin_global_action_{i}"):
                admin_action(action)


def reports():
    df = visible_customers()
    section("PDF Report Generator", "Professional report-ready views. Use browser print or Save as PDF from the Streamlit page.")
    if is_branch_manager():
        report_options = [
            "Branch Performance Report",
            "Customer Report",
            "RM Performance Report",
            "Deposit Recovery Report",
            "Export PDF",
            "Export Excel",
        ]
    else:
        report_options = ["Executive Summary Report", "Individual Customer Report", "Opportunity Report"]
    report_type = st.selectbox(
        "Report Type",
        report_options,
    )
    st.markdown('<div class="report-card">Use Ctrl+P in the browser and choose Save as PDF after selecting the report view.</div>', unsafe_allow_html=True)
    if report_type in ["Executive Summary Report", "Branch Performance Report", "Export PDF", "Export Excel"]:
        kpi_row(df)
        pipeline_view(df)
        opportunity_table(df, 10)
        if report_type in ["Export PDF", "Export Excel"]:
            st.success(f"{report_type} request prepared successfully for the selected branch view.")
    elif report_type in ["Individual Customer Report", "Customer Report"]:
        customer_360()
    elif report_type == "RM Performance Report":
        team_performance()
    else:
        st.subheader("Top Recovery Opportunities")
        opportunity_table(df, 15)


def audit_trail():
    section("Audit Trail", "Governance log tracking score creation, modification, approval, old score, new score, actor and reason.")
    st.dataframe(st.session_state.audit_logs, hide_index=True, use_container_width=True)


def user_admin():
    section("User Administration", "Role-based user access governance for the SBI NRI relationship intelligence workflow.")
    rows = []
    for role, config in ROLE_CONFIG.items():
        rows.append([config["employee"], role, config["unit"], ", ".join(config["permissions"])])
    st.dataframe(pd.DataFrame(rows, columns=["Employee", "Role", "Unit", "Access Summary"]), hide_index=True, use_container_width=True)


def route(module):
    routes = {
        "Executive Command Center": executive_command_center,
        "Management Insights Center": management_insights,
        "Branch Operations Center": branch_operations_center,
        "Relationship Intelligence Assessment Center": assessment_center,
        "Score Approval Workbench": approval_workbench,
        "Customer 360 View": customer_360,
        "Customer Reactivation Tracker": reactivation_tracker,
        "Team Performance Dashboard": team_performance,
        "Country Intelligence Module": country_intelligence,
        "RM Workload Balancer": workload_balancer,
        "Management Alert Center": alert_center,
        "Scoring Methodology": methodology,
        "Platform Administration & Model Configuration": platform_administration,
        "PDF Report Generator": reports,
        "Audit Trail": audit_trail,
        "User Administration": user_admin,
    }
    routes[module]()


def main():
    inject_css()
    init_state()
    if not st.session_state.logged_in:
        login_page()
        return
    module = sidebar()
    route(module)


if __name__ == "__main__":
    main()
