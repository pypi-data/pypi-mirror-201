"""
Class Simulation

2020, July 22
"""

import time
import warnings

import numpy as np

from . import solver as slv


class Simulation:
    """
    Class to convert network information
    (how the components are connected to each other)
    and component information
    (equations for each component)
    to a single non-linear system of equations
    (function vector + Jacobian)
    describing the whole system.

    Solving this system is to be done by a solver.
    This object contains a solver object in the property self.solver.
    (Future functionality: possibility to select a solver manually etc.)

    The Class Solver interacts heavily with the System class
    and expects the following methods to be available:

    - ``evaluate_equations()``
    - ``update_state()``
    - ``equation_to_string()``

    as well as the following properties:

    - ``system``
    - ``phi``, ``H`` and ``A``
    - ``arguments``
    - ``nb_arguments`` and ``nb_network_equations``
    - ``times`` and ``duration`` and ``verbose``

    :param system_to_simulate: System object with components and how they are connected
    :param duration: amount of time the system will be simulated for
    :param step: initial time increment
    :param step_min: minimal time increment during the simulation
    :param step_max: maximal time increment during the simulation
    :param max_steps: maximum amount of time increments before the
                      simulation is terminated prematurely. A value of 0 disables this
                      behavior (default)
    :param verbose: level of information printed in the console
                    during the simulation. All messages belonging to a level with a
                    number lower than or equal to the provided parameter will be
                    displayed, with the possible levels being:

                     * -1: simulation start and end messages
                     * 0 (default): simulation progress in % steps
                     * 1: system matrices on iterations with bad convergence
    """
    def __init__(self, system_to_simulate, duration=10, step=None,
                 step_min=None, step_max=None, max_steps=0, verbose=0):

        # Check input
        if step_min is not None and step_max is not None and step_min > step_max:
            raise Warning('Parameter step_min should not be larger than step_max.')

        # Assign arguments to properties
        self.verbose = verbose

        # Load system to simulate
        self.system = system_to_simulate
        connectivity_message = self.system.get_connectivity_message()
        if len(connectivity_message) > 0 and self.verbose >= -1:
            msg = '{}!'.format(connectivity_message) + \
                  'Are you sure you did not forget any connections?'
            warnings.warn(msg, UserWarning, stacklevel=2)

        # Timing
        self.duration = duration

        # Resolve stepping settings
        self.duration = duration
        if step is None:
            step_vals = [s for s in (step_max, step_min) if s is not None]
            if len(step_vals) > 0:
                step = sum(step_vals)/len(step_vals)
            else:
                step = self.duration/100.
        self.max_steps = max_steps

        # Initialize matrix construction (dicts etc.)
        self.arguments = []
        self.nb_arguments = 0
        self.nb_states = 0
        self.phi_index_slice_by_component_by_component = {}
        self.phi_index_by_component_argument = {}
        self.state_index_slice_by_component = {}
        self.states_index_by_component_argument = {}
        self.nb_component_equations = 0
        self.nb_network_equations = 0
        self.init_matrixconstruction()

        # Construct the matrices
        # Initialize empty Jacobian
        self.H = np.zeros((self.nb_arguments, self.nb_arguments))
        # Fill network matrix
        self.fill_network_matrix(self.H)
        # Network matrix (= upper part of H)
        # Note: A keeps pointing to upper part of H,
        # so changing A will affect H as well.
        self.A = self.H[:self.nb_network_equations, :]

        # values vector = result of evaluated equations
        # leave this to the solver...
        #self.g = np.zeros(self.nb_arguments)

        # Create the argument matrix, aka the matrix with the vector
        # of all unknowns for each timestep
        self.phi = np.array(0)
        # and create the state matrix,
        # which holds the internal component states for each timestep
        self.state = np.array(0)
        # These two arrays are filled by the method initialize_memory

        # Time series (to be set by solver)
        self.times = np.array(0)
        # Step counter - denotes current step of simulation
        self.simstep = 0

        # Select the solver
        # self.solver = slv.ImplicitEulerNewtonConstantTimeStep(self, step)
        self.solver = slv.ImplicitEulerNewtonAdaptiveTimeStep(self, step,
                                                              step_min, step_max)

    def init_matrixconstruction(self):
        """
        Create some LUT-style lists and dicts
        so data can be moved around quickly
        in the simulation loop.

        :return: None
        """
        # collocate arguments (Variable objects) of all components into a list
        self.arguments = []
        self.states = []
        for component in self.system.components:
            self.arguments.extend(component.arguments)
            self.states.extend(component.states)
        self.nb_arguments = len(self.arguments)
        self.nb_states = len(self.states)
        # make a dict to quickly map arguments of a component
        # to the indices of phi
        self.phi_index_slice_by_component = {}
        self.phi_index_by_component_argument = {}
        self.state_index_slice_by_component = {}
        self.state_index_by_component_state = {}
        for component in self.system.components:
            k = []
            for i in range(len(component.arguments)):
                arg = component.arguments[i]
                phi_index = self.arguments.index(arg)
                k.append(phi_index)
                self.phi_index_by_component_argument[arg] = phi_index
            self.phi_index_slice_by_component[component] = slice(k[0], k[-1]+1)
            k = []
            for i in range(len(component.states)):
                s = component.states[i]
                state_index = self.states.index(s)
                k.append(state_index)
                self.state_index_by_component_state[s] = state_index
            self.state_index_slice_by_component[component] = slice(k[0], k[-1]+1)\
                if len(k) else slice(0)
        # Count number of component equations
        self.nb_component_equations = sum(c.nb_equations for c in self.system.components)

    def fill_network_matrix(self, A):
        """
        Fill the network matrix.
        The network matrix is constant over the simulation, at least
        supposing the network configuration does not change. It is thus
        sufficient to calculate it a single time.

        There are two types of network equations, one for across
        variables and one for through variables. 
        At each node, all across variables have to be equal. Thus for
        each node n-1 equations, n being the number of components
        attached to that node.
        Concerning the through variables, the sum of all through
        variables should be zero at each node, thus one equation for each
        node.

        :param A: system Jacobian matrix, numpy ndarray n x n, n=len(phi)
        :return: None
        """
        irow = 0
        for node in self.system.nodes:
            # Get across variables to relate together
            across_keys = set(var.key for var in node.get_variables(orientation='across'))
            for key in across_keys:
                # Get all across variables
                variables = node.get_variables(key=key)
                # Get their indices in the argument list
                phi_indices = [self.phi_index_by_component_argument[arg] for arg in variables]
                # Equate their values pair-wise
                for pair1, pair2 in zip(phi_indices[:-1], phi_indices[1:]):
                    A[irow, pair1] = 1
                    A[irow, pair2] = -1
                    irow += 1

            # Get through variables to relate together
            through_keys = set(var.key for var in node.get_variables(orientation='through'))
            for key in through_keys:
                # Get all through variables
                variables = node.get_variables(key=key)
                # Get their indices in the argument list
                phi_indices = [self.phi_index_by_component_argument[arg] for arg in variables]
                # Equate their sum to zero
                A[irow, phi_indices] = 1
                irow += 1

        self.nb_network_equations = irow

    def check_issolvable(self):
        """
        Warns when number of equations doesn't equal number of unknowns.
        :return: None
        """
        is_solvable = self.nb_network_equations + self.nb_component_equations == self.nb_arguments
        if not is_solvable:
            msg = 'This system does not seem to be solvable! ' +\
                  'The number of equations (network and component) ' +\
                  'should equal the number of unknowns, however encountered:' +\
                  '\n  nb of network eq:   ' + str(self.nb_network_equations) +\
                  '\n  nb of component eq: ' + str(self.nb_component_equations) +\
                  '\n  nb of unknowns:     ' + str(self.nb_arguments) + '.'
            warnings.warn(msg, UserWarning, stacklevel=2)

    def equation_to_string(self, equation_index):
        """
        Return a string describing the equation with the provided index
        in a human-readable format. For a network equation, this string
        contains the involved variables and their coefficients. For a
        component equation, this string mentions the component label and
        the index of the equation in the list of equations of that
        particular component.

        :param equation_index: index of the row in the simulation
                               equation matrix corresponding to the desired equation
        :return eq_str: string representing the equation
        """
        eq_str = ""
        # handle network equations
        if equation_index < self.nb_network_equations:
            for coeff_ID, coeff in enumerate(self.A[equation_index, :]):
                if coeff != 0:
                    # add sign of coefficient
                    if coeff < 0:
                        eq_str += "- "
                    elif len(eq_str) > 0:
                        eq_str += "+ "
                    # add value of coefficient
                    if abs(coeff) != 1:
                        eq_str += "{}*".format(abs(coeff))
                    # add name of corresponding variable
                    eq_str += "{} ".format(self.arguments[coeff_ID].short_str())
        # handle component equations
        else:
            curr_eq_ind = self.nb_network_equations
            comp_ind = 0
            comp_eq_ind = 0
            # find the index of the component and the index of the equation in
            # the component matching with the global equation index
            while curr_eq_ind < equation_index:
                curr_eq_ind += 1
                if comp_eq_ind < self.system.components[comp_ind].nb_equations-1:
                    # transition to next equation in this component
                    comp_eq_ind += 1
                else:
                    # transition to next component
                    comp_eq_ind = 0
                    comp_ind += 1
            eq_str = "{} equation {}".format(
                self.system.components[comp_ind].label, comp_eq_ind)

        return eq_str.strip()

    def print_equations(self):
        """
        Print a human-readable representation of the full system of
        equations to the console.

        :return: None
        """
        # get every equation string
        eq_strs = [self.equation_to_string(i) for i in
                   range(self.nb_network_equations+self.nb_component_equations)]
        # get maximum equation text width for alignment
        max_len = max([len(eq) for eq in eq_strs])
        # print equations
        for i, eq in enumerate(eq_strs):
            print('eq {}: {} = {}'.format(i, eq.rjust(max_len), 0))

    def map_phi_to_components(self, phi):
        """
        Send addresses of arguments over time to components, so one can
        get the data from the component without passing by the Simulation
        object. Furthermore, it avoids duplicating the data.

        :param phi: numpy ndarray m x n with the argument vector over
                    time (m = nb timesteps and n = nb arguments)
        :return: None
        """
        for component, i in self.phi_index_slice_by_component.items():
            component.argument_history = phi[:, i]

    def map_state_to_components(self, state):
        """
        Send addresses of state over time to components, so one can
        get the data from the component without passing by the Simulation
        object. Furthermore, it avoids duplicating the data.

        :param state: numpy ndarray m x n with the state vector over
                      time (m = nb timesteps and n = nb states)
        :return: None
        """
        for component, i in self.state_index_slice_by_component.items():
            component.state_history = state[:, i]

    def initialize_memory(self, nb_steps):
        """
        Initialize all arrays that will hold the simulation results
        through time. This includes
        - The vector with time values
        - Component argument and state histories (in Component class)
        - The simulation phi matrix with all arguments over time
        All previously stored results are overwritten.
        This method initializes the arrays with zeros
        and therefore does not use the ``initial_value`` attribute
        of the Variable objects.
        
        :param nb_steps: estimated amount of time steps in the simulation
        :return: None
        """
        # Allocate time vector
        # The values it contains are filled in by the solver
        self.times = np.zeros(nb_steps)

        # Allocate phi and state matrices
        # And map them to the components
        self.phi = np.zeros((nb_steps, self.nb_arguments), dtype=float)
        self.state = np.zeros((nb_steps, self.nb_states), dtype=float)
        self.map_phi_to_components(self.phi)
        self.map_state_to_components(self.state)

    def set_initial_values_phi(self, step=0):
        """
        Takes the initial values from the component argument Variable objects
        and writes them to the simulation memory (matrix 'phi').

        :param step: simulation step at which to write the initial value
        :return: None
        """
        self.phi[step, :] = [a.initial_value for a in self.arguments]

    def set_initial_values_state(self, step=0):
        """
        Takes the initial values from the component state Variable objects
        and writes them to the simulation memory (matrix 'state').

        :param step: simulation step at which to write the initial value
        :return: None
        """
        self.state[step, :] = [s.initial_value for s in self.states]

    def extend_memory(self, nb_extra_steps):
        """
        Increase the size of the simulation memory without overwriting
        previous results. This deals with the same entities as described
        in the documentation of initialize_memory

        :param nb_extra_steps: amount of time steps by which to increase
                               the memory
        :return: None
        """
        # Extend time vector
        self.times = np.append(self.times, 
                               self.times[-1]*np.ones(nb_extra_steps))
        # Extend phi and state matrices
        self.phi = np.append(self.phi,
                             self.phi[0, :]*np.ones((nb_extra_steps, 1)),
                             axis=0)
        self.state = np.append(self.state,
                               np.zeros((nb_extra_steps, self.nb_states)),
                               axis=0)
        # Update links to argument and state results in components
        self.map_phi_to_components(self.phi)
        self.map_state_to_components(self.state)

    def slice_memory(self, start_step, end_step):
        """
        Decrease the size of the simulation memory by taking a slice out
        of it. This deals with the same entities as described in the
        documentation of initialize_memory

        # TODO update such that takes slice as argument

        :param start_step: index of the first time step in the range to
                           maintain
        :param end_step: index of the first time step outside the range
                         to maintain
        :return: None
        """
        # Truncate time vector
        self.times = self.times[start_step:end_step]
        # Truncate phi and state matrices
        self.phi = self.phi[start_step:end_step,:]
        self.state = self.state[start_step:end_step, :]
        # Update links to argument and state results in components
        self.map_phi_to_components(self.phi)
        self.map_state_to_components(self.state)

    def run(self):
        """
        Run simulation, with the parameters specified previously.

        :return: None
        """
        # Check whether system is solvable
        self.check_issolvable()

        # Reset current simulation step index to zero
        self.simstep = 0
        # Reset simulation memory
        self.initialize_memory(self.solver.get_nb_steps_estimate())
        self.set_initial_values_phi()
        self.set_initial_values_state()

        # Simulation time steps at which a progress message will be printed
        pstep = 5
        progress_pts = [(p/100.*self.duration, p) for p in range(pstep, 101, pstep)]

        # Do the simulation loop
        if self.verbose >= -1:
            print('\nSimulation progress:   0 %', end='', flush=True)
            start_time_process = time.process_time()
            start_time = time.time()

        solver_convergence = True
        while solver_convergence and \
                self.times[self.simstep] < self.duration and \
                (self.max_steps <= 0 or self.simstep <= self.max_steps):
            # Increase memory size if necessary
            if self.simstep+1 >= self.times.size:
                self.extend_memory(self.solver.get_nb_steps_estimate() -
                                   self.times.size)
            # Run solver
            solver_status = self.solver.run_step(self.simstep)
            if solver_status is None:
                solver_convergence = True
            else:
                if isinstance(solver_status, (list, tuple)):
                    solver_convergence = solver_status[0]
                    solver_message = solver_status[1]
                else:
                    solver_convergence = solver_status
                    solver_message = ""
            # Update simulation step index
            self.simstep += 1
            # Print some progress information
            if self.verbose >= -1 and \
               self.times[self.simstep] >= progress_pts[0][0]:
                print('\b\b\b\b\b{:3d} %'.format(progress_pts[0][1]), end='')
                del progress_pts[0]
        print()

        # Clean up excess memory when the simulation finishes
        self.slice_memory(0, self.simstep+1)

        # Print time data
        if self.verbose >= -1:
            # Get run time
            end_time_process = time.process_time()
            end_time = time.time()
            run_time_process = end_time_process - start_time_process
            run_time = end_time - start_time
            # Print error messages
            if not solver_convergence and len(solver_message) > 0:
                print(solver_message)
            elif self.max_steps > 0 and self.simstep >= self.max_steps:
                print("Maximum number of simulation increments reached")
            # Print exit messages
            run_time_process_str = '{:.2f}'.format(run_time_process) + ' s'
            run_time_str = '{:.2f}'.format(run_time) + ' s'
            if self.times[self.simstep] < self.duration:
                print('Simulation terminated after', run_time_str, '(process:', run_time_process_str + ')')
            else:
                print('Simulation finished in', run_time_str, '(process:', run_time_process_str + ')')

    def evaluate_equations(self, simstep, g, H, elapsed_time, dt):
        """
        Evaluate component equations to obtain evaluated function vector
        (equation residuals) and jacobian.
        This method will call the method ``Component.evaluate``
        on each component.
        This method will also call the method ``Component.update_state``
        on each component.

        Note: This function does not evaluate (or update) the network
        equations (upper part of the jacobian 'H')!

        :param simstep: simulation timestep index to start from
        :param g: numpy ndarray for the evaluated function vector
        :param H: numpy ndarray for the evaluated jacobian
        :param elapsed_time: time elapsed
        :param dt: timestep (0 for explicit Euler, dt for implicit Euler)
        :return: None
        """

        # Counter of equation row index to write to
        irow = self.nb_network_equations
        for component in self.system.components:
            nb_a = len(component.arguments)
            nb_s = len(component.states)
            ka = self.phi_index_slice_by_component[component]
            ks = self.state_index_slice_by_component[component]

            # Get references to arguments and state belonging to that component
            arguments = self.phi[simstep+1, ka]
            state = self.state[simstep, ks]
            # Get references to residuals and large jacobian (will be written to)
            k = component.nb_equations
            jacobian_full = H[irow:irow+k, ka]
            residuals = g[irow:irow+k]
            irow += component.nb_equations

            # Update state if nonzero timestep,
            if dt != 0:
                state_new = np.zeros(nb_s)
                j_state2arg = np.zeros((nb_s, nb_a))
                component.update_state(state_new, j_state2arg, state, arguments, dt)
            else:
                state_new = state[:]

            # Allocate jacobians
            j_val2state = np.zeros((component.nb_equations, nb_s))
            j_val2arg = np.zeros((component.nb_equations, nb_a))

            # state_new = (state + state_new)/2

            # Evaluate residual equations
            component.evaluate(residuals, j_val2state, j_val2arg, state_new, arguments, elapsed_time)

            # combine state and argument jacobians
            jacobian_full[:] = j_val2arg
            if dt != 0:
                jacobian_full[:] = jacobian_full + np.inner(j_val2state, j_state2arg.T)

    def update_state(self, simstep, dt):
        """
        Update the state variables in all components using the arguments
        in self.phi at step n + 1 (n = 'simstep').
        This method will call the method ``Component.update_state``
        on each component.

        :param simstep: simulation timestep index to start from
        :param dt: timestep
        :return: None
        """
        for component in self.system.components:
            nb_a = len(component.arguments)
            nb_s = len(component.states)
            if len(component.states):
                arguments = self.phi[(simstep+1, self.phi_index_slice_by_component[component])]

                k = self.state_index_slice_by_component[component]
                state = self.state[simstep, k]

                state_new = np.zeros(nb_s)
                j_state2arg = np.zeros((nb_s, nb_a))

                component.update_state(state_new, j_state2arg, state, arguments, dt)

                # state_new = (state_new + state)/2

                # Write out state to component
                self.state[simstep+1, k] = state_new
