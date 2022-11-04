---
title: Field element division with big numbers in Rust
date: 2021/09/15
description: How to deal with field element division in Rust
tags:
  - cryptography
  - rust
  - math
---

## Introduction

Yo everybody, now that we have addition and multiplication, we're going to need division.

Elliptic curve point addition requires field element addition, substraction, multiplication, square and division.
Substraction is very similar to addition and square is very similar to multiplication so I won't cover them. Modular division is a different story.

So we need to calculate $a / b$ with $b \neq 0$. Like in normal division, field division is the inverse of multiplication therefore:

$a / b = a \cdot 1 / b = a \cdot b^{-1}$

if we can get the modular inverse of b, we can then multiply it by a.


I'm going to evaluate 2 main methods:

* Fermat little theorem
* Binary GCD

## Fermat little theorem

Fermat little theorem demonstrates that when P is prime:

$x^{-1} \equiv x^{P - 2} \mod P$

Because we already have the multiplication working, we could indeed handle exponentiation.
Of course, we don't have to do $P - 2 - 1$ multiplications of x as we can store intermediary results and it can be done with some multiplications and squaring to have [fast exponentiation](https://en.wikipedia.org/wiki/Exponentiation_by_squaring#Basic_method).

It's definitely interesting and multiplications on a 64 bits x86 CPU are quite fast but most of my research showed that GCD is a good way to support multiple platforms.

The intent of this lib is to be part of a blockchain node and I like that you could run a node from a raspberry pi.

