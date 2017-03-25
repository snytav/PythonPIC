# coding=utf-8

import pytest
from numpy import pi

from plotting import plotting
from run_coldplasma import cold_plasma_oscillations


def get_dominant_mode(S):
    data = S.grid.energy_per_mode_history
    weights = (data ** 2).sum(axis=0) / (data ** 2).sum()

    max_mode = weights.argmax()
    # max_index = data[:, max_mode].argmax()
    return max_mode


@pytest.mark.parametrize("push_mode", range(1, 32, 3))
def test_linear_dominant_mode(push_mode):
    plasma_frequency = 1
    N_electrons = 1024
    NG=64
    qmratio=-1

    run_name = f"CO_LINEAR_{push_mode}"
    S = cold_plasma_oscillations(f"data_analysis/{run_name}/{run_name}.hdf5", qmratio=qmratio, plasma_frequency=plasma_frequency, NG=NG,
                                 N_electrons=N_electrons, push_mode=push_mode, save_data=False)
    calculated_dominant_mode = get_dominant_mode(S)
    assert calculated_dominant_mode == push_mode, (
        f"got {get_dominant_mode} instead of {push_mode}",
        plotting(S, show=False, save=False, animate=False))
    return S
