---
title: Deutsch Oracle Problem
date: 2022/11/10
description: Introduction to quantum computing
tags:
  - quantum computing
  - problem
  - math
---

## Intro

Here is a small introduction about quantum computing and how it works.
Knowing almost nothing about this part of computer science, I decided to dig into the rabbit hole and read more about it.
I'm still very new at this (a noob) so I hope that this article makes some kind of sense. I found that the best way for me to understand a concept is to explain it completely so here it is!

In this article/tutorial, we're going to discover qubits, why are they different from classical bits, how we can build quantum logic gates, and we're going to solve a simple problem where quantum computers actually outperform classical computers. Pretty awesome.

Also the quantum world is actually hard to conceptualize usually. I read that our native languages are not fit for it, therefore it's usually easier to see the math.

Let's jump into the quantum realm.

<img src="/img/quantum/antman.gif" alt="Ant-Man quantumania"/>

## Classical bits representation

Classical bits are units that represent 2 states: 0 or 1. It's the foundation of classical computing.

For the rest of the article, we're going to use a vector notation:

* bit 0: $\begin{pmatrix}1\\0\end{pmatrix}$ or using the Dirac vector notation: $\ket{0}$
* and bit 1: $\begin{pmatrix}0\\1\end{pmatrix}$ or: $\ket{1}$

A good way to remember which bit is which, you can think of the vector as an array with 1 at the index of the bit.

Now there are 4 operations we can apply to a bit: Identity, Negation, Set 0, Set 1.
We can actually use a matrix as a transformation operator.

#### Identity

$f(x) = x$

| $f(\ket{0}) = \ket{0}$ | $f(\ket{1}) = \ket{1}$ |
|------------------------|------------------------|
| $\begin{pmatrix}1 & 0 \\0 & 1\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}$ | $\begin{pmatrix}1 & 0 \\0 & 1\end{pmatrix}\begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix}$ |

#### Negation

$f(x) = \neg{x}$

| $f(\ket{0}) = \ket{1}$ | $f(\ket{1}) = \ket{0}$ |
|------------------------|------------------------|
| $\begin{pmatrix}0 & 1 \\1 & 0\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix}$ | $\begin{pmatrix}0 & 1 \\1 & 0\end{pmatrix}\begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}$ |

#### Set 0

$f(x) = 0$

| $f(\ket{0}) = \ket{0}$ | $f(\ket{1}) = \ket{0}$ |
|------------------------|------------------------|
| $\begin{pmatrix}1 & 1 \\0 & 0\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}$ | $\begin{pmatrix}1 & 1 \\0 & 0\end{pmatrix}\begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}$ |

#### Set 1

$f(x) = 1$

| $f(\ket{0}) = \ket{1}$ | $f(\ket{1}) = \ket{1}$ |
|------------------------|------------------------|
| $\begin{pmatrix}0 & 0 \\1 & 1\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix}$ | $\begin{pmatrix}0 & 0 \\1 & 1\end{pmatrix}\begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix}$ |


### Multiple bits

To represent multiple classical bits and keep consistency with each of the operations, we can use the tensor product of multiple vectors, each vector representing a single bit.

For 2 bits, it looks like: $\begin{pmatrix}a\\b\end{pmatrix} \otimes \begin{pmatrix}c\\d\end{pmatrix} = \begin{pmatrix}ac\\ad\\bc\\bd\end{pmatrix}$

For 3 bits: $\begin{pmatrix}a\\b\end{pmatrix} \otimes \begin{pmatrix}c\\d\end{pmatrix} \otimes \begin{pmatrix}e\\f\end{pmatrix} = \begin{pmatrix}ace\\acf\\ade\\adf\\bce\\bcf\\bde\\bdf\end{pmatrix}$

Example:

|  |  |  |  |
|--|--|--|--|
| $\ket{00} = \begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}1\\0\\0\\0\end{pmatrix}$ | $\ket{01} = \begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}0\\1\\0\\0\end{pmatrix}$ | $\ket{10} = \begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}0\\0\\1\\0\end{pmatrix}$ | $\ket{11} = \begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}0\\0\\0\\1\end{pmatrix}$ |

And again we see that $\ket{N}$ is a vector with a 1 at the Nth index.

### Multi bits gates

#### CNOT gate

One common gate is called the CNOT gate. It takes 2 bits in input and "returns" 2 bits. The 1st bit is called the control bit and the 2nd bit is called the target bit. It behaves like this:

* If the control bit is 0, the target bit is left unchanged.
* If the control bit is 1, the target bit is flipped.

It can be represented as a matrix as well: $\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix}$

