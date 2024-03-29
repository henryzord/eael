# A Survey of Evolutionary Algorithms for Supervised Ensemble Learning

This repository is a supplementary material to the paper 

> Cagnini, Henry E.L., das Dôres, Silvia C.N., Freitas, Alex A., Barros, Rodrigo C. A Survey of Evolutionary Algorithms 
> for Supervised Ensemble Learning. In Knowledge Engineering Review. 2022.

The data shown here was used to generate tables and figures in the paper. 



## Contents

* [bibliography.bib](bibliography.bib): The bibliography as used in the LaTeX project. Contains references not only for
  surveyed papers, but for other work too.
* [data.json](data.json): Metadata on the reviewed papers featured in the survey. 
* [index.html](index.html): a master table, compiled from the [data.json](data.json) file, that shows all collected 
  information on reviewed papers. You can view the rendered page in 
  [https://henryzord.github.io/eael](https://henryzord.github.io/eael).

## Installation

These instructions are only necessary if you want to manipulate the metadata.

This repository uses Python and [Anaconda](https://www.anaconda.com/products/individual) in order to run - but it 
probably also runs on virtualenv.

### If using Anaconda

1. Create a new environment:
   
   ```bash
   conda create --name eael --yes
   ```
   
2. Activate it: 

   ```bash
   conda activate eael
   ```

3. Install conda libraries:

   ```bash
   conda install --file conda_requirements.txt -c conda-forge --yes
   ```
   
4. Install pip libraries:

   ```bash
   pip install --requirement pip_requirements.txt
   ```
   
## Usage

There are two main scripts:

* [scripts/base_learners.py](scripts/base_learners.py): generates the base learners figure in the paper.
* [scripts/master_table.py](scripts/master_table.py): generates the master table page.
