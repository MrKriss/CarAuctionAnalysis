#Instalation

the easiest way to install dependencies and ensure a reproducable environment for this analysis is to install with the conda utility. Conda as part of the Python Anaconda Distribution [http://continuum.io/downloads#py34](http://continuum.io/downloads#py34), or the Miniconda installed [http://conda.pydata.org/miniconda.html](http://conda.pydata.org/miniconda.html)

To set up a virtual environment and install all the requirements run: 

```
conda create --name <env_name> --file conda_requirements.txt
```

Then the following will activate the environment

```
source activate <env_name>
```

The envornment can be deactivated by running

```
source deactivate
```

# Compatibility

The notebook files in this repository have been generated using the latest IPython 3.0 format for .ipynb, these may not display correctly on earlier versions of IPython.  

All code was developed on Python 3.4

# Running the Analysis




Three notebooks are provided in this repository along with the raw data:

* Car_Auction_Data_Prep.ipnb
