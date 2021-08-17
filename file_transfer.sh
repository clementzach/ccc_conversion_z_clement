
echo "starting file reformat procedure"

python3 extract_by_location.py

Rscript merge_spreadsheets.R


if ! [ -d used_files ] ; then
mkdir used_files
fi

for file in ./*.pdf; do
        mv "$file" used_files
done

for file in ./*.xlsx; do
        mv "$file" used_files
done

echo "file reformat procedure completed. The pdf and excel files used were moved to the used_files folder"