|  |  |  |  |
|--|--|--|--|
| $C(\ket{00}) = \ket{00}$ | $C(\ket{01}) = \ket{01}$ | $C(\ket{10}) = \ket{11}$ | $C(\ket{11}) = \ket{10}$ |
| $\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix} \begin{pmatrix}1\\0\\0\\0\end{pmatrix} = \begin{pmatrix}1\\0\\0\\0\end{pmatrix}$ | $\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix} \begin{pmatrix}0\\1\\0\\0\end{pmatrix} = \begin{pmatrix}0\\1\\0\\0\end{pmatrix}$ | $\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix} \begin{pmatrix}0\\0\\1\\0\end{pmatrix} = \begin{pmatrix}0\\0\\0\\1\end{pmatrix}$ | $\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix} \begin{pmatrix}0\\0\\0\\1\end{pmatrix} = \begin{pmatrix}0\\0\\1\\0\end{pmatrix}$ |

We can see the 2 parts in the matrix with $\begin{pmatrix}1 & 0\\0 & 1\end{pmatrix}$ reflecting the identity part (leaving the target unchanged) and the $\begin{pmatrix}0 & 1\\1 & 0\end{pmatrix}$ reflecting the flipping part.

## Qubits

Qubits are physical objets (ions, photons, nucleus, electrons, ...) that can be used as units of quantum measurement. The difference with classical bits is that qubits can represent states that are neither 0 or 1, but a proportion of both 0 and 1 at the same time.

That weird state is called superposition.

And because we're in the quantum world, it's only when we measure a qubit that it collapses with a probability to finally be 0 or 1. 

Now the way I understand it is with an example, if you have 3 bits, you can make 8 combinations: `000`, `001`, `010`, `011`, `100`, `101`, `110`, and `111`. However you're only getting 1 information out of 3 bits.

In superposition, you can imagine that your qubits are in all those states at the same times, so 3 qubits gets 8 pieces of information, even though you can't measure that information yet.

Mesuring is what makes all your qubits to collapse to a state, therefore coming back to being classical bits.

The power of qubits is to use superposition so that N Qubits gives you $2^N$ bit of information only until you measure your results. Exponential information!

<img src="/img/quantum/unlimited_powers.gif" alt="unlimited powers gif">

When I started reading about Qubits, I couldn't make sense of it but again, math is the language we need to understand it better.

### Representation of Qubits

Qubits can also be written as vectors with each element of the vector a probability, and so a qubit is represented as: $\begin{pmatrix}a\\b\end{pmatrix}$ with $||a||^2 + ||b||^2 = 1$ with $a, b \in \mathbb{C}$ and so it has the probability $||a||^2$ to be 0 and $||b||^2$ to be 1.

so it can also look like $\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$ or even $\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$ which works because $\left|\left|\frac{1}{\sqrt{2}}\right|\right|^2 + \left|\left|-\frac{1}{\sqrt{2}}\right|\right|^2 = 1$

Note that in both these examples, the Qubit has 50% chance to collapse to either 0 or 1! When it's 50/50, it's called equal superposition.

Our classical bits vectors are just specific qubits, with:

$\ket{0} = \begin{pmatrix}1\\0\end{pmatrix}$ having the probability 100% of being a 0 and $\ket{1} = \begin{pmatrix}0\\1\end{pmatrix}$ having the probability 100% of being a 1

We now have some tools to manipulate our qubits, we can apply a CNOT to a pair of qubits or simply flip a qubit state, whatever that state is and even if we don't know it, for example:

$\begin{pmatrix}0 & 1\\1 & 0\end{pmatrix} \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$

### Operations on qubits

