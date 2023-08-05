
# ipyNiiVue

ipyNiiVue is a Python / [Niivue](https://github.com/niivue/niivue) bridge for [Jupyter Widgets](https://jupyter.org/widgets). A Python API is used to interact with NiiVue.

## Getting started

### Installation
```sh
conda create -n ipyniivue-dev -c conda-forge nodejs yarn python jupyterlab
conda activate ipyniivue-dev
git clone https://github.com/niivue/ipyniivue.git
cd ipyniivue
npm i
pip install -e . --user
npm run watch
```
Then, in another terminal/cmd window:
```sh
jupyter lab
```

To view changes made in the typescript, reload the jupyter page. To view changes made in the python, restart the kernel.

### Usage
![example](docs/example.png)
