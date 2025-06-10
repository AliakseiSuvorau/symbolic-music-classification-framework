import simplejson as json
from collections import Counter
import config
import matplotlib.pyplot as plt


def display_bar_plot(labels, counts, x_label, y_label, title):
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='skyblue')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


with open(config.tagged_midis_file, 'r') as f:
    data = json.load(f)

genre_counts = Counter(entry['genre'] for entry in data)

genres = list(genre_counts.keys())
counts = list(genre_counts.values())

display_bar_plot(
    labels=genres,
    counts=counts,
    x_label="Genres",
    y_label="# records",
    title="Distribution of data between classes"
)
