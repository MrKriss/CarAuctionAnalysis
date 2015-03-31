#Installation

The easiest way to install dependencies and ensure a reproducible environment for this analysis is to use the `conda` utility. `conda` is part of the Python Anaconda Distribution [http://continuum.io/downloads#py34](http://continuum.io/downloads#py34), or can be installed separately as a minimal installation with the Miniconda installer [http://conda.pydata.org/miniconda.html](http://conda.pydata.org/miniconda.html)

To set up a virtual environment and install all the requirements run: 

```
conda create --name <env_name> --file conda_requirements.txt
```

Then the following will activate the environment

```
source activate <env_name>
```

The environment can be deactivated by running

```
source deactivate
```

## A Note on Compatibility

The notebook files in this repository have been generated using the latest IPython 3.0 format for .ipynb, these may not display correctly on earlier versions of IPython.  

All code was developed on Python 3.4 and has not been tested on Python 2.x . However there is no need to install Python 3 globally if installing with conda above, as the Python 3 that is installed will be isolated to the specified virtual environment. 

Tested and developed on MacBook Pro, Mid 2010, OS X 10.9.5

# Running the Analysis

The following files are provided in this repository:

1. centralcarauctions.html  -  This is the raw data captured in HTML format from the [central car auctions website](http://www.centralcarauctions.com/trade/vehicles/price-guide/price-guide?page=1) on July 2014.
2. Car_Auction_Data_Prep.ipnb  -  As well as saving the data to csv as `car_auction_raw.csv`, this file preprocesses the raw data to produce a `car_auction_processed.csv` and then encodes the features to produce a `car_auction_enc.csv` file.
3. Car_Auction_EDA.ipnb  -  Conducts exploratory data analysis on the preprocessed and encoded data previously generated.
4. Car_Auction_Preliminary_Analysis_GBRT.ipynb  -  Performs preliminary analysis using Gradient Boosting Regression Trees. The loss function is investigated along with deviance and feature importance plots. 

Once the virtual environment is setup and is activate, these notebooks should be run in order 2 to 4 as listed above so that intermittent data files are created. 

The IPython notebook can be started in the cloned directory by first navigating to it, then running:

```
ipython notebook --notebook-dir=.
```





