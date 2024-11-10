import subprocess
import pandas as pd
import os

def run_white_rabbit(scan_file):
    output_file = os.path.join(os.path.dirname(scan_file), "scan_report.csv")
    command = ["java", "-jar", "whiterabbit-1.0.0.jar", "-s", scan_file, "-o", output_file]
    subprocess.run(command, check=True)
    print(f"White Rabbit scan report: {output_file}")
    return output_file

def run_rabbit_in_hole(scan_report):
    mapping_file = os.path.join(os.path.dirname(scan_report), "rabbit_mapping.csv")
    command = ["java", "-jar", "rabbitinahat-1.0.0.jar", "-i", scan_report, "-o", mapping_file]
    subprocess.run(command, check=True)
    print(f"Rabbit-in-a-Hole mapping: {mapping_file}")
    return mapping_file

def run_usagi_mapping(source_file):
    output_mapping = os.path.join(os.path.dirname(source_file), "usagi_mappings.csv")
    command = ["java", "-jar", "usagi_v1.4.3.jar", "-i", source_file, "-o", output_mapping, "-vocab", "athena_vocab_path/"]
    subprocess.run(command, check=True)
    print(f"Usagi mapping completed: {output_mapping}")
    return output_mapping

def load_and_check_mappings(output_mapping):
    mapping_df = pd.read_csv(output_mapping)
    # Post-processing, validation, or cleaning here
    return mapping_df

def automate_omop_mapping(scan_file, source_file):
    output_file = run_white_rabbit(scan_file)
    mapping_file = run_rabbit_in_hole(output_file)
    output_mapping = run_usagi_mapping(source_file)
    mapping_df = load_and_check_mappings(output_mapping)
    print("Mapping process completed.")
    return mapping_df

# Eg
scan_file = "path/to/your/source_data_file.csv"
source_file = "path/to/your/source_codes.csv"

final_mapping = automate_omop_mapping(scan_file, source_file)