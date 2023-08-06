# sopel-arxiv

A plugin for summarizing links to [arXiv.org](https://arxiv.org) in the IRC bot
[Sopel](https://sopel.chat/).

## Installation

```bash
$ pip install sopel-arxiv
```

## Usage

When this plugin is active, the bot will look for links to arXiv articles and
try to report their titles, authors, and summaries. Links directly to PDFs are
also supported.

```
<SnoopJ> https://arxiv.org/abs/0811.3772
<terribot> [arXiv] “What if Time Really Exists?” Sean M. Carroll — «Despite the
obvious utility of the concept, it has often been argued that time does not
exist. I take the opposite perspective: let's imagine that time does exist, and
the universe is described by a quantum state obeying ordinary time-dependent
quantum mechanics. Reconciling this simple picture with the known facts about
our universe turns out to be a non-trivial task, but by taking it…»
```
