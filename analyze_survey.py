"""Capstone analysis: Stack Overflow-style developer survey (survey-data.csv)."""
import json
import os
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = os.path.expanduser("~/workspace/coursera-course9")
os.chdir(BASE)

df = pd.read_csv("survey-data.csv", low_memory=False)
print("shape:", df.shape)
N = len(df)


def count_multi(series):
    """Count semicolon-separated multi-value cells; strip whitespace; skip NaN."""
    c = Counter()
    for val in series.dropna():
        for item in str(val).split(";"):
            item = item.strip()
            if item:
                c[item] += 1
    return c


def top_list(counter, n):
    return [{"name": k, "count": int(v)} for k, v in counter.most_common(n)]


findings = {"total_respondents": int(N)}

# ---------------- A. Demographics ----------------
demo = {}
demo["top_countries"] = top_list(count_multi(df["Country"]), 10)

age_mid = {
    "Under 18 years old": 16, "18-24 years old": 21, "25-34 years old": 29.5,
    "35-44 years old": 39.5, "45-54 years old": 49.5, "55-64 years old": 59.5,
    "65 years or older": 68, "Prefer not to say": np.nan,
}
age_num = df["Age"].map(age_mid)
demo["age_buckets"] = [
    {"bucket": k, "count": int(v)}
    for k, v in df["Age"].value_counts(dropna=False).items()
]
demo["age_mean"] = round(float(age_num.mean()), 1)
demo["age_median"] = round(float(age_num.median()), 1)

demo["top_education"] = top_list(count_multi(df["EdLevel"]), 8)
demo["employment"] = top_list(count_multi(df["Employment"]), 10)
n_prof = int((df["MainBranch"] == "I am a developer by profession").sum())
demo["pct_professional_developers"] = round(100 * n_prof / N, 1)
demo["mainbranch"] = top_list(count_multi(df["MainBranch"]), 6)
findings["demographics"] = demo
print("\n== A. Demographics ==")
print("countries:", demo["top_countries"][:5])
print("age mean/median:", demo["age_mean"], demo["age_median"])
print("% professional devs:", demo["pct_professional_developers"])

# ---------------- B. Languages ----------------
lang_have = count_multi(df["LanguageHaveWorkedWith"])
lang_want = count_multi(df["LanguageWantToWorkWith"])
langs = {
    "top_have": top_list(lang_have, 10),
    "top_want": top_list(lang_want, 10),
}
# rising stars among top 20 by Have
top20 = [k for k, _ in lang_have.most_common(20)]
rows = []
for k in top20:
    h, w = lang_have[k], lang_want.get(k, 0)
    rows.append({"name": k, "have": h, "want": w, "gap": w - h,
                 "ratio": round(w / h, 3) if h else None})
langs["rising_by_gap"] = sorted(
    [{"name": r["name"], "gap": r["gap"]} for r in rows],
    key=lambda x: -x["gap"])[:5]
langs["rising_by_ratio"] = sorted(
    [r for r in rows if r["ratio"]],
    key=lambda x: -x["ratio"])[:5]
langs["rising_by_ratio"] = [
    {"name": r["name"], "want_have_ratio": r["ratio"]}
    for r in langs["rising_by_ratio"]
]
findings["languages"] = langs
print("\n== B. Languages (have) ==", langs["top_have"][:5])
print("== B. Languages (want) ==", langs["top_want"][:5])
print("rising by gap:", langs["rising_by_gap"])
print("rising by ratio:", langs["rising_by_ratio"])

# ---------------- C. Databases ----------------
db_have = count_multi(df["DatabaseHaveWorkedWith"])
db_want = count_multi(df["DatabaseWantToWorkWith"])
dbs = {"top_have": top_list(db_have, 10), "top_want": top_list(db_want, 10)}
dbs["biggest_gainers"] = sorted(
    [{"name": k, "have": db_have[k], "want": db_want.get(k, 0),
      "gap": db_want.get(k, 0) - db_have[k]}
     for k in [x for x, _ in db_have.most_common(20)]],
    key=lambda x: -x["gap"])[:5]
findings["databases"] = dbs
print("\n== C. Databases (have) ==", dbs["top_have"][:5])
print("== C. Databases (want) ==", dbs["top_want"][:5])
print("gainers:", dbs["biggest_gainers"])

