
echo "starting file reformat procedure"

python3 extract_by_location.py

Rscript merge_spreadsheets.R

echo "file reformat completed"
