Diffusion (PDE Solvers) in CompuCell3D
=========================================

One of the most important and time-consuming parts of the CC3D
simulation is the process of solving Partial Differential Equations, which
describe behavior of certain simulation objects (usually chemical
fields). Most of the CC3D PDE solvers solve PDEs with diffusive terms.
Since we are dealing with moving boundary condition problems, it was
easiest and probably most practical to use explicit scheme of Finite
Difference method. Most of CC3D PDE solvers run on multi core
architectures and we also have GPU solvers which run and high
performance GPU’s and they also provide biggest speedups in terms of
performance. Because CC3D solvers were implemented at different stages of the CC3D
life cycle and often in response to particular user requests, CC3DML
specification may differ from solver to solver. However, the basic
structure of CC3DML PDE solver code follows a pattern.

For most use cases, we recommend `Diffusion Solver FE <diffusion_solver.html>`_. For the highest level of customization, we recommend `Reaction Diffusion Solver with Finite Volume Method (FVM) <reaction_diffusion_solver_fvm.html>`_. Please see the below reference to find the right PDE solver for your use case. 

**General Reference**

.. toctree::
    :maxdepth: 1

    accessing_concentration_fields_managed_of_pde_solvers
    boundary_conditions_diffusion
    diffusion_solver_settings

**Solvers**

.. toctree::
    :maxdepth: 1

    advection_diffusion_solver
    diffusion_solver
    fast_diffusion_solver_2D
    flexible_diffusion_solver
    kernel_diffusion_solver
    reaction_diffusion_solver
    reaction_diffusion_solver_fvm
    steady_state_diffusion_solver
    fluctuation_compensator_addon