# ---------------- D. IDEs ----------------
ide_have = count_multi(df["NEWCollabToolsHaveWorkedWith"])
ide_want = count_multi(df["NEWCollabToolsWantToWorkWith"])
findings["ides"] = {
    "top_have": top_list(ide_have, 10),
    "top_want": top_list(ide_want, 10),
}
print("\n== D. IDEs (have) ==", findings["ides"]["top_have"][:5])
print("== D. IDEs (want) ==", findings["ides"]["top_want"][:5])

# ---------------- E. Webframes / Platforms ----------------
findings["webframes_have_top8"] = top_list(
    count_multi(df["WebframeHaveWorkedWith"]), 8)
findings["platforms_have_top8"] = top_list(
    count_multi(df["PlatformHaveWorkedWith"]), 8)
print("\n== E. Webframes ==", findings["webframes_have_top8"][:4])
print("== E. Platforms ==", findings["platforms_have_top8"][:4])

# ---------------- F. Compensation ----------------
comp = df["ConvertedCompYearly"]
comp_clean = comp.dropna()
comp_clean = comp_clean[comp_clean <= 1e7]
findings["compensation"] = {
    "n_with_comp": int(comp_clean.shape[0]),
    "median": round(float(comp_clean.median()), 0),
    "mean": round(float(comp_clean.mean()), 0),
}
print("\n== F. Comp overall: median =",
      findings["compensation"]["median"], "(anchor ~65000)")

top6_countries = [d["name"] for d in demo["top_countries"][:6]]
med_by_country = []
for ctry in top6_countries:
    vals = comp_clean[df["Country"] == ctry]
    med_by_country.append({
        "name": ctry,
        "median_comp": round(float(vals.median()), 0) if len(vals) else None,
        "n": int(len(vals)),
    })
findings["compensation"]["median_by_country_top6"] = med_by_country
print("median by country:", med_by_country)


def has_token(series, token):
    """True where the semicolon-token list contains token exactly."""
    return series.apply(
        lambda s: isinstance(s, str)
        and token in [t.strip() for t in s.split(";")])


med_by_lang = []
for d in langs["top_have"][:5]:
    lang = d["name"]
    mask = has_token(df["LanguageHaveWorkedWith"], lang)
    vals = comp_clean[mask]
    med_by_lang.append({
        "name": lang,
        "median_comp": round(float(vals.median()), 0) if len(vals) else None,
        "n": int(len(vals)),
    })
findings["compensation"]["median_by_language_top5"] = med_by_lang
print("median by language:", med_by_lang)

# ---------------- G. Job satisfaction ----------------
js = df["JobSat"].dropna()
# scale 0-10: satisfied >=7, neutral 5-6, dissatisfied <=4
sat = int((js >= 7).sum()); neu = int(((js >= 5) & (js < 7)).sum())
dis = int((js < 5).sum())
findings["job_satisfaction"] = {
    "n_responses": int(len(js)),
    "distribution": [
        {"score": float(k), "count": int(v)}
        for k, v in sorted(js.value_counts().items())
    ],
    "pct_satisfied_ge7": round(100 * sat / len(js), 1),
    "pct_neutral_5_6": round(100 * neu / len(js), 1),
    "pct_dissatisfied_le4": round(100 * dis / len(js), 1),
    "mean_score": round(float(js.mean()), 2),
}
print("\n== G. JobSat: satisfied %s%%, dissatisfied %s%% ==" % (
    findings["job_satisfaction"]["pct_satisfied_ge7"],
    findings["job_satisfaction"]["pct_dissatisfied_le4"]))

# ---------------- H. Gender/age note ----------------
findings["notes"] = {
    "gender_column": "none - dataset has no gender column",
    "age_column": "categorical buckets; mapped to midpoints for mean/median",
}

with open("findings.json", "w") as f:
    json.dump(findings, f, indent=2, ensure_ascii=False)
print("\nfindings.json written")

# ================= CHARTS =================
plt.rcParams.update({"font.size": 10})
DPI = 150


def hbar(names, values, title, xlabel, fname, color="#1f77b4"):
    fig, ax = plt.subplots(figsize=(10, 6))
    y = np.arange(len(names))
    ax.barh(y, values, color=color)
    ax.set_yticks(y); ax.set_yticklabels(names)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel); ax.set_title(title, fontweight="bold")
    for i, v in enumerate(values):
        ax.text(v, i, f" {v:,}", va="center", fontsize=9)
    fig.tight_layout(); fig.savefig(fname, dpi=DPI); plt.close(fig)
    print("chart:", fname)


