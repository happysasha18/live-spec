What is to be done: Make the acceptance path refuse any command other than the one a row was admitted with, refuse a receipt when the environment's run mode decides no verdict, and refuse by name (rather than guess) a tree whose run-mode contract cannot be read, while the row's own recorded acceptance still runs, passes, and closes the row.
Why: Right now any other command can ride into the receipt a close reads, so an unscoped broad run or a run made under a no-verdict mode can wrongly become a row's closing evidence.
How long: 12-39 minutes, based on three closed rows in the same group (q-830, q-831, q-832).
Echo-name placed: Close rests on recorded acceptance.
