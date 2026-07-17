"""
chart.py
Matplotlib chart components themed to match SearchAI's dark UI.
Used for training/validation curves, score histograms and correlation
heatmaps. All figures use static/sample data — no training logic here,
purely a presentational wrapper ready to be fed real metrics later.
"""

from collections import Counter
import re

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import LinearSegmentedColormap
import customtkinter as ctk
from styles.theme import Color, Radius, Spacing
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

# Shared matplotlib rcParams so every chart looks consistent
plt.rcParams.update({
    "figure.facecolor": Color.BG_CARD,
    "axes.facecolor": Color.BG_CARD,
    "axes.edgecolor": Color.BORDER,
    "axes.labelcolor": Color.TEXT_SECONDARY,
    "text.color": Color.TEXT_PRIMARY,
    "xtick.color": Color.TEXT_MUTED,
    "ytick.color": Color.TEXT_MUTED,
    "grid.color": Color.BORDER_SOFT,
    "font.size": 10,
    "font.family": ["Segoe UI", "Arial", "DejaVu Sans", "sans-serif"],
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.4,
    "legend.frameon": False,
    "legend.labelcolor": Color.TEXT_SECONDARY,
})


class ChartCanvas(ctk.CTkFrame):
    """Embeds a matplotlib Figure inside a rounded dark frame."""

    def __init__(self, master, figure, **kwargs):
        super().__init__(
            master,
            fg_color=Color.BG_CARD,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Color.BORDER_SOFT,
            **kwargs,
        )
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.configure(bg=Color.BG_CARD, highlightthickness=0)
        widget.pack(fill="both", expand=True, padx=Spacing.SM, pady=Spacing.SM)
        self.canvas = canvas


# ---------------------------------------------------------------------
# Sample-data figure builders (static/demo data, ready to be replaced
# with real arrays coming from the training/evaluation backend).
# ---------------------------------------------------------------------

def build_empty_figure(message):

    fig, ax = plt.subplots(
        figsize=(9.6,4),
        dpi=100
    )

    ax.text(
        0.5,
        0.5,
        message,
        ha="center",
        va="center",
        fontsize=13,
        color=Color.TEXT_MUTED
    )

    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig

def build_training_curves_figure():
    """Line charts: training vs validation loss and accuracy per epoch."""
    rng = np.random.default_rng(42)
    epochs = np.arange(1, 31)

    train_loss = 0.9 * np.exp(-epochs / 9) + rng.normal(0, 0.01, len(epochs)) + 0.05
    val_loss = 0.9 * np.exp(-epochs / 10) + 0.03 * np.sin(epochs / 3) + rng.normal(0, 0.015, len(epochs)) + 0.09
    train_acc = 1 - 0.85 * np.exp(-epochs / 8) + rng.normal(0, 0.005, len(epochs))
    val_acc = 1 - 0.85 * np.exp(-epochs / 9) - 0.02 * np.sin(epochs / 4) + rng.normal(0, 0.01, len(epochs))

    fig, (ax_loss, ax_acc) = plt.subplots(1, 2, figsize=(9.6, 3.6), dpi=100)
    fig.subplots_adjust(wspace=0.28, left=0.07, right=0.98, top=0.86, bottom=0.16)

    ax_loss.plot(epochs, train_loss, color=Color.PRIMARY, linewidth=2, label="Train Loss")
    ax_loss.plot(epochs, val_loss, color=Color.WARNING, linewidth=2, label="Val Loss")
    ax_loss.set_title("Loss", color=Color.TEXT_PRIMARY, fontsize=12, fontweight="bold", loc="left")
    ax_loss.set_xlabel("Epoch")
    ax_loss.legend(loc="upper right", fontsize=9)

    ax_acc.plot(epochs, train_acc, color=Color.SUCCESS, linewidth=2, label="Train Accuracy")
    ax_acc.plot(epochs, val_acc, color=Color.PRIMARY, linewidth=2, linestyle="--", label="Val Accuracy")
    ax_acc.set_title("Accuracy", color=Color.TEXT_PRIMARY, fontsize=12, fontweight="bold", loc="left")
    ax_acc.set_xlabel("Epoch")
    ax_acc.legend(loc="lower right", fontsize=9)

    for ax in (ax_loss, ax_acc):
        for spine in ax.spines.values():
            spine.set_color(Color.BORDER_SOFT)

    return fig


