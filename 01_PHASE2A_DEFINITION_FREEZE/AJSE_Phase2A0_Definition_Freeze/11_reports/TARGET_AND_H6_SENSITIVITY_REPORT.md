# Frozen target definition

For node `i`, origin `t`, and H in {1,3,6}, the AJSE task predicts the arithmetic mean of real observed hourly speeds at `t+1,...,t+H`. Targets are never filled. H=1 requires 1/1 observed hour, H=3 requires 3/3, and the H=6 primary analysis requires at least 5/6. A predeclared H=6 6/6 complete-case analysis is descriptive sensitivity only.

This definition is separate from the current v2 point-ahead target. Phase 2A-1 must add a new module rather than modifying the current function in place.
