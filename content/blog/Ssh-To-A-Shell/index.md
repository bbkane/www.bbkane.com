+++
title = "SSH to a Shell"
date = 2024-12-20
+++

I have a project on a VM I always need to start the same way:

```bash
ssh myvm
zsh  # start zsh manually because I don't wnat to change the startup shell
cd ~/path/to/project
```

Today I figured out how to replace that with:
```
ssh_my_project
```

Background information: `zsh` is installed via Homebrew.

First step: make `zsh` load homebrew by putting the following in the VM's  `~/.zshrc`:

```zsh
# Add Homebrew to PATH if it doesn't exist
if ! command -v brew &> /dev/null; then
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
fi
```

At this point I can SSH in:

```bash
# -t : allocate a ptty : https://serverfault.com/a/977106
ssh myvm -t '/home/linuxbrew/.linuxbrew/bin/zsh'
```

However, I still want to change the directory with `zsh` exiting. Fortunately, someone else [has a solution](https://superuser.com/a/230090): put the following at the end of the VM's `~/.zshrc`:

```zsh
if [[ $1 == eval ]]
then
    "$@"
set --
fi
```

I can now make the alias:

```zsh
ssh_to_project() {
    ssh myvm -t '/home/linuxbrew/.linuxbrew/bin/zsh -is eval "cd ~/path/to/project"'
}
```

Which does exactly what I want.
