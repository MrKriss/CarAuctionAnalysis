#Introduction

This analysis is a work in progress as I investage the hammer price that various cars fetched on the website 
[http://www.centralcarauctions.com](http://www.centralcarauctions.com), which runs online and showroom car auctions. The site keeps a back catalogue of all the cars they have ever sold, and what price they went for. 

The Python code and notbooks in this repository source updated data from this website, and step through the analysis I have performed. 

The work is predominantly exploritory in nature so far, though overall I am interested in looking at the following questions:

* What factors influence the hammer price?
* What models of car keep their value the longest?
* What models of car are most commonly auctioned?

#Installation

To replicate these results it is important to ensure that the environmnet I ran them in is reproduced on other machines. 
The easiest way to do this is to use the `conda` commnad line utility from Continuuim Analytics. 

This utility is part of their Python Anaconda Distribution [http://continuum.io/downloads#py34](http://continuum.io/downloads#py34), or can be installed separately as a minimal installation with their Miniconda installer [http://conda.pydata.org/miniconda.html](http://conda.pydata.org/miniconda.html)

`conda` not only handles the dependencies when installing packages, but can also sets up environments much like the virtualenv environments. These keep downloaded packages and versions isolated from each other. More info available [here](http://conda.pydata.org/docs/intro.html).

Once `conda` is installed, to setup an environment and install the required dependencies into it, run: 

```
conda create --name <env_name> --file conda_requirements.txt
```

Then the following will activate the environment (by putting it at the front of your PATH)

```
source activate <env_name>
```

The environment can be deactivated by running the following (which will reset your PATH back to how it was):

```
source deactivate
```

## A Note on Compatibility

The notebook files in this repository have been generated using the latest IPython 3.0 format for .ipynb files, these may not display correctly on earlier versions of IPython.  

All code was developed on Python 3.4 and has not been tested on Python 2.x . However there is no need to install Python 3 globally if installing with conda above, as the Python 3 that is installed will be isolated to the specified virtual environment. 

Tested and developed on MacBook Pro, Mid 2010, OS X 10.10.2

# Running the Analysis

The following files are provided in this repository:

1. `source_data.py`  -  Functions within this script handle the fetching, parsing and preprocessing of data from the [central car auctions website](http://www.centralcarauctions.com/trade/vehicles/price-guide/price-guide?page=1). These functions are called by `Car_Auction_EDA.ipnb` to produce the following files: 
    * `cca_data_raw.csv` - The raw data before preprocessing. 
    * `cca_data_pro.csv` - The data after preprocessing.
    * `cca_data_enc.csv` - The data after all categorical variables have been encoded. This is necessary for the analysis performed in `Car_Auction_Preliminary_Analysis_GBRT.ipynb`
    * `decoder.pkl` - A dictionary of arrays that map back from the encoded data to their original values. 
2. `Car_Auction_EDA.ipnb`  -  Sources the data if necessary using `source_data.py` or loads from disk. Conducts exploratory data analysis on the preprocessed and data generated.
3. `Car_Auction_Preliminary_Analysis_GBRT.ipynb`  -  Performs preliminary analysis using Gradient Boosting Regression Trees. The loss function is investigated along with deviance and feature importance plots. 

The IPython notebook can be started in the cloned directory by first navigating to it, and running:

```
ipython notebook --notebook-dir=.
```