def build_histogram_figure():
    """Histogram of AI relevance scores across the dataset."""
    rng = np.random.default_rng(7)
    relevant = rng.beta(6, 2, 620)
    irrelevant = rng.beta(2, 6, 380)
    scores = np.concatenate([relevant, irrelevant])

    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=100)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.88, bottom=0.15)

    ax.hist(scores, bins=25, color=Color.PRIMARY, alpha=0.85, edgecolor=Color.BG_CARD)
    ax.axvline(0.5, color=Color.DANGER, linestyle="--", linewidth=1.5, label="Relevance threshold (0.50)")
    ax.set_title("Distribution of AI Relevance Scores", color=Color.TEXT_PRIMARY,
                 fontsize=12, fontweight="bold", loc="left")
    ax.set_xlabel("Relevance score")
    ax.set_ylabel("Number of articles")
    ax.legend(loc="upper left", fontsize=9)

    for spine in ax.spines.values():
        spine.set_color(Color.BORDER_SOFT)

    return fig


def build_correlation_heatmap_figure():
    """Correlation matrix heatmap across article-level numeric features."""
    labels = ["Relevance\nScore", "Keyword\nMatch", "Citation\nCount", "Pub.\nYear", "Journal\nImpact"]
    rng = np.random.default_rng(3)
    base = rng.normal(0, 1, (5, 400))
    weights = np.array([
        [1.0, 0.72, 0.35, -0.10, 0.55],
        [0.72, 1.0, 0.28, -0.05, 0.40],
        [0.35, 0.28, 1.0, 0.15, 0.62],
        [-0.10, -0.05, 0.15, 1.0, 0.08],
        [0.55, 0.40, 0.62, 0.08, 1.0],
    ])
    corr = weights  # symmetric, already in [-1, 1], used directly for a clean demo matrix

    fig, ax = plt.subplots(figsize=(6.4, 5.4), dpi=100)
    fig.subplots_adjust(left=0.22, right=0.95, top=0.90, bottom=0.18)

    cmap = plt.cm.get_cmap("RdBu_r")
    im = ax.imshow(corr, cmap=cmap, vmin=-1, vmax=1)

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=9, rotation=30, ha="right")
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_title("Feature Correlation Matrix", color=Color.TEXT_PRIMARY,
                 fontsize=12, fontweight="bold", loc="left")

    for i in range(len(labels)):
        for j in range(len(labels)):
            value = corr[i, j]
            text_color = "#1E1E1E" if abs(value) > 0.6 else Color.TEXT_PRIMARY
            ax.text(j, i, f"{value:.2f}", ha="center", va="center",
                    color=text_color, fontsize=9, fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color=Color.TEXT_MUTED, labelcolor=Color.TEXT_MUTED)
    cbar.outline.set_edgecolor(Color.BORDER_SOFT)

    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig


# ---------------------------------------------------------------------
# AI Model Evaluation (semantic similarity pipeline) — shared constants
# ---------------------------------------------------------------------

CATEGORY_LABELS = ["Highly Relevant", "Relevant", "Low Relevance", "Noise"]
CATEGORY_COLORS = [Color.SUCCESS, Color.PRIMARY, Color.WARNING, Color.DANGER]
CATEGORY_MARKERS = ["o", "s", "^", "x"]

# Similarity thresholds used to assign a category to an article
THRESHOLDS = {
    "Highly Relevant": 0.65,
    "Relevant": 0.50,
    "Low Relevance": 0.35,
    "Noise": 0.00,
}


def build_similarity_histogram_figure(metrics):
    """
    Histogram of the real cosine similarity scores.
    """
    if metrics is None:
        return build_empty_figure(
            "Run a search to generate metrics."
        )

    scores = np.array(metrics["similarity_scores"])

    fig, ax = plt.subplots(
        figsize=(9.6,3.8),
        dpi=100
    )

    fig.subplots_adjust(
        left=0.08,
        right=0.98,
        top=0.86,
        bottom=0.16
    )

    ax.hist(
        scores,
        bins=20,
        color=Color.PRIMARY,
        alpha=0.9,
        edgecolor=Color.BG_CARD
    )

    threshold = metrics["similarity_threshold"]

    ax.axvline(
        threshold,
        color=Color.DANGER,
        linestyle="--",
        linewidth=2,
        label=f"Threshold ({threshold:.2f})"
    )

    ax.set_title(
        "Similarity Score Distribution",
        fontsize=12,
        fontweight="bold",
        color=Color.TEXT_PRIMARY,
        loc="left"
    )

    ax.set_xlabel("Cosine Similarity")
    ax.set_ylabel("Articles")

    ax.legend()

    for spine in ax.spines.values():
        spine.set_color(Color.BORDER_SOFT)

    return fig