Note that all operations on qubits have to be [reversible](https://en.wikipedia.org/wiki/Reversible_computing).
An operation is said to be reversible if knowing the output and the function, you're able to know or reconstruct the input.

Identity and Negation are reversible, however Set-0 and Set-1 are not.
Indeed, both functions are constant and don't use the input at all, so knowing the result it's impossible to know what the input was.

For constant operations, like Set-0 and Set-1, we can instead configure a gate using multiple Qubits. We'll see how this works next in the article.

## Bloch sphere

So far, we've been using matrixes but it also helps to visualize common Qubits on a sphere. It is called the [Bloch sphere](https://en.wikipedia.org/wiki/Bloch_sphere)

To make it easy, we can consider Qubits with $a, b \in \mathbb{R}$ and so in that case, we only need a circle (which simplifies the drawings).

We can use the probability to be 0 as the x coordinate and the probability to be 1 as the y coordinate. It looks like this:

<div style="position: relative; width: 300px; height: 300px">
  <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
  <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
  <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
  <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
  <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
  <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
  <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
  <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div> 
  <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
    <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
    <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
  </svg>
</div>

We can actually navigate through the circle, for example bit flips:

<div style="position: relative; width: 300px; height: 300px">
  <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
  <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
  <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
  <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
  <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
  <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
  <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
  <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div> 
  <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
    <defs>
      <marker id="startarrow" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
        <polygon points="5 0, 5 7, 0 3.5" fill="#f00" />
      </marker>
      <marker id="endarrow" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
       <polygon points="0 0, 5 3.5, 0 7" fill="#f00" />
      </marker>
    </defs>
    <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
    <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="190" y1="90" x2="110" y2="10" stroke="#f00" stroke-width="2" marker-end="url(#endarrow)" marker-start="url(#startarrow)"/>
    <line x1="45" y1="45" x2="155" y2="155" stroke="#f00" stroke-width="2" marker-end="url(#endarrow)" marker-start="url(#startarrow)"/>
    <line x1="10" y1="110" x2="90" y2="190" stroke="#f00" stroke-width="2" marker-end="url(#endarrow)" marker-start="url(#startarrow)"/>
    <circle cx="170" cy="30" r="10" stroke="#f00" stroke-width="2" marker-mid="url(#startarrow)" fill="rgba(0,0,0,0)"/>
    <circle cx="30" cy="170" r="10" stroke="#f00" stroke-width="2" marker-mid="url(#startarrow)" fill="rgba(0,0,0,0)"/>
  </svg>
</div>

## Hadamard gate

Another gate we need before we dig into the problem we want to solve is the [Hadamard gate](https://en.wikipedia.org/wiki/Hadamard_transform#Quantum_computing_applications)

The hadamard gate takes a Qubit in equal superposition and turns it to a $\ket{0}$ or a $\ket{1}$. It's matrix representation looks like: $\begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix}$

|  |  |  |  |
|--|--|--|--|
|$\begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix} \begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}$|$\begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix} \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix}$|$\begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix} \begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}0\\-1\end{pmatrix}$|$\begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix} \begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}-1\\0\end{pmatrix}$|

and on our Bloch circle:

<div style="position: relative; width: 300px; height: 300px">
  <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
  <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
  <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
  <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
  <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
  <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
  <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
  <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div> 
  <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
    <defs>
      <marker id="startarrow2" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
        <polygon points="5 0, 5 7, 0 3.5" fill="#00f" />
      </marker>
      <marker id="endarrow2" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
       <polygon points="0 0, 5 3.5, 0 7" fill="#00f" />
      </marker>
    </defs>
    <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
    <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="110" y1="25" x2="155" y2="155" stroke="#00f" stroke-width="2" marker-end="url(#endarrow2)" marker-start="url(#startarrow2)"/>
    <line x1="45" y1="45" x2="90" y2="175" stroke="#00f" stroke-width="2" marker-end="url(#endarrow2)" marker-start="url(#startarrow2)"/>
    <line x1="25" y1="105" x2="45" y2="155" stroke="#00f" stroke-width="2" marker-end="url(#endarrow2)" marker-start="url(#startarrow2)"/>
    <line x1="160" y1="55" x2="175" y2="100" stroke="#00f" stroke-width="2" marker-end="url(#endarrow2)" marker-start="url(#startarrow2)"/>
  </svg>
</div>

## The Deutsch oracle problem

We're going to write a system with multiple gates so that we can actually find a result to a question faster than on a classical computer.

The question is: Given an unknown function, is this function constant (Set-0 / Set-1) or is this function variable (Identity / Negation)?

### Classical approach

On a classical computer it could look like this:

<div style="position: relative; width: 400px; height: 200px;">
  <div style="position: absolute; left: 60px; top: 60px;">$\ket{x}$</div>
  <div style="position: absolute; left: 260px; top: 60px;">$f(\ket{x})$</div>
  <svg width="400" height="200">
    <line x1="50" y1="100" x2="150" y2="100" stroke="#00f" stroke-width="2"/>
    <path d="M150 50 L200 50 M200 50 L200 150 M200 150 L150 150 M150 150 L150 50" stroke="#00f" stroke-width="2" fill="none" />
    <text x="160" y="100" fill="#00f">?</text>
    <line x1="200" y1="100" x2="300" y2="100" stroke="#00f" stroke-width="2"/>
  </svg>
</div>

And in order to know what the function is, we can use 2 queries:

| f(0) | f(1) | Result   |
|------|------|----------|
| 0    | 0    | f = Set-0    |
| 0    | 1    | f = Identity |
| 1    | 0    | f = Negation |
| 1    | 1    | f = Set-1    |

Knowing if the function is constant or variable takes also 2 queries.


### Quantum approach

On a quantum computer, remember that our function has to be reversible so we need a way for Set-0 and Set-1 to be reversible as well first.

