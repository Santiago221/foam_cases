# Foam Cases

A collection of OpenFOAM cases, automation scripts, and utilities developed for Computational Fluid Dynamics (CFD) research. The repository focuses on the simulation of internal and external flows, porous media, and Triply Periodic Minimal Surface (TPMS) structures, providing reproducible workflows for mesh generation, simulation execution, and post-processing.

---

## Overview

This repository contains reference OpenFOAM cases and Python tools designed to automate CFD studies involving multiple operating conditions. It was developed to support research on pressure losses, porous media characterization, and TPMS-based geometries.

The workflow covers the entire simulation process:

- Case generation
- Mesh creation
- Mesh refinement
- Solver execution
- Batch simulation
- Post-processing
- Data analysis

The project is intended for researchers and engineers working with OpenFOAM who need a reusable framework for parametric studies.

---

## Repository Structure

```
foam_cases/
│
├── 0.case_snappy_funcionando/
│   Reference case for mesh generation using snappyHexMesh.
│
├── 1.case_case_simpleFOAM_Laminar/
│   Laminar internal flow simulation.
│
├── 2.tpms_case_malha/
│   TPMS mesh generation and preprocessing.
│
├── 3.tpmsrun_turbulent/
│   Turbulent TPMS simulations.
│
├── 4.external_flow/
│   External flow simulations around STL geometries.
│
├── 5.Mesh_doc_ref_case/
│   Reference case used for automated mesh generation and
│   parametric studies.
│
└── scripts/
    Python scripts for automation and post-processing.
```

---

## Features

- Automated OpenFOAM case generation
- Parametric studies for multiple Reynolds numbers
- Structured mesh generation using **blockMesh**
- Local mesh refinement using **snappyHexMesh**
- Internal and external flow simulations
- TPMS geometry support
- Laminar and turbulent flow cases
- Automated simulation execution
- Automated post-processing
- Pressure drop analysis
- Darcy–Forchheimer parameter estimation

---

## Main Applications

This repository is intended for CFD studies involving:

- Porous media
- TPMS structures
- Pressure loss evaluation
- Heat exchanger geometries
- Additive manufacturing applications
- Hydraulic characterization
- Parametric CFD analyses

---

## Software Requirements

- OpenFOAM (tested with OpenFOAM v13)
- Python 3.10+
- NumPy
- Pandas
- SciPy
- Matplotlib
- Seaborn

Additional Python packages may be required depending on the post-processing scripts.

---

## Typical Workflow

1. Select or create a reference OpenFOAM case.
2. Generate the computational mesh using `blockMesh`.
3. Refine the mesh using `snappyHexMesh` (when applicable).
4. Configure the simulation parameters.
5. Run the solver.
6. Execute the Python post-processing scripts.
7. Analyze pressure losses and hydraulic parameters.

---

## Automation

Several Python scripts are included to automate repetitive CFD tasks, including:

- Automatic case creation
- Boundary condition updates
- Reynolds number sweep generation
- Initial turbulence parameter calculation
- Batch simulation execution
- Simulation restart management
- Result extraction
- Data organization
- Plot generation

These tools significantly reduce the manual effort required for large parametric studies.

---

## Research Context

The repository has been developed as part of research activities involving Computational Fluid Dynamics (CFD), with particular emphasis on the hydraulic characterization of TPMS-based porous structures.

Its primary goal is to provide a reproducible and automated simulation environment that simplifies the execution of large simulation campaigns while ensuring consistency across different cases.

---

## Future Improvements

Planned improvements include:

- Docker support
- Continuous Integration (CI)
- Automatic mesh quality reports
- Parallel execution utilities
- Automatic report generation
- Improved documentation for each case
- Validation against experimental data

---

## Contributing

Contributions are welcome.

If you would like to improve the repository, fix bugs, or add new simulation cases, feel free to open an issue or submit a pull request.

---

## License

This repository is intended for academic and research purposes.

Choose an appropriate open-source license (e.g., MIT, BSD, or GPL) before public distribution.

---

## Author

**Rodrigo Santiago**

Msc. Researcher in Mechanical Engineering

Computational Fluid Dynamics (CFD) • OpenFOAM • Porous Media • TPMS • Additive Manufacturing
