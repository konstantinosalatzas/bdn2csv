# bdn2csv

bdn2csv is a Python parser that converts SAS Business Data Network (BDN) XML Export file to CSV Import file

As the SAS BDN can be:

* imported from XML or CSV file but
* exported only to XML file,

bdn2csv transforms an XML Export file into an equivalent CSV Import file:

* for a user to edit it manually as a spreadsheet,

* for a developer to process it programmatically as a table

and to import the result CSV file into SAS BDN.

## Usage

### As a module

Example:

```py
import bdn2csv

bdn2csv.convert(xml_path="./Export.xml", csv_path="./Import.csv")
```

### As a CLI

Example:

```sh
cd bdn2csv
python bdn2csv.py ./Export.xml ./Import.csv
```

## Installation

### From source

```sh
git clone https://github.com/konstantinosalatzas/bdn2csv.git
cd bdn2csv
python -m pip install bdn2csv
```

## Extra features

### path2id

The path2id feature:

* parses SAS BDN REST API GET /terms response JSON and
* computes the one-to-one mapping between term paths and ids

to construct a CSV file with term path and id as columns, each row corresponding to a term.

Example of usage as a CLI:

```sh
cd bdn2csv
python bdn2csv.py --path2id ./Response.json ./path2id.csv
```

### viz

The viz feature:

* constructs a directed graph with:
  - vertices corresponding to terms and
  - edges corresponding to term relationships,

* plots and saves the graph as a PNG image

to visualize the BDN terms and the relationships between them.

Example of usage:

```py
import bdn2csv

bdn2csv.visualize(csv_path="./Import.csv", png_path="./viz.png")
```
