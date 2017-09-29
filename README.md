# i3 workspace hinting
Based on [https://github.com/disconsis/dotfiles/tree/master/.config/i3](https://github.com/disconsis/dotfiles/tree/master/.config/i3)

Allows dynamic renaming and renumbering of i3 workspaces in the i3 window manager, as well as limited visualization of windows in a workspace
by adding unicode icons to the workspace title based on the apps it contains.

If you only want dynamic workspace renaming, you can do it without scripts,
see [this question](https://faq.i3wm.org/question/1774/rename-workspace-with-i3-input-using-numbers-and-text.1.html) in
the i3 faq. However, you'll have to re-type the workspace number each time to
avoid breaking your key bindings.

## Setup dynamic workspace renaming/numbering
 * Ensure you have
   * python3
   * pip for python 3, with which you can install [https://pypi.python.org/pypi/i3ipc](https://pypi.python.org/pypi/i3ipc)
     and [https://pypi.python.org/pypi/fasteners](https://pypi.python.org/pypi/fasteners)  

   On Debian-based distros,
   ```
   sudo apt-get install python3 python3-pip
   pip3 install i3ipc
   pip3 install fasteners
   ```
 * Clone this repository to `~/.i3/hinting`
 * Add to your `~.i3/config` the following:  
   ```
   bindsym $mod+n exec --no-startup-id i3-input -P 'Rename or renumber workspace: ' -F 'exec python3 ~/.i3/hinting/rename_ws.py rename "%s"'
   ```
   To preserve key bindings (switch to workspace, move container to workspace), ensure
   the key bindings are defined using the workspace *number* n notation, not
   workspace n notation.  
   __YES:__
   ```
   bindsym $mod+1 workspace number 1
   bindsym $mod+2 workspace number 2
   ```
   __NO:__
      ```
      bindsym $mod+1 workspace 1
      bindsym $mod+2 workspace 2
      ```
 * Restart i3
 
 
## Using dynamic renaming / renumbering
Strike the `mod+n` keys (usually Windows key + letter n). A floating prompt should
appear onscreen.

In the prompt, you may enter:
 * Just a number. This will reset the current workspace's number, leaving its name
   unchanged.
 * Just a name. This will rename the workspace (the text displayed after the colon),
   leaving its number unchanged.
 * A number, a colon, and a name. This will simultaneously renumber and
   rename the workspace.