The way to do it is to actually rewire our system to use multiple qubits for all the operations: Identity, Negation, Set-0, Set-1.

In the real world, note that qubits are resources that are changed, so in this case, we need 2 qubits:

* the input qubit that is left unchanged (in blue)
* the output qubit where the result is written (in red)

<div style="position: relative; width: 400px; height: 200px;">
  <div style="position: absolute; left: 60px; top: 40px;">$\ket{0}$</div>
  <div style="position: absolute; left: 60px; top: 90px;">$\ket{x}$</div>
  <div style="position: absolute; left: 260px; top: 40px;">$f(\ket{x})$</div>
  <div style="position: absolute; left: 260px; top: 90px;">$\ket{x}$</div>
  <svg width="400" height="200">
    <line x1="50" y1="75" x2="150" y2="75" stroke="#f00" stroke-width="2"/>
    <line x1="50" y1="125" x2="150" y2="125" stroke="#00f" stroke-width="2"/>
    <path d="M150 50 L200 50 M200 50 L200 150 M200 150 L150 150 M150 150 L150 50" stroke="#00f" stroke-width="2" fill="none" />
    <text x="160" y="100" fill="#00f">?</text>
    <line x1="200" y1="75" x2="300" y2="75" stroke="#f00" stroke-width="2"/>
    <line x1="200" y1="125" x2="300" y2="125" stroke="#00f" stroke-width="2"/>
  </svg>
</div>

It's intuitive to understand that having the input qubit left unchanged gives us an information for Set-0 and Set-1 that allows us to know what the function is.

Let's now write all our operations using 2 qubits with the input the MSB (most significant bit) and the output the LSB (least significant bit).

It is normal to be confused by this part at first but hopefully it gets clearer afterwards.

To recap: we want to write all our operations as reversible operations (because this is how quantum computers work) and to do this, we pass an additional "output" qubit as input to our function. This qubit is initialized to $\ket{0}$ and is used to write the result of the operation, while the input qubit on the other hand is left unchanged. We'll see that using 2 qubits allows us to write reversible operations.

#### Set-0

<div style="position: relative; width: 400px; height: 160px;">
  <div style="position: absolute; left: 60px; top: 20px;">$\ket{0}$</div>
  <div style="position: absolute; left: 60px; top: 70px;">$\ket{x}$</div>
  <div style="position: absolute; left: 260px; top: 20px;">$\ket{0}$</div>
  <div style="position: absolute; left: 260px; top: 70px;">$\ket{x}$</div>

  <svg width="400" height="160">
    <line x1="50" y1="50" x2="300" y2="50" stroke="#f00" stroke-width="2"/>
    <line x1="50" y1="100" x2="300" y2="100" stroke="#00f" stroke-width="2"/>
    <path d="M150 25 L200 25 M200 25 L200 125 M200 125 L150 125 M150 125 L150 25" stroke="#00f" stroke-width="2" fill="none" />
  </svg>
</div>

In this case, we have nothing to do, the output qubit is already set to 0, and we want to leave the input qubit unchanged, so we can just leave our qubits as they are.

| Step | $\ket{00}$ | $\ket{10}$ |
|------|------------|------------|
| | $f(\ket{00}) = \ket{00}$ | $f(\ket{10}) = \ket{10}$ |
| identity | $\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{pmatrix} \begin{pmatrix}1\\0\\0\\0\end{pmatrix} = \begin{pmatrix}1\\0\\0\\0\end{pmatrix}$ | $\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{pmatrix} \begin{pmatrix}0\\0\\1\\0\end{pmatrix} = \begin{pmatrix}0\\0\\1\\0\end{pmatrix}$ |

#### Set-1

<div style="position: relative; width: 400px; height: 160px;">
  <div style="position: absolute; left: 60px; top: 20px;">$\ket{0}$</div>
  <div style="position: absolute; left: 60px; top: 70px;">$\ket{x}$</div>
  <div style="position: absolute; left: 260px; top: 20px;">$\ket{1}$</div>
  <div style="position: absolute; left: 260px; top: 70px;">$\ket{x}$</div>
  <svg width="400" height="160">
    <rect x="160" y="35" width="30" height="30" fill="#f00"/>
    <text x="170" y="55" fill="#fff">X</text>
    <line x1="50" y1="50" x2="160" y2="50" stroke="#f00" stroke-width="2"/>
    <line x1="50" y1="100" x2="300" y2="100" stroke="#00f" stroke-width="2"/>
    <line x1="190" y1="50" x2="300" y2="50" stroke="#f00" stroke-width="2"/>
    <path d="M150 25 L200 25 M200 25 L200 125 M200 125 L150 125 M150 125 L150 25" stroke="#00f" stroke-width="2" fill="none" />
  </svg>
</div>

