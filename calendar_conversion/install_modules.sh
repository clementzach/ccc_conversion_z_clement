



for package in arrow datetime ics pandas numpy openpyxl
do
	pip3 install $package
done

python3 ics_to_excel.py