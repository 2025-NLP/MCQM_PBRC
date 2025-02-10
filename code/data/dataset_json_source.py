import json

def convert_to_json_format(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        sentences = []
        labels = {"PER": [], "LOC": [], "ORG": [], "MISC": []}  # Initialize with new label types
        for line in f:
            if line.strip():  # Skip empty lines
                if line.startswith('-DOCSTART-'):  # Skip lines starting with -DOCSTART-
                    continue
                    
                parts = line.strip().split()
                word = parts[0]
                tag = parts[-1]  # Assume the label is in the last column
                
                sentences.append(word)  # Add word to sentence
                if tag.startswith('B-'):
                    entity = tag[2:].upper()  # Convert entity type to uppercase
                    labels[entity].append(word)  # New entity
                elif tag.startswith('I-'):
                    entity_key = tag[2:].upper()  # Get current entity type
                    if entity_key in labels and labels[entity_key]:  # Ensure entity type exists and is not empty
                        labels[entity_key][-1] += " " + word  # Add word to current entity

            else:
                if sentences:  # If an empty line is encountered, the previous sentence is complete
                    # Keep only the existing entity types
                    filtered_labels = {key: [val.strip() for val in labels[key]] for key in labels if labels[key]}
                    data.append({"text": " ".join(sentences), "label": filtered_labels})
                    sentences = []
                    labels = {"PER": [], "LOC": [], "ORG": [], "MISC": []}  # Reset labels

        # Process the last sentence at the end of the file
        if sentences:
            filtered_labels = {key: [val.strip() for val in labels[key]] for key in labels if labels[key]}
            data.append({"text": " ".join(sentences), "label": filtered_labels})

    return data

# Example usage
json_data = convert_to_json_format('./conll2003/train.txt')
# Save the data as a JSON file, with each entry on a new line
with open('./conll2003/train.json', 'w', encoding='utf-8') as f:
    for entry in json_data:
        json.dump(entry, f, ensure_ascii=False)
        f.write('\n')  # Each entry on a new line

print("Conversion completed.")