This time we have to flip our "output" qubit so it becomes 1, we just added a negation gate.

| Step | $\ket{00}$ | $\ket{10}$ |
|------|------------|------------|
| | $f(\ket{00}) = \ket{01}$ | $f(\ket{10}) = \ket{11}$ |
| identity | $\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{pmatrix} \begin{pmatrix}1\\0\\0\\0\end{pmatrix} = \begin{pmatrix}1\\0\\0\\0\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix}$ | $\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{pmatrix} \begin{pmatrix}0\\0\\1\\0\end{pmatrix} = \begin{pmatrix}0\\0\\1\\0\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix}$ |
| X | $\begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}0 & 1\\1 & 0\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}0\\1\\0\\0\end{pmatrix}$ | $\begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}0 & 1\\1 & 0\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}0\\0\\0\\1\end{pmatrix}$ |

#### Identity

<div style="position: relative; width: 400px; height: 160px;">
  <div style="position: absolute; left: 60px; top: 20px;">$\ket{0}$</div>
  <div style="position: absolute; left: 60px; top: 70px;">$\ket{x}$</div>
  <div style="position: absolute; left: 260px; top: 20px;">$\ket{x}$</div>
  <div style="position: absolute; left: 260px; top: 70px;">$\ket{x}$</div>
  <svg width="400" height="160">
    <line x1="50" y1="50" x2="300" y2="50" stroke="#f00" stroke-width="2"/>
    <line x1="50" y1="100" x2="300" y2="100" stroke="#00f" stroke-width="2"/>
    <path d="M150 25 L200 25 M200 25 L200 125 M200 125 L150 125 M150 125 L150 25" stroke="#00f" stroke-width="2" fill="none" />
    <circle cx="175" cy="50" r="8" fill="none" stroke-width="2" stroke="#f00"/>
    <line x1="175" y1="42" x2="175" y2="100" stroke="#f00" stroke-width="2"/>
    <circle cx="175" cy="100" r="3" fill="#f00"/>
  </svg>
</div>

In this case we have to use a CNOT gate, with the input as the control bit.

| Step | $\ket{00}$ | $\ket{10}$ |
|------|------------|------------|
| | $f(\ket{00}) = \ket{00}$ | $f(\ket{10}) = \ket{11}$ |
| CNOT | $C\left(\begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix}\right) = \begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix} \begin{pmatrix}1\\0\\0\\0\end{pmatrix} = \begin{pmatrix}1\\0\\0\\0\end{pmatrix}$ | $C\left(\begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix}\right) = \begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix} \begin{pmatrix}0\\0\\1\\0\end{pmatrix} = \begin{pmatrix}0\\0\\0\\1\end{pmatrix}$ |

#### Negation

<div style="position: relative; width: 400px; height: 160px;">
  <div style="position: absolute; left: 60px; top: 20px;">$\ket{0}$</div>
  <div style="position: absolute; left: 60px; top: 70px;">$\ket{x}$</div>
  <div style="position: absolute; left: 260px; top: 20px;">$\neg{\ket{x}}$</div>
  <div style="position: absolute; left: 260px; top: 70px;">$\ket{x}$</div>
  <svg width="400" height="160">
    <line x1="50" y1="50" x2="300" y2="50" stroke="#f00" stroke-width="2"/>
    <line x1="50" y1="100" x2="300" y2="100" stroke="#00f" stroke-width="2"/>
    <path d="M150 25 L200 25 M200 25 L200 125 M200 125 L150 125 M150 125 L150 25" stroke="#00f" stroke-width="2" fill="none" />
    <circle cx="165" cy="50" r="8" fill="none" stroke-width="2" stroke="#f00"/>
    <line x1="165" y1="42" x2="165" y2="100" stroke="#f00" stroke-width="2"/>
    <circle cx="165" cy="100" r="3" fill="#f00"/>
    <rect x="180" y="42" width="15" height="15" fill="#f00"/>
    <text x="184" y="54" font-size="0.8em" fill="#fff">X</text>
  </svg>
</div>

And negation is pretty much same as identity with the CNOT gate, where we just flip the result by adding a negation gate.

| Step | $\ket{00}$ | $\ket{10}$ |
|------|------------|------------|
| | $f(\ket{00}) = \ket{01}$ | $f(\ket{10}) = \ket{10}$ |
| CNOT | $C\left(\begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix}\right) = \begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix} \begin{pmatrix}1\\0\\0\\0\end{pmatrix} = \begin{pmatrix}1\\0\\0\\0\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix}$ | $C\left(\begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix}\right) = \begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix} \begin{pmatrix}0\\0\\1\\0\end{pmatrix} = \begin{pmatrix}0\\0\\0\\1\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}0\\1\end{pmatrix}$ |
| X | $\begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}0 & 1\\1 & 0\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}0\\1\\0\\0\end{pmatrix}$ | $\begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}0 & 1\\1 & 0\end{pmatrix}\begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix} \otimes \begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}0\\0\\1\\0\end{pmatrix}$ |

