---
title: Field element multiplication with big numbers in Rust
date: 2021/07/26
description: How to deal with field element multiplication in Rust
tags:
  - cryptography
  - rust
  - math
---

## Introduction

We saw in the [addition part 1](/2021/07/07/crypto/modular-addition.html) multiple ways to represent our field elements which is key to optimization.

The final version was 4 x u52 and 1 x 48 to store our 256 bits leaving the extra bits for the carry.

```{.rust .numberLines}
pub struct Fe {
    d: [u64; 5]
}
```

## The long multiplication

### Algo with 4 x u64

To make it easier we can start working with 4 u64 digits as we did for the addition, so $a \times b$:

\begin{align*}
& && [t_7] && [t_6] && [t_5] && [t_4] && [t_3] && [t_2] && [t_1] && [t_0]\\
& \\
&       && && && && && a_3 && a_2 && a_1 && a_0\\
&\times && && && && && b_3 && b_2 && b_1 && b_0\\
\hline
& && && && && && b_0 \cdot a_3 && b_0 \cdot a_2 && b_0 \cdot a_1 && b_0 \cdot a_0\\
& && && && && b_1 \cdot a_3 && b_1 \cdot a_2 && b_1 \cdot a_1 && b_1 \cdot a_0 && 0\\
& && && && b_2 \cdot a_3 && b_2 \cdot a_2 && b_2 \cdot a_1 && b_2 \cdot a_0 && 0 && 0\\
& && && b_3 \cdot a_3 && b_3 \cdot a_2 && b_3 \cdot a_1 && b_3 \cdot a_0 && 0 && 0 && 0\\
\hline
& && +c_6 && +c_5 && +c_4 && +c_3 && +c_2 && +c_1 && +c_0 && 0\\
\end{align*}

I labeled each column with $t_i$ with $i := 0 \rightarrow 7$ so it's easier.
And finally we also define $c_i$ with $i := 0 \rightarrow 6$ as the carries for each column.

Since we represent $a$ and $b$ with 4 digits, there are now 8 terms in our result:

\begin{align}
& t_0 = b_0 \cdot a_0\\
& t_1 = b_0 \cdot a_1 + b_1 \cdot a_0 + c_0\label{eq:t_1}\\
& t_2 = b_0 \cdot a_2 + b_1 \cdot a_1 + b_2 \cdot a_0 + c_1\\
& t_3 = b_0 \cdot a_3 + b_1 \cdot a_2 + b_2 \cdot a_1 + b_3 \cdot a_0 + c_2\label{eq:t_3}\\
& t_4 = b_1 \cdot a_3 + b_2 \cdot a_2 + b_3 \cdot a_1 + c_3\\
& t_5 = b_2 \cdot a_3 + b_3 \cdot a_2 + c_4\\
& t_6 = b_3 \cdot a_3 + c_5\\
& t_7 = c_6\\
\end{align}

Now we have an issue here, because most of these terms can exceed 128 bits while we only have a u128. For example $t_1$ \\eqref{eq:t_1} is $64 \times 64 + 64 \times 64 + 64 \rightarrow 129$, meaning we would need 129 bits.

Fortunately if we go back to our u52 strategy, we don't have this issue anymore because at worse $t_3$ \\eqref{eq:t_3} is $52 \times 52 + 52 \times 52 + 52 \times 52 + 52 \times 52 + 52 \rightarrow 106$ i.e. requires 106 bits

### Algo with 4 x u52 + u48

Let's get back to our u52 baby

<img src="/img/crypto/modular-multiplication/barney_wink.gif">

Now our beautiful multiplication looks more like:

