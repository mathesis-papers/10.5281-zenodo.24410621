# Exact least prime factors and exceptional classes for Wu's conjectures on $(2^{2^n}+1)2^{2^{2^n}}-1$

For `G_m = (2^(2^m)+1) 2^(2^(2^m)) - 1`, the note proves the least-prime-factor
values on Wu's four progressions, including the exceptional classes of the third
and fourth, extending Schott's and Wu's earlier bounds. Its primary source is the July 10, 2026 FORMULA block in
[OEIS A227244](https://oeis.org/A227244), revision 54 (July 12, 2026).

## Build

Use Tectonic 0.17.0 from the extracted directory:

```sh
tectonic --untrusted note.tex
```

Alternatively, use a standard LaTeX installation with the packages named at the
top of `note.tex`:

```sh
pdflatex -no-shell-escape note.tex
pdflatex -no-shell-escape note.tex
```

The bibliography is embedded in `note.tex`; no BibTeX input is required.
`residue-table.tex` is the only TeX input. `metadata.json` gives authors,
license, problem identifiers and the pinned Lean source link.

## Check the modular proof

Python 3, with its standard library alone, suffices:

```sh
python3 verify.py > actual-output.json
diff -u checker-output.json actual-output.json
```

The expected status is `pass`. For the four progressions, the program checks the complete prime lists,
445 periodicity premises, 347 residue classes, their 347 one-period shifts,
55 progression intersections and 34 direct integer comparisons. The reduction
lemma in the note proves that the finite zero sets determine the values at all
indices; the computations alone are not an all-index extrapolation.
The `siblings` object gives the small-prime residue tables, the first five Fermat
primes, the factorization `F_5 = 641 * 6700417`, 55 Fermat congruences and six
totient equalities. Their general consequences are written proofs in the note.

## Scope

The pinned `.result` declarations linked in the note give primeness, divisibility
and minimality for Conjectures 1 and 2, Conjecture 3 under two noncoverage
hypotheses, and Conjecture 4 outside its excluded class. The extra values on the
excluded classes follow from the written proof and modular tables.
The note also reproves the earlier lower bound and `a(4n+5)=11`, characterizes
all indices with value 11, and determines the residues modulo earlier Fermat numbers.
For the cross-reference A000215 it credits Sela Fried's 2025 proofs of Layman's
formula and the Fermat-number implication of Hasler's conjecture, and his
counterexample to Cloitre's assertion. It strengthens the last result to
`phi(F_j-2) = (F_j-1)/2` if and only if `j <= 5`.
These corollaries are written proofs, distinct from the four linked Lean declarations.
The source archive contains this note, its inputs and the finite checker.

The public scientific sources are OEIS A227244, OEIS A000215 (revision 344),
and Sela Fried, *On several conjectures stated in A000215* (2025),
https://oeis.org/A000215/a000215_1.pdf. Exact locators and source coverage are in
the note. The bibliography is deliberately focused on these directly used sources.

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0: https://creativecommons.org/licenses/by/4.0/.
