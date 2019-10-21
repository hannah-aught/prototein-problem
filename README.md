# prototein-problem
This repository include a set of programs which generate `.cnf` files
from binary sequences, as well as a set of pipeline testers which
compare the results of running the SAT solver [pLingeling](http://fmv.jku.at/lingeling/) 
and the ILP solver [Gurobi](https://www.gurobi.com/) on the same binary sequences.

## HPsat Programs
The `HPsat.py` and `HPsat-3D.py` programs are used produce the `.cnf` files for a given
binary sequence file and a goal number of contacts.

### Dependencies
These programs depend on the class file `Condition.py`. This is used to prevent
excess memory use issues and should be located in the same parent directory as
the programs. Both programs also require their input to be located in a `./input`
directory.

### Usage
To call either program, use the following command:
`python3 <program name> <input file name> <goal number of contacts> <path to output directory>`
Note that all input files are assumed to be in a `./input` directory, so there
is no need to specify a path.

## Pipeline Testing Programs
There are two pipeline programs, `HPsat-pipeline-3D.py` and `HPsat-pipeline.py`
included in the `src` file, which are used for testing a set sequences and
reporting their results to test files.

### Dependencies
The pipeline programs have the same dependencies as the HPsat programs, along with a few more:
* The `HPb.pl`, `HPb1.pl`, and `HPb1-3D.py` programs should be in the same directory as the
pipeline programs
* The [pLingeling](http://fmv.jku.at/lingeling/#download) executable should be in the 
`./lingeling` directory
* The lingeling directory also requires an input directory (`./lingeling/input`), which
is where all the cnf files will be genereated.
should also be in the same directory as the pipeline program.
* [Gurobi](https://www.gurobi.com/) needs to be installed.

### Usage
To call either program, use the following command:
`python3 <program name> <list of input files> -o <path to output directory>`
The ouput directory is an optional argument. If unspecified, it defaults to `./output`.
Like the HPsat programs, the input directory is assumed to be `./input`, so there
is no need to pass a path to the input files.

## Generating Binary Sequence Input Files
The `gen_random_sequences.py` and `get_sequences.py` programs are used to generate
random and real binary sequence files, respectively. These binary sequence files
can later be used as input for the pipeline testers and the HPsat programs.

### Real sequences
To generate the binary sequence files for the real sequences found in the `Dataset`
folder, run the following command after creating a `./input` directory:

`python3 get_sequences.py`

This will generate the files and put them in the `./input` directory.

### Random sequences
`gen_random_sequences.py` generates n binary sequence files, each containing a 
binary sequence of length k, and an average percentage of ones, p in each.

The command to run this program is:
`python3 gen_random_sequences.py <length of each sequence> <number of files to generate> <percentage of ones> <output path> <prefix for file names>`

