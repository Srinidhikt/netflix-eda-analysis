from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

pdf_path = "netflix_eda_report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Exploratory Data Analysis Report - Netflix Titles", styles["Title"]))
story.append(Spacer(1, 12))

intro_text = """
This report presents exploratory data analysis (EDA) of the Netflix dataset.
It includes statistical summaries, data distribution visualizations, and
observations to identify patterns, trends, and relationships in the data.
"""
story.append(Paragraph(intro_text, styles["BodyText"]))
story.append(Spacer(1, 12))

def add_image_with_caption(image_path, caption):
    story.append(Image(image_path, width=400, height=250))
    story.append(Paragraph(caption, styles["BodyText"]))
    story.append(Spacer(1, 12))

add_image_with_caption("content_type_distribution.png", "Figure 1: Distribution of Movies vs TV Shows")
add_image_with_caption("top_countries.png", "Figure 2: Top 10 Countries by Content Count")
add_image_with_caption("correlation_heatmap.png", "Figure 3: Correlation Heatmap of Numerical Features")
add_image_with_caption("release_year_distribution.png", "Figure 4: Distribution of Release Years")
add_image_with_caption("rating_distribution.png", "Figure 5: Content Rating Distribution")

observations = """
Key Observations:
1. Movies constitute a larger proportion of content compared to TV Shows.
2. The United States dominates in content production, followed by India and the United Kingdom.
3. Release year distribution shows significant growth in Netflix content from 2015 onwards.
4. Most content falls under ratings 'TV-MA' and 'TV-14'.
5. Correlation heatmap reveals no strong correlation between numeric variables, indicating diverse distribution.
"""
story.append(Paragraph(observations, styles["BodyText"]))

doc.build(story)
print(f"PDF saved as {pdf_path}")