\begin{align*}
& && [t_9] && [t_8] && [t_7] && [t_6] && [t_5] && [t_4] && [t_3] && [t_2] && [t_1] && [t_0]\\
& \\
&       && && && && && && a_4 && a_3 && a_2 && a_1 && a_0\\
&\times && && && && && && b_4 && b_3 && b_2 && b_1 && b_0\\
\hline
& && && && && && && b_0 \cdot a_4 && b_0 \cdot a_3 && b_0 \cdot a_2 && b_0 \cdot a_1 && b_0 \cdot a_0\\
& && && && && && b_1 \cdot a_4 && b_1 \cdot a_3 && b_1 \cdot a_2 && b_1 \cdot a_1 && b_1 \cdot a_0 && 0\\
& && && && && b_2 \cdot a_4 && b_2 \cdot a_3 && b_2 \cdot a_2 && b_2 \cdot a_1 && b_2 \cdot a_0 && 0 && 0\\
& && && && b_3 \cdot a_4 && b_3 \cdot a_3 && b_3 \cdot a_2 && b_3 \cdot a_1 && b_3 \cdot a_0 && 0 && 0 && 0\\
& && && b_4 \cdot a_4 && b_4 \cdot a_3 && b_4 \cdot a_2 && b_4 \cdot a_1 && b_4 \cdot a_0 && 0 && 0 && 0 && 0\\
\hline
& && +c_8 && +c_7 && +c_6 && +c_5 && +c_4 && +c_3 && +c_2 && +c_1 && +c_0 && \\
\end{align*}

\begin{align}
& t_0 = b_0 \cdot a_0\\
& t_1 = b_0 \cdot a_1 + b_1 \cdot a_0 + c_0\\
& t_2 = b_0 \cdot a_2 + b_1 \cdot a_1 + b_2 \cdot a_0 + c_1\\
& t_3 = b_0 \cdot a_3 + b_1 \cdot a_2 + b_2 \cdot a_1 + b_3 \cdot a_0 + c_2\\
& t_4 = b_0 \cdot a_4 + b_1 \cdot a_3 + b_2 \cdot a_2 + b_3 \cdot a_1 + b_4 \cdot a_0 + c_3\\
& t_5 = b_1 \cdot a_4 + b_2 \cdot a_3 + b_3 \cdot a_2 + b_4 \cdot a_1+ c_4\\
& t_6 = b_2 \cdot a_4 + b_3 \cdot a_3 + b_4 \cdot a_2 + c_5\\
& t_7 = b_3 \cdot a_4 + b_4 \cdot a_3 + c_6\\
& t_8 = b_4 \cdot a_4 + c_7\\
& t_9 = c_8\\
\end{align}

We can also see our result R as $R = R_1 \cdot 2^{256} + R_0$ with:

* $R_0$ composed of the digits $t_0, t_1, t_2, t_3, t_4$
* $R_1$ composed of the digits $t_5, t_6, t_7, t_8, t_9$

Now because of the size of $R_1$, it's actually more interesting to reduce our result modulo $P$ directly in the multiplication as opposed to our previous [add function](/2021/07/07/crypto/modular-addition.html) in which we could store the carry in the extra bits.

The final purpose is to be able to make multiplications of numbers close to $P$ so the carry $R_1$ won't fit in our 64-bits reserved space.

Similarly to the addition, we have 3 cases:

1. $R_1 = 0$ and $R_0 < P$

$R = R_0$

2. $R_1 = 0$, $P <= R_0 < 2^{256}$

$R = R_0 - P$

3. $R_1 > 0$

$R = R_0 + R_1 \cdot (2^{256} - P)$

For more clarity, let's define $P_0 = 2^{256} - P = 2^{32} + 977$, we can now have:

\begin{align}
& t_0 = b_0 \cdot a_0 + t_5 \cdot P_0\\
& t_1 = b_0 \cdot a_1 + b_1 \cdot a_0 + c_0 + t_6 \cdot P_0\\
& t_2 = b_0 \cdot a_2 + b_1 \cdot a_1 + b_2 \cdot a_0 + c_1 + t_7 \cdot P_0\\
& t_3 = b_0 \cdot a_3 + b_1 \cdot a_2 + b_2 \cdot a_1 + b_3 \cdot a_0 + c_2 + t_8 \cdot P_0\\
& t_4 = b_0 \cdot a_4 + b_1 \cdot a_3 + b_2 \cdot a_2 + b_3 \cdot a_1 + b_4 \cdot a_0 + c_3 + t_9 \cdot P_0\\
\end{align}

Cool, now we have new carries to propagate:

\begin{align}
& t_0 = b_0 \cdot a_0 + t_5 \cdot P_0 + c_4' \cdot P_0\\
& t_1 = b_0 \cdot a_1 + b_1 \cdot a_0 + c_0 + t_6 \cdot P_0 + c_0' + c_0''\\
& t_2 = b_0 \cdot a_2 + b_1 \cdot a_1 + b_2 \cdot a_0 + c_1 + t_7 \cdot P_0 + c_1' + c_1''\\
& t_3 = b_0 \cdot a_3 + b_1 \cdot a_2 + b_2 \cdot a_1 + b_3 \cdot a_0 + c_2 + t_8 \cdot P_0 + c_2' + c_2''\\
& t_4 = b_0 \cdot a_4 + b_1 \cdot a_3 + b_2 \cdot a_2 + b_3 \cdot a_1 + b_4 \cdot a_0 + c_3 + t_9 \cdot P_0 + c_3' + c_3''\\
\end{align}

It's actually way easier to see it this way:


\begin{align}
&& A \times B = & R_1 \cdot 2^{256} + R_0\\
&& (A \times B) \mod P = & R_0 + R_1 \cdot (2^{256} - P)\\
&& = & R_0 + R_1 \cdot P_0\\
\end{align}

### NOW IN RUST LADIES AND GENTLEMEN



```{.rust .numberLines}
    pub fn mul(&self, b: &Self) -> Self {
        const M52: u128 = 0x000fffffffffffffu128; // 2^52 - 1
        const M48: u128 = 0x0000ffffffffffffu128; // 2^48 - 1
        const P0: u128 = 0x1000003d1u128; // 2^32 + 977

        let (a0, a1, a2, a3, a4) = (self.d[0], self.d[1], self.d[2], self.d[3], self.d[4]);
        let (b0, b1, b2, b3, b4) = (b.d[0], b.d[1], b.d[2], b.d[3], b.d[4]);

        let (
            mut t0, mut t1, mut t2,
            mut t3, mut t4, mut t5,
            mut t6, mut t7, mut t8
        ): (
            u64, u64, u64,
            u64, u64, u64,
            u64, u64, u64
        );
        let t9: u64;

        let mut t: u128;
        let mut c: u128;

        t = a0 as u128 * b0 as u128;
        t0 = (t & M52) as u64;
        t >>= 52;
        t += a0 as u128 * b1 as u128 +
            a1 as u128 * b0 as u128;
        t1 = (t & M52) as u64;
        t >>= 52;
        t += a0 as u128 * b2 as u128 +
            a1 as u128 * b1 as u128 +
            a2 as u128 * b0 as u128;
        t2 = (t & M52) as u64;
        t >>= 52;
        t += a0 as u128 * b3 as u128 +
            a1 as u128 * b2 as u128 +
            a2 as u128 * b1 as u128 +
            a3 as u128 * b0 as u128;
        t3 = (t & M52) as u64;
        t >>= 52;
        t += a0 as u128 * b4 as u128 +
            a1 as u128 * b3 as u128 +
            a2 as u128 * b2 as u128 +
            a3 as u128 * b1 as u128 +
            a4 as u128 * b0 as u128;
        t4 = (t & M52) as u64;
        t >>= 52;
        c = t4 as u128 >> 48;
        t4 &= M48 as u64;

        t += a1 as u128 * b4 as u128 +
            a2 as u128 * b3 as u128 +
            a3 as u128 * b2 as u128 +
            a4 as u128 * b1 as u128;
        t5 = (t & M52) as u64;
        t >>= 52;
        t5 = t5 << 4 | c as u64;
        c = t5 as u128 >> 52;
        t5 &= M52 as u64;

        t += a2 as u128 * b4 as u128 +
            a3 as u128 * b3 as u128 +
            a4 as u128 * b2 as u128;
        t6 = (t & M52) as u64;
        t >>= 52;
        t6 = t6 << 4 | c as u64;
        c = t6 as u128 >> 52;
        t6 &= M52 as u64;
        
        t += a3 as u128 * b4 as u128 +
            a4 as u128 * b3 as u128;
        t7 = (t & M52) as u64;
        t >>= 52;
        t7 = t7 << 4 | c as u64;
        c = t7 as u128 >> 52;
        t7 &= M52 as u64;

        t += a4 as u128 * b4 as u128;
        t8 = (t & M52) as u64;
        t >>= 52;
        t8 = t8 << 4 | c as u64;
        c = t8 as u128 >> 52;
        t8 &= M52 as u64;

        t9 = (t << 4 | c) as u64;

        // 1st reduction R = R1 + R0 * P0
        t = t0 as u128 + t5 as u128 * P0;
        t0 = (t & M52) as u64;
        t >>= 52;

        t += t1 as u128 + t6 as u128 * P0;
        t1 = (t & M52) as u64;
        t >>= 52;

        t += t2 as u128 + t7 as u128 * P0;
        t2 = (t & M52) as u64;
        t >>= 52;

        t += t3 as u128 + t8 as u128 * P0;
        t3 = (t & M52) as u64;
        t >>= 52;

        t += t4 as u128 + t9 as u128 * P0;
        t4 = (t & M52) as u64;
        t >>= 52;
        c = (t4 >> 48) as u128;
        t4 &= M48 as u64;

        c = c | t << 4;

        // 2nd pass
        t = t0 as u128 + c * P0;
        t0 = (t & M52) as u64;
        t >>= 52;

        t += t1 as u128;
        t1 = (t & M52) as u64;
        t >>= 52;

        t += t2 as u128;
        t2 = (t & M52) as u64;
        t >>= 52;

        t += t3 as u128;
        t3 = (t & M52) as u64;
        t >>= 52;

        t += t4 as u128;
        t4 = (t & M48) as u64;

        Self { d: [t0, t1, t2, t3, t4] }
    }
```

Finally let's write a quick test:

```{.rust .numberLines}
    #[test]
    fn it_multiply_field_elements() {
        // A=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffbfefffffc2f = p - 2^42
        // B=0xfffffffffffffffffffffffffffffffffffffffffffffffffffff7fefffffc2f = p - 2^43
        let a = Fe::new(
            0xffffffffffffffffu64,
            0xffffffffffffffffu64,
            0xffffffffffffffffu64,
            0xfffffbfefffffc2fu64,
        );
        let b = Fe::new(
            0xffffffffffffffffu64,
            0xffffffffffffffffu64,
            0xffffffffffffffffu64,
            0xfffff7fefffffc2fu64,
        );
        let r = a.mul(&b);
        // r = ((p - 2^42) * (p - 2^43)) % p
        let expected = Fe::new(
            0x0000000000000000u64,
            0x0000000000000000u64,
            0x0000000000200000u64,
            0x0000000000000000u64,
        );
        assert_eq!(r, expected);
    }
```

and we now have a multiplication.

# JUST LIKE THAT

<img src="/img/crypto/modular-multiplication/booya.gif">

Verbose, but it works.

### Optimizations

#### Carry-saver

Okay, now let's just think about it, we actually don't have to propate the carry after the 2nd pass.
Same as the addition, we can just use our carry-save storage.

A very simple way to prove it is to work with the worst case scenario: $(P - 1)(P - 1)$

After the 1st pass, it gives us a result $R0 = \mathrm{1000003d0fffffffffffffffffffffffffffffffffffffffffffffffefffff85dfff16f60}_{16}$
Or $R0 = 2^{256} \times \mathrm{1000003d0}_{16} + \mathrm{fffffffffffffffffffffffffffffffffffffffffffffffefffff85dfff16f60}_{16}$

Now applying the 2nd pass:
\begin{align}
R1 & = \mathrm{fffffffffffffffffffffffffffffffffffffffffffffffefffff85dfff16f60}_{16} + \mathrm{1000003d0}_{16} \times (2^{32} + 977)\\
\end{align}

$\mathrm{1000003d0}_{16} \times (2^{32} + 977)$ is 65 bits so our first digit needs 66 bits.
We only have 12 extra bits on the 1st digit $d_0$, so we need to propagate the carry on the 2nd digit $d_1$

And we don't have to go further for now, we can still work with few operations before we overflow our 320 bits storage.

Let's remove the last carry propagation on t3 and t4:

```{.rust .numberLines}
        // ...
        // 2nd pass
        t = t0 as u128 + c * P0;
        t0 = (t & M52) as u64;
        t >>= 52;

        t += t1 as u128;
        t1 = (t & M52) as u64;

        Self { d: [t0, t1, t2, t3, t4] }
```

#### Combine operations

Another optimization would be to combine the operations on $t_0$, we have:

```rust
        // 1st pass
        t = t0 as u128 + t5 as u128 * P0;
        t0 = (t & M52) as u64;
        // ...
        // 2nd pass
        t = t0 as u128 + c * P0;
        t0 = (t & M52) as u64;
```

Could be nice to combine those just so we save some instructions, better to do $t_0 + (a + b)P_0$ than $t_0 + aP_0 + bP_0$

We can use the fact that we don't need to propagate the carry over $t_3$ and $t_4$ on the 2nd pass. Therefore, we can work with them first.

#### Final version

```{.rust .numerLines}
    pub fn mul(&mut self, b: &Self) -> Self {
        const M52: u128 = 0x000fffffffffffffu128; // 2^52 - 1
        const M48: u64 = 0x0000ffffffffffffu64; // 2^48 - 1
        const P0: u128 = 0x1000003d1u128; // 2^32 + 977
        const P1: u128 = 0x1000003d10u128; // 2^32 + 977 << 4

        let (a0, a1, a2, a3, a4) = (
            self.d[0] as u128, self.d[1] as u128, self.d[2] as u128,
            self.d[3] as u128, self.d[4] as u128
        );
        let (b0, b1, b2, b3, b4) = (
            b.d[0] as u128, b.d[1] as u128, b.d[2] as u128,
            b.d[3] as u128, b.d[4] as u128
        );
        let mut tx: u128;
        let mut cx: u128;
        let (t0, t1, t2, mut t3, mut t4, mut t5): (u64, u64, u64, u64, u64, u128);
        let c4: u64;

        // t3
        tx = a0 * b3 + a1 * b2 + a2 * b1 + a3 * b0;
        // t8
        cx = a4 * b4;
        // t3 + t8 * P1
        tx += (cx & M52) * P1;
        cx >>= 52;
        t3 = (tx & M52) as u64;
        tx >>= 52;

        // t4
        tx += a0 * b4 + a1 * b3 + a2 * b2 + a3 * b1 + a4 * b0;
        // (c3 + t4) + (c8 + t9) * P1
        tx += cx * P1;
        t4 = (tx & M52) as u64;
        tx >>= 52;
        c4 = t4 >> 48;
        t4 &= M48;

        // t5
        cx = tx + a1 * b4 + a2 * b3 + a3 * b2 + a4 * b1;
        // t0
        tx = a0 * b0;
        t5 = cx & M52;
        cx >>= 52;
        t5 = (t5 << 4) | c4 as u128;
        // c9 + t0 + (c4 + t5) * P0
        tx += t5 * P0;
        t0 = (tx & M52) as u64;
        tx >>= 52;

        // t1
        tx += a0 * b1 + a1 * b0;
        // t6
        cx += a2 * b4 + a3 * b3 + a4 * b2;
        // c0 + t1 + (c5 + t6) * P1
        tx += (cx & M52) * P1;
        cx >>= 52;
        t1 = (tx & M52) as u64;
        tx >>= 52;

        // t2
        tx += a0 * b2 + a1 * b1 + a2 * b0;
        // t7
        cx += a3 * b4 + a4 * b3;
        // t2 + t7 * P1
        tx += (cx & M52) * P1;
        cx >>= 52;
        t2 = (tx & M52) as u64;
        tx >>= 52;

        // t23
        tx += cx * P1 + t3 as u128;
        t3 = (tx & M52) as u64;
        tx >>= 52;
        // t24
        tx += t4 as u128;
        t4 = tx as u64;

        Self { d: [t0, t1, t2, t3, t4] }
    }
```
