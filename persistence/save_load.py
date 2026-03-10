############################################################################################
# save_load.py
#
# Last edit: Michael Schnabel
# Last updated: 09 March 2026
#
# Thin persistence interface. Delegates to engine/score.py for JSON I/O.
############################################################################################

from engine.score import load_scores, save_scores


# To use:
# from persistence.save_load import load_scores, save_scores