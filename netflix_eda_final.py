import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import nbformat as nbf

# =========================
# 1. Load the dataset
# =========================
df = pd.read_excel("netflix_titles_c.xlsx")

# Basic cleaning: Fill NaN with 'Unknown'
df.fillna("Unknown", inplace=True)

# =========================
# 2. PDF report setup
# =========================
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Netflix EDA Report", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, ln=True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 8, body)
        self.ln()

pdf = PDF()
pdf.add_page()

# =========================
# 3. Dataset Info
# =========================
info_str = str(df.info())
pdf.chapter_title("Dataset Info")
pdf.chapter_body("Dataset contains {} rows and {} columns.\n".format(df.shape[0], df.shape[1]))
pdf.chapter_body("Columns: " + ", ".join(df.columns))

# =========================
# 4. Describe statistics
# =========================
desc_stats = df.describe(include="all").transpose()
desc_stats.to_csv("describe_stats.csv")
pdf.chapter_title("Descriptive Statistics")
pdf.chapter_body("See 'describe_stats.csv' for detailed descriptive statistics.")

# =========================
# 5. Value counts for content type
# =========================
content_counts = df["content_type"].value_counts()
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="content_type", palette="Set2")
plt.title("Content Type Distribution")
plt.savefig("content_type.png")
plt.close()

pdf.chapter_title("Content Type Distribution")
pdf.chapter_body("Observation: Movies are more prevalent than TV Shows in the dataset.")
pdf.image("content_type.png", w=100)

# =========================
# 6. Release Year Distribution
# =========================
plt.figure(figsize=(10,4))
sns.histplot(df["release_yr"], bins=30, kde=False, color="skyblue")
plt.title("Release Year Distribution")
plt.savefig("release_year.png")
plt.close()

pdf.chapter_title("Release Year Distribution")
pdf.chapter_body("Observation: Most titles were released after 2015, showing Netflix's recent content surge.")
pdf.image("release_year.png", w=150)

# =========================
# 7. Rating Distribution
# =========================
plt.figure(figsize=(10,4))
sns.countplot(data=df, y="rating", order=df["rating"].value_counts().index, palette="coolwarm")
plt.title("Rating Distribution")
plt.savefig("rating_dist.png")
plt.close()

pdf.chapter_title("Rating Distribution")
pdf.chapter_body("Observation: TV-MA and TV-14 are the most common ratings, reflecting mature audience focus.")
pdf.image("rating_dist.png", w=150)

# =========================
# 8. Heatmap (correlation)
# =========================
# Convert release_yr to numeric (already int), encode duration approx
df["duration_num"] = df["duration"].str.extract('(\d+)').astype(float)
corr = df[["release_yr", "duration_num"]].corr()

plt.figure(figsize=(5,4))
sns.heatmap(corr, annot=True, cmap="Blues")
plt.title("Correlation Heatmap")
plt.savefig("heatmap.png")
plt.close()

pdf.chapter_title("Correlation Heatmap")
pdf.chapter_body("Observation: Duration has little correlation with release year.")
pdf.image("heatmap.png", w=120)

# =========================
# 9. Pairplot
# =========================
sns.pairplot(df[["release_yr", "duration_num"]].dropna())
plt.savefig("pairplot.png")
plt.close()

pdf.chapter_title("Pairplot")
pdf.chapter_body("Observation: Scatterplot confirms no strong trend between release year and duration.")
pdf.image("pairplot.png", w=120)

# =========================
# 10. Save PDF
# =========================
pdf.output("netflix_report.pdf")
print("PDF report generated: netflix_report.pdf")

# =========================
# 11. Create Jupyter Notebook
# =========================
nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell("# Netflix EDA Notebook"))
cells.append(nbf.v4.new_code_cell("""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("netflix_titles_c.xlsx")
df.fillna("Unknown", inplace=True)

df.info()
df.describe(include="all").transpose()
"""))

cells.append(nbf.v4.new_markdown_cell("## Content Type Distribution"))
cells.append(nbf.v4.new_code_cell("""
sns.countplot(data=df, x="content_type", palette="Set2")
plt.title("Content Type Distribution")
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("## Release Year Distribution"))
cells.append(nbf.v4.new_code_cell("""
sns.histplot(df["release_yr"], bins=30, kde=False, color="skyblue")
plt.title("Release Year Distribution")
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("## Rating Distribution"))
cells.append(nbf.v4.new_code_cell("""
sns.countplot(data=df, y="rating", order=df["rating"].value_counts().index, palette="coolwarm")
plt.title("Rating Distribution")
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("## Correlation Heatmap"))
cells.append(nbf.v4.new_code_cell("""
df["duration_num"] = df["duration"].str.extract('(\\d+)').astype(float)
sns.heatmap(df[["release_yr", "duration_num"]].corr(), annot=True, cmap="Blues")
plt.title("Correlation Heatmap")
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("## Pairplot"))
cells.append(nbf.v4.new_code_cell("""
sns.pairplot(df[["release_yr", "duration_num"]].dropna())
plt.show()
"""))

nb["cells"] = cells
with open("netflix_eda_notebook.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Jupyter Notebook saved as netflix_eda_notebook.ipynb")
