---
title: The Halting problem
date: 2022/09/20
description: How Alan Turing solved the halting problem
tags:
  - logic
  - turing
  - problem
---

An interesting [decision problem](https://en.wikipedia.org/wiki/Decision_problem) I've read about is called the Halting problem.

## Decision problem

In short, a decision problem is basically a question regarding some input(s) that is answered by yes or no (true or false).

For example: Given 3 integers `x`, `y` and `z`, is the addition equals to 100?

This decision problem has an effective solution to find the correct answer, no matter the input, it is **decidable**.

```{.python .numberLines}
def eq_100(x: int, y: int, z: int) -> bool:
    return (x + y + z) == 100
```

Ok, that's not very impressive.
As opposed to decidable, some decision problems are said to be **non decidable** i.e. there is no existing method to guarantee a correct answer for any inputs.
This is the case for the halting problem.

## The halting problem

The question is: Is it possible for a program to determine if another program given an input will eventually halt (or loop forever).

Note that it's a decision problem because we have a question regarding some inputs (a program `P` and an input `I`) that is answered by yes or no (`P` will halt or not).

For this problem to be decidable, we need to find a program that finds the correct answer no matter the program it is given.
I can tell you the answer right now, it is not decidable, there is no such program.

Alan Turing actually solved it in a clever way by using *reductio ad absurdum*.

Suppose we have a program `R` that takes 2 inputs: a program `P` and another input `I`, and is able to tell us if `P(I)` is going to halt or not.

<img alt="r drawing" src="/img/misc/the-halting-problem/r.png">

Now, imagine if we create a program `R'` that gives its 2 inputs to `R` and:

- if the result of `R(P, I)` is true i.e. `P` with `I` will halt, then it loops forever.
- if the result of `R(P, I)` is false i.e. `P` with `I` will not halt, then it returns true.

something like this:

<img alt="r' drawing" src="/img/misc/the-halting-problem/r2.png">

What happens if give our program `R'` to `R'`?

<img alt="r' drawing" src="/img/misc/the-halting-problem/r3.png">

`R'` will give `R'` to `R` and so we have 2 cases:

- if `R'` is supposed to halt, `R` will return true, which will make `R'` loop forever
- if `R'` is not supposed to halt, `R` will return false, which will make `R'` halts and return true

In both cases, we have a paradox: when `R` tells us that `R'` is supposed to halt, it loops forever and vice versa.

We started with the assumption that `R` would be able to tell us whether a program is going to halt or not and we ended up with a paradox, therefore the assumption was bad.

### An example with some python

Same story, let's assume that there is a function `is_halting` that takes 2 arguments:

- the content of a source file `src` that is given an input. A source could be: `src = "print('args:', arg)"`
- another input `arg`

```{.python .numberLines}
def is_halting(src: str, arg: Any) -> bool:
    # ...
    return result
```

When this function is executed, it either returns `True` or `False` depending on whether `src` associated with `arg` will halt or not.

<img alt="is_halting drawing" src="/img/misc/the-halting-problem/is_halting.png">

Now, let's make a program `paradox.py` that wraps our function.

Basically, we want to make a program that gives some source code and an argument to `is_halting` and if it returns `True`, it loops forever, else -if it is not supposed to halt-, we will print True.
It could look like:

```{.python .numberLines}
# ...
src = sys.argv[1]
arg = sys.argv[2]

result = is_halting(src, arg)
if result == True:
    # loop forever
    while True:
        pass
else:
    print(True)
```

<img alt="paradox.py drawing" src="/img/misc/the-halting-problem/paradox_py.png">

Finally, let see what happens when we give paradox.py to itself:

- If paradox.py is supposed to be halting, we will loop forever, meaning `paradox.py` is not halting. Oops.
- If paradox.py is **not** supposed to halt, we will get an answer, meaning it is actually halting. Oops, I did it again.

<img alt="paradox.py drawing given itself as inputs" src="/img/misc/the-halting-problem/paradox_py2.png">

We can then conclude that there is function `is_halting` that can gives a correct result.
