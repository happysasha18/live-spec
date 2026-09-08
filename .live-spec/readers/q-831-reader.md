What is to be done: Make a long multi-part run print its live progress (the full list of targets up front, then each one starting and finishing) instead of going silent for hours, and fix a separate history report so it shows the real recorded duration of past runs instead of a meaningless file-modification timestamp.
Why: A silent multi-hour run leaves a watcher unable to tell working from hung, and the duration report is currently reading a meaningless number when the true duration was already recorded and simply needs to be read from the right place.
How long: 2 to 4 hours, based on the four-step plan (a change and its test proof, twice over) since there is no comparable past work in this tree to estimate from.
Echo-name placed: Live output, real durations
