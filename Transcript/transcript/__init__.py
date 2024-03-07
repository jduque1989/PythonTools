
--boundary_.oOo._tf4xzTocS1VgmT8NcNhw2J2gn6v4o7k5
Content-Length: 1475
Content-Type: application/octet-stream
X-File-MD5: ffeffa59c90c9c4a033c7574f8f3fb75
X-File-Mtime: 1709697548
X-File-Path: /DiamondsBucket/CODING/Python-tools/Transcript/.venv/lib/python3.11/site-packages/MarkupSafe-2.1.5.dist-info/LICENSE.rst

Copyright 2010 Pallets

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1.  Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

2.  Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

3.  Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

--boundary_.oOo._tf4xzTocS1VgmT8NcNhw2J2gn6v4o7k5
Content-Length: 6659
Content-Type: application/octet-stream
X-File-MD5: 367bfbef5f4e8d80a49db5df5788c3b4
X-File-Mtime: 1709697545
X-File-Path: /DiamondsBucket/CODING/Python-tools/Transcript/.venv/share/man/man1/isympy.1

'\" -*- coding: us-ascii -*-
.if \n(.g .ds T< \\FC
.if \n(.g .ds T> \\F[\n[.fam]]
.de URL
\\$2 \(la\\$1\(ra\\$3
..
.if \n(.g .mso www.tmac
.TH isympy 1 2007-10-8 "" ""
.SH NAME
isympy \- interactive shell for SymPy
.SH SYNOPSIS
'nh
.fi
.ad l
\fBisympy\fR \kx
.if (\nx>(\n(.l/2)) .nr x (\n(.l/5)
'in \n(.iu+\nxu
[\fB-c\fR | \fB--console\fR] [\fB-p\fR ENCODING | \fB--pretty\fR ENCODING] [\fB-t\fR TYPE | \fB--types\fR TYPE] [\fB-o\fR ORDER | \fB--order\fR ORDER] [\fB-q\fR | \fB--quiet\fR] [\fB-d\fR | \fB--doctest\fR] [\fB-C\fR | \fB--no-cache\fR] [\fB-a\fR | \fB--auto\fR] [\fB-D\fR | \fB--debug\fR] [
-- | PYTHONOPTIONS]
'in \n(.iu-\nxu
.ad b
'hy
'nh
.fi
.ad l
\fBisympy\fR \kx
.if (\nx>(\n(.l/2)) .nr x (\n(.l/5)
'in \n(.iu+\nxu
[
{\fB-h\fR | \fB--help\fR}
|
{\fB-v\fR | \fB--version\fR}
]
'in \n(.iu-\nxu
.ad b
'hy
.SH DESCRIPTION
isympy is a Python shell for SymPy. It is just a normal python shell
(ipython shell if you have the ipython package installed) that executes
the following commands so that you don't have to:
.PP
.nf
\*(T<
>>> from __future__ import division
>>> from sympy import *
>>> x, y, z = symbols("x,y,z")
>>> k, m, n = symbols("k,m,n", integer=True)
    \*(T>
.fi
.PP
So starting isympy is equivalent to starting python (or ipython) and
executing the above commands by hand. It is intended for easy and quick
experimentation with SymPy. For more complicated programs, it is recommended
to write a script and import things explicitly (using the "from sympy
import sin, log, Symbol, ..." idiom).
.SH OPTIONS
.TP
\*(T<\fB\-c \fR\*(T>\fISHELL\fR, \*(T<\fB\-\-console=\fR\*(T>\fISHELL\fR
Use the specified shell (python or ipython) as
console backend instead of the default one (ipython
if present or python otherwise).

Example: isympy -c python

\fISHELL\fR could be either
\&'ipython' or 'python'
.TP
\*(T<\fB\-p \fR\*(T>\fIENCODING\fR, \*(T<\fB\-\-pretty=\fR\*(T>\fIENCODING\fR
Setup pretty printing in SymPy. By default, the most pretty, unicode
printing is enabled (if the terminal supports it). You can use less
pretty ASCII printing instead or no pretty printing at all.

Example: isympy -p no

\fIENCODING\fR must be one of 'unicode',
\&'ascii' or 'no'.
.TP
\*(T<\fB\-t \fR\*(T>\fITYPE\fR, \*(T<\fB\-\-types=\fR\*(T>\fITYPE\fR
Setup the ground types for the polys. By default, gmpy ground types
are used if gmpy2 or gmpy is installed, otherwise it falls back to python
ground types, which are a little bit slower. You can manually
choose python ground types even if gmpy is installed (e.g., for testing purposes).

Note that sympy ground types are not supported, and should be used
only for experimental purposes.

Note that the gmpy1 ground type is primarily intended for testing; it the
use of gmpy even if gmpy2 is available.

This is the same as setting the environment variable
SYMPY_GROUND_TYPES to the given ground type (e.g.,
SYMPY_GROUND_TYPES='gmpy')

The ground types can be determined interactively from the variable
sympy.polys.domains.GROUND_TYPES inside the isympy shell itself.

Example: isympy -t python

\fITYPE\fR must be one of 'gmpy',
\&'gmpy1' or 'python'.
.TP
\*(T<\fB\-o \fR\*(T>\fIORDER\fR, \*(T<\fB\-\-order=\fR\*(T>\fIORDER\fR
Setup the ordering of terms for printing. The default is lex, which
orders terms lexicographically (e.g., x**2 + x + 1). You can choose
other orderings, such as rev-lex, which will use reverse
lexicographic ordering (e.g., 1 + x + x**2).

Note that for very large expressions, ORDER='none' may speed up
printing considerably, with the tradeoff that the order of the terms
in the printed expression will have no canonical order

Example: isympy -o rev-lax

\fIORDER\fR must be one of 'lex', 'rev-lex', 'grlex',
\&'rev-grlex', 'grevlex', 'rev-grevlex', 'old', or 'none'.
.TP
\*(T<\fB\-q\fR\*(T>, \*(T<\fB\-\-quiet\fR\*(T>
Print only Python's and SymPy's versions to stdout at startup, and nothing else.
.TP
\*(T<\fB\-d\fR\*(T>, \*(T<\fB\-\-doctest\fR\*(T>
Use the same format that should be used for doctests. This is
equivalent to '\fIisympy -c python -p no\fR'.
.TP
\*(T<\fB\-C\fR\*(T>, \*(T<\fB\-\-no\-cache\fR\*(T>
Disable the caching mechanism. Disabling the cache may slow certain
operations down considerably. This is useful for testing the cache,
or for benchmarking, as the cache can result in deceptive benchmark timings.

This is the same as setting the environment variable SYMPY_USE_CACHE
to 'no'.
.TP
\*(T<\fB\-a\fR\*(T>, \*(T<\fB\-\-auto\fR\*(T>
Automatically create missing symbols. Normally, typing a name of a
Symbol that has not been instantiated first would raise NameError,
but with this option enabled, any undefined name will be
automatically created as a Symbol. This only works in IPython 0.11.

Note that this is intended only for interactive, calculator style
usage. In a script that uses SymPy, Symbols should be instantiated
at the top, so that it's clear what they are.

This will not override any names that are already defined, which
includes the single character letters represented by the mnemonic
QCOSINE (see the "Gotchas and Pitfalls" document in the
documentation). You can delete existing names by executing "del
name" in the shell itself. You can see if a name is defined by typing
"'name' in globals()".

The Symbols that are created using this have default assumptions.
If you want to place assumptions on symbols, you should create them
using symbols() or var().

Finally, this only works in the top level namespace. So, for
example, if you define a function in isympy with an undefined
Symbol, it will not work.
.TP
\*(T<\fB\-D\fR\*(T>, \*(T<\fB\-\-debug\fR\*(T>
Enable debugging output. This is the same as setting the
environment variable SYMPY_DEBUG to 'True'. The debug status is set
in the variable SYMPY_DEBUG within isympy.
.TP
-- \fIPYTHONOPTIONS\fR
These options will be passed on to \fIipython (1)\fR shell.
Only supported when ipython is being used (standard python shell not supported).

Two dashes (--) are required to separate \fIPYTHONOPTIONS\fR
from the other isympy options.

For example, to run iSymPy without startup banner and colors:

isympy -q -c ipython -- --color