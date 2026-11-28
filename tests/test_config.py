"""Check that config constants match the plan text verbatim."""

import pytest

from gk_sweeper import config as C

EXPECTED = {
    "SEED": 2026,
    "IDSSE_FPS": 25,
    "PITCH_LENGTH": 105.0,
    "PITCH_WIDTH": 68.0,
    "PITCH_HALF_X": 52.5,
    "GOAL_POST_Y": 3.66,
    "PLAYERS_PER_TEAM": 11,
    "SG_WINDOW": 7,
    "SG_DERIV": 1,
    "MIN_SEGMENT_FRAMES": 7,
    "SPEED_CAP": 12.0,
    "FLICKER_MAX_FRAMES": 5,
    "SEQUENCE_WARMUP_S": 2.0,
    "SAMPLE_WINDOW_S": 1.0,
    "BALL_CARRIER_RADIUS": 2.0,
    "MIN_BALL_GOAL_DIST": 30.0,
    "PRESSURE_RADIUS": 4.0,
    "NEAR_LINE_MARGIN": 5.0,
    "DEPTH_GRID_START": 1,
    "DEPTH_GRID_STEP": 2,
    "DEPTH_CARRIER_GAP": 8.0,
    "DEPTH_CAP": 60.0,
    "MAX_LATERAL_DEVIATION": 8.0,
    "GRID_CELL": 2.0,
    "PPCF_SIGMA_T": 0.54,
    "PPCF_LAMBDA_ATT": 3.99,
    "PPCF_KAPPA_DEF": 1.72,
    "GK_LAMBDA_MULT": 3.0,
    "BOX_X_MAX": 16.5,
    "BOX_Y_ABS_MAX": 20.16,
    "PLAYER_MAX_SPEED": 5.0,
    "REACTION_TIME": 0.7,
    "BALL_SPEED": 15.0,
    "PPCF_DT": 0.04,
    "PPCF_T_MAX": 10.0,
    "PPCF_CONVERGENCE": 0.99,
    "OFFSIDE_TOLERANCE": 0.2,
    "T_SIGMA": 23.9,
    "T_ALPHA": 1.04,
    "LOT_SIGMA_T": 0.45,
    "LOT_LAMBDA": 4.3,
    "LOT_KAPPA_DEF": 1.0,
    "XG_COMMON_N": 51_899,
    "XG_SET_N": 46_825,
    "XG_SET_GOALS": 3_776,
    "XG_EMPTY_N": 427,
    "XG_EMPTY_GOALS": 155,
    "XG_SET_GK_MAX_DIST": 6.0,
    "XG_EMPTY_GK_MIN_DIST": 10.0,
    "EXTRAP_PERCENTILE": 99,
    "A_RADIUS": 6.0,
    "GK_SPEED": 5.0,
    "TAU": 0.5,
    "TAU_CARRIER": 0.0,
    "V_SHOT": 20.0,
    "W_DENOM_FLOOR": 1e-9,
    "C_BOUNDS": (-2.0, 2.0),
    "SW_BOUNDS": (0.05, 1.5),
    "C_FALLBACK": -0.7,
    "M_N": 4_647,
    "M_GOALS": 1_382,
    "RHO_C_SW_THRESHOLD": 0.9,
    "B_CANDIDATES": (0.0, 0.25, 0.5),
    "B_SHOT_WINDOW_S": 3.0,
    "B_MIN_COUNT": 30,
    "B_FALLBACK": 0.25,
    "TIE_TOL": 1e-6,
    "DELTA": 0.10,
    "EPSILON": 1e-4,
    "R_DENOM_FLOOR": 1e-4,
    "EXTRAP_FLAG_PERCENTILE": 95,
    "POWELL_MAX_ITER": 50,
    "BOOTSTRAP_N": 1_000,
    "FIXED_DMAX_MIN_B": 68.0,
    "DESC_B_EDGES": (30.0, 45.0, 60.0),
    "DESC_L_EDGES": (20.0, 30.0, 40.0),
    "DESC_MIN_SEQUENCES": 30,
    "PILOT_N_FRAMES": 200,
    "PILOT_TIME_LIMIT_S": 0.1,
    "PILOT_C_MAX_DIFF": 0.01,
    "GPU_CPU_TOL": 1e-7,
    "PILOT_MEAN_W_D1_LIMIT": 0.05,
    "V51_GK_X_RANGE": (5.0, 25.0),
    "V51_GAP_RANGE": (10.0, 35.0),
    "V52_MAX_MEDIAN_DIST": 3.0,
    "V55_SHOT_WINDOW_S": 10.0,
    "S56_EXPENSIVE_N_FRAMES": 2_000,
    "SB_SHOTS_N_ROWS": 100_864,
    "SB_PSHOT_COMPETITION_ID": 2,
    "SB_PSHOT_SEASON_ID": 27,
    "SB_PSHOT_N_MATCHES": 380,
    "IDSSE_N_DISTINCT_GK": 10,
}


@pytest.mark.parametrize("name,value", sorted(EXPECTED.items()))
def test_constant_matches_plan(name, value):
    assert getattr(C, name) == value


def test_lambda_def_is_kappa_times_lambda_att():
    assert C.PPCF_LAMBDA_DEF == pytest.approx(1.72 * 3.99)


def test_grid_centers():
    # plan 4-2: x = 1, 3, ..., 103 plus half cell centre 104.5; y = -33, ..., 33
    assert C.GRID_X_CENTERS[0] == 1.0 and C.GRID_X_CENTERS[-2] == 103.0
    assert C.GRID_X_CENTERS[-1] == 104.5 and len(C.GRID_X_CENTERS) == 53
    assert C.GRID_Y_CENTERS[0] == -33.0 and C.GRID_Y_CENTERS[-1] == 33.0
    assert len(C.GRID_Y_CENTERS) == 34


def test_idsse_matches():
    assert set(C.IDSSE_MATCH_IDS) == {
        "J03WMX", "J03WN1", "J03WPY", "J03WOH", "J03WQQ", "J03WOY", "J03WR9"}


def test_tbd_values_are_unset():
    # Values not given by the plan must stay unset until a user decision.
    assert C.SG_POLYORDER is None
    assert C.EXTRAP_FLAG_B_BINS is None and C.EXTRAP_FLAG_L_BINS is None
    assert C.S56_DELTA is None
