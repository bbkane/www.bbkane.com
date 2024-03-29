+++
title = "Setting Up PowerShell Updated"
date = 2016-07-14
updated = 2016-12-25
aliases = [ "2016/07/14/Setting-Up-PowerShell-Updated.html" ]
+++

I've streamlined and improved my method of installing PowerShell:

First, run the `cmd` script as Administrator to install [chocolatey](https://chocolatey.org/)
and PowerShell version 4, and allow powershell scripts to be run.
The current version of the script lives at
[my backup repo](https://github.com/bbkane/backup/blob/master/windows/install_choco.cmd)

```cmd
@echo off
goto check_Permissions

:check_Permissions
    echo Administrative permissions required. Detecting permissions...

    net session >nul 2>&1
    if %errorLevel% == 0 (
        echo Success: Administrative permissions confirmed.
	goto install
    ) else (
        echo Failure: Current permissions inadequate.
	pause
	exit
    )


:install

@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin

choco install powershell4

@powershell Set-ExecutionPolicy RemoteSigned

PAUSE
```

Then reboot.

When you're back, make a profile if there isn't one:

```powershell
New-Item -Path $PROFILE -ItemType file
```

Open it:

```powershell
notepad $PROFILE
```


Copy the following things into it (these are from [my profile](https://github.com/bbkane/backup/blob/master/windows/Microsoft.PowerShell_profile.ps1):

```powershell
function Install-PowerShellGoodies()
{

    (new-object Net.WebClient).DownloadString("http://psget.net/GetPsGet.ps1") | iex

    Install-Module PSReadline
    # Don't forget to install git to make this work
    Install-Module posh-git
}
```

Re-source your profile and run it:

```powershell
. $PROFILE
Install-PowerShellGoodies
```

Finally, get a better console. I really like [ConEmu](https://conemu.github.io/)

```powershell
# As admin:
choco install conemu
```
