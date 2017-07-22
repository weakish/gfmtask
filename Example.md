1. [x] Supports both `x` and `X`.

    GitHub's [blog post][1375] mentions `x`.

    In fact, GFM supports both `x` and `X`.

    [1375]: https://github.com/blog/1375-task-lists-in-gfm-issues-pulls-comments

2. [x] Support all lists

    https://daringfireball.net/projects/markdown/syntax#list

    Markdown list marks: `\+`, `-`, `\*` and `[[:digit:]]\.`.

    GFM support all of these list marks.

    - [X] test
    * [X] test
    + [X] test

    1. [X] numbered list
    324. [X] three digital

3. [x] Only match list items.

    This - [ ] will not trigger completion?


4. [x] Create a new todo for current line

    Turning current line to a todo item.

    - [x] if current line is already a list item.

    - [x] if current line is a normal line.

5. [x] Create a new todo under cursor.

    The above item `Create a new todo for current line` already handles
    indention correctly.
    Thus this is only useful on an empty line.
    Which is already be handled by MarkdownEditing plugin
    when the empty line is just below a one line list item.
    Otherwise it is trivial to write a normal line,
    and use above function to convert.
    No need for an extra command.

6. [x] Create a new todo below current line

    In a task list, with MarkDownEditing,
    hitting `Enter` will automatically prefix `- [ ]`.
    No need for an extra command.

7. [x] Create a new todo above current line

    Combined with `4` and editor commands, this is trivial.

8. [x] Move task up and down.

    Just use editor command.
    The advantage of gfmtask is all editor commands are available.

9. [ ] Submit to packagecontrol.io

    https://packagecontrol.io/docs/submitting_a_package

10. [ ] Integrate with git.

    - [x] Hide result window.
    - [x] fall back to built-in committer
    - [x] expose a command
    - [ ] example external committer
        * [ ] shell lib
            + [ ] library organize
            + [ ] parsing/escaping (testable)
                - [ ] zigj
                    * [ ] swift on os x
                        - [x] sprinkle
    - [ ] doc

11. [x] Sublime Text 2 support.

    I do not use Sublime Text 2.
    Pull request is welcome.

12. [x] Highlight next task.

    - [x] Check lldb.
    - [x] Check pry-byebug.
    - [x] Find next task.
        1.  Topside down.
        2.  Inside out.
        * [x] Find next main tasks.
    - [x] Highlight
        + [x] Display on Sublime Text.
            * We could add a right caret at the gutter, but it is small.
            * [x] MarkdownEditing theme does not have highlight colors.
            * [x] MarkdownEditing ships a MarkdownEditor-Focus.tmTheme. But it has no syntax highlight except for urls.
            * [x] Change `Packages/MarkdownEditing/MarkdownEditor.tmTheme`:
                ```xml
                <key>lineHighlight</key>
                <string>#e6e6e6</string>
                ```
                Change `#e6e6e6` to `#B6B6B6`
        + [x] Preserve on file.
            Based on current `next` implementation, this is useless.
        + [x] Auto change source when going forward.
            See above.
    - [x] Fold.
        + See https://github.com/fermads/sublime-autofold/blob/master/AutoFold.py
        * [x] listen on load.
        * [x] listen on save.
        * [x] fold task itself
        * [x] fold nested block.
        * [x] load_async

13. [x] Menu: Package settings

14. [x] pr MarkDownEditing theme

15. [ ] Call committer on save.
    - [ ] Commit current approach.
    - [ ] Stop hook into `gfmtask_toggle_done`.

16. [x] messages.json
