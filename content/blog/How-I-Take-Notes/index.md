+++
title = "How I Take Notes"
date = 2022-02-11
+++

As an SRE, I work with a number of protocols, systems, and languages, but also
get interrupted quite frequently to fix things, answer questions, fulfull
requests, etc. This is fine, in fact generally I really enjoy helping people,
but it does make me lose context frequently. In addition, I don't have the
greatest memory. Sometimes even when I am concentrating on one thing, some
odd idea  will pop into my head that I MUST consider more. For example, the
other day I was working on something and suddenly started to wonder if I could
store my browser's bookmarks (of which I have a few thousand) into LDAP and
query them easily...

Anyway, when I started my current job and moved to California in 2018, I
figured I better get some good notes so I didn't have to ask people things
twice. Since then, I've grown to rely heavily on these notes, and I've gotten
some benefits I didn't expect as well. During an oncall incident, I find I'm
able to keep "the big picture" in my head more easily by writing my findings in
my notes - I can record my current questions as I look at the evidence, forget
about them and come back to them later if my most promising suspicion doesn't
yeild results. During normal work, when I get a random wacky idea I don't have
time to play with, I write it down and (most of the time) my brain lets me
return to the task at hand. I also make my notes available to my colleagues for
their searching too, which has helped a few of them out over the years.

For these notes to be as effective as they are for me, I have the following needs:

## Requirements

- I need to own my personal notes and LinkedIn needs to own my work notes. No
  "just keep your data in our cloud" services.
- export to plain text - especially needed for migration from one app to another
- easy sync between my Mac and my Android
- easy editing on my Mac and Android phone
- searchable
- quick startup time, especially on Mac
- paste to save image support.
- image export
- inline image support in the editor

In particular, inline image support within editors that also support plain text
export is hard to find, but super helpful for several of my use cases. Fairly
often, I need to save screenshots of different graphs and infer what to do or
ask next from how they look. Inline images can also be nice for embedding
diagrams or app screenshots. So many markdown apps don't support this, with
some using a preview pane instead. A preview pane takes too much space when I
need the majority of my monitors' real estate to frantically click through code
bases, portals, graphs, wikis, Google searches, emails, and instant messages.

## Nice-to-haves

- simple
- browsable (i.e., find stuff easily on a rainy day)
- open source writing apps
- usable with Vim for quick edits
- easy to learn markup language
- viewable online

## My System

The system I've landed on is:

- Format: plain markdown files in a folder. I'm used to writing markdown for GitHub READMEs and my blog anyway and it's easy to read and write in a simple text editor.
- Sync: Git and GitHub to sync between Mac and Android. GitHub also provides a web interface to read my notes.
- Editor: Vim or [Typora](https://typora.io/) on Mac. Pasting an image into Typora automatically saves the image as a file, types an image markdown link, and shows the inline image below the link.
- Android: [GitJournal](https://gitjournal.io/) on my phone. I really love this app because it slots so nicely with the rest of my system, works quite well, allows note searching, is [open source](https://gitjournal.io/), and has a very nice maintainer.
- Mac Search: [ripgrep](https://github.com/BurntSushi/ripgrep) to search my notes on my Mac. It auto-colors results and is super fast.

I use the following Bash function to add some options to ripgrep:

```bash
# recursively search markdown files
rgmd() { rg --type md --ignore-case "$@" }
```

As for note organization, I have a gigantic `notes.md` file for notes that don't belong to any category. When something grows enough, I add it to `<category>.md`. I don't generally think to hard about this because it's so easy to search or change later if I don't like how it looks.

I've used this system for the past couple of years at this point, trying new alternatives occasionally (I found Typora less than a year ago). The only feature I wish I had was better browsing capability, maybe with tags or something.

## Things to Try

- It might be fun to convert my notes into a static site similar to this blog. [Zola](https://www.getzola.org/) offers [search](https://www.getzola.org/documentation/content/search/), which might be fun to play with.
- [Roam](https://roamresearch.com/), [Obsidian](https://obsidian.md/), or [Foam](https://github.com/foambubble/foam), maybe combined with [Readwise](https://readwise.io/) to slurp bookmarked tweets or something. (these aren't open source, but the data is still plaintext). Critically, I don't think any of these tools offer inline image support, which is a dealbreaker for me.
