import sys, re, json
import warnings
import pandas as pd
warnings.filterwarnings("ignore")

# Map common review-tool export headers to canonical names.
ALIASES = {
    "cycle": ["Cycle", "Review cycle", "Campaign"],
    "type": ["Review type", "Relationship", "Reviewer type", "Form"],
    "reviewer": ["Reviewer", "Reviewer email", "Author"],
    "reviewee": ["Reviewee", "Reviewee email", "Employee", "Subject"],
    "topic": ["Topic", "Competency", "Section"],
    "question": ["Question", "Question text", "Prompt"],
    "answer": ["Answer", "Response", "Text answer", "Comment"],
    "score": ["Score", "Rating", "Numeric answer"],
}
NON_ANSWER = (r"^(-+|\.+|/|n/?a|no|none|nothing|not really|not sure|all good|nėra|neturiu|nieko|"
              r"viskas gerai|нічого|немає|ничего|нет)\b|nothing to add|no comments?|can'?t think|"
              r"see above|said above|as above|as mentioned|jau anksčiau|sunku pasakyti")
EXAMPLE = (r"for example|e\.g\.|for instance|such as|when (s?he|they|we|i)\b|project|client|customer|"
           r"meeting|launch|deadline|last (month|quarter|year)|\b(q[1-4]|jan|feb|mar|apr|may|jun|jul|aug|"
           r"sep|oct|nov|dec)\w*\b|\d")
LOW_VIS = (r"don'?t work (closely|much|together)|rarely work|limited interaction|haven'?t worked|"
           r"not enough (context|interaction|information)|hard to (say|evaluate|judge)|can'?t (evaluate|assess)")


def pick(df, key):
    for c in ALIASES[key]:
        if c in df.columns:
            return c
    return None


def words(s):
    return len(str(s).split()) if isinstance(s, str) else 0


def main(path):
    raw = pd.read_csv(path)
    cols = {k: pick(raw, k) for k in ALIASES}
    d = pd.DataFrame({k: raw[c] if c else None for k, c in cols.items()})
    d["type"] = d["type"].fillna("All") if cols["type"] else "All"
    d["cycle"] = d["cycle"].fillna("") if cols["cycle"] else ""
    d["answer"] = d["answer"].fillna("").astype(str).str.strip()
    d["score"] = pd.to_numeric(d["score"], errors="coerce") if cols["score"] else float("nan")
    d["w"] = d["answer"].map(words)
    qtext = d["question"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
    # Same generic text (e.g. "explain your rating") can repeat under several topics: keep them apart.
    d["q"] = (d["topic"].astype(str) + " :: " + qtext) if cols["topic"] else qtext
    d["q"] = d["q"].str.slice(0, 160)
    d["form"] = d["reviewer"].astype(str) + "|" + d["reviewee"].astype(str) + "|" + d["type"].astype(str) + "|" + d["cycle"].astype(str)
    rated = d["score"].notna()
    out = {"file": path, "columns_used": cols, "rows": len(d), "by_type": {}}

    for rt, g in d.groupby("type"):
        r = g[rated.loc[g.index]]
        o = g[~rated.loc[g.index]].copy()
        o["non"] = o["answer"].str.lower().str.contains(NON_ANSWER, regex=True) | (o["w"] < 4)
        o["ex"] = o["answer"].str.contains(EXAMPLE, case=False, regex=True)
        o["lowvis"] = o["answer"].str.contains(LOW_VIS, case=False, regex=True)
        t = {
            "forms": g["form"].nunique(),
            "reviewees": g["reviewee"].nunique(),
            "reviewers": g["reviewer"].nunique(),
            "reviewers_per_reviewee_median": float(g.groupby("reviewee")["reviewer"].nunique().median()),
            "reviewees_with_lt3_reviewers_pct": round(float((g.groupby("reviewee")["reviewer"].nunique() < 3).mean() * 100), 1),
        }
        if len(r):
            top = r["score"].max()
            pf = r.groupby("form")["score"].agg(["min", "max", "count", "std"])
            pf = pf[pf["count"] >= 3]
            t["ratings"] = {
                "scale_max": float(top),
                "distribution_pct": (r["score"].value_counts(normalize=True).sort_index() * 100).round(1).to_dict(),
                "labels": r.groupby("score")["answer"].agg(lambda s: s.value_counts().index[0]).to_dict(),
                "forms_rated": len(pf),
                "same_score_everywhere_pct": round(float((pf["min"] == pf["max"]).mean() * 100), 1) if len(pf) else None,
                "all_top_score_forms": int(((pf["min"] == top)).sum()),
                "all_top_score_pct": round(float((pf["min"] == top).mean() * 100), 1) if len(pf) else None,
            }
            means = r.groupby("q")["score"].agg(["mean", "size"]).round(2)
            t["ratings"]["mean_by_question"] = means.sort_values("size", ascending=False).head(15)["mean"].to_dict()
            wide = r.pivot_table(index="form", columns="q", values="score", aggfunc="first")
            if wide.shape[1] >= 3:
                c = wide.corr().values
                n = c.shape[0]
                vals = [c[i, j] for i in range(n) for j in range(i + 1, n) if pd.notna(c[i, j])]
                t["ratings"]["mean_inter_item_correlation"] = round(sum(vals) / len(vals), 2) if vals else None
            # all-top rate by number of reviewers the reviewee had (anonymity check)
            nrev = g.groupby("reviewee")["reviewer"].nunique()
            pf2 = pf.copy()
            pf2["n"] = [nrev.get(f.split("|")[1], 0) for f in pf2.index]
            pf2["band"] = pd.cut(pf2["n"], [0, 2, 4, 1000], labels=["1-2", "3-4", "5+"])
            t["ratings"]["all_top_pct_by_reviewer_count"] = (
                pf2.groupby("band", observed=True).apply(lambda x: round(float((x["min"] == top).mean() * 100), 1)).to_dict())
        if len(o):
            q = o.groupby("q").agg(
                answers=("w", "size"), median_words=("w", "median"), mean_words=("w", "mean"),
                under10_pct=("w", lambda s: (s < 10).mean() * 100), over30_pct=("w", lambda s: (s >= 30).mean() * 100),
                non_answer_pct=("non", lambda s: s.mean() * 100), example_pct=("ex", lambda s: s.mean() * 100),
            ).round(1).reset_index()
            t["open_questions"] = q.sort_values("answers", ascending=False).to_dict("records")
            t["open_overall"] = {
                "answers": len(o), "median_words": float(o["w"].median()),
                "over30_pct": round(float((o["w"] >= 30).mean() * 100), 1),
                "non_answer_pct": round(float(o["non"].mean() * 100), 1),
                "example_pct": round(float(o["ex"].mean() * 100), 1),
                "low_visibility_mentions": int(o["lowvis"].sum()),
                "dash_only_answers": int(o["answer"].str.fullmatch(r"[-./]+").sum()),
            }
            t["open_examples"] = {
                "rich": o[(o["w"] >= 50) & o["ex"]]["answer"].str[:300].head(3).tolist(),
                "weak": o[o["non"] & (o["w"] > 0)]["answer"].value_counts().head(10).to_dict(),
                "low_visibility": o[o["lowvis"]]["answer"].str[:200].head(3).tolist(),
            }
        out["by_type"][str(rt)] = t
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
