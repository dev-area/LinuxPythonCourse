# 6 · BASH Scripting — Exercises

> Answers: [answers/06-bash-scripting.md](../answers/06-bash-scripting.md)

**1.** Write a script `hello` that stores your name in a variable and prints `Hello, <name>`.

**2.** Read a name interactively (prompt) and greet the user.

**3.** Extend the arguments example to also print the argument count and the last argument.

**4.** Store the output of `date +%F` in a variable and print it.

**5.** Default a variable: use `$1` if given, otherwise `world`.

**6.** Write a script that exits with status 1 and a usage message if given no arguments.

**7.** Take a filename as `$1` and print "readable"/"not readable" using an `if` with `[ -r ]`.

**8.** Rewrite an `if [ ... -a ... ]` test using the `[[ ... && ... ]]` form.

**9.** Check whether the directory named in `$1` exists; if not, create it.

**10.** Print the numbers 1 to 10 using the C-style `(( ))` for loop.

**11.** Print a countdown from 10 to 1.

**12.** Use a while loop with a counter to print `0..4`.

**13.** Loop over all `*.log` files in the current directory and `gzip` each one.

**14.** Read the file named in `$1` line by line and print each line with its line number.

**15.** Write a case statement mapping `start` | `stop` | `restart` to a message, with a usage default.

**16.** Write a function `add` that adds its two arguments and returns the result as its exit status; print `$?`.

**17.** Write a function that returns success (0) when its argument is an even number.

**18.** Write a script that sums all of its numeric arguments.

**19.** Iterate over an array of hostnames and ping each once.

**20.** Given `f="report.txt"`, print it without the extension and in upper case.

**21.** Using `getopts`, parse a `-v` flag and a `-o <file>` option, echoing what was seen.

**22.** Explain what `${A:?}` does and when you would use it.

**23.** Use `trap` to catch Ctrl+C, print "Interrupted", and keep the loop running.

**24.** Safely loop over `"$@"` so filenames containing spaces stay intact.

**25.** Create a FIFO and write a reader loop (like `fifotest`). How do you send it data?