|  |
|--|
| $f(\ket{00}) = \ket{01}$ |
| $f(\ket{10}) = \ket{10}$ |


### Resolution

Now that we defined all the operations using 2 qubits, how can we know if a function is constant or variable using a single query?

The solution is to:

1. initialize 2 qubits to $\ket{0}$
2. apply a bit flip, so both are now $\ket{1}$
3. apply the Hadamard gate, so both are now in equal superposition: $\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$
4. apply the function f
5. apply the Hadamard gate again
6. measure the result:
  * if the function is constant, it should be $\ket{11}$
  * if the function is variable, it should be $\ket{01}$

<div style="position: relative; width: 400px; height: 200px;">
  <div style="position: absolute; left: 60px; top: 40px;">$\ket{0}$</div>
  <div style="position: absolute; left: 60px; top: 90px;">$\ket{0}$</div>
  <svg width="400" height="200">
    <line x1="50" y1="75" x2="150" y2="75" stroke="#f00" stroke-width="2"/>
    <line x1="50" y1="125" x2="150" y2="125" stroke="#00f" stroke-width="2"/>
    <path d="M150 50 L200 50 M200 50 L200 150 M200 150 L150 150 M150 150 L150 50" stroke="#00f" stroke-width="2" fill="none" />
    <text x="160" y="100" fill="#00f">?</text>
    <line x1="200" y1="75" x2="300" y2="75" stroke="#f00" stroke-width="2"/>
    <line x1="200" y1="125" x2="300" y2="125" stroke="#00f" stroke-width="2"/>
    <rect x="90" y="68" width="15" height="15" fill="#f00"></rect>
    <rect x="120" y="68" width="15" height="15" fill="#0a0"></rect>
    <rect x="90" y="118" width="15" height="15" fill="#f00"></rect>
    <rect x="120" y="118" width="15" height="15" fill="#0a0"></rect>
    <rect x="215" y="68" width="15" height="15" fill="#0a0"></rect>
    <rect x="215" y="118" width="15" height="15" fill="#0a0"></rect>
    <rect x="250" y="68" width="45" height="15" fill="#000"></rect>
    <rect x="250" y="118" width="45" height="15" fill="#000"></rect>
    <text x="92" y="80" fill="#fff">X</text>
    <text x="122" y="80" fill="#fff">H</text>
    <text x="92" y="130" fill="#fff">X</text>
    <text x="122" y="130" fill="#fff">H</text>
    <text x="217" y="80" fill="#fff">H</text>
    <text x="217" y="130" fill="#fff">H</text>
    <text x="252" y="80" fill="#fff" font-size="0.7em">Measure</text>
    <text x="252" y="130" fill="#fff" font-size="0.7em">Measure</text>
  </svg>
</div>

After the first 3 steps, both qubits are always in state: $\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$

Let see what happens from each function:

#### Set-0

| Step |                | Notes |
|------|----------------|-------|
| 4. Apply Set-0 gate | $f(\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$ | Input and Output are left unchanged |
| 5. Apply H gate to each qubits | $H(\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix}\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix}$ <br> $H(\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix}\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix}$ | |

which gives us: $\ket{11}$

<table style="width: 100%">
  <colgroup>
    <col style="width: 50%">
    <col style="width: 50%">
  </colgroup>
  <thead>
    <tr class="header">
      <th>Input Qubit</th>
      <th>Output Qubit</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td style="text-align: center">
    <div style="position: relative; width: 300px; height: 300px; display: inline-block">
      <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div> 
      <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
        <defs>
          <marker id="startarrow2" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="5 0, 5 7, 0 3.5" fill="#00f" />
          </marker>
          <marker id="endarrow2" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
           <polygon points="0 0, 5 3.5, 0 7" fill="#00f" />
          </marker>
        </defs>
        <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
        <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="110" y1="25" x2="155" y2="155" stroke="#00f" stroke-width="2" marker-start="url(#startarrow2)"/>
      </svg>
    </div>
  </td>
  <td style="text-align: center">
    <div style="position: relative; width: 300px; height: 300px; display: inline-block">
      <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
     <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div> 
     <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
       <defs>
         <marker id="startarrow2" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
           <polygon points="5 0, 5 7, 0 3.5" fill="#00f" />
         </marker>
         <marker id="endarrow2" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
       <polygon points="0 0, 5 3.5, 0 7" fill="#00f" />
      </marker>
    </defs>
    <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
    <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="110" y1="25" x2="155" y2="155" stroke="#00f" stroke-width="2" marker-start="url(#startarrow2)"/>
  </svg>