def build_category_bar_figure(metrics):
    """
    Horizontal bar chart using the real category counts.
    """

    if metrics is None:
        return build_empty_figure(
            "Run a search to generate metrics."
        )

    labels = [
        "Highly Relevant",
        "Relevant",
        "Low Relevance",
        "Noise"
    ]

    counts = [
        metrics["category_counts"].get("Highly Relevant", 0),
        metrics["category_counts"].get("Relevant", 0),
        metrics["category_counts"].get("Low Relevance", 0),
        metrics["category_counts"].get("Noise", 0),
    ]

    colors = [
        Color.SUCCESS,
        Color.PRIMARY,
        Color.WARNING,
        Color.DANGER,
    ]

    fig, ax = plt.subplots(
        figsize=(9.6,3.2),
        dpi=100
    )

    fig.subplots_adjust(
        left=0.22,
        right=0.96,
        top=0.88,
        bottom=0.16
    )

    y = np.arange(len(labels))

    bars = ax.barh(
        y,
        counts,
        color=colors,
        height=0.55
    )

    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    ax.invert_yaxis()

    ax.set_xlabel("Articles")

    ax.set_title(
        "Articles per Category",
        fontsize=12,
        fontweight="bold",
        color=Color.TEXT_PRIMARY,
        loc="left"
    )

    for bar, value in zip(bars, counts):

        ax.text(
            bar.get_width()+0.5,
            bar.get_y()+bar.get_height()/2,
            str(value),
            va="center",
            fontsize=10,
            fontweight="bold"
        )

    for spine in ax.spines.values():
        spine.set_color(Color.BORDER_SOFT)

    return fig

def build_category_pie_figure(metrics):
    """
    Pie chart using the real category counts.
    """
    
    if metrics is None:
        return build_empty_figure(
            "Run a search to generate metrics."
        )

    labels = [
        "Highly Relevant",
        "Relevant",
        "Low Relevance",
        "Noise"
    ]

    counts = [
        metrics["category_counts"].get("Highly Relevant",0),
        metrics["category_counts"].get("Relevant",0),
        metrics["category_counts"].get("Low Relevance",0),
        metrics["category_counts"].get("Noise",0),
    ]

    colors = [
        Color.SUCCESS,
        Color.PRIMARY,
        Color.WARNING,
        Color.DANGER,
    ]

    fig, ax = plt.subplots(
        figsize=(5.4,5),
        dpi=100
    )

    fig.subplots_adjust(
        left=0.05,
        right=0.95,
        top=0.88,
        bottom=0.05
    )

    wedges, _, _ = ax.pie(
        counts,
        colors=colors,
        autopct="%1.0f%%",
        startangle=90,
        pctdistance=0.75,
        wedgeprops={
            "linewidth":2,
            "edgecolor":Color.BG_CARD
        }
    )

    ax.legend(
        wedges,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5,-0.02),
        ncol=2,
        fontsize=9
    )

    ax.set_title(
        "Category Share",
        fontsize=12,
        fontweight="bold",
        color=Color.TEXT_PRIMARY
    )

    return fig

def build_pca_scatter_figure(metrics):
    """
    PCA projection of the real embedding vectors.
    """

    if metrics is None:
        return build_empty_figure(
            "Run a search to generate metrics."
        )

    embeddings = np.asarray(metrics["embeddings"])

    categories = metrics["dataframe"]["Category"].values

    projection = PCA(
        n_components=2,
        random_state=42
    ).fit_transform(embeddings)

    fig, ax = plt.subplots(
        figsize=(9.6,5.2),
        dpi=100
    )

    fig.subplots_adjust(
        left=0.08,
        right=0.98,
        top=0.90,
        bottom=0.10
    )

    config = {

        "Highly Relevant":(
            Color.SUCCESS,
            "o"
        ),

        "Relevant":(
            Color.PRIMARY,
            "s"
        ),

        "Low Relevance":(
            Color.WARNING,
            "^"
        ),

        "Noise":(
            Color.DANGER,
            "x"
        ),

    }

    for category,(color,marker) in config.items():

        mask = categories == category

        if mask.sum()==0:
            continue

        ax.scatter(

            projection[mask,0],

            projection[mask,1],

            color=color,

            marker=marker,

            s=45,

            alpha=0.85,

            edgecolors=Color.BG_CARD,

            linewidths=0.6,

            label=category

        )

    ax.set_title(
        "Embedding Projection (PCA)",
        fontsize=12,
        fontweight="bold",
        color=Color.TEXT_PRIMARY,
        loc="left"
    )

    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")

    ax.legend()

    for spine in ax.spines.values():
        spine.set_color(Color.BORDER_SOFT)

    return fig


