import csv
import re
import pandas as pd
import matplotlib.pyplot as plt

in_file = "/home/set-iitgn-vm/Desktop/Lab2 stt/bug_fix_diffs_llm.csv"

keywords = [
    "fix", "fixed", "fixes", "bug", "crash",
    "solves", "resolution", "resolve", "issue", "regression",
    "fall back", "assert", "coverity", "reproducible",
    "stack", "broken", "differential testing", "error",
    "hang", "test fix", "steps to reproduce", "failure",
    "leak", "stack trace", "heap overflow", "freeze",
    "problem", "overflow", "avoid", "workaround",
    "break", "stop"
]



def is_precise(msg, fname=None, thresh=3):
    if not msg:
        return False
    score = 0
    if fname and fname.lower() in msg.lower():
        score += 1
    if re.match(r"^(add|fix|update|remove)\b", msg.lower()):
        score += 1
    if any(k in msg.lower() for k in keywords):
        score += 1
    if re.search(r"\.py|\.cpp|function|method|class|error|crash|exception|leak", msg.lower()):
        score += 2
    return score >= thresh

df = pd.read_csv(in_file)

# --- Adding precision labels ---
df["Dev_Precise"] = df["Developer Message"].apply(is_precise)
df["LLM_Precise"] = df["LLM Inference"].apply(is_precise)
df["Rect_Precise"] = df["Rectified Message"].apply(is_precise)

# Calculating  hit rates 
total = len(df)
dev_precise = df["Dev_Precise"].sum()
llm_precise = df["LLM_Precise"].sum()
rect_precise = df["Rect_Precise"].sum()

hit_rates = {
    "Developer": round(dev_precise / total * 100, 3),
    "LLM": round(llm_precise / total * 100, 3),
    "Rectifier": round(rect_precise / total * 100, 3),
}


print("  Hit Rates (RQ1–RQ3) ")
for k, v in hit_rates.items():
    print(f"{k}: {v}% precise")

df.to_csv("bug_fixes_eval.csv", index=False)

plt.bar(hit_rates.keys(), hit_rates.values())
plt.ylabel("Hit Rate (%)")
plt.title("Commit Message Precision Comparison")
plt.show()