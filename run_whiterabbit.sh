#!/bin/bash

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <output_consolidated_report.xlsx> <path_to_data_file1.csv> <path_to_data_file2.csv> ..."
  exit 1
fi

# Arguments
OUTPUT_REPORT=$1          # Path to the final consolidated report (e.g., consolidated_report.xlsx)
shift                     # Shift to access the remaining arguments (input data files)
DATA_FILES=("$@")         # Array of paths to input data files

WHITE_RABBIT_JAR="scripts/WhiteRabbit.jar"
RABBIT_IN_A_HAT_JAR="scripts/RabbitInAHat.jar"
COMBINE_REPORTS_SCRIPT="scripts/combine_reports.py"

TEMP_REPORT_FILES=()

echo "Running WhiteRabbit on multiple files..."
for DATA_FILE in "${DATA_FILES[@]}"; do
  BASENAME=$(basename "$DATA_FILE" .csv)
  TEMP_REPORT="temp_${BASENAME}_report.xlsx"
  
  echo "Running WhiteRabbit on $DATA_FILE..."
  java -jar "$WHITE_RABBIT_JAR" -s "$DATA_FILE" -o "$TEMP_REPORT"

  if [ $? -ne 0 ]; then
    echo "WhiteRabbit failed to create the profiling report for $DATA_FILE."
    exit 1
  fi

  echo "WhiteRabbit report for $DATA_FILE saved to $TEMP_REPORT"
  TEMP_REPORT_FILES+=("$TEMP_REPORT")
done

echo "Combining individual WhiteRabbit reports into $OUTPUT_REPORT..."
python "$COMBINE_REPORTS_SCRIPT" "$OUTPUT_REPORT" "${TEMP_REPORT_FILES[@]}"

if [ $? -ne 0 ]; then
  echo "Failed to combine WhiteRabbit reports."
  exit 1
fi

echo "Combined report saved as $OUTPUT_REPORT"

echo "Opening RabbitInAHat for mapping..."
java -jar "$RABBIT_IN_A_HAT_JAR" "$OUTPUT_REPORT"

echo "RabbitInAHat launched for manual mapping. Please complete the mapping in the RabbitInAHat interface."