def build_similarity_heatmap_figure(metrics):
    """
    Pairwise cosine similarity between the Top-10 most relevant articles.
    """

    if metrics is None:
        return build_empty_figure(
            "Run a search to generate metrics."
        )


    df = metrics["dataframe"]

    embeddings = np.asarray(metrics["embeddings"])

    top = (
        df
        .sort_values("Similarity", ascending=False)
        .head(10)
    )

    indices = top.index.to_numpy()

    matrix = cosine_similarity(
        embeddings[indices]
    )

    labels = [
        f"A{i+1}"
        for i in range(len(indices))
    ]

    fig, ax = plt.subplots(
        figsize=(7,6),
        dpi=100
    )

    fig.subplots_adjust(
        left=0.18,
        right=0.95,
        top=0.90,
        bottom=0.15
    )

    im = ax.imshow(
        matrix,
        cmap="YlGnBu",
        vmin=0,
        vmax=1
    )

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))

    ax.set_xticklabels(
        labels,
        rotation=45,
        fontsize=8
    )

    ax.set_yticklabels(
        labels,
        fontsize=8
    )

    ax.set_title(
        "Top-10 Article Similarity",
        fontsize=12,
        fontweight="bold",
        loc="left"
    )

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):

            ax.text(
                j,
                i,
                f"{matrix[i,j]:.2f}",
                ha="center",
                va="center",
                fontsize=7
            )

    fig.colorbar(im)

    return fig


def build_keywords_bar_figure(metrics):

    if metrics is None:
        return build_empty_figure(
            "Run a search to generate metrics."
        )

    df = metrics["dataframe"]

    text = ""

    for column in [

        "Author Keywords",

        "Index Keywords"

    ]:

        if column in df.columns:

            text += " ".join(

                df[column]
                .fillna("")
                .astype(str)
                .tolist()

            )

    words = re.findall(
        r"[A-Za-z][A-Za-z\-]+",
        text.lower()
    )

    stopwords = {

        "and",
        "or",
        "of",
        "the",
        "using",
        "based",
        "study",
        "analysis",
        "approach",
        "system",
        "method"

    }

    words = [

        w

        for w in words

        if w not in stopwords

        and len(w) > 3

    ]

    counter = Counter(words)

    top = counter.most_common(10)

    labels = [k for k,_ in top]

    counts = [v for _,v in top]

    fig, ax = plt.subplots(
        figsize=(9.6,4),
        dpi=100
    )

    y = np.arange(len(labels))

    bars = ax.barh(
        y,
        counts,
        color=Color.PRIMARY
    )

    ax.set_yticks(y)

    ax.set_yticklabels(labels)

    ax.invert_yaxis()

    ax.set_title(
        "Most Frequent Keywords",
        fontsize=12,
        fontweight="bold",
        loc="left"
    )

    for bar,value in zip(bars,counts):

        ax.text(

            value+0.2,

            bar.get_y()+bar.get_height()/2,

            str(value),

            va="center"

        )

    return fig


def build_threshold_bar_figure():
    """Horizontal gauge showing the similarity thresholds used for category assignment."""
    bounds = [0.0, 0.35, 0.50, 0.65, 1.0]
    labels = ["Noise", "Low Relevance", "Relevant", "Highly Relevant"]
    colors = [Color.DANGER, Color.WARNING, Color.PRIMARY, Color.SUCCESS]

    fig, ax = plt.subplots(figsize=(9.6, 2.2), dpi=100)
    fig.subplots_adjust(left=0.06, right=0.98, top=0.78, bottom=0.30)

    for i in range(len(bounds) - 1):
        width = bounds[i + 1] - bounds[i]
        ax.barh(0, width, left=bounds[i], color=colors[i], height=0.5, edgecolor=Color.BG_CARD, linewidth=2)
        ax.text(bounds[i] + width / 2, 0, labels[i], ha="center", va="center",
                fontsize=9, fontweight="bold", color="#1E1E1E")

    for b in bounds:
        ax.axvline(b, color=Color.BG_CARD, linewidth=2)
        ax.text(b, -0.42, f"{b:.2f}", ha="center", fontsize=9, color=Color.TEXT_MUTED)

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, 0.6)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("Category Assignment Thresholds (Cosine Similarity)", color=Color.TEXT_PRIMARY,
                 fontsize=12, fontweight="bold", loc="left")
    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig