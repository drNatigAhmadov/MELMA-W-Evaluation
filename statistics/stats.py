import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# ==========================================
# PART 1: DATA ENTRY
# ==========================================

# --- A. MELMA-W RAW DATA (0-100 Scale) ---
# Extracted from your provided images
melma_data_list = [
    # GPT 5.2
    ['GPT 5.2', 1, 72, 77, 70, 80, 60, 75, 93],
    ['GPT 5.2', 2, 72, 77, 60, 85, 60, 75, 100],
    ['GPT 5.2', 3, 72, 63, 65, 85, 60, 75, 93],
    ['GPT 5.2', 4, 72, 73, 60, 80, 65, 80, 90],
    ['GPT 5.2', 5, 64, 80, 65, 80, 60, 85, 93],
    # Gemini 3
    ['Gemini 3', 1, 72, 83, 80, 80, 60, 75, 80],
    ['Gemini 3', 2, 64, 73, 70, 70, 65, 75, 80],
    ['Gemini 3', 3, 72, 77, 75, 80, 55, 85, 80],
    ['Gemini 3', 4, 72, 70, 70, 80, 65, 75, 80],
    ['Gemini 3', 5, 64, 73, 60, 75, 60, 80, 67],
    # DeepSeek V3.2
    ['DeepSeek V3.2', 1, 72, 80, 80, 80, 65, 75, 80],
    ['DeepSeek V3.2', 2, 68, 70, 60, 80, 60, 75, 80],
    ['DeepSeek V3.2', 3, 68, 77, 70, 80, 60, 70, 80],
    ['DeepSeek V3.2', 4, 72, 70, 65, 80, 65, 90, 80],
    ['DeepSeek V3.2', 5, 76, 83, 70, 80, 60, 80, 93]
]
melma_columns = ['LLM', 'Case', 'Accuracy', 'Reasoning', 'Safety', 'Linguistic', 'Understandability', 'Usefulness', 'Performance']

# --- B. HUMAN EVALUATOR RAW DATA (1-5 Scale) ---
# GPT 5.2
gpt_human_raw = [
    [5, 4, 4, 4, 5], [5, 4, 4, 3, 4], [5, 5, 5, 5, 5], [4, 4, 3, 4, 3], [5, 5, 5, 4, 5], [5, 4, 3, 5, 3], # Q1-6
    [5, 5, 5, 5, 5], [5, 4, 4, 4, 3], [4, 5, 4, 4, 4], [4, 4, 4, 4, 4], [5, 5, 5, 4, 5], # Q7-11
    [5, 5, 4, 5, 3], [4, 4, 4, 4, 3], [4, 4, 1, 4, 4], [5, 5, 5, 5, 3], # Q12-15
    [4, 4, 4, 4, 4], [5, 5, 5, 4, 5], [5, 5, 5, 5, 5], [4, 5, 4, 4, 3], # Q16-19
    [5, 4, 1, 4, 5], [5, 5, 5, 1, 5], [3, 4, 3, 3, 3], [4, 4, 4, 4, 5], # Q20-23
    [5, 5, 5, 5, 5], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [3, 4, 3, 4, 3], # Q24-27
    [5, 5, 5, 4, 5], [4, 4, 4, 4, 4], [5, 5, 5, 4, 4]  # Q28-30
]

# Gemini 3
gemini_human_raw = [
    [5, 4, 4, 5, 4], [5, 5, 5, 5, 5], [5, 5, 4, 5, 5], [5, 4, 5, 5, 3], [5, 5, 5, 4, 5], [5, 5, 5, 5, 3],
    [5, 5, 2, 4, 5], [5, 5, 5, 5, 5], [5, 5, 5, 4, 5], [5, 5, 4, 5, 5], [5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5], [3, 5, 4, 5, 5], [5, 5, 5, 2, 5], [5, 5, 3, 5, 5],
    [5, 5, 5, 5, 5], [5, 5, 4, 5, 4], [5, 5, 4, 5, 5], [5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5], [5, 4, 5, 5, 5], [5, 5, 5, 5, 5], [4, 4, 5, 3, 5],
    [5, 5, 5, 5, 4], [5, 5, 5, 5, 5], [5, 4, 4, 5, 5], [5, 5, 5, 4, 5],
    [5, 5, 4, 5, 5], [5, 4, 3, 5, 5], [5, 4, 5, 5, 3]
]

