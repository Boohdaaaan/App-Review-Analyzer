import base64
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO


def generate_plots(metrics: dict, app_name: str, top_n_countries: int = 10) -> dict[str, str]:
    """Generate plots for the given metrics."""
    plt.style.use("bmh")
    fig = plt.figure(figsize=(15, 10))

    # Header
    total_reviews = sum(d["count"] for d in metrics["rating_distribution"].values())
    fig.suptitle(f'Analysis of {total_reviews:,} Reviews for "{app_name}"', fontsize=16, y=1.0)

    # 1. Ratings Bar Chart
    ax1 = fig.add_subplot(231)
    ratings_data = metrics["rating_distribution"]
    ax1.bar(ratings_data.keys(), [d["count"] for d in ratings_data.values()], color="skyblue")
    ax1.set_title(f"Rating Distribution (AVG: {metrics['average_rating']})")
    ax1.set_xlabel("Rating")
    ax1.set_ylabel("Number of Reviews")

    # 2. Sentiment Bar Chart
    ax2 = fig.add_subplot(232)
    sentiment_data = metrics["sentiment_distribution"]
    sentiment_counts = [d["count"] for d in sentiment_data.values()]
    ax2.bar(sentiment_data.keys(), sentiment_counts, color="lightgreen")
    ax2.set_title("Sentiment Distribution")
    ax2.set_ylabel("Number of Reviews")
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # 3. Top Countries Bar Chart
    ax3 = fig.add_subplot(233)
    country_data = metrics["country_distribution"]
    # Sort countries by count and get top N
    sorted_countries = dict(
        sorted(
            country_data.items(),
            key=lambda x: x[1]["count"],
            reverse=True,
        )[:top_n_countries]
    )
    ax3.bar(
        sorted_countries.keys(),
        [d["count"] for d in sorted_countries.values()],
        color="salmon",
    )
    ax3.set_title(f"Top {top_n_countries} Countries Distribution")
    ax3.set_ylabel("Number of Reviews")
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # 4. Ratings Pie Chart
    ax4 = fig.add_subplot(234)
    ratings_percentages = [d["percentage"] for d in ratings_data.values()]
    ax4.pie(
        ratings_percentages,
        labels=[f"{i} Stars" for i in ratings_data.keys()],
        autopct="%1.1f%%",
        colors=plt.cm.Blues(np.linspace(0.3, 0.7, 5)),
    )
    ax4.set_title("Rating Distribution")
    
    # 5. Sentiment Pie Chart
    ax5 = fig.add_subplot(235)
    sentiment_percentages = [d["percentage"] for d in sentiment_data.values()]
    colors = ["#ff9999", "#ffcc99", "#99cc99", "#66b3ff", "#c2c2f0"]
    ax5.pie(
        sentiment_percentages,
        labels=[f"{s}" for s in sentiment_data.keys()],
        autopct="%1.1f%%",
        colors=colors,
    )
    ax5.set_title("Sentiment Distribution")
    
    # 6. Countries Pie Chart (New)
    ax6 = fig.add_subplot(236)
    country_percentages = [d["percentage"] for d in sorted_countries.values()]
    ax6.pie(
        country_percentages,
        labels=[f"{c}" for c in sorted_countries.keys()],
        autopct="%1.1f%%",
        colors=plt.cm.Pastel1(np.linspace(0, 1, top_n_countries)),
    )
    ax6.set_title(f"Top {top_n_countries} Countries Distribution")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Convert plot to base64 string
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close(fig)
    
    return {
        "image": image_base64,
        "format": "png",
        "encoding": "base64"
    }
