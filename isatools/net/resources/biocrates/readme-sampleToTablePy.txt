To run sampleToTable.py, you must first create your virtual environment for the application.

1) First create a folder called venv
	> mkdir venv
2) Then you create the virtual environment
	> virtualenv venv
3) Activate the virtual environment
	> source venv/bin/activate
4) As sampleToTable.py uses the Beautiful Soup package, you would need to install Beautiful Soap in your virtual environment
	> pip install beautifulsoup4
5) Now you are ready to run the convertor
	> python sampleToTable.py biocrates-shorter-testfile.xml