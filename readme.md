## CAPP 30122 Final Project: Chicago Public Schools SQRP Playground
### Ali Pelczar, Lily Grier, and Launa Greer
 
#### A Django web application. Allows users to build a school quality rating policy (SQRP) for the Chicago Public Schools (CPS). Uses the model configuration to rate each high school in the district and then generate a bias score for the SQRP as a whole.  Data is visualized through a map, list of school records, and series of regression plots.

![alt text](sqrp/static/img/Configure_Model.JPG "Configure Model")

![alt text](sqrp/static/img/View_Results.JPG "View Results")

![alt text](sqrp/static/img/View_Bias_Score.JPG "View Bias Score")


**Language Requirements:**  
Python-3.8.1

**VM Setup:**  
(1) Ensure that Python-3.8.1 has been installed in the 'usr/local/bin' folder.
(Other locations can be used, but the script in the next step will have to be
modified accordingly.) If building Python [on Ubuntu from source](https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/),
the package 'libsqlite3-dev' must be installed first with `apt-get install libsqlite3-dev`.

(2) Run the command `bash install.sh` from the project root. The script verifies the
current installation of Python; creates a new virtual environment, 'env'; and
then installs all required packages in that environment using the requirements.txt file.

(3) Activate the virtual environment with the command `source env/bin/activate`.
To deactivate it, type `deactivate`.

(4) Launch the Django web application from the project root with the
command `python3 manage.py runserver`. Once the server is running,
navigate to your local webhost, `http://127.0.0.1:8000/`, in your broswer of 
choice. The page usually takes 5-10 seconds to load due to the presence of a 
map and the dynamic creation of SVG plots through the matplotlib package. Future
iterations of this project would attempt to cut down this load time. For optimal
performance, it is recommended to launch the project from Visual Studio code
instead of running it in the VM.

There is also a bug in Ubuntu in which the Django server states that the port is
already in use. To resolve this error should it arise, kill the associated processes 
with `sudo fuser -k 8000/tcp`. To stop the server at any time, press `Ctrl-C`.

(5) Optionally test the creation and population of the database tables by 
running the command `python3 -m core.clients.dbclient` from the project root.
It deletes the tables if they exist and then rebuilds them again using the 
`setup()` function in `dbclient.py`.

**Description:**  
In the web interface, a user may adjust slider widgets to set the 
relative weights for each school indicator. (The page is initialized with the
weights from the 2018-2019 school year.) If the user does not want to include an
input in the rating system, the user should leave that input’s weight as zero.

The backend program takes those inputs, generates a rating system based on those
inputs, and assigns each school a rating accordingly. If inputs are missing for
a particular school, the algorithm reassigns those weights to a different inputs
(for details about this reassignment, see the “Reassignment Logic” section of
the Appendix). Finally, the backend calculates a bias score for the user's SQRP
model, which communicates how well schools’ scores align with the 
demographics of their student bodies. The interface returns the bias score for 
the specified policy along with individual ratings for each of the schools and a
series of three regression plots.