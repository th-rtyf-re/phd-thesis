My PhD thesis
=============

This repository contains my PhD thesis, ["Algebraic invariants for filtered
spaces and their computation"](https://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-380673).

My thesis uses my LuaLaTeX thesis class [`kthpq-thesis`](https://github.com/th-rtyf-re/kthpq-thesis),
with some modifications.

How it works
------------

This section is mostly a reminder for myself. I wrote these files in [VS Code](https://code.visualstudio.com/)
with the [LaTeX Workshop](https://github.com/james-yu/latex-workshop) extension.

### Structure

The main file is [`thesis-main.tex`](thesis-main.tex). The inputted files are
split into [`headers`](headers/) for the preamble, [`includes`](includes/) for
the main thesis content, and [`papers`](papers/) for the included papers.
Figures are found in [`figs`](figs/), bibliographic entries in [`bib`](bib/).

### Programs and scripts

Various programs and scripts were used to make this thesis; they are located in
[`util`](util/).

* [`flipbook.py`](util/flipbook.py) generates the flipbook in the _kappa_, with
  some extra functions to interact with the filtered simplicial complex. Before
  running this, be sure to create the directory `figs/flip/`.
* [`morse.py`](util/morse.py) generates the example of critical points of a
  height function on a torus (page 41).
* [`split.sh`](util/split.sh) splits the output PDF into parts that KTH's
  printing service, US-AB, likes. Before running this, be sure to create the
  directory `util/split/`.

Errata
------

The published version of this thesis is version 1.1 (May 3, 2026, commit
1d293f7). Since then, the following mistakes have been found:

* On page 233 (Paper D, Section D.1.4), the
  
  > description (D.1.2)
  
  should refer to the equation in Section D.1.2; this equation should have been
  numbered, and indeed is in the arXiv version of the paper (corrected in
  commit c467e6a).
* On page 245 (Paper D, proof of Proposition D.21), the
  
  > Equations (D.2.2) and (D.2.2)
  
  are referring to the two previous equations, which should have been numbered,
  and indeed are in the arXiv version of the paper (corrected in commit
  c467e6a).

Note that there is a small mistake on page 91, Section 4.4 of Paper A. This is
acknowledged and corrected on pages 48-49, in Chapter 4.

License
-------

The published version of this thesis is copyrighted by me, Isaac Ren. I'm not
really sure what the legal implications are for the repository, but you can
copy the "code" part of this repository, e.g., the various macros and hacks
used on top of `kthpq-thesis`. However, maybe avoid copying the content of the
thesis and the included papers :)