+++
title = "Learn Git"
date = 2018-03-26
updated = 2019-01-26
aliases = [ "2018/03/26/Learn-Git.html" ]
+++

# Tutorials

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

# Random Notes

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

## Merge a repo into a subdirectory into another repo

This is from [StackOverflow](https://stackoverflow.com/a/76831513/2958070). I was able to
follow the steps exactly, except for needing to use absolute paths instead of
relative ones.

Fix up repo1:

```bash
cd path/to/repo1
mkdir repo1
# move all non-hidden files and folders into `repo1/`
mv * repo1/
# move all hidden files and folders into `repo1/`
mv .* repo1/
# Now move the .git dir back to where it belongs, since it was moved by the
# command just above
mv repo1/.git .
# commit all these changes into this repo
git add -A
git status
git commit -m "Move all files & folders into a subdir"
```

```bash
cd path/to/new_repo

# --------------------------------------------------------------------------
# 1. Merge repo1, with all files and folders and git history, into new_repo
# --------------------------------------------------------------------------

# Add repo1 as a local "remote" named `repo1`
# - Note: this assumes that new_repo, repo1, and repo2 are all at the same
#   directory level and inside the same parent folder. If this is *not* the
#   case, no problem. Simply change `"../repo1"` below to the proper
#   relative *or* absolute path to that repo! Ex: `"path/to/repo1"`.
git remote add repo1 "../repo1"
# View all of your remotes.
# - You'll now see `repo1` as a remote which points to the local "URL"
#   of "../repo1"
git remote -v

# Fetch all of repo1's files and history into new_repo's .git dir.
# - Note that `repo1` here is the name of the remote alias that you just
#   added above.
git fetch repo1
# View the new locally-stored, remote-tracking hidden branch that was just
# created for you.
# - `git branch -r` will now show a new hidden branch named `repo1/main` or
#   `repo1/master` or whatever your main branch was named there.
git branch -r

# Assuming that your new hidden branch that you just fetched is called
# `repo1/main`, let's merge that into our currently-checked-out branch now.
# - This merges repo1's files and folders and git history into new_repo.
# - change `repo1/main` to `repo1/some_other_branch` if you want to merge in
#   `some_other_branch` instead.
# - Immediately after running this command, you will now see a new folder,
#   `repo1`, with all of its files and folders within it, created inside
#   the `new_repo` directory.
git merge --allow-unrelated-histories repo1/main
# Since you have independent sub-folders prepared inside repo1 and repo2,
# there will be no conflicts whatsoever. When the git merge editor opens
# up, just save and close it to complete the merge. Optionally, add any
# comments you wish before saving and closing it.

# Now, remove the remote named "repo1", since we no longer need it.
git remote remove repo1
# View all remotes to ensure it is now gone
git remote -v

# See the new commit status. If `repo1` had 100 commits in it, for instance,
# `git status` will now show this, since `new_repo` now has those 100
# commits plus this new merge commit in it:
#
#       $ git status
#       On branch main
#       Your branch is ahead of 'origin/main' by 101 commits.
#         (use "git push" to publish your local commits)
#
#       nothing to commit, working tree clean
#
git status
# Push to a remote, if you have one configured
git push
```

## Apply a patch from one commit onto another

This is useful when you're working on a branch, then the branch gets squashed on top of master but you push further commits onto the branch...

```bash
git diff <commit-range> > ~/tmp.patch
git checkout master
git apply ~/tmp.patch
```

## Move a git tag

Copied from [StackOverflow](https://stackoverflow.com/questions/8044583/how-can-i-move-a-tag-on-a-git-branch-to-a-different-commit)

Remove locally:

```bash
git tag -d v0.1  
```

Remove on remote:

```bash
git push origin --delete v0.1
```

Then re-add locally and push v0.1 to the most recent commit:

```bash
git tag -a v0.1
git push origin --tags
```

## Remove parts of a repo!

I'm splitting the tech bits of my `journal` repo into a `techjournal` repo.

First, search for non-tech things (like notes about food). From [StackOverflow](https://stackoverflow.com/a/2928721):

```bash
git log -p --all -S food -- projects | vim -
```

This search is case-sensitive, so I ran it with `Food` too, and it lets me double-check that the tech notes don't have food content.

Next install `git-filter-repo` to filter out the folders I don't specify:

```bash
brew install git-filter-repo
```

Do a fresh clone of my `journal` repo and use that as this is a destructive operation.

Then, modify their [example](https://github.com/newren/git-filter-repo?tab=readme-ov-file#simple-example-with-comparisons) to save only the tech notes:

```bash
git filter-repo --path projects/ --path tech.md --path showdowns/ --path old/tech/ --path tech.assets
```

And... that's it. This saves the history of those paths. Unfortunately, this doesn't preserve history beyond file moves (so If I, in the past, move notes into `old`, the previous commit information of those files is lost after the move.) I'd like to preserve more history than that, but I'm not sure it's possible and I feel like I could sync hours I'd rather spend on something else trying to.

