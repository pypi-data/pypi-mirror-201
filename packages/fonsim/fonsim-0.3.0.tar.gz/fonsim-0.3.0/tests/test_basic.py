"""
! To be superseded by proper unit tests, with asserts etc. !

Do some very basic testing
"""

import pytest
from pytest import approx


def test_import():
    import fonsim as fons


def test_wavefunction():
    import fonsim as fons
    waves = [(0, 0.900), (0.50, 0.100)]
    wave_function = fons.wave.Custom(waves) * 1e5 + fons.pressure_atmospheric


def test_systemgeneration():
    import fonsim as fons
    system = fons.System('my_system')


def test_components():
    import fonsim as fons
    c1 = fons.PressureSource('source_00', pressure=1.8e5)
    c2 = fons.Container('container_00', fluid=fons.air, volume=50e-6)
    c3 = fons.CircularTube('tube_00', fluid=fons.air, diameter=2e-3, length=0.60)
    c4 = fons.FlowRestrictor('restrictor_00', fluid=fons.air, diameter=2e-3, k=0.5)
    c5 = fons.FreeActuator('actu_00', fluid=fons.air, curve=None)


def test_networkconstruction():
    import fonsim as fons
    system = fons.System('my_system')
    c1 = fons.PressureSource('source_00', pressure=1.8e5)
    system.add(c1)


def test_connectingcomponents():
    import fonsim as fons
    system = fons.System("my_system")
    c1 = fons.PressureSource("source_00", pressure=1.8e5)
    system.add(c1)
    c2 = fons.Container("container_00", fluid=fons.air, volume=50e-6)
    system.add(c2)
    system.connect("source_00", "container_00")


def test_simulation():
    import fonsim as fons
    waves = [(0, 0.900), (0.50, 0.100)]
    wave_function = fons.wave.Custom(waves) * 1e5 + fons.pressure_atmospheric
    system = fons.System('my_system')
    c1 = fons.PressureSource('source_00', pressure=wave_function)
    system.add(c1)
    c2 = fons.Container('container_00', fluid=fons.air, volume=50e-6)
    system.add(c2)
    c3 = fons.CircularTube("tube_00", fluid=fons.air, diameter=2e-3, length=0.60)
    system.add(c3)
    system.connect('source_00', 'tube_00')
    system.connect('tube_00', 'container_00')

    sim = fons.Simulation(system, duration=1.0, step=1e-3, step_min=1e-3, step_max=1e-3)
    sim.run()

    a1 = sim.times
    a2 = system.get('source_00').get('pressure')
    a3 = system.get('container_00').get('pressure')
    a4 = system.get('container_00').get('massflow')

    # Check lengths of simulation data output arrays
    assert len(a1) == 1001
    assert len(a2) == 1001
    assert len(a3) == 1001
    assert len(a4) == 1001

    # Check values
    assert a1[0] == approx(0, abs=1e-3)
    assert a1[-1] == approx(1, abs=1e-3)
    assert a3[0] == approx(fons.pressure_atmospheric, abs=2e5*1e-2)
    assert a3[-1] == approx(fons.pressure_atmospheric + 0.1e5, abs=2e5*1e-2)


@pytest.fixture(scope='session')
def sim_01():
    import fonsim as fons
    waves = [(0, 0.900), (0.50, 0.100)]
    wave_function = fons.wave.Custom(waves) * 1e5 + fons.pressure_atmospheric
    system = fons.System('my_system')
    c1 = fons.PressureSource('source_00', pressure=wave_function)
    system.add(c1)
    c2 = fons.Container('container_00', fluid=fons.air, volume=50e-6)
    system.add(c2)
    c3 = fons.CircularTube("tube_00", fluid=fons.air, diameter=2e-3, length=0.60)
    system.add(c3)
    system.connect('source_00', 'tube_00')
    system.connect('tube_00', 'container_00')

    sim = fons.Simulation(system, duration=1.0, step=1e-3)
    sim.run()

    return system, sim


@pytest.mark.parametrize('test_input', [
    400, 497, 498, 499, 500, 501, 502, 503, 600,
])
def test_run_step(sim_01, test_input):
    """
    Check wether running running method ``run_step``
    when a simulation has already been run
    changes the result (no or minimal changes ought to occur).
    """
    simstep = test_input

    system, sim = sim_01

    a1 = sim.times
    a2 = system.get('source_00').get('pressure')
    a3 = system.get('container_00').get('pressure')
    a4 = system.get('container_00').get('massflow')

    sim.solver.run_step(simstep=simstep)

    a1b = sim.times
    a2b = system.get('source_00').get('pressure')
    a3b = system.get('container_00').get('pressure')
    a4b = system.get('container_00').get('massflow')

    assert a1 == approx(a1b)
    assert a2 == approx(a2b)
    assert a3 == approx(a3b)
    assert a4 == approx(a4b)
