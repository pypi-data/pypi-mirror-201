Power Markets
===============

This package includes data from power markets in Europe.

After installing the package, data is available as an [intake catalog](https://intake.readthedocs.io/en/latest/index.html). As an example:

```python
import intake

generation = intake.cat["markets"].generation(country="EL").read()
available_capacity = intake.cat["markets"].capacity(country="EL").read()
```

In addition, the package offers two CLI commands: one to download data from TSOs and one to extract datasets.


The type of data to download can be:
- `dispatch` includes the inputs and results of the day-ahead scheduling
- `availabilities` includes data about the available capacity for all dispatchable power
generation units
- `reservoirs` includes data about the filling rates of the hydropower plants
- `ntc` includes data about the net transfer capability for power imports and exports.


The datasets to extract from the raw data can be:
- `load`: extracts the load dataset from the `dispatch` data
- `reserves`: extracts the secondary reserves dataset from the `dispatch` data
- `committed`: extracts the committed capacity dataset from the `dispatch` data
- `imports`: extracts the power imports dataset from the `dispatch` data
- `exports`: extracts the power exports dataset from the `dispatch` data
- `res`: extracts the RES generation dataset from the `dispatch` data
- `available`: extracts the available capacity dataset from the `availabilities` data
- `reservoirs`: extracts the water reservoir levels (for hydro plants) dataset from the `reservoirs` data
- `ntc_imports`: extracts dataset for total NTC (net transfer capacity) for imports from the `ntc` data
- `ntc_exports`: extracts dataset for total NTC (net transfer capacity) for exports from the `ntc` data.

Use
```bash
power-markets fetch -h
```
to see the arguments for the `fetch` command, and 

```bash
power-markets extract -h
```

for the `extract` command.

The `power-markets` package can be installed using pip:

```bash
pip install power-markets
```
