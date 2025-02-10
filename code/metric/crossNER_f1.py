import json
from collections import Counter

def calculate_metrics(pred_file, true_file, label_list):
    """
    Calculate precision, recall, and F1 score for different labels in NER task.
    
    Args:
        pred_file (str): Path to the prediction file (JSON format).
        true_file (str): Path to the ground truth file (JSON format).
        label_list (list): List of labels to evaluate.

    Returns:
        dict: Label-wise precision, recall, and F1 scores.
        dict: Overall metrics (micro, macro, weighted).
    """
    
    # Load the prediction and true data from JSON files
    with open(pred_file, "r", encoding="utf-8") as f:
        pred_data = [json.loads(line) for line in f]

    with open(true_file, "r", encoding="utf-8") as f:
        true_data = [json.loads(line) for line in f]

    # Initialize counts for true positives, predictions, and true entities
    true_counts = {label: 0 for label in label_list}
    pred_counts = {label: 0 for label in label_list}
    tp_counts = {label: 0 for label in label_list}

    # Iterate through the true and predicted entities for each item
    for true_item, pred_item in zip(true_data, pred_data):
        for label in label_list:
            # Get the list of true and predicted entities for the current label
            true_entities = true_item['label'].get(label, [])
            pred_entities = pred_item['label'].get(label, [])

            # Update the true and predicted counts for the label
            true_counts[label] += len(true_entities)
            pred_counts[label] += len(pred_entities)

            # Count the occurrences of each entity in true and predicted lists
            true_counter = Counter(true_entities)
            pred_counter = Counter(pred_entities)

            # Calculate true positives for the label
            for entity in pred_counter:
                if entity in true_counter:
                    tp_counts[label] += min(true_counter[entity], pred_counter[entity])

    # Calculate precision, recall, and F1 for each label
    results = {}
    for label in label_list:
        precision = tp_counts[label] / pred_counts[label] if pred_counts[label] > 0 else 0
        recall = tp_counts[label] / true_counts[label] if true_counts[label] > 0 else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

        results[label] = {
            "precision": precision,
            "recall": recall,
            "f1": f1
        }

    # Calculate overall (micro, macro, weighted) metrics
    total_tp = sum(tp_counts.values())
    total_pred = sum(pred_counts.values())
    total_true = sum(true_counts.values())

    # Micro-average metrics
    micro_precision = total_tp / total_pred if total_pred > 0 else 0
    micro_recall = total_tp / total_true if total_true > 0 else 0
    micro_f1 = (2 * micro_precision * micro_recall / (micro_precision + micro_recall)) if (micro_precision + micro_recall) > 0 else 0

    # Macro-average metrics
    macro_precision = sum([results[label]["precision"] for label in results if results[label]["precision"] > 0]) / len(results)
    macro_recall = sum([results[label]["recall"] for label in results if results[label]["recall"] > 0]) / len(results)
    macro_f1 = (2 * macro_precision * macro_recall / (macro_precision + macro_recall)) if (macro_precision + macro_recall) > 0 else 0

    # Weighted-average metrics
    weighted_precision = sum([(true_counts[label] / total_true) * results[label]["precision"] for label in results if total_true > 0])
    weighted_recall = sum([(true_counts[label] / total_true) * results[label]["recall"] for label in results if total_true > 0])
    weighted_f1 = (2 * weighted_precision * weighted_recall / (weighted_precision + weighted_recall)) if (weighted_precision + weighted_recall) > 0 else 0

    # Return the results
    return results, {
        "micro_precision": micro_precision,
        "micro_recall": micro_recall,
        "micro_f1": micro_f1,
        "macro_precision": macro_precision,
        "macro_recall": macro_recall,
        "macro_f1": macro_f1,
        "weighted_precision": weighted_precision,
        "weighted_recall": weighted_recall,
        "weighted_f1": weighted_f1
    }

# Define label sets for different domains
label_list_science = [
    "scientist", "person", "university", "organisation", "country", 
    "location", "discipline", "enzyme", "protein", "chemicalcompound", 
    "chemicalelement", "event", "astronomicalobject", "academicjournal", 
    "award", "theory", "misc"
]

label_list_politics = [
    "politician", "person", "organisation", "politicalparty", "event", 
    "election", "country", "location", "misc"
]

label_list_music = [
    "musicgenre", "song", "band", "album", "musicalartist", "musicalinstrument", 
    "award", "event", "country", "location", "organisation", "person", "misc"
]

label_list_ai = [
    "field", "task", "product", "algorithm", "researcher", "metrics", 
    "university", "country", "person", "organisation", "location", 
    "misc", "conference", "programlang"
]

label_list_literature = [
    "book", "writer", "award", "poem", "event", "magazine", 
    "person", "location", "organisation", "country", "misc", "literarygenre"
]

# Example configuration: Choose the domain you want (science, politics, music, etc.)
domain = "politics"  # Change this line to select the domain ('science', 'politics', 'music', etc.)

# Set the label list based on the chosen domain
if domain == "science":
    label_list = label_list_science
elif domain == "politics":
    label_list = label_list_politics
elif domain == "music":
    label_list = label_list_music
elif domain == "ai":
    label_list = label_list_ai
elif domain == "literature":
    label_list = label_list_literature
else:
    raise ValueError("Unsupported domain. Please choose 'science', 'politics', 'music', 'ai', or 'literature'.")

# Provide paths to prediction and ground truth files
pred_file_path = r"G:/NER/NER/flan_t5_crossner_output/politics/cot_politics.json"
true_file_path = r"G:/NER/NER/CrossNER-main/ner_data/politics/dev.json"

# Call the function and get results
label_metrics, overall_metrics = calculate_metrics(pred_file_path, true_file_path, label_list)

# Print the label-wise metrics
print("Label-wise Metrics:")
for label, metrics in label_metrics.items():
    print(f"{label}: Precision: {metrics['precision']:.4f}, Recall: {metrics['recall']:.4f}, F1: {metrics['f1']:.4f}")

# Print the overall metrics (micro, macro, weighted)
print("\nMicro Metrics:")
print(f"Micro Precision: {overall_metrics['micro_precision']:.4f}")
print(f"Micro Recall: {overall_metrics['micro_recall']:.4f}")
print(f"Micro F1: {overall_metrics['micro_f1']:.4f}")

print("\nMacro Metrics:")
print(f"Macro Precision: {overall_metrics['macro_precision']:.4f}")
print(f"Macro Recall: {overall_metrics['macro_recall']:.4f}")
print(f"Macro F1: {overall_metrics['macro_f1']:.4f}")

print("\nWeighted Metrics:")
print(f"Weighted Precision: {overall_metrics['weighted_precision']:.4f}")
print(f"Weighted Recall: {overall_metrics['weighted_recall']:.4f}")
print(f"Weighted F1: {overall_metrics['weighted_f1']:.4f}")
