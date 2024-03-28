+++
title = "03 - Untyped Arithmatic Expressions"
date = 2024-03-23
+++

Language:

```python
t ::=
	true  # constant true
	false  # constant false
	if t then t else t  # conditional
	0  # constant 0
	succ t  # successor
	pred t  # predecessor
	iszero t  # zero test
```

---

Notice that the syntax of terms permits the formation of some dubious- looking terms like succ true and if 0 then 0 else 0. We shall have more to say about such terms later—indeed, in a sense they are precisely what makes this tiny language interesting for our purposes, since they are examples of the sorts of nonsensical programs we will want a type system to exclude.

---

(3.2.1) Definition [Terms, inductively]: The set of terms is the smallest set T such that

1. {true, false, 0} ⊆ T ;
2. ift1 ∈T,then{succt1,predt1,iszerot1}⊆T;
3. ift1 ∈T,t2 ∈T,andt3 ∈T,thenift1 thent2 elset3 ∈T.

---

(3.2.4) How many elements does $S_3$​ have?

[Permutations and combinations (Algebra 2, Discrete mathematics and probability) – Mathplanet](https://www.mathplanet.com/education/algebra-2/discrete-mathematics-and-probability/permutations-and-combinations)

[Permutations Calculator nPr](https://www.calculatorsoup.com/calculators/discretemathematics/permutations.php)

Things I could have gotten wrong:

- permutations vs combinations - I don't think I did. Order matters for this, `if true then 0 else false` is not the same as `if false then true else 0` etc.
- I could be double-counting the initial set...

$$
\begin{flalign}
|S_0| &= 0 && S_0 = {\empty}\\
|S_1| &= 3 && S_1 = \{true, false, 0\}\\
|S_2| &= 3 && \{true, false, 0\}\\
      &+ P(|S_1|, 1) * 3 && \text{3 options for all in the set}\\
      &+ P(|S_1|, 3) * 1\\
      &= 3 + P(3,1)*3 + P(3,3)*1\\
      &= 3 + 9 + 6 = 18\\
|S_3| &= 3 + P(|S_2|,1)*3 + P(|S_2|,3) * 1\\
      &= 3 + P(18,1)*3 + P(18,3)*1\\
      &= 3 + 54 + 4896 = 4953
      
\end{flalign}
$$

Um, their solution is far different...

Ok, the issue was that my permutations didn't consider replacement into the set. i.e., doesn't allow something like `if 0 then 0 else 0`. That's even easier to compute - it's $|S_i|^n$.

then, the solution makes more sense.
$$
|S_{i}| = 3 + |S_{i-1}|*3 + |S_{i-1}|^3*1
$$
Let's move on.

---

(3.2.5)  Exercise [««]: Show that the sets Si are cumulative—that is, that for each i

we have Si ⊆ Si+1.

Induction refresher

https://math.libretexts.org/Courses/Mount_Royal_University/MATH_1150%3A_Mathematical_Reasoning/3%3A_Number_Patterns/3.1%3A_Proof_by_Induction

https://www.youtube.com/watch?v=LJpouCMAAfE

