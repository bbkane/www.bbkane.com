+++
title = "Learn Git"
date = 2018-03-26
updated = 2019-01-26
aliases = [ "2018/03/26/Learn-Git.html" ]
+++

Git is a famously powerful and [famously confusing](https://xkcd.com/1597/) version control system
used by software engineers everywhere. Increasingly, as other types of work
begin to look more like software engineering (in my case network and systems
engineering), git becomes useful for those folks as well. In that regard, here
are some resources to learn git. I recommend you start at the top, get enough to
work with, play with git by yourself, and return for the more advanced stuff
when the basics don't cover your needs anymore.

- Atlassian covers some good ways to [install Git](https://www.atlassian.com/git/tutorials/install-git). I recommend the Homebrew method if you're on a Mac and use [Homebrew](https://brew.sh/). It'll make it easy to install and update Git as well as other software.
- [Git Essentials
  LiveLessons](https://www.safaribooksonline.com/library/view/git-essentials-livelessons/9780134655284/)
  is a Safari Books Online video course for teaching the very beginnings of
  git. It's not a free resource, but it's a good one.
- The [Git Tutorial](https://git-scm.com/docs/gittutorial) is a short text
  introduction to using git.
- GitHub makes an [interactive tutorial](https://try.github.io/levels/1/challenges/1).
- [js.org](https://learngitbranching.js.org/) has a very nice interactive tutorial on Git branches.

Once you have a decent workflow with git, you need to learn some of the theory
behind it and the more in-depth commands it offers:

- The [Git User Manual](https://git-scm.com/docs/user-manual.html) is a
  relatively short introduction to some of git's features
- [Pro Git](https://git-scm.com/book/en/v2) is a free online book for learning
  git that goes from beginner level to expert level. Very useful for learning
  the commands.
- [“Getting Git” by Scott Chacon](https://vimeo.com/14629850) is a great video
  explaining how git tracks content internally. A lot of git suddenly makes much
  more sense once you see it from the inside out.
- [Git For Ages 4 And Up](https://www.youtube.com/watch?v=1ffBJ4sVUb4) is
  another really good video explaining git internals (though it's not perfect:
  questions interrupt the presenter, and it's cut short). As a bonus, I think
  everyone was required to dress like a hipster for it.

Git is such a flexible tool that there are multiple workflows possible for it.
Different teams will choose different workflows, but here are some of the more
popular ones:

- Atlassian makes a git tutorial centered around their product BitBucket - a
  pretty good git hosting center. It includes a [comparison of
  workflows](https://www.atlassian.com/git/tutorials/comparing-workflows).
- GitHub also highlights a workflow method [in one of their
  guides](https://guides.github.com/introduction/flow/).

# Git Notes

## Forking and Syncing with GitHub

Sometimes I need to make a change to a public repo I own (like my dotfiles)
from my work laptop. I can't simply clone the repo and make the change because
my work laptop doesn't have access to my personal logins so I don't have
permissions to push (by design, not necessity). So, here's how to do a PR workflow

- Work PC: In GitHub, fork the repo to my work GitHub account
- Work PC: In the terminal, clone the repo
- Work PC: In the terminal, make the change, commit, and push
- Work PC: In GitHub, make a PR to the personal repo
- Home PC: In GitHub, merge the PR
- Work PC: In GitHub, sync the fork (button at the top)
- Work PC: In the terminal: `git pull` to pull the merge commit

Many of these steps use GitHub's web UI. There's [other ways](https://stackoverflow.com/questions/39819441/keeping-a-fork-up-to-date) to do parts of this with Git directly, but they're not as convenient for me.

## Moving commits to a new branch

I try to work on new features in a branch, but sometimes I just work on master and need to move to different branches. Luckily, [Stackoverflow](https://stackoverflow.com/a/22654961/2958070) has me covered:

```bash
git checkout -b newbranch # switch to a new branch
git branch -f master HEAD~3 # make master point to some older commit
```

## Delete a local remote-tracking branch

From [StackOverflow](https://stackoverflow.com/a/23961231/2958070):

```bash
$ git branch -a
  helpcolumns
* master
  remotes/origin/bbkane/issue46
  remotes/origin/helpcolumns
  remotes/origin/master
  remotes/origin/searchFuncPtr

$ git fetch origin --prune
From https://github.com/bbkane/warg
 - [deleted]         (none)     -> origin/bbkane/issue46
 - [deleted]         (none)     -> origin/searchFuncPtr
```

## Git blame with Log Ranges

From [Git Tips 1: Oldies but Goodies](https://blog.gitbutler.com/git-tips-1-theres-a-git-config-for-that/#git-blame-and-log-with-line-ranges)

```bash
git blame -L 28,43 path/to/file
```

or

```bash
git log -L28,43:gitbutler-ui/src/lib/vbranches/types.ts
```

See the post for more options, like looking for code that moved.

