"""Shared constants for the GK sweeper study.

Every value is copied verbatim from docs/gk-sweeper-research-plan.md (the plan).
Each entry cites its plan clause. Values the plan does not specify are left as
None with a "# TBD (question pending)" marker; do not fill them without a user
decision recorded in docs/gk-sweeper/decisions.md.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Environment and paths (CLAUDE.md, plan 8)
# ---------------------------------------------------------------------------
SEED = 2026  # plan 4-6, 4-7, 8
REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"  # CLAUDE.md (git-ignored)
RAW_IDSSE_DIR = RAW_DIR / "idsse"
RAW_SB_EVENTS_DIR = RAW_DIR / "statsbomb" / "events"
RAW_SB_MATCHES_FILE = RAW_DIR / "statsbomb" / "matches_2_27.json"
SB_DERIVED_DIR = REPO_ROOT / "data" / "derived" / "statsbomb"
SB_SHOTS_CSV = SB_DERIVED_DIR / "shots.csv"  # plan 3-1
SB_MATCHES_CSV = SB_DERIVED_DIR / "matches.csv"  # plan 3-1
DERIVED_DIR = REPO_ROOT / "data" / "derived" / "gk_sweeper"  # plan 8

# ---------------------------------------------------------------------------
# 3-1. Data
# ---------------------------------------------------------------------------
KLOPPY_VERSION = "3.19.1"  # plan 3-1, 8
IDSSE_MATCH_IDS = (  # plan 3-1
    "J03WMX", "J03WN1", "J03WPY", "J03WOH", "J03WQQ", "J03WOY", "J03WR9",
)
IDSSE_FPS = 25  # plan 3-1
IDSSE_N_DISTINCT_GK = 10  # plan 3-1
IDSSE_N_TEAM_MATCHES = 14  # plan 3-1
SB_SHOTS_N_ROWS = 100_864  # plan 3-1
SB_SHOTS_COLUMNS = (  # plan 3-1
    "match_id", "x", "y", "gk_x", "gk_y", "goal",
    "shot_type", "body_part", "has_freeze", "xg",
)
SB_PSHOT_COMPETITION_ID = 2  # plan 3-1 (Premier League)
SB_PSHOT_SEASON_ID = 27  # plan 3-1 (2015/16)
SB_PSHOT_N_MATCHES = 380  # plan 3-1

# ---------------------------------------------------------------------------
# 3-2. Coordinates, identification, velocity
# ---------------------------------------------------------------------------
PITCH_LENGTH = 105.0  # plan 3-1, 3-2-1: X = x * 105
PITCH_WIDTH = 68.0  # plan 3-1, 3-2-1: Y = (y - 0.5) * 68
PITCH_HALF_X = 52.5  # plan 3-2-3 direction threshold; 4-2 offside cap
GOAL_POST_Y = 3.66  # plan 3-2-3, 4-3 (posts at (0, +-3.66))
GK_POSITION_NAME = "Goalkeeper"  # plan 3-2-2 (metadata starting_position)
PLAYERS_PER_TEAM = 11  # plan 3-2-2
SG_WINDOW = 7  # plan 3-2-4 (Savitzky-Golay window, frames)
SG_DERIV = 1  # plan 3-2-4 ("1차" read as first derivative)
SG_POLYORDER = None  # TBD (question pending): plan says "창 7, 1차"; polyorder unclear
MIN_SEGMENT_FRAMES = 7  # plan 3-2-4 (segments shorter than 7 frames unused)
SPEED_CAP = 12.0  # plan 3-2-4 (m/s, clip)

# ---------------------------------------------------------------------------
# 1, 3-3. Analysis frames
# ---------------------------------------------------------------------------
DEAD_BALL_RESTART_OPEN_PLAY_S = 2.0  # plan 1 (restart + 2 s counts as open play)
SAMPLE_WINDOW_S = 1.0  # plan 3-3 (first passing frame per 1 s window from half start)
FLICKER_MAX_FRAMES = 5  # plan 3-3-2 (changes shorter than 5 frames merged)
SEQUENCE_WARMUP_S = 2.0  # plan 3-3-2 (frames >= 2 s after sequence start)
BALL_CARRIER_RADIUS = 2.0  # plan 3-3-3 (m, 2D)
MIN_BALL_GOAL_DIST = 30.0  # plan 3-3-4 (|B| >= 30 m)
EXPECTED_N_FRAMES_RANGE = (7_000, 10_000)  # plan 3-3 (expected, not a gate)

# ---------------------------------------------------------------------------
# 3-4. Context variables
# ---------------------------------------------------------------------------
PRESSURE_RADIUS = 4.0  # plan 3-4 (m)
NEAR_LINE_MARGIN = 5.0  # plan 3-4 (onside attackers with x <= L + 5 m)

# ---------------------------------------------------------------------------
# 4-1. Counterfactual positions
# ---------------------------------------------------------------------------
DEPTH_GRID_START = 1  # plan 4-1 (D = {1, 3, 5, ...})
DEPTH_GRID_STEP = 2  # plan 4-1
DEPTH_CARRIER_GAP = 8.0  # plan 4-1 (d_max = min(|B| - 8, 60))
DEPTH_CAP = 60.0  # plan 4-1
CF_GK_SPEED = 0.0  # plan 4-1 (counterfactual GK velocity set to 0)
MAX_LATERAL_DEVIATION = 8.0  # plan 4-1 (frames above excluded from RQ3)

# ---------------------------------------------------------------------------
# 4-2. Defensive OBSO: grid, PPCF, offside, transition
# ---------------------------------------------------------------------------
GRID_CELL = 2.0  # plan 4-2 (m)
GRID_X_CENTERS = tuple(float(x) for x in range(1, 104, 2)) + (104.5,)  # plan 4-2
GRID_Y_CENTERS = tuple(float(y) for y in range(-33, 34, 2))  # plan 4-2
PPCF_SIGMA_T = 0.54  # plan 4-2 (Spearman 2018 MAP, s)
PPCF_LAMBDA_ATT = 3.99  # plan 4-2 (1/s)
PPCF_KAPPA_DEF = 1.72  # plan 4-2 (lambda_def = 1.72 * 3.99)
PPCF_LAMBDA_DEF = PPCF_KAPPA_DEF * PPCF_LAMBDA_ATT  # plan 4-2
GK_LAMBDA_MULT = 3.0  # plan 4-2 (inside defending box only)
BOX_X_MAX = 16.5  # plan 4-2 (box: x <= 16.5)
BOX_Y_ABS_MAX = 20.16  # plan 4-2 (box: |y| <= 20.16)
PLAYER_MAX_SPEED = 5.0  # plan 4-2 (m/s, LaurieOnTracking)
REACTION_TIME = 0.7  # plan 4-2 (s)
BALL_SPEED = 15.0  # plan 4-2 (m/s, ball travel |r - B| / 15)
PPCF_DT = 0.04  # plan 4-2 (integration step, s)
PPCF_T_MAX = 10.0  # plan 4-2 (s)
PPCF_CONVERGENCE = 0.99  # plan 4-2
OFFSIDE_TOLERANCE = 0.2  # plan 4-2 (exclude attackers with x < line - 0.2 m)
T_SIGMA = 23.9  # plan 4-2 (m, Spearman 2018)
T_ALPHA = 1.04  # plan 4-2 (C^alpha)

# LaurieOnTracking alternative set (plan 2, 5-3): only sigma_t, lambda, kappa swapped
LOT_SIGMA_T = 0.45  # plan 2
LOT_LAMBDA = 4.3  # plan 2
LOT_KAPPA_DEF = 1.0  # plan 2

# ---------------------------------------------------------------------------
# 4-3. StatsBomb learned components
# ---------------------------------------------------------------------------
SB_PITCH_LENGTH = 120.0  # plan 3-1, 4-3
SB_PITCH_WIDTH = 80.0  # plan 3-1, 4-3 (x' = (120 - x)*105/120, y' = (y - 40)*68/80)
XG_FILTER_GENDER = "male"  # plan 4-3
XG_FILTER_HAS_FREEZE = 1  # plan 4-3
XG_FILTER_SHOT_TYPE = "Open Play"  # plan 4-3
XG_FILTER_EXCLUDE_BODY_PART = "Head"  # plan 4-3 (headers excluded)
XG_COMMON_N = 51_899  # plan 4-3
XG_SET_GK_MAX_DIST = 6.0  # plan 4-3 (GK inside triangle and GK-G <= 6 m)
XG_SET_N = 46_825  # plan 4-3
XG_SET_GOALS = 3_776  # plan 4-3
XG_EMPTY_GK_MIN_DIST = 10.0  # plan 4-3 (outside triangle and GK-G >= 10 m)
XG_EMPTY_N = 427  # plan 4-3
XG_EMPTY_GOALS = 155  # plan 4-3
PSHOT_SET_PIECE_PASS_TYPES = (  # plan 4-3 (previous pass excluded)
    "Corner", "Free Kick", "Throw-in", "Goal Kick", "Kick Off",
)
PSHOT_LABEL_ACTIONS = ("Pass", "Shot", "Dispossessed", "Miscontrol")  # plan 4-3
PSHOT_SKIP_ACTIONS = ("Carry", "Dribble", "Pressure", "Duel")  # plan 4-3
EXTRAP_PERCENTILE = 99  # plan 4-3: rho_set, rho_empty, p_shot limits = 99th pct of training distance
CV_FOLDS = 5  # plan 4-3 (match-level 5-fold CV)

# ---------------------------------------------------------------------------
# 4-4. Scoring term S and return-failure probability w
# ---------------------------------------------------------------------------
A_RADIUS = 6.0  # plan 4-4 (A(r) = triangle cap circle of radius 6 m)
GK_SPEED = 5.0  # plan 4-4 (t_need = dist / 5)
TAU = 0.5  # plan 4-4 (s; 0 in the ball carrier's cell)
TAU_CARRIER = 0.0  # plan 4-4
V_SHOT = 20.0  # plan 4-4 (m/s)
W_DENOM_FLOOR = 1e-9  # plan 4-4
C_BOUNDS = (-2.0, 2.0)  # plan 4-4 (s)
SW_BOUNDS = (0.05, 1.5)  # plan 4-4 (s)
C_FALLBACK = -0.7  # plan 4-4 (used if c estimate hits a bound)
M_N = 4_647  # plan 4-4 (intermediate sample M)
M_GOALS = 1_382  # plan 4-4
RHO_C_SW_THRESHOLD = 0.9  # plan 4-4 (|rho| > 0.9 widens c sensitivity)
B_CANDIDATES = (0.0, 0.25, 0.5)  # plan 4-4
B_SHOT_WINDOW_S = 3.0  # plan 4-4 (SHOT within 3 s in same sequence)
B_MIN_COUNT = 30  # plan 4-4 (w >= 0.5 frames and SHOT events)
B_W_THRESHOLD = 0.5  # plan 4-4
B_FALLBACK = 0.25  # plan 4-4

# ---------------------------------------------------------------------------
# 4-5. Per-frame metrics
# ---------------------------------------------------------------------------
TIE_TOL = 1e-6  # plan 4-5, D-021
DELTA = 0.10  # plan 4-5
EPSILON = 1e-4  # plan 4-5 (goals)
R_DENOM_FLOOR = 1e-4  # plan 4-5 (R = dO / max(min O, 1e-4))
EXTRAP_FLAG_PERCENTILE = 95  # plan 4-5 (d_obs 95th percentile per |B| x L bin)
EXTRAP_FLAG_B_BINS = None  # TBD (question pending): plan 4-5 does not define the |B| x L bins
EXTRAP_FLAG_L_BINS = None  # TBD (question pending)

# ---------------------------------------------------------------------------
# 4-6. Analysis
# ---------------------------------------------------------------------------
QUANTILE = 0.5  # plan 4-6 (QuantReg q = 0.5)
POWELL_MAX_ITER = 50  # plan 4-6
BOOTSTRAP_N = 1_000  # plan 4-6
FIXED_DMAX_MIN_B = 68.0  # plan 4-6 (|B| >= 68 m subsample)
DESC_B_EDGES = (30.0, 45.0, 60.0)  # plan 4-6 (|B| {30-45, 45-60, >=60})
DESC_L_EDGES = (20.0, 30.0, 40.0)  # plan 4-6 (L {<20, 20-30, 30-40, >=40})
DESC_MIN_SEQUENCES = 30  # plan 4-6
N_LOMO = 7  # plan 4-6

# ---------------------------------------------------------------------------
# 4-7. Pilot
# ---------------------------------------------------------------------------
PILOT_N_FRAMES = 200  # plan 4-7
PILOT_TIME_LIMIT_S = 0.1  # plan 4-7 (per frame-depth)
PILOT_FALLBACK_SAMPLE_S = 2.0  # plan 4-7
PILOT_TOTAL_LIMIT_H = 24.0  # plan 4-7
PILOT_FALLBACK_DEPTH_STEP = 4.0  # plan 4-7
PILOT_C_MAX_DIFF = 0.01  # plan 4-7
GPU_CPU_TOL = 1e-7  # plan 4-7, D-021
PILOT_MEAN_W_D1_LIMIT = 0.05  # plan 4-7
PILOT_R_MEDIAN_LIMIT = 0.05  # plan 4-7
PILOT_BOUNDARY_MIN_SHARE = 0.80  # plan 4-7

# ---------------------------------------------------------------------------
# 5. Validation
# ---------------------------------------------------------------------------
V51_GK_X_RANGE = (5.0, 25.0)  # plan 5-1
V51_GAP_RANGE = (10.0, 35.0)  # plan 5-1
V52_MAX_MEDIAN_DIST = 3.0  # plan 5-2 (m)
V52_OFFSET_RANGE_S = (-2.0, 2.0)  # plan 5-2
V52_OFFSET_STEP_S = 0.04  # plan 5-2
V53_OUTCOME_EVENT_TYPES = (  # plan 5-3
    "PASS", "SHOT", "RECOVERY", "GENERIC:TacklingGame", "GENERIC:OtherBallAction",
)
V53_EXCLUDE_EVENT_TYPES = ("FOUL_COMMITTED", "GENERIC:Delete")  # plan 5-3
V54_GK_DIST_EDGES = (0.0, 4.0, 10.0)  # plan 5-4 ({0-4, 4-10, >=10 m})
V54_CI_LEVEL = 0.95  # plan 5-4 (Wilson)
V55_SHOT_WINDOW_S = 10.0  # plan 5-5
S56_TAU = (0.0, 1.0)  # plan 5-6
S56_V_SHOT = (15.0, 25.0)  # plan 5-6
S56_SW_MULT = (0.5, 2.0)  # plan 5-6
S56_C_SHIFT = 0.3  # plan 5-6 (c +- 0.3 s)
S56_A_RADIUS = (4.0, 8.0)  # plan 5-6
S56_T_SIGMA = (14.0, 30.0)  # plan 5-6
S56_T_ALPHA = (0.0, 2.0)  # plan 5-6
S56_DELTA = None  # TBD (question pending): plan 5-6 lists delta but gives no values
S56_EXPENSIVE_N_FRAMES = 2_000  # plan 5-6
S56_GK_MAX_SPEED = (4.0, 7.0)  # plan 5-6
S56_REACTION_TIME = (0.5, 1.0)  # plan 5-6
S56_BALL_SPEED = (12.0, 20.0)  # plan 5-6

# ---------------------------------------------------------------------------
# 7. Replication (Metrica)
# ---------------------------------------------------------------------------
METRICA_MATCH_IDS = (1, 2, 3)  # plan 7
METRICA_GK_ID_WINDOW_S = 30.0  # plan 7
