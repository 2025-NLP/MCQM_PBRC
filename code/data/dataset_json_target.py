import json

def get_labels_by_domain(domain):
    if domain == "literature":
        return [
            "book", "writer", "award", "poem", "event", "magazine", 
            "person", "location", "organisation", "country", "misc", "literarygenre"
        ]
    elif domain == "politics":
        return [
            "politician", "person", "organisation", "politicalparty", 
            "event", "election", "country", "location", "misc"
        ]
    elif domain == "science":
        return [
            "scientist", "person", "university", "organisation", 
            "country", "location", "discipline", "enzyme", "protein", 
            "chemicalcompound", "chemicalelement", "event", "astronomicalobject", 
            "academicjournal", "award", "theory", "misc"
        ]
    elif domain == "music":
        return [
            "musicgenre", "song", "band", "album", "musicalartist", 
            "musicalinstrument", "award", "event", "country", "location", 
            "organisation", "person", "misc"
        ]
    elif domain == "ai":
        return [
            "field", "task", "product", "algorithm", "researcher", 
            "metrics", "university", "country", "person", "organisation", 
            "location", "misc", "conference", "programlang"
        ]
    else:
        return []


def convert_ner_to_json_with_cot(file_path, target_file_path, cot_file_path=None):
    data = []

    # Read the cot.txt file content (if cot_file_path is provided)
    cot_data = []
    if cot_file_path:
        with open(cot_file_path, 'r', encoding='utf-8') as cot_file:
            current_cot = []
            for line in cot_file:
                line = line.strip()
                if line:  # Non-empty line
                    current_cot.append(line)
                elif current_cot:  # If an empty line is encountered and we have content, save the current cot
                    cot_data.append(" ".join(current_cot))
                    current_cot = []
            if current_cot:  # If there is remaining content at the end of the file
                cot_data.append(" ".join(current_cot))

    # Read the original dataset file and process it
    with open(file_path, 'r', encoding='utf-8') as f:
        sentences = []

        labels = get_labels_by_domain("ai")
        print(labels)

        cot_index = 0  # Index for the cot content

        for line in f:
            if line.strip():  # Non-empty line
                if line.startswith('-DOCSTART-'):  # Skip lines starting with -DOCSTART-
                    continue
                
                parts = line.strip().split()
                word = parts[0]
                tag = parts[-1]  # Assuming the label is in the last column
                
                sentences.append(word)  # Add word to sentence
                if tag.startswith('B-'):
                    entity_type = tag[2:].lower()  # Convert entity type to lowercase
                    labels[entity_type].append(word)  # New entity
                elif tag.startswith('I-'):
                    entity_type = tag[2:].lower()  # Get current entity type
                    if entity_type in labels and labels[entity_type]:  # Ensure entity type exists and is not empty
                        labels[entity_type][-1] += " " + word  # Add word to current entity

            else:  # Empty line encountered, indicating the end of a sentence
                if sentences:  # Process the current sentence
                    filtered_labels = {key: [val.strip() for val in labels[key]] for key in labels if labels[key]}
                    # Get corresponding cot information (if available)
                    cot_info = cot_data[cot_index] if cot_index < len(cot_data) else "" if cot_file_path else ""
                    data.append({
                        "text": " ".join(sentences),
                        "label": filtered_labels,
                        "cot": cot_info
                    })
                    sentences = []
                    labels = {key: [] for key in labels}  # Reset labels
                    cot_index += 1  # Move to the next cot content

        # Process any remaining sentence at the end of the file
        if sentences:
            filtered_labels = {key: [val.strip() for val in labels[key]] for key in labels if labels[key]}
            cot_info = cot_data[cot_index] if cot_index < len(cot_data) else "" if cot_file_path else ""
            data.append({
                "text": " ".join(sentences),
                "label": filtered_labels,
                "cot": cot_info
            })

    # Save the result as a JSON file, with each entry on a new line
    with open(target_file_path, 'w', encoding='utf-8') as f:
        for entry in data:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')  # Each entry on a new line

    print(f"Conversion completed, saved as {target_file_path}")

# Example usage
convert_ner_to_json_with_cot(
    './ner_data/ai/test.txt',
    './ner_data/ai/test.json',
    './ner_data/ai/test_cot.json'
)