</div>
</td>
</tr>
</tbody>
</table>

#### Set-1

| Step |                | Notes |
|------|----------------|-------|
| 4. Apply Set-1 gate | $f(\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$ | Input is left unchanged <br> Output is flipped |
| 5. Apply H to each qubits | $H(\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix}\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix}$ <br> $H(\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix}\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}0\\-1\end{pmatrix}$ | |

which gives us: $\ket{11}$

> Note that $\begin{pmatrix}0\\-1\end{pmatrix} = \ket{1}$ simply because there is a probability $||-1||^2$ to be 1.

<table style="width: 100%">
  <colgroup>
    <col style="width: 50%">
    <col style="width: 50%">
  </colgroup>
  <thead>
    <tr class="header">
      <th>Input Qubit</th>
      <th>Output Qubit</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td style="text-align: center">
    <div style="position: relative; width: 300px; height: 300px; display: inline-block">
      <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div> 
      <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
        <defs>
          <marker id="startarrow2" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="5 0, 5 7, 0 3.5" fill="#00f" />
          </marker>
          <marker id="endarrow2" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
           <polygon points="0 0, 5 3.5, 0 7" fill="#00f" />
          </marker>
        </defs>
        <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
        <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="110" y1="25" x2="155" y2="155" stroke="#00f" stroke-width="2" marker-start="url(#startarrow2)"/>
      </svg>
    </div>
  </td>
  <td style="text-align: center">
    <div style="position: relative; width: 300px; height: 300px; display: inline-block">
      <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
     <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div> 
     <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
       <defs>
         <marker id="startarrow2" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
           <polygon points="5 0, 5 7, 0 3.5" fill="#00f" />
         </marker>
         <marker id="endarrow2" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
       <polygon points="0 0, 5 3.5, 0 7" fill="#00f" />
      </marker>
    </defs>
    <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
    <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="155" y1="155" x2="45" y2="45" stroke="#00f" stroke-width="2" marker-end="url(#endarrow2)"/>
    <line x1="45" y1="45" x2="100" y2="175" stroke="#00f" stroke-width="2" marker-end="url(#endarrow2)"/>
  </svg>
</div>
</td>
</tr>
</tbody>
</table>

#### Identity

| Step |                | Notes |
|------|----------------|-------|
| 4. Apply Identity gate | $f(\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$ | $C(\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix}\begin{pmatrix}\frac{1}{2}\\-\frac{1}{2}\\-\frac{1}{2}\\\frac{1}{2}\end{pmatrix} = \frac{1}{2}\begin{pmatrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 0 & 1\\0 & 0 & 1 & 0\end{pmatrix}\begin{pmatrix}1\\-1\\-1\\1\end{pmatrix}$ <br>$= \frac{1}{2}\begin{pmatrix}1\\-1\\1\\-1\end{pmatrix} = \begin{pmatrix}\frac{1}{2}\\-\frac{1}{2}\\\frac{1}{2}\\-\frac{1}{2}\end{pmatrix} = \begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$ |
| 5. Apply H to each qubits | $H(\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix}\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}$ <br> $H(\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix}\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}0\\1\end{pmatrix}$ | |

which gives us: $\ket{01}$

<table style="width: 100%">
  <colgroup>
    <col style="width: 50%">
    <col style="width: 50%">
  </colgroup>
  <thead>
    <tr class="header">
      <th>Input Qubit</th>
      <th>Output Qubit</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td style="text-align: center">
    <div style="position: relative; width: 300px; height: 300px; display: inline-block">
      <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div> 
      <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
        <defs>
          <marker id="startarrow2" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="5 0, 5 7, 0 3.5" fill="#00f" />
          </marker>
          <marker id="endarrow2" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
           <polygon points="0 0, 5 3.5, 0 7" fill="#00f" />
          </marker>
        </defs>
        <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
        <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="155" y1="50" x2="155" y2="155" stroke="#00f" stroke-width="2" marker-start="url(#startarrow2)"/>
        <line x1="155" y1="50" x2="175" y2="100" stroke="#00f" stroke-width="2" marker-end="url(#endarrow2)"/>
      </svg>
    </div>
  </td>
  <td style="text-align: center">
    <div style="position: relative; width: 300px; height: 300px; display: inline-block">
      <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
     <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
     <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
       <defs>
         <marker id="startarrow2" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
           <polygon points="5 0, 5 7, 0 3.5" fill="#00f" />
         </marker>
         <marker id="endarrow2" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
       <polygon points="0 0, 5 3.5, 0 7" fill="#00f" />
      </marker>
    </defs>
    <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
    <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="110" y1="25" x2="155" y2="155" stroke="#00f" stroke-width="2" marker-start="url(#startarrow2)"/>
  </svg>
