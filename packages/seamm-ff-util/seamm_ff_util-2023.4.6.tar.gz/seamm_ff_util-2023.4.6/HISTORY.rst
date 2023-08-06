=======
History
=======

2023.4.6 -- Added support for Buckingham potentials
   * Also improved unit handling across all terms in forcefields.
     
2023.3.5 -- Added molecule numbers for LAMMPS input
   * Added the molecule number for each atom for when using LAMMPS
     
2023.2.6 -- Added handling of OPLS-AA forcefield
   * Added handling of the OPLS-AA forcefield
   * Moved documentation to new MolSSI theme and diátaxis layout
   * Cleaned up internal dependencies and workflows for GitHub

2022.5.29 -- Fixed bug typing larger systems
   * Fixed bug with atom typing due to limit in matches. by @paulsaxe in #59

2022.2.3 -- Fixed bug due to changing ordering of atoms.
   * Fixed bug with atom type assignment due to changed order of atoms. In the process,
     switch to using RDKit directly, which is both more direct and avoids the ordering
     problem.
     
0.1.0 -- (2017-12-05)
   * First release on PyPI.