names = [d["name"] for d in langs["top_have"]]
hbar(names, [d["count"] for d in langs["top_have"]],
     "Top 10 Programming Languages Currently Used",
     "Respondents", "chart_top_languages.png", color="#2ca02c")

# grouped Have vs Want for top 10 by Want
topw = [d["name"] for d in langs["top_want"]]
have_v = [lang_have.get(k, 0) for k in topw]
want_v = [lang_want.get(k, 0) for k in topw]
fig, ax = plt.subplots(figsize=(10, 6))
y = np.arange(len(topw)); h = 0.38
ax.barh(y - h / 2, have_v, h, label="Have worked with", color="#1f77b4")
ax.barh(y + h / 2, want_v, h, label="Want to work with", color="#ff7f0e")
ax.set_yticks(y); ax.set_yticklabels(topw); ax.invert_yaxis()
ax.set_xlabel("Respondents"); ax.legend()
ax.set_title("Language Trends: Current Use vs Future Demand (top 10 by demand)",
             fontweight="bold")
fig.tight_layout(); fig.savefig("chart_language_trends.png", dpi=DPI)
plt.close(fig); print("chart: chart_language_trends.png")

names = [d["name"] for d in dbs["top_have"]]
hbar(names, [d["count"] for d in dbs["top_have"]],
     "Top 10 Database Technologies Currently Used",
     "Respondents", "chart_top_databases.png", color="#9467bd")

topw = [d["name"] for d in dbs["top_want"]]
have_v = [db_have.get(k, 0) for k in topw]
want_v = [db_want.get(k, 0) for k in topw]
fig, ax = plt.subplots(figsize=(10, 6))
y = np.arange(len(topw)); h = 0.38
ax.barh(y - h / 2, have_v, h, label="Have worked with", color="#1f77b4")
ax.barh(y + h / 2, want_v, h, label="Want to work with", color="#ff7f0e")
ax.set_yticks(y); ax.set_yticklabels(topw); ax.invert_yaxis()
ax.set_xlabel("Respondents"); ax.legend()
ax.set_title("Database Trends: Current Use vs Future Demand (top 10 by demand)",
             fontweight="bold")
fig.tight_layout(); fig.savefig("chart_database_trends.png", dpi=DPI)
plt.close(fig); print("chart: chart_database_trends.png")

names = [d["name"] for d in findings["ides"]["top_have"]]
hbar(names, [d["count"] for d in findings["ides"]["top_have"]],
     "Top 10 IDEs / Collaboration Tools Currently Used",
     "Respondents", "chart_top_ides.png", color="#17becf")

names = [d["name"] for d in demo["top_countries"]]
hbar(names, [d["count"] for d in demo["top_countries"]],
     "Top 10 Respondent Countries", "Respondents",
     "chart_top_countries.png", color="#e377c2")

cn = [d["name"] for d in med_by_country]
cv = [d["median_comp"] for d in med_by_country]
fig, ax = plt.subplots(figsize=(10, 6))
y = np.arange(len(cn))
ax.barh(y, cv, color="#8c564b")
ax.set_yticks(y); ax.set_yticklabels(cn); ax.invert_yaxis()
ax.set_xlabel("Median yearly compensation (USD)")
ax.set_title("Median Compensation by Country (top 6)",
             fontweight="bold")
for i, v in enumerate(cv):
    ax.text(v, i, f" ${v:,.0f}", va="center", fontsize=9)
fig.tight_layout(); fig.savefig("chart_compensation_by_country.png", dpi=DPI)
plt.close(fig); print("chart: chart_compensation_by_country.png")

fig, ax = plt.subplots(figsize=(10, 6))
vals = age_num.dropna()
ax.hist(vals, bins=[12, 18, 24, 34, 44, 54, 64, 75],
        color="#7f7f7f", edgecolor="white")
ax.set_xlabel("Age (bucket midpoints)")
ax.set_ylabel("Respondents")
ax.set_title("Age Distribution of Respondents", fontweight="bold")
fig.tight_layout(); fig.savefig("chart_age_dist.png", dpi=DPI)
plt.close(fig); print("chart: chart_age_dist.png")

print("\nALL DONE")
