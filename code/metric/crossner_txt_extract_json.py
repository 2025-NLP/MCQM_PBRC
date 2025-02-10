import json

def convert_to_json(input_path, output_path, valid_labels):
    """
    Convert a plain text file with labeled data into a JSON format.

    Args:
        input_path (str): Path to the input text file.
        output_path (str): Path to the output JSON file.
        valid_labels (list): List of valid labels to consider while parsing.
    """
    data=[]
    with open(input_path, "r", encoding="utf-8") as file:
        current_text = None
        current_label = {k: [] for k in valid_labels}  # Initialize label dictionary
        count = 0
        for line in file:
            line = line.strip()
            count += 1
            if line.startswith("input:"):
                # Handle new example
                current_text = line[len("input: "):].strip()
                current_label = {k: [] for k in valid_labels}  # Reset labels

            elif line.startswith("result:"):
                # Extract content after "result:" and remove the prefix
                result = line[len("result: "):].strip()

                # Split by semicolon to separate each label part
                parts = result.split("; ")
                for part in parts:
                    part = part.strip()  # Remove extra spaces
                    if "->" in part:
                        # Split label and entity
                        try:
                            label_part, entity_part = part.split(": ", 1)
                            entity_type = label_part.strip().lower()  # Normalize label type

                            # Remove prefix from entity type
                            entity_type = entity_type.split("->", 1)[-1].strip()

                            # Check if the label is in the valid labels list
                            if entity_type in valid_labels:
                                entities = [name.strip() for name in entity_part.split(",") if name.strip()]  # Split and clean entities
                                current_label[entity_type].extend(entities)  # Add entities to the label
                            else:
                                print(line)
                                print(count)
                                print(f"Warning: Unrecognized label type '{entity_type}' encountered.")  # Output warning
                        except:
                            print(line)
                            print(count)

            elif line == "" and current_text is not None:
                # Add the current example to the data list
                example = {
                    "text": current_text,
                    "label": {k: v for k, v in current_label.items() if v}  # Only include non-empty labels
                }
                data.append(example)

                # Reset current_text and current_label
                current_text = None
                current_label = {k: [] for k in valid_labels}

    # Write all examples into the JSON file, one per line
    with open(output_path, "w", encoding="utf-8") as json_file:
        for entry in data:
            json_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

# Example usage: Choose your valid labels list dynamically
valid_labels_science = [
    "scientist", "person", "university", "organisation", "country", 
    "location", "discipline", "enzyme", "protein", "chemicalcompound", 
    "chemicalelement", "event", "astronomicalobject", "academicjournal", 
    "award", "theory", "misc"
]

valid_labels_politics = [
    "politician", "person", "organisation", "politicalparty", "event", 
    "election", "country", "location", "misc"
]

valid_labels_music = [
    "musicgenre", "song", "band", "album", "musicalartist", "musicalinstrument", 
    "award", "event", "country", "location", "organisation", "person", "misc"
]

valid_labels_technology = [
    "field", "task", "product", "algorithm", "researcher", "metrics", 
    "university", "country", "person", "organisation", "location", 
    "misc", "conference", "programlang"
]

valid_labels_literature = [
    "book", "writer", "award", "poem", "event", "magazine", 
    "person", "location", "organisation", "country", "misc", "literarygenre"
]

# Example configuration: Choose the domain you want (science, politics, music, etc.)
domain = "science"  # Change this line to select the domain ('science', 'politics', 'music', etc.)

# Set the valid labels based on the chosen domain
if domain == "science":
    valid_labels = valid_labels_science
elif domain == "politics":
    valid_labels = valid_labels_politics
elif domain == "music":
    valid_labels = valid_labels_music
elif domain == "technology":
    valid_labels = valid_labels_technology
elif domain == "literature":
    valid_labels = valid_labels_literature
else:
    raise ValueError("Unsupported domain. Please choose 'science', 'politics', 'music', 'technology', or 'literature'.")

# Call the function with input and output paths
convert_to_json(r"G:/NER/NER/flan_t5_crossner_output/science/science_test.txt", 
                r"G:/NER/NER/flan_t5_crossner_output/science/science_test_2.json", 
                valid_labels)