It actually seems that Parity uses [a similar approach](https://github.com/paritytech/libsecp256k1/blob/3c2a3c2b1cbdfa37555e3d9de3b4e5114693901c/core/src/field.rs#L1546) as for now.

## Extended euclidean arithmetic

Extended euclidean arithmetic extends the Euclidean arithmetic - duh - so we can compute the modular inverse.

### GCD

While reading on how to deal with modular inverse, I found out an interesting method using the GCD (greatest common divisor).

Commonly, the Euclidean algorithm we learn at school looks like this:

\begin{align*}
& r_0 = a\\
& r_1 = b\\
& r_2 = r_0 - q_{0}r_1\\
& r_3 = r_1 - q_{1}r_2\\
& ... \\
& r_{k} = r_{k-2} - q_{k-2}r_{k-1}\\
& r_{k+1} = r_{k-1} - q_{k-1}r_{k} = 0\\
\end{align*}

And if we want the GCD of two numbers a and b, we just iterate until $r_{k+1} = 0$ and we have $r_k = gcd(a, b)$

Example with $a = 2023, b = 714$:
\begin{align*}
& r_0 = 2023\\
& r_1 = 714\\
& r_2 = 2023 - 2 * 714 = 595\\
& r_3 = 714 - 1 * 595 = \textbf{119}\\
& r_4 = 595 - 5 * 119 = 0\\
\end{align*}

Thanks and bye.

### Bézout's identity

Ok great but how does it help finding the modular inverse?

Well now we have to use [Bézout's identity](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity), quoting wikipedia:

> Let a and b be integers with greatest common divisor d. Then there exist integers x and y such that ax + by = d. More generally, the integers of the form ax + by are exactly the multiples of d. 

It allows us to write this:

$ax + by = gcd(a, b)$

It becomes useful when a and b are co-prime because in this case:

$ax + by = 1$

$ax = b(-y) + 1$

Exactly like we would write an euclidean division: $a' = bq + r$ with $a' = ax$

And we can deduce: $ax \equiv 1 \mod b$, therefore x is the multiplicative inverse of a mod b, and this is exactly what we want.

### Extended Euclidean algorithm

*How to calculate x and y?*

The Extended Euclidean algorithm is actually about finding Bézout coefficients x and y:

\begin{align*}
& r_0 = a, r_1 = b\\
& x_0 = 1, x_1 = 0\\
& y_0 = 0, y_1 = 1\\
& r_2 = r_0 - q_{0}r_1\\
& x_2 = x_0 - q_{0}x_1\\
& y_2 = y_0 - q_{0}y_1\\
& r_3 = r_1 - q_{1}r_2\\
& x_3 = x_1 - q_{0}x_2\\
& y_3 = y_1 - q_{0}y_2\\
& ... \\
& r_{k} = r_{k-2} - q_{k-2}r_{k-1}\\
& x_{k} = x_{k-2} - q_{k-2}x_{k-1}\\
& y_{k} = y_{k-2} - q_{k-2}y_{k-1}\\
& r_{k+1} = r_{k-1} - q_{k-1}r_{k} = 0\\
\end{align*}

It gives us: $gcd(a, b) = r_k = ax_k + by_k$

### Application for P

If a and b are co-prime, $ax \equiv 1 \mod b$

Well, our P is prime itself so we already know that a and P are co-prime, i.e. $ax \equiv 1 \mod P$ and we can calculate x thanks to the extended euclidean algo.

In python it looks like:

```{.python .numberLines}
P = 2**256 - 2**32 - 977

def modinv(a, m):
    r0 = a
    r1 = m
    x = 1
    y = 0
    i = 0
    while r1 != 0:
        q = r0 // r1
        tmp = r0 - q * r1
        tmp2 = x - q * y
        r0 = r1
        r1 = tmp
        x = y
        y = tmp2
        i += 1
    if x < 0:
        x += m
    return x0
```

Now if we want $a/b$ we can do:

```{.python}
a * modinv(b, P)
```

Another way is to modify the function so that x0 is initialized with the dividend directly, it works the same way because x0 is not involved in the loop condition and we only subtract values to it.

For now, it's unclear if it's better and a simple modinv and multiplication though.

Anyway...

## TADAM

<img alt="Winner gif" src="/img/crypto/modular-division/winner.gif">

Okay, that's cool but coming back to Rust, we cannot actually use our field element type here because we need signedness and all the operations without a reduction to P.

We need a new type that handles signedness, multiplication, integer division, addition and substraction. This type would need at least 257 bits: 1 bit for the sign, 256 bits to represent numbers close to P.

After dealing with our field element type, this seems easy enough except for the integer division. Indeed, if we want to compute a quotient of two big numbers. There are multiple interesting algorithms to deal with this but a simpler method is to use the binary GCD algorithm.

Please follow me, it's this way:

<img alt="Down gif" src="/img/crypto/modular-division/down.gif">

## Extended Binary GCD

The interesting part of this GCD algorithm is that it allows us to compute the GCD with only divisions by 2, so only right shifts.

The algorithm is described as follow [on wikipedia](https://en.wikipedia.org/wiki/Binary_GCD_algorithm):

\begin{align}
& gcd(u, 0) = u & gcd(0, v) = v\\
& gcd(2u, 2v) = 2 \cdot gcd(u, v) &&\\
& gcd(2u, v) = gcd(u, v) \mbox{ if v is odd} & gcd(u, 2v) = gcd(u, v) \mbox{ if u is odd} &\\
& gcd(u, v) = gcd(|u − v|, min(u, v)) \mbox{ if u and v are both odd}\\
\end{align}

### Implementation

Taking the definition, it can be written this way:

```{.python .numberLines}
def bin_gcd(u, v):
    if u == 0:
        return v
    if v == 0:
        return u
    k = 1
    while u != v:
        if u & 0x1 == 0:
            if v & 0x1 != 0:
                # gcd(2u, v) = gcd(u, v)
                u >>= 1
            else:
                # gcd(2u, 2v) = 2 * gcd(u, v)
                u >>= 1
                v >>= 1
                k <<= 1
        elif v & 0x1 == 0:
            # gcd(u, 2v) = gcd(u, v)
            v = v >> 1
        else:
            # gcd(u, v) = gcd(|u - v|, min(u, v))
            if u > v:
                u = (u - v)
            else:
                tmp = u
                u = (v - u)
                v = tmp
    return u * k
```

### Binary mod inverse

Now this is a very basic implementation but in our case we want to integrate x such as $ux \equiv 1 \mod P$ to create a modinv function.

Some interesting things to notice before writing a modinv version:

* the factor `k` isn't necessary anymore, as it doesn't play a role in the calculation, it's just used to compute the GCD which would be 1 in our case
* all the divisions by 2 are exact

Refactoring our function, we can integrate x and y like we did before:

```python
def div2(x, m):
    if x & 1:
        x += m
    return x >> 1

def modinv(a, m):
    u = a
    v = m
    x = 1
    y = 0
    while u != v:
        if (u & 0x01) == 0x00:
            u >>= 1
            x = div2(x, m)
        elif (v & 0x01) == 0x00:
            v >>= 1
            y = div2(y, m)
        elif u > v:
            u = (u - v) >> 1
            x = div2(x - y, m)
        else:
            v = (v - u) >> 1
            y = div2(y - x, m)
    return y
```

Note that we have a new `div2` function because to compute an exact division, we want the dividend to be even. If it's is odd, we can just add the -prime- moduli to it. Some possible optimizations will be covered in a next article.

It can be further simplified by just switching $u$ and $v$ when $u < v$:

```{.python .numberLines}
def modinv_classic(a, m):
    u = a
    v = m
    x = 1
    y = 0
    while u != 0:
        if (u & 0x01) == 0x00:
            u >>= 1
            x = mdiv2(x, m)
        else:
            if u < v:
                tmp = u
                u = v
                v = tmp
                tmp = x
                x = y
                y = tmp
            u = (u - v) >> 1
            x = div2(x - y, m)
    return y
```

## Let's rust

### Recap

A quick recap, we want to add a modinv function to our field element type.

For this, we need to create a modified binary gcd function that calculates the modular inverse of a value x. This function needs to work with signed numbers. Thus, we need to create a signed integer type.

### Scalar

We want to represent numbers on 256 bits + 1 bit for the sign. However as we actually do multiple additions and substraction, it could be interesting to keep a carry and even more interesting to use the same carry-save tricks we use on our field element type.

#### modinv

This time `modinv` isn't optimized specifically for $P$, instead we can pass a modulo m just so we can re-use the type:

```{.rust .numberLines}
#[derive(Clone, Copy, PartialEq, Eq)]
pub struct Scalar {
    pub d: [u64; 5]
}

impl Scalar {
    // ...
    fn div2_mod(&mut self, m: &Self) {
        if !self.is_even() {
            self.add_assign(m);
        }
        self.div2()
    }

    pub fn modinv(&mut self, m: &Self) {
        let mut b = *m;
        let mut x = Self::from_u64(1u64);
        let mut y = Self::from_u64(0u64);

        while !self.is_zero() {
            if self.is_even() {
                self.div2();
                x.div2_mod(m);
            } else {
                if *self < b {
                    mem::swap(self, &mut b);
                    mem::swap(&mut x, &mut y);
                }
                *self -= b;
                self.div2();
                x -= y;
                x.div2_mod(m);
            }
        }
        y.normalize(m);
        *self = y;
    }
}
```

It works exactly the same way as the python function. The only trick is to define the `div2` function as a shift by 1. I didn't go much into details about the other functions implementation because it mainly depends on the limb representation of the Scalar but if we forget about carry optimization, [it looks like this](https://github.com/alexlren/astrel_secp256k1/blob/71f553bace9bede731355d54a3d5c06cb6dfd41d/src/modinv.rs).

Now for the carry optim version, we could simply implement something similar to our field element, and keep 1 bit per limb for the sign but that's out of scope.

#### Field element division

We can simply define our field element `inverse`:

```{.rust .numberLines}
    pub fn to_scalar(&self) -> Scalar {
        let d0 = (self.d[0] >> 0) | (self.d[1] << 52);
        let d1 = (self.d[1] >> 12) | (self.d[2] << 40);
        let d2 = (self.d[2] >> 24) | (self.d[3] << 28);
        let d3 = (self.d[3] >> 36) | (self.d[4] << 16);

        Scalar::new(0, d3, d2, d1, d0)
    }

    pub fn from_scalar(&mut self, n: &Scalar) {
        let d0 = n.d[0] & 0x000fffffffffffff;
        let d1 = n.d[0] >> 52 | (n.d[1] & 0x000000ffffffffff) << 12;
        let d2 = n.d[1] >> 40 | (n.d[2] & 0x000000000fffffff) << 24;
        let d3 = n.d[2] >> 28 | (n.d[3] & 0x000000000000ffff) << 36;
        let d4 = n.d[3] >> 16;

        self.d = [d0, d1, d2, d3, d4];
    }

    pub fn inverse(&mut self) {
        self.reduce();
        let mut n = self.to_scalar();
        n.modinv(&P);
        self.from_scalar(&n);
    }
```

and even some syntactic sugar for the division itself:

```{.rust .numberLines}
    pub div_assign(&mut self, rhs: &Self) {
        let n = *rhs;
        n.inverse();
        return self.mul_assign(n);
    }

```

Alright, time to go to bed everyone.
