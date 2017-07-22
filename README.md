gfmtask
========

[GFM task list][] under Sublime Text.


[GFM task list]: https://github.com/blog/1375-task-lists-in-gfm-issues-pulls-comments

Usage
------

### Shortcut

`<A-x>` a.k.a. `Alt+X`.

### Command palette

`gfmtask: Toggle Done`

### Example

- [ ] Press `<A-x>` to mark this task as done.
- [x] Press `<A-x>` to mark this task as todo (revert done).
    1. [ ] Also works on nested lists.
    2. Press `<A-x>` to transform a normal list item to a task.

Pressing `<A-x>` on a normal line will also transform it to a task.


Configuration
---------------

### Shortcut

I bind it to `<C-d>`.

```json
[
  { "keys": ["ctrl+d"], "command": "gfmtask_toggle_done" }
]
```

### Scopes

This plugin is enable for markdown files only.
There is no configuration option.
If you want to use it on other files,
set the file syntax to markdown temporarily.

License
---------

Code is under 0BSD.

Icons are copyrighted by [Google][], under [CC-BY][].

[Google]: https://design.google.com/icons/
[CC-BY]: https://creativecommons.org/licenses/by/4.0/
