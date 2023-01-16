# tph

tph is an APL and Befunge inspired 2d array programming language.

# Contents

* [Reasoning](#reasoning)
  * [Stacks vs Arrays](#stacks-vs-arrays)
  * [Using Array but in 2D](#using-array-but-in-2d)
* [Installation](#installation)
  * [Using the language](#using-the-language)
* [Operations and symbols](#operations-and-symbols)
    * [Arrows](#arrows)
    * [Input](#input)
    * [Output](#output)
    * [Range](#range)
    * [Double Range](#double-range)
    * [Double Independent Range](#double-independent-range)
    * [Modulus](#modulus)
    * [Logic AND](#logic-and)
    * [Logic OR](#logic-or)
    * [Erase](#erase)
    * [Copy](#copy)
    * [Simple Sum](#simple-sum)
    * [Direct Sum](#direct-sum)
    * [Program End](#program-end)
* [Bugs, Issues, Etc](#bugs-issues-etc)
* [How to contribute](#how-to-contribute)


# Reasoning

The idea behind this programming language is thinking of what if Befunge and APL(probably J?) decided to merge. For those who have no idea what those big mouth words mean, read the subsection below. For those who know stack and array languages, you can skip the next subsection.

## Stacks vs Arrays

There are some languages that make use of stacks to store and manipulate data. And there are some languages that make use of arrays to store and manipulate them. "What are the difference?" you may ask and to simply put:

**Stacks**
* they store and read data as _first-in-last-out_ (FILO);
* they can only access the last element of the stack and usually operations can handle the second-to–last one;

**Arrays**
* they store and read data as _first-in-first-out_ (FIFO)
* but they can store as many as they want and access/manipulate any of them (or all of them)


There is a main array that follow the code flows and two auxiliary arrays: left-hand-side (lhs) and rhs arrays, each one responsible to function in certain conditions according to operations applied.

## Using Array but in 2D

The idea is to have data, one character operations (from 256 UTF-8 ASCII-based chars) and arrows directing your program main flow. Single digit data such as integer numbers from 0 to 9 can be placed without any extra syntax sugar. Strings need to have `"` in between the start and end of it (and may have a skip operation inside of it. More on that later.) Multi-digit integers or float numbers need parenthesis around the digits to be considered a single number. Some operations may use auxiliary arrays to retrieve, manipulate or stored data on them, and usually they are placed on the left-hand-side (lhs) -or rhs- of the current program flow. Program has a program flow (the main flow), auxiliary flow (either lhs or rhs) and they may or may be not the current flow. Last but not least (actually yeah), the program must always end with a `@`.

# Installation

Requirements: 
* Python 3.8+
* **Strongly** recommended a virtual environment, such as Anaconda/conda, poetry, venv, pyenv, etc.
* [Arpeggio package](https://textx.github.io/Arpeggio/2.0/) (parser using PEG notation);
* [Click package](https://click.palletsprojects.com/en/8.1.x/) (to manage setup configurations);

After cloning this repository, go to its root folder and run the following command:
```
pip install -e .
```

## Using the language
Write code on a .tph file and use the command `tph <file>` to run it. You can additionally run `tph -p <file>` to print the program code before interpreting it. 

Have fun!

# Operations and symbols

Here there will be some explanation on the operations.

### Arrows
Defined as `<` (**less than**), `>` (**greater than**), `^` (**caret**), `v` (**small v**)/ `V` (**capital v**). They are used to change the direction of the code flow (main or auxiliary). Operations are always performed according to the current direction of the code flow, so main can be in the right, left, up or down direction and its relative position will be the lhs and rhs.

### Input
Defined as `b` symbol (**small b**). It receives input from the user (single value, many values separated by either comma or spaces, integers, floats* and strings*) and stores by concatenating it to the main array tail (FIFO).

*to be implemented.

### Output
Defined as `r` symbol (**small r**). It prints the current array in the current flow.

### Range
Defined as `i` symbol (**small i**). It acts like a range in Python or foldl in Haskell (inspired in APL's iota). It pops out the last element `N` from the current array* and generates a `range(0, N)` arrays that will be concatenated to the current array.

*currently implemented only for the main array.

### Double Range
Defined as `ï` symbol (**small i with umlaut**). It performs exactly the same operation as `i` and then replicates the result into the lhs array.

### Double Independent Range
Defined as `Ï` symbol (**capital i with umlaut**). It performs the same operation as `i` but with main array's and lhs array's last element and concatenates each result to their respective arrays.

### Modulus
Defined as `%` symbol (**percentage**). It provides a modulus on each element `A` of the main array to each element `B` of the lhs array. It can execute logic operations on lhs that will be prepared in such a way to execute all the lhs array elements at once. The values in which `A mod B == 0` will be kept into the main array, whereas the other results will be stored in the rhs array. According to where the code continues (on the main flow or on the rhs flow), the according array may be reassigned as main.

### Logic AND
Defined as `&` symbol (**ampersand**). It performs an `AND` logic operation on pairs of values of the array or, in case it is assigned to auxiliary flow during an operation execution, it will be applied over the later operation results.

### Logic OR
Defined as `|` symbol (**vertical bar**). It performs an `OR` logic operation in the same fashion as the [logic AND](#logic-and).

### Erase
Defined as `$` symbol (**dollar sign**). It empties the main array.

### Copy
Defined as `c` symbol (**small c**). It copies the main array and concatenates it into the current auxiliary array.

### Simple Sum
Defined as `+` symbol (**plus sign**). It sums up all the elements of the array, consuming them and placing the result in the array.

### Direct Sum
Defined as `D` symbol (**capital d**). It sums each element of the main array of each element of the lhs array, consuming them and placing the result in the main array.

### Program End
Defined as `@` symbol (**at sign**). It is placed to determine the end of the program.

# Bugs, Issues, Etc
The code is in continuous experimentation and many things may crash. Drop an issue in the repository.

# How to contribute
Drop a message on [Mastodon](https://qubit-social.xyz/@dooms) or on [Twitter](https://twitter.com/byDooms), or send an issue with a PR explaning what is going on.