# Cleaning-policy report

The cleaned input contains 244,477 records. Confidence >=0.80 is frozen as the draft primary rule; 1,170 records fall below 0.80. Current v2 code accepts any finite confidence in [0,1] and does not enforce the draft confidence threshold, speed maximum, travel-time minimum, valid_* flags, or road-closure rule.

Candidate speed maxima 120/130/160/200 km/h are reported descriptively only. The observed maximum does not establish a physical/provider limit. Because the existing 160 km/h value is explicitly soft and no authoritative physical limit was found, `speed_max=USER_APPROVAL_REQUIRED`.

No provider-status field exists. Traffic state is a traffic condition, not a provider quality status. A proposed valid-flag policy is documented, but the accepted/rejected status whitelist remains `USER_APPROVAL_REQUIRED`.

Final cleaning was not executed.
