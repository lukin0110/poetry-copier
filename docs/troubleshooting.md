# Troubleshooting

## `Permission denied (publickey)` in the DevContainer on macOS

1. Add all private keys to the ssh-agent: `ssh-add -A`
2. Reboot Docker Desktop
3. Reopen VSCode

`SSH Keys` should be shared now with the `DevContainer` 😎

### Other useful commands

1. Restart the ssh-agent: `eval "$(ssh-agent -s)"`
2. View ssh keys: `ssh-add -l`

### Problem description
On macOS, `SSH Keys` are not always automatically shared between the host and the `DevContainer`. They are lazily added to 
the *SSH Agent*. When they're not added to the *SSH Agent*, you'll get the following error when trying to execute 
`git pull`, `git push` or `git clone` commands in the `DevContainer`:
```bash
Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

Related issue on `vscode-remote-release`: [Automatically add SSH keys to ssh-agent](https://github.com/microsoft/vscode-remote-release/issues/4024)
