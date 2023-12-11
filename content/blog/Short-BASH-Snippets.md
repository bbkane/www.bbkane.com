+++
title = "Short BASH Snippets"
date = 2018-09-09
updated = 2021-01-20
aliases = [ "2018/09/09/Short-BASH-Snippets.html" ]
+++

## BASH script starter

I put this at the top of all my scripts because most of the time I want scripts to fail on errors, and half the time I want the script to run in the directory it's in.

```bash
#!/bin/bash

# exit the script on command errors or unset variables
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

# https://stackoverflow.com/a/246128/295807
# readonly script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# cd "${script_dir}"
```

## Get the full path to a file

This is perl wrapped in Bash, but it's cross-platform and works on Mac and Linux. The alternative, `readlink -f` doesn't work on Mac.

```bash
fullpath() {
    local -r full=$(perl -e 'use Cwd "abs_path";print abs_path(shift)' "$1")
    echo "$full"
}
```

## Print a BASH command

This snippet prints the command before running it. Stolen from [StackOverflow](https://stackoverflow.com/a/19226038). Great for debugging!

```bash
set -x
command
{ set +x; } 2>/dev/null
```


## Generate and use colored print commands

Running scripts with colored output can make them much friendlier. Consider taking out the newlines if you want nested color prints. I almost never do, so I'm leaving them in...

### Define the function factory

```bash
make_print_color() {
    color_name="$1"
    color_code="$2"
    color_reset="$(tput sgr0)"
    if [ -t 1 ] ; then
        eval "print_${color_name}() { printf \"${color_code}%s${color_reset}\\n\" \"\$1\"; }"
    else  # Don't print colors on pipes
        eval "print_${color_name}() { printf \"%s\\n\" \"\$1\"; }"
    fi
}
```

### Generate pretty print functions and use them

```bash
# https://unix.stackexchange.com/a/269085/185953
make_print_color "red" "$(tput setaf 1)"
make_print_color "green" "$(tput setaf 2)"
make_print_color "yellow" "$(tput setaf 3)"
make_print_color "blue" "$(tput setaf 4)"

print_red "Always"
print_green "Seeing"
print_yellow "in"
print_blue "Color!"

# print to stderr: https://stackoverflow.com/a/2990533/2958070
print_red "Error!" >&2
```

## Simple but effective backup command.

```bash
bak() {
    date_string="$(date +'%Y-%m-%d.%H.%M.%S')"
    if [[ -d "$1" ]]; then
        local -r no_slash="${1%/}"
        cp -r "${no_slash}" "${no_slash}.${date_string}.bak"
    elif [[ -f "$1" ]]; then
        cp "$1" "${1}.${date_string}.bak"
    else
        echo "Only files and directories supported"
    fi
}
```

## Run a shell command on file change

I like to use [`entr`](http://www.entrproject.org/) for this. Generate some filenames and pipe them to `entr`. The `-c` option clears the screen and the `-s` option means use the shell.

```bash
ls log.txt | entr -c -s 'date && tail log.txt'
```

## Run a Server and open a browser with the link

I use a snippet similar to this when I want to open a browser after I run a
blocking command (usually starting a server). I use this particular example to
learn Elm. I have something similar to run Jekyll for my blog.

```bash
learn_elm() {
    cd ~/Code/Elm || echo "Non-existant dir"
    code .
    if [[ "$(uname)" == "Darwin" ]]; then
        open_command=open
    elif [[ "$(uname)" == "Linux" ]]; then
        open_command=xdg-open
    fi
    # Open a subshell in a fork
    (sleep 2 && "${open_command}" "http://127.0.0.1:8000") &
    # Run the blocking command
    elm reactor
}
```

## Simple Task Runner

For when you want to run some long commands with a shortcut. It does very limited arg parsing.

```bash
print_help(){
    cat << EOF
Workflow:
    $0 first|1
    $0 second|2
EOF
}

first() {
    echo "I'm first"
}

second() {
    echo "I'm second!"
}

set +u
if [ -z ${1+x} ]; then
    print_help
fi
set -u

case "$1" in
    first|1)
        first
    ;;
    second|2)
        second
    ;;
    *)
        echo "Unmatched command: $1"
        print_help
    ;;
esac
```

## Tee `stderr` and `stdout`to files

Save both `stderr` and `stdout` to a file. Only works in Bash. From StackOverflow

```bash
# https://stackoverflow.com/a/59435204
{ { time ./tmp_import.sh | tee tmp_import_log.stdout;} 3>&1 1>&2 2>&3- | tee tmp_import_log.stderr;} 3>&1 1>&2 2>&3-
```

## Process each line on a file

From [Unix StackExchange](https://unix.stackexchange.com/a/580545/185953). I like to combine it with printing the command used.

```bash
while IFS='' read -r line || [ -n "${line}" ]; do
    set -x
    echo "$line"
    { set +x; } 2>/dev/null
done < ./file.txt
```

You can also pipe lines to the while loop:

```bash
pbpaste | while IFS='' read -r line || [ -n "${line}" ]; do
    echo "line: $line"
done
```

## Iterating inline arrays in `Zsh`

Not a Bash snippet, but useful nonetheless :) . From [SuperUser](https://superuser.com/a/877181/643441)

```bash
for d (www.linkedin.com www.reddit.com www.google.com) {
    dig +short +noshort "$d"
}
```

## Diff everything in a directory!

Consider doing a git clean before this:

```bash
git clean -xd --dry-run
git clean -xd --force
```

```bash
diff -qr -x '.git' folder1/ folder2/
```

## Cross-platform colored diff

A colleague got this from somewhere on StackOverflow:

```bash
function vdiff() {
    # colored diff
    diff $@ | sed 's/^-\([^-]*\)/\x1b[31;1m-\1/;s/^+\([^+]*\)/\x1b[32;1m+\1/;s/^@/\x1b[36;1m@/;s/$/\x1b[0m/'
}
```

## Customize `dig`

Unfortunately, there's no way to use multiple name servers

```bash
dig +noall +answer +question +identify @dns2.p09.nsone.net. -q linkedin.com -t ns -q linkedin.com -t a
```

## Search and replace across files

Most people use `sed` for this, but `sed` differs between MacOS and Linux. Taken from [StackOverflow](https://stackoverflow.com/a/27985566/2958070):

```bash
perl -pi -w -e 's/search/replace/g;' *.php
```

- -e means execute the following line of code.
- -i means edit in-place
- -w write warnings
- -p loop through lins and print

See [Perl 101 - Command-line Switches](https://perl101.org/command-line-switches.html) for other useful Perl switches.

This can be combined with `find` to run recursively:

```bash
find . -name '*.py' -print0 | xargs -0 perl -pi -w -e 's/"2022-04-01"/"2022-04-01-preview"/g;'
```

It's also possible to [ignore files](https://stackoverflow.com/a/29744243/2958070) (NOTE: this works on MacOS)

```bash
find . -type f -not -path '*/\.git\/*' -not -path '\./rename.sh' -print0 \
    | xargs -0 perl -pi -w -e 's/example-python-cli/new-project-name/g;'
```

## Clean unwanted Homebrew formulas

Show dependency graph (optional)

```bash
brew deps --installed --graph
```

Show formulas that nothing depends on (and how many dependencies they have) - https://stackoverflow.com/a/55445034/2958070

```bash
brew leaves | xargs brew deps --formula --for-each | sed "s/^.*:/$(tput setaf 4)&$(tput sgr0)/"
```

Then uninstall something:

```bash
brew uninstall [thing]
```

brew will refuse to uninstall the formula if another formula depends on it.

Run https://docs.brew.sh/Manpage#autoremove---dry-run to uninstall dependencies that are no longer needed.

```bash
brew autoremove
```

## List images in the terminal

Expecially useful for getting the right images in blog Markdown image links. `imgcat` comes from [these iTerm2 docs](https://iterm2.com/documentation-images.html).

```bash
imgcat -H 400px -r -p index.assets/*
```

