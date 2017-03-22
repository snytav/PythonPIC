import numpy as np

from run_twostream import two_stream_instability


def test_linear_regime_beam_stability():
    run_name = f"TS_LINEAR"
    S = two_stream_instability(f"data_analysis/{run_name}/{run_name}.hdf5",
                               NG=64,
                               N_electrons=512,
                               )
    assert (~did_it_thermalize(S)).all()


def test_nonlinear_regime_beam_instability():
    run_name = f"TS_NONLINEAR"
    S = two_stream_instability(f"data_analysis/{run_name}/{run_name}.hdf5",
                               NG=64,
                               N_electrons=1024,
                               plasma_frequency=5,
                               dt=0.2 / 5,
                               NT=300 * 5
                               )
    assert did_it_thermalize(S).all()


def did_it_thermalize(S):
    initial_velocities = np.array([s.velocity_history[0, :, 0].mean() for s in S.list_species])
    initial_velocity_stds = np.array([s.velocity_history[0, :, 0].std() for s in S.list_species])
    average_velocities = np.array([s.velocity_history[:, :, 0].mean() for s in S.list_species])
    return np.abs((initial_velocities - average_velocities)) > initial_velocity_stds