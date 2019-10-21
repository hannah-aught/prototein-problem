# prototein-problem

## HPsat Programs

## Pipeline Testing Programs
There are two pipeline programs, `HPsat-pipeline-3D.py` and `HPsat-pipeline.py`
included in the `src` file, which are used for testing a set sequences and
reporting their results to test files.

### Dependencies
Like the `HPsat` programs, the pipeline programs require `Condition.py` to be in
the same directory they are in. They also depend on `HPb.pl`, `HPb1.pl`, and
`HPb1-3D.py`, which should also be in the same directory as the pipeline program.
Both programs depend on the pLingeling executable, which should be in a
`lingeling` directory with the same parent as the pipeline programs. The
`lingeling` directory should also have an `input` subdirectory, which is where
the `.cnf` files will be generated. The final requirement is an `input` directory,
which should be in the same directory as the pipeline programs and is where the
input sequences should be stored.