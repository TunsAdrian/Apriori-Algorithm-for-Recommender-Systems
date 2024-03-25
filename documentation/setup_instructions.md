# Setup Instructions

The project was implemented completely using Python 3.x version, using the following libraries: "csv", "operator", "itertools" and "collections". 

In order to install and run the application, a system capable of running Python 3.x is needed, requiring therefore:
    
- Operating System: Linux- Ubuntu 16.04 to 17.10, or Windows 7 to 10 
- RAM Memory: 2GB (4GB preferable)

The recommended way of running the project on a system where Python 3.x version is installed is the following:
	
- Open the project in an IDE (e.g. PyCharm IDE)
- Configure a new interpreter using the locally installed Python distribution
  - Recommendation: create a virtual environment on which the corresponding libraries will be installed
- Install the required libraries ("csv", "operator", "itertools" and "collections"), using pip or other package installers
- For using the application from a terminal, without the GUI part:
  - Go at the end of the file, and uncomment one of the desired function calls, from the three main functions:
    - start_data_mining() - used to start the actual data mining
    - get_length_itemsets(1) - used to get the n-length itemsets; Note: replace "1" with desired "n" value
    - movie_recommendation() - used to make a movie recommendation
- For using the application with the GUI part:
  - Go to the gui.py file and run it


