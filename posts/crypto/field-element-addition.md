---
title: Field element addition with big numbers in Rust
date: 2021/07/07
description: How to deal with field element addition in Rust
tags:
  - cryptography
  - rust
  - math
---

## Introduction

As I started to get interested in cryptography, I quickly tried to implement private key signing and verification.

One of the fundamentals is to use [finite fields](https://en.wikipedia.org/wiki/Finite_field_arithmetic) with a big prime P as the order of the field.

As I read mostly about [secp256k1](https://www.secg.org/sec2-v2.pdf), I'll deal with:

$P = 2^{256} - 2^{32} − 2^9 − 2^8 − 2^7 − 2^6 − 2^4 − 1$

usually shortened as:

$P = 2^{256} - 2^{32} - 977$

Making a poc in python is quite easy:

```{.python .numberLines}
P = 2**256 - 2**32 - 977

class Fe:
    def __init__(self, val):
        self.val = val

    def __add__(self, b):
        return self.__class__((self.val + b.val) % P)

    def __mul__(self, b):
        return self.__class__((self.val * b.val) % P)
```

Here `self.val`, `b` and `P` are supposedly close to 2<sup>256</sup> which is fine because Python already supports integers of arbitrary size. Python actually *mallocs* an array of `uint32_t` and splits the original number in power of 2<sup>30</sup> when dealing with big numbers.

## Field element representation in Rust

### The common approach

In C or Rust, we could imagine doing the same thing aka $(a + b) \mod P$ but then you'd have to find an integer type that fits at least 256 bits.

Is that enough?

Not really, if you add two u256 numbers, the maximum result is $2^{256} - 1 + 2^{256} - 1$, i.e. $2^{257} - 2$ so we need to handle an extra carry bit.

If we want to multiply two u256 numbers, the maximum result is $(2^{256} - 1)(2^{256} - 1)$ i.e. $2^{512} - 2^{257} + 1$ so now we also need a u512 type.

```{.rust .numberLines}
// after implementing u256 and u512

const P: u256 = (2u512.pow(256) - 0x100000000u256 - 0x3d1u256) as u256;

struct Fe {
    val: u256
}

impl Fe {
    fn new(val: u256) -> Self {
        Self { val }
    }

    fn add(&self, b: &Self) -> Self {
        let tmp: u512 = (self.val as u512 + b.val as u512) % (P as u512);

        Self { val: tmp as u256 }
    }

    fn mul(&self, b: &Self) -> Self {
        let tmp: u512 = (a as u512 * b.val as u512) % (P as u512);

        Self { val: tmp as u256 }
    }
}
```

1. We had to create 2 new integer types with one serving only as a temporary carry storage
2. There is a lot of waste for the addition as it needs at max 257 bits, meaning meaning 255 bits are just zeros and most generally all the explicit casts waste memory.

### Integer representation

We haven't talked yet about how to represent a u256, but since Rust supports u128, u64, u32, u16 and u8, we could use an array of "digits" to represent our number, just like Python does.

As we want to be efficient and limit the number of operations, 2 x u128 could be a good choice except we would still need to handle a carry when adding or multiplying the high or low digits of 2 u256.

For now, a better choice is to actually use 4 x u64 as it limits the number of instructions and we can use u128 as a temporary storage.

Finally, we would benefit from the x86_64 [imul instruction](https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-instruction-set-reference-manual-325383.pdf#G5.88727) instruction that can do multiplication of 2 u64 as `64x64 -> 128`.

```{.rust .numberLines}
pub struct Fe {
    d: [u64; 4]
}

impl Fe {
    pub fn new(d3: u64, d2: u64, d1: u64, d0: u64) -> Self {
        Self { d: [d0, d1, d2, d3] }
    }
}
```

### Addition v1

Ok, let's now define an `add` method (I'm not bringing additional traits yet):

```{.rust .numberLines}
    pub fn add(&self, b: &Self) -> Self {
        let (d0, d1, d2, d3): (u64, u64, u64, u64);
        let mut tmp: u128;

        tmp = self.d[0] as u128 + b.d[0] as u128;
        d0 = tmp as u64;
        tmp >>= 64;
        tmp += self.d[1] as u128 + b.d[1] as u128;
        d1 = tmp as u64;
        tmp >>= 64;
        tmp += self.d[2] as u128 + b.d[2] as u128;
        d2 = tmp as u64;
        tmp >>= 64;
        tmp += self.d[3] as u128 + b.d[3] as u128;
        d3 = tmp as u64;
        tmp >>= 64;
        // tmp here holds the final carry

        Self { d: [d0, d1, d2, d3] }
    }
```

Ok, so far we can make an addition of two u256, but we haven't dealt with the modulo part or the final carry.

Actually we can define the result of $A + B$ as:

$A + B = R_1 \cdot 2^{256} + R_0$

with: $R_0 < 2^{256}$ and $R_1 \in (0, 1)$

*Note: It helps to pick this form since our storage is 256 bits.*

This gives us 3 cases:

#### $R_1 = 0, R_0 < P$ (i.e. $R < P$)

The result is already less than $P$ so nothing to do:

\begin{equation}
(A + B) \mod P = R_0\label{eq:1}
\end{equation}

#### $R_1 = 0, R_0 \ge P$ (i.e. $P \le R < 2^{256}$)

Here the result hasn't overflowed 2<sup>256</sup>.

\begin{equation}
(A + B) \mod P = R_0 - P\label{eq:2}
\end{equation}

It's easy to prove:

\begin{align*}
& R_0 \mod P = R_0 - P\lfloor\frac{R_0}{P}\rfloor\\
& P \le R_0 < 2^{256} < 2P\\
& 1 \le \frac{R_0}{P} < 2\\
& \Rightarrow \lfloor\frac{R_0}{P}\rfloor = 1\\
& \Rightarrow R_0 \mod P = R_0 - P\\
& \Rightarrow (A + B) \mod P = R_0 - P\\
\end{align*}

#### $R_1 = 1$ (i.e. $R \ge 2^{256}$)

Here the result has overflowed. In this case:

\begin{equation}
(A + B) \mod P = R_0 + 2^{32} - 977\label{eq:3}
\end{equation}

And here is the proof:

\begin{align*}
& A + B & = & R_0 + 2^{256}\\
& (A + B) \mod P & = & (R_0 + 2^{256}) \mod P\\
& & = & R_0 \mod P + 2^{256} \mod P\\
\end{align*}

yet:

\begin{align*}
& A < P, B < P & \Rightarrow & A + B < 2P\\
& 2^{256} + R_0 < 2P & \Rightarrow & R_0 < 2P - 2^{256}\\
& P < 2^{256} & \Rightarrow & R_0 < P\\
& & \Rightarrow & R_0 \mod P = R_0\\
\end{align*}

And from \\eqref{eq:1}

$2^{256} \mod P = 2^{256} - P$

so:
\begin{align*}
& (A + B) \mod P = R_0 + 2^{256} - P\\
& (A + B) \mod P = R_0 + 2^{32} + 977\\
\end{align*}

### Addition v2

Let's add the modulo part in the addition:

```{.rust .numberLines}
    pub fn add(&self, b: &Self) -> Self {
        let (mut d0, mut d1, mut d2, mut d3): (u64, u64, u64, u64);
        let mut tmp: u128;

        tmp = self.d[0] as u128 + b.d[0] as u128;
        d0 = tmp as u64;
        tmp >>= 64;
        tmp += self.d[1] as u128 + b.d[1] as u128;
        d1 = tmp as u64;
        tmp >>= 64;
        tmp += self.d[2] as u128 + b.d[2] as u128;
        d2 = tmp as u64;
        tmp >>= 64;
        tmp += self.d[3] as u128 + b.d[3] as u128;
        d3 = tmp as u64;
        tmp >>= 64;

        // N = [d0, d1, d2, d3]
        // tmp is the extra carry
        if tmp > 0 {
            // R = N + 2**32 + 977
            tmp = d0 as u128 + 0x1000003d1u128;
            d0 = tmp as u64;
            tmp >>= 64;
            tmp += d1 as u128;
            d1 = tmp as u64;
            tmp >>= 64;
            tmp += d2 as u128;
            d2 = tmp as u64;
            tmp >>= 64;
            tmp += d3 as u128;
            d3 = tmp as u64;
        } else if d3 == 0xffffffffffffffffu64 &&
                  d2 == 0xffffffffffffffffu64 &&
                  d1 == 0xffffffffffffffffu64 &&
                  d0 >= 0xfffffffefffffc2fu64 {
            // P <= R < 2^256
            // R -= P
            d0 -= 0xfffffffefffffc2fu64;
            d1 = 0;
            d2 = 0;
            d3 = 0;
        }

        Self { d: [d0, d1, d2, d3] }
    }
```

### Addition v3

Now that works well but usually we have to deal with multiple additions in a row so this is not super optimized.
Suppose we have $((((a + b \mod P) + c) \mod P) + d) \mod P$, it would be more efficient to do $(a + b + c + d) \mod P$ 

In order to do this, we'd have to store the carry for later.

```{.rust .numberLines}
pub struct Fe {
    d: [u64; 4], // digits
    c: u64 // carry
}
```

With a 64 bits for the carry, it lets us do max 63 additions before we have to reduce the result, so let's write a reduce function and the updated add version:

```{.rust .numberLines}
    pub fn add(&self, b: &Self) -> Self {
        let (d0, d1, d2, d3): (u64, u64, u64, u64);
        let mut tmp: u128;

        tmp = self.d[0] as u128 + b.d[0] as u128;
        d0 = tmp as u64;
        tmp >>= 64;
        tmp += self.d[1] as u128 + b.d[1] as u128;
        d1 = tmp as u64;
        tmp >>= 64;
        tmp += self.d[2] as u128 + b.d[2] as u128;
        d2 = tmp as u64;
        tmp >>= 64;
        tmp += self.d[3] as u128 + b.d[3] as u128;
        d3 = tmp as u64;
        tmp >>= 64;

        Self { d: [d0, d1, d2, d3], c: self.c + b.c + tmp as u64 }
    }

    pub fn reduce(&mut self) {
        let (mut d0, mut d1, mut d2, mut d3) = (self.d[0], self.d[1], self.d[2], self.d[3]);
        let mut c: u128 = self.c as u128;
        let mut tmp: u128;

        if c > 0 {
            tmp = d0 as u128 + c * 0x1000003d1u128;
            d0 = tmp as u64;
            tmp >>= 64;
            tmp += d1 as u128;
            d1 = tmp as u64;
            tmp >>= 64;
            tmp += d2 as u128;
            d2 = tmp as u64;
            tmp >>= 64;
            tmp += d3 as u128;
            d3 = tmp as u64;
            tmp >>= 64;
            c = tmp;
            if c > 0 { // 2nd pass
                tmp = d0 as u128 + c * 0x1000003d1u128;
                d0 = tmp as u64;
                tmp >>= 64;
                tmp += d1 as u128;
                d1 = tmp as u64;
                tmp >>= 64;
                tmp += d2 as u128;
                d2 = tmp as u64;
                tmp >>= 64;
                tmp += d3 as u128;
                d3 = tmp as u64;
            }
        } else if d3 == 0xffffffffffffffffu64 &&
                  d2 == 0xffffffffffffffffu64 &&
                  d1 == 0xffffffffffffffffu64 &&
                  d0 >= 0xfffffffefffffc2fu64 {
            d0 -= 0xfffffffefffffc2fu64;
            d1 = 0;
            d2 = 0;
            d3 = 0;
        }

        self.d = [d0, d1, d2, d3];
        self.c = 0;
    }
```

Now we can make several additions, store the carries in c and finally reduce to P at the very end.

Let's also write a test:

```{.rust .numberLines}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_adds_field_elements_carry() {
        let a = Fe::new(
            0xffffffffffffffffu64,
            0xffffffffffffffffu64,
            0xffffffffffffffffu64,
            0xfffffffefffffc2eu64,
        ); // P - 1
        let b = &a;
        let r = a.add(b);
        let rb = &r;
        let mut r2 = r.add(rb);
        // r2 = ((p - 1 + p - 1) + (p - 1 + p - 1))
        // we overflow p 3 times, so the carry should be 3
        assert_eq!(r2.c, 3);
        r2.reduce();
        // r2 = ((p - 1 + p - 1) + (p - 1 + p - 1)) % p
        let expected = Fe::new(
            0xffffffffffffffffu64,
            0xffffffffffffffffu64,
            0xffffffffffffffffu64,
            0xfffffffefffffc2bu64,
        );
        assert_eq!(r2, expected);
    }
```

### Addition v4

Another optimization would be to use a carry save strategy. If we look at the addition, we propagate the carry on each digit. It's actually possible to reduce the storage size of each digit in order to keep bits for the carry.

I actually discovered it by looking at the [bitcoin implementation](https://github.com/bitcoin/bitcoin/blob/master/src/secp256k1/src/field_5x52.h) and by [asking the question](https://twitter.com/shaoner/status/1400208945277456400) directly to Pieter Wuille, the author of the libsecp256k1 used in bitcoin.

#### How it works

Instead of using 4 x u64 + a u64 carry, we could use 4 x u52 + 1 x u48 to represent our number (physically stored as 5 x u64) while keeping extra bits for the carry.

Now we don't have to propagate the carry anymore in the addition, it will be stored in the extra bits, as we have 12 extra bits for the 4 first digits and 16 bits for the last.

It allows us to rewrite the addition this way:

```{.rust .numberLines}
    pub fn add(&self, b: &Self) -> Self {
        let (d0, d1, d2, d3, d4): (u64, u64, u64, u64, u64);

        d0 = self.d[0] + b.d[0];
        d1 = self.d[1] + b.d[1];
        d2 = self.d[2] + b.d[2];
        d3 = self.d[3] + b.d[3];
        d4 = self.d[3] + b.d[3];

        Self { d: [d0, d1, d2, d3, d4] }
    }
```

We now have a 5th digit but it's pretty easy with less instructions. We can actually do 12 additions before one of the smallest carries overflows which is plenty enough.

Finally, we also have to rewrite our reduce function and optionally update our `new` method so it can easily transform 4 x u64 to 4 x u52 + 1 x u48, here is the final implementation:

```{.rust .numberLines}
impl Fe {
    pub fn new(d3: u64, d2: u64, d1: u64, d0: u64) -> Self {
        let (t0, t1, t2, t3): (u64, u64, u64, u64);
        let t4: u64;

        t0 = d0 & 0x000fffffffffffff;
        t1 = d0 >> 52 | (d1 & 0x000000ffffffffff) << 12; // 12 + 40
        t2 = d1 >> 40 | (d2 & 0x000000000fffffff) << 24; // 24 + 28
        t3 = d2 >> 28 | (d3 & 0x000000000000ffff) << 36; // 36 + 16
        t4 = d3 >> 16; // 48

        Self { d: [t0, t1, t2, t3, t4] }
    }

    pub fn add(&self, b: &Self) -> Self {
        let (d0, d1, d2, d3, d4): (u64, u64, u64, u64, u64);

        d0 = self.d[0] + b.d[0];
        d1 = self.d[1] + b.d[1];
        d2 = self.d[2] + b.d[2];
        d3 = self.d[3] + b.d[3];
        d4 = self.d[4] + b.d[4];

        Self { d: [d0, d1, d2, d3, d4] }
    }

    pub fn reduce(&mut self) {
        let (mut d0, mut d1, mut d2, mut d3, mut d4) = (self.d[0], self.d[1], self.d[2], self.d[3], self.d[4]);
        let mut c: u64;

        c = d4 >> 48;
        d4 &= 0x0000ffffffffffffu64;
        d0 += c * 0x1000003d1u64;
        d1 += d0 >> 52;
        d0 &= 0x000fffffffffffffu64;
        d2 += d1 >> 52;
        d1 &= 0x000fffffffffffffu64;
        d3 += d2 >> 52;
        d2 &= 0x000fffffffffffffu64;
        d4 += d3 >> 52;
        d3 &= 0x000fffffffffffffu64;

        if d4 > 0x0000ffffffffffffu64 {
            c = d4 >> 48;
            d4 &= 0x0000ffffffffffffu64;
            d0 += c * 0x1000003d1u64;
            d1 += d0 >> 52;
            d0 &= 0x000fffffffffffffu64;
            d2 += d1 >> 52;
            d1 &= 0x000fffffffffffffu64;
            d3 += d2 >> 52;
            d2 &= 0x000fffffffffffffu64;
            d4 += d3 >> 52;
            d3 &= 0x000fffffffffffffu64;
        }

        self.d = [d0, d1, d2, d3, d4];
    }
}
```

We also dropped the case $P \le R < 2^{256}$ because now this is handled by the carry itself.

The tradeoff comes with the multiplication / square operations because as explained by Pieter, we would have to do more digit operations in the multiplication Fe x Fe.

I still need to benchmark it and see if it's worth it because Elliptic curve point addition contains almost as many field element additions as field element multiplications.

*Why not 2 x u104 + 1 x 48?*

In the multiplication typically, we need to handle the carries differently. Using a long multiplication, we'd have to multiply 2 u104 resulting in 208 bits.

Anyway, see ya my bros ✌️
