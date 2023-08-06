Usage
======

1. `dcli configure` - Configure dockyard CLI 
2. `dcli login` - Login to dockyard  
3. `dcli list` - List dockyard workspaces
4. `dcli activate` - Set active workspace. Subsequent commands use this workspace if no workspace name is specified.
5. `dcli ssh [workspace name] [command]` - SSH to dockyard workspace
6. `dcli scp <source> <target>` - Transfer files/directories to/from workspace.

    a) source/target could be a local path (including .)

    b) source/target could be a remote relative path inside workspace directory `<workspace_name>:<path>`

    c) source/target could be a remote full path inside workspace `<workspace_name>:/<path>` or `<workspace_name>:~/<path>`

7. `dcli code` - Start local VSCode and connect to dockyard workspace

8. `dcli vnc` -  VNC connection to dockyard workspace

9. `dcli start` - Start given workspace

10. `dcli stop` - Stop given workspace

11. `dcli hpc create` -    create parallel cluster

12. `dcli hpc delete` -    delete parallel cluster

13. `dcli hpc list` -      list aws parallel clusters

14. `dcli hpc save` -      backup the parallel cluster head node

15. `dcli hpc ssh` -       ssh/run a command inside parallel cluster head node