</div>
</td>
</tr>
</tbody>
</table>

#### Negation

| Step |                | Notes |
|------|----------------|-------|
| 4. Apply Identity gate | $f(\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix} \otimes \begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$ | Same as previously but with an additional bit flip on the output |
| 5. Apply H to each qubits | $H(\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix}\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}$ <br> $H(\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}) = \begin{pmatrix}\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{pmatrix}\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix} = \begin{pmatrix}0\\-1\end{pmatrix}$ | |

which gives us: $\ket{01}$

<table style="width: 100%">
  <colgroup>
    <col style="width: 50%">
    <col style="width: 50%">
  </colgroup>
  <thead>
    <tr class="header">
      <th>Input Qubit</th>
      <th>Output Qubit</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td style="text-align: center">
    <div style="position: relative; width: 300px; height: 300px; display: inline-block">
      <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div> 
      <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
        <defs>
          <marker id="startarrow2" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="5 0, 5 7, 0 3.5" fill="#00f" />
          </marker>
          <marker id="endarrow2" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
           <polygon points="0 0, 5 3.5, 0 7" fill="#00f" />
          </marker>
        </defs>
        <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
        <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
        <line x1="155" y1="50" x2="155" y2="155" stroke="#00f" stroke-width="2" marker-start="url(#startarrow2)"/>
        <line x1="155" y1="50" x2="175" y2="100" stroke="#00f" stroke-width="2" marker-end="url(#endarrow2)"/>
      </svg>
    </div>
  </td>
  <td style="text-align: center">
    <div style="position: relative; width: 300px; height: 300px; display: inline-block">
      <div style="position: absolute; top: calc(50% - 25px); left: 0; width: 50px; text-align: center">$\begin{pmatrix}-1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: 0; left: calc(25px + 200px / 2); width: 50px; text-align: center">$\begin{pmatrix}0\\1\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(50% - 25px); left: calc(100% - 50px); width: 50px; text-align: center">$\begin{pmatrix}1\\0\end{pmatrix}$</div>
      <div style="position: absolute; top: calc(100% - 50px); left: calc(50% - 25px); width: 50px; text-align: center">$\begin{pmatrix}0\\-1\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 25px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
      <div style="position: absolute; top: 225px; left: 25px; width: 50px; text-align: center">$\begin{pmatrix}-\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
     <div style="position: absolute; top: 225px; left: 225px; width: 50px; text-align: center">$\begin{pmatrix}\frac{1}{\sqrt{2}}\\-\frac{1}{\sqrt{2}}\end{pmatrix}$</div>
     <svg width="200" height="200" style="position: absolute; top: 50px; left: 50px">
       <defs>
         <marker id="startarrow2" markerWidth="5" markerHeight="7" refX="5" refY="3.5" orient="auto">
           <polygon points="5 0, 5 7, 0 3.5" fill="#00f" />
         </marker>
         <marker id="endarrow2" markerWidth="5" markerHeight="7" refX="0" refY="3.5" orient="auto" markerUnits="strokeWidth">
       <polygon points="0 0, 5 3.5, 0 7" fill="#00f" />
      </marker>
    </defs>
    <circle cx="100" cy="100" r="80" fill="#fff" stroke="#000" stroke-width="2"/>
    <line x1="0" y1="100" x2="200" y2="100" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="100" y1="-100" x2="100" y2="200" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="25" y1="25" x2="175" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="175" y1="25" x2="25" y2="175" stroke="#aaa" stroke-dasharray="2" stroke-width="1"/>
    <line x1="45" y1="45" x2="155" y2="155" stroke="#00f" stroke-width="2" marker-start="url(#startarrow2)"/>
    <line x1="45" y1="45" x2="100" y2="175" stroke="#00f" stroke-width="2" marker-end="url(#endarrow2)"/>
  </svg>
</div>
</td>
</tr>
</tbody>
</table>

### Recap

* Using our system with Set-0 and Set-1 operations, we end up with $\ket{11}$ as the output
* Using our system with Identity and Negation operations, we end up with $\ket{01}$ as the output

For each those cases, it took us 1 single query to the operation as opposed to 2 queries on a classic computer.

<img src="/img/quantum/dwight.gif" alt="Dwight victory gif"/>

The [Deutsch–Jozsa algorithm](https://en.wikipedia.org/wiki/Deutsch%E2%80%93Jozsa_algorithm) generalizes the idea using functions that take N-bit input and generate single 0 or 1 bit, i.e. $f\{0,1\}^n \rightarrow \{0,1\}$