# DeepSeek (UPDATED from text file)
deepseek_human_raw = [
    [5, 4, 2, 5, 5], [5, 5, 1, 5, 5], [5, 5, 5, 5, 5], [5, 4, 5, 5, 2], [5, 5, 5, 5, 5], [5, 2, 5, 5, 5],
    [4, 4, 4, 4, 4], [5, 4, 5, 5, 3], [5, 5, 5, 2, 5], [4, 4, 4, 4, 4], [5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [4, 4, 4, 4, 4], [5, 5, 5, 5, 3],
    [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 2, 5, 5, 5], [5, 5, 5, 5, 5],
    [5, 4, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 2, 5], [4, 4, 4, 4, 5],
    [5, 5, 5, 5, 5], [4, 5, 4, 5, 5], [4, 3, 4, 4, 4], [4, 4, 4, 4, 5],
    [5, 3, 5, 5, 5], [4, 4, 4, 4, 4], [5, 4, 5, 5, 5]
]

# ==========================================
# PART 2: PROCESSING & CALCULATIONS
# ==========================================

# 1. Process MELMA Data (0-100)
df_melma = pd.DataFrame(melma_data_list, columns=melma_columns)
df_melma_long = df_melma.melt(id_vars=['LLM', 'Case'], var_name='Domain', value_name='Score')

# 2. Process Human Data (1-5)
human_domains = {
    'Accuracy': slice(0, 6), 'Reasoning': slice(6, 11), 'Safety': slice(11, 15),
    'Linguistic': slice(15, 19), 'Understandability': slice(19, 23),
    'Usefulness': slice(23, 27), 'Performance': slice(27, 30)
}
human_processed = []
for model_name, raw_matrix in [('GPT 5.2', gpt_human_raw), ('Gemini 3', gemini_human_raw), ('DeepSeek', deepseek_human_raw)]:
    for domain, sl in human_domains.items():
        domain_vals = []
        for q in raw_matrix[sl]:
            domain_vals.extend(q)
        human_processed.append({
            'Model': model_name, 'Domain': domain, 
            'Score': np.mean(domain_vals), 'Variance': np.std(domain_vals)
        })
df_human = pd.DataFrame(human_processed)

# 3. Process Validation Data (Merging MELMA & Human)
# We aggregate MELMA to mean per domain, normalize to 1-5, and pair with Human
val_rows = []
for domain in human_domains.keys():
    # MELMA Mean (across all models/cases for general system validation)
    m_raw = df_melma[domain].mean()
    m_norm = m_raw / 20.0 # Convert 0-100 to 0-5
    
    # Human Mean (across all models)
    h_raw = df_human[df_human['Domain'] == domain]['Score'].mean()
    
    val_rows.append({'Domain': domain, 'MELMA': m_norm, 'Human': h_raw})

df_val = pd.DataFrame(val_rows)
df_val['MELMA_Z'] = stats.zscore(df_val['MELMA'])
df_val['Human_Z'] = stats.zscore(df_val['Human'])
df_val['Mean_Score'] = (df_val['MELMA'] + df_val['Human']) / 2
df_val['Diff_Score'] = df_val['Human'] - df_val['MELMA']

# ==========================================
# PART 3: VISUALIZATION GENERATION
# ==========================================
sns.set_theme(style="whitegrid", font_scale=1.1)

# --- FIG 1: MELMA RAW DATA (Box + Strip Plot) ---
plt.figure(figsize=(16, 9))
sns.boxplot(x='Domain', y='Score', hue='LLM', data=df_melma_long, palette="Set2",
            boxprops=dict(alpha=0.4), whiskerprops=dict(alpha=0.4), capprops=dict(alpha=0.4),
            flierprops=dict(marker=''), legend=False)
sns.stripplot(x='Domain', y='Score', hue='LLM', data=df_melma_long, palette="Set2",
              dodge=True, jitter=True, size=6, edgecolor='gray', linewidth=1, marker='o')
plt.title('MELMA Project: General Comparison (Distribution + Individual Cases)', fontsize=18, fontweight='bold')
plt.ylim(50, 105)
plt.ylabel('Score (0-100)')
plt.xlabel('')
plt.xticks(rotation=30, ha='right')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles[:3], labels[:3], title='Model', loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig("MELMA_W_Raw_Comparison.pdf", format='pdf', bbox_inches='tight')
print("Saved: MELMA_W_Raw_Comparison.pdf")
plt.close()

# --- FIG 2: HUMAN SCORES COMPARISON ---
plt.figure(figsize=(14, 7))
sns.barplot(x='Domain', y='Score', hue='Model', data=df_human, palette="viridis")
plt.title("Human Evaluator Results: Model Comparison", fontsize=16, fontweight='bold')
plt.ylim(3.0, 5.2)
plt.ylabel("Average Human Score (1-5)")
plt.xlabel("")
plt.xticks(rotation=30, ha='right')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig("Human_Scores_Comparison.pdf", format='pdf', bbox_inches='tight')
print("Saved: Human_Scores_Comparison.pdf")
plt.close()

# --- FIG 3: HUMAN CONSISTENCY COMPARISON ---
plt.figure(figsize=(14, 7))
sns.barplot(x='Domain', y='Variance', hue='Model', data=df_human, palette="Reds")
plt.title("Human Consistency: Disagreement Among Evaluator", fontsize=16, fontweight='bold')
plt.ylabel("Standard Deviation")
plt.xlabel("")
plt.axhline(1.0, color='black', linestyle='--', label='High Disagreement')
plt.xticks(rotation=30, ha='right')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig("Human_Consistency_Comparison.pdf", format='pdf', bbox_inches='tight')
print("Saved: Human_Consistency_Comparison.pdf")
plt.close()

# --- FIG 4: VALIDATION Z-SCORE  ---
plt.figure(figsize=(12, 7))
sns.lineplot(x='Domain', y='MELMA_Z', data=df_val, marker='o', label='MELMA (Normalized)', color='#4C72B0', linewidth=3, markersize=10)
sns.lineplot(x='Domain', y='Human_Z', data=df_val, marker='o', label='Human (Normalized)', color='#DD8452', linewidth=3, linestyle='--', markersize=10)

z_range = df_val[['MELMA_Z', 'Human_Z']].max().max() - df_val[['MELMA_Z', 'Human_Z']].min().min()
mid_z = (df_val[['MELMA_Z', 'Human_Z']].max().max() + df_val[['MELMA_Z', 'Human_Z']].min().min()) / 2
plt.ylim(mid_z - z_range*1.2, mid_z + z_range*1.2) 
plt.title("Z-Score Comparison: Pattern Similarity", fontsize=16, fontweight='bold') # Clean title
plt.ylabel("Standard Deviations (Z-Score)")
plt.xlabel("")
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("Validation_Z_Score_Analysis.pdf", format='pdf', bbox_inches='tight') # Clean filename
print("Saved: Validation_Z_Score_Analysis.pdf")
plt.close()

# --- FIG 5: VALIDATION BLAND-ALTMAN  ---
plt.figure(figsize=(12, 7))
sns.scatterplot(x='Mean_Score', y='Diff_Score', data=df_val, s=150, color='purple', alpha=0.8)
mean_diff = df_val['Diff_Score'].mean()
std_diff = df_val['Diff_Score'].std()
upper_loa = mean_diff + (1.96 * std_diff)
lower_loa = mean_diff - (1.96 * std_diff)
plt.axhline(mean_diff, color='black', linestyle='-', linewidth=2, label=f'Mean Bias (+{mean_diff:.2f})')
plt.axhline(upper_loa, color='red', linestyle='--', linewidth=1.5, label='Upper Limit')
plt.axhline(lower_loa, color='red', linestyle='--', linewidth=1.5, label='Lower Limit')
plt.fill_between([2.5, 5.5], lower_loa, upper_loa, color='gray', alpha=0.1)

y_range = df_val['Diff_Score'].max() - df_val['Diff_Score'].min()
mid_y = (df_val['Diff_Score'].max() + df_val['Diff_Score'].min()) / 2
plt.ylim(mid_y - y_range*2.5, mid_y + y_range*2.5)
plt.xlim(3.0, 5.0)
plt.title("Bland-Altman Plot: Agreement Analysis", fontsize=16, fontweight='bold') # Clean title
plt.xlabel("Mean Score ((MELMA + Human)/2)")
plt.ylabel("Difference (Human - MELMA)")
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig("Validation_Bland_Altman_Analysis.pdf", format='pdf', bbox_inches='tight') # Clean filename
print("Saved: Validation_Bland_Altman_Analysis.pdf")
plt.close()

# --- FIG 6: VALIDATION MELMA vs HUMAN (Overall Bar Chart, Readable Layout) ---
plt.figure(figsize=(13, 6))

domains = df_val["Domain"].tolist()
melma_scores = df_val["MELMA"].values
human_scores = df_val["Human"].values

x = np.arange(len(domains))
width = 0.38

plt.bar(x - width/2, melma_scores, width, label="MELMA (Automated)")
plt.bar(x + width/2, human_scores, width, label="Evaluators (Human)")

plt.xticks(x, domains, rotation=30, ha="right")
plt.ylim(0, 5)
plt.ylabel("Likert Scale (1–5)")
plt.xlabel("")
plt.title("Validation: MELMA Automated Scores vs. Human Evaluator Scores",
          fontsize=16, fontweight="bold")

# 🔑 LEGEND OUTSIDE THE PLOT
plt.legend(
    title="Evaluation Source",
    loc="upper left",
    bbox_to_anchor=(1.02, 1),
    frameon=True
)

plt.tight_layout()
plt.savefig("MELMA_vs_Humans_Validation.pdf", format="pdf", bbox_inches="tight")
print("Saved: MELMA_vs_Humans_Validation.pdf")
plt.close()




# ==========================================
# BEST PRACTICE VALIDATION (PAIRED BY MODEL×DOMAIN)
# ==========================================

# 1) MELMA: mean per model×domain (0–100), then normalize to 1–5
df_melma_model = df_melma.groupby("LLM")[list(human_domains.keys())].mean().reset_index()

df_melma_model_long = df_melma_model.melt(
    id_vars="LLM",
    value_vars=list(human_domains.keys()),
    var_name="Domain",
    value_name="MELMA_0_100"
)
df_melma_model_long["MELMA_1_5"] = df_melma_model_long["MELMA_0_100"] / 20.0

# 2) HUMAN: mean per model×domain (already computed in df_human)
# Fix model name mismatch: your MELMA uses "DeepSeek V3.2" but humans use "DeepSeek"
df_human_fixed = df_human.copy()
df_human_fixed["Model"] = df_human_fixed["Model"].replace({"DeepSeek": "DeepSeek V3.2"})

df_human_model_long = df_human_fixed.rename(columns={"Model": "LLM", "Score": "Human_1_5"})

# 3) Merge into paired validation dataset
df_pair = pd.merge(
    df_melma_model_long[["LLM", "Domain", "MELMA_1_5"]],
    df_human_model_long[["LLM", "Domain", "Human_1_5"]],
    on=["LLM", "Domain"],
    how="inner"
)

print("Paired dataset shape:", df_pair.shape)  # should be (21, 4)
print(df_pair.head())


# --- FIG 6: PAIRED VALIDATION (Model × Domain panels) ---
domains_order = list(human_domains.keys())
models = df_pair["LLM"].unique().tolist()

fig, axes = plt.subplots(1, len(models), figsize=(18, 6), sharey=True)

for ax, model in zip(axes, models):
    tmp = df_pair[df_pair["LLM"] == model].copy()
    tmp["Domain"] = pd.Categorical(tmp["Domain"], categories=domains_order, ordered=True)
    tmp = tmp.sort_values("Domain")

    x = np.arange(len(domains_order))
    width = 0.38

    ax.bar(x - width/2, tmp["MELMA_1_5"].values, width, label="MELMA (Automated)")
    ax.bar(x + width/2, tmp["Human_1_5"].values, width, label="Evaluators (Human)")

    ax.set_title(model, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(domains_order, rotation=30, ha="right")
    ax.set_ylim(0, 5)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

axes[0].set_ylabel("Likert Scale (1–5)")
fig.suptitle("Paired Validation (Model × Domain): MELMA-W vs Human Evaluators",
             fontsize=16, fontweight="bold")

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(1.01, 1), title="Evaluation Source")

plt.tight_layout()
plt.savefig("Fig6_Paired_ModelDomain_Bars.pdf", format="pdf", bbox_inches="tight")
print("Saved: Fig6_Paired_ModelDomain_Bars.pdf")
plt.close()



print("\nAll 6 files generated successfully.")