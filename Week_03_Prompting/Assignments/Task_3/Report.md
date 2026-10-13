I chose precision because it is simple and shows how many returned rows are correct.

Precision = correct returned rows / all returned rows

I calculate it for each question and average the scores over all  questions. For an empty output, I give 1 if the expected result is also empty, otherwise 0. SQL errors get 0.

RISE: 54.26%
RACE: 60.76%
CAR: 98.25%

Precision complements accuracy. It does not replace it. It measures extra results but does not measure missing results.