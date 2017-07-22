"""GFM task list under Sublime Text."""


import re

import sublime
import sublime_plugin


def get_setting(key):
    """
    Given a key, return its value from `gfmtask.sublime-settings`.

    Return `None` if the value is empty.
    """
    settings = sublime.load_settings('gfmtask.sublime-settings')
    setting = settings.get(key)
    if settings == '':
        return None
    else:
        return setting
        pass
    pass


def get_file_path():
    """
    Get current file's directory.

    Return `None` if there is no file path available.
    """
    try:
        file_path = sublime.active_window().extract_variables()['file_path']
    except KeyError:
        return None
    else:
        return file_path


def is_markdown(view):
    """Determine if the given view location is Markdown."""
    if view is None:
        return False
    else:
        try:
            location = view.sel()[0].begin()
        except IndexError:
            return False
            pass
        pass
    matcher = 'text.html.markdown'

    return view.match_selector(location, matcher)
    pass


def invoke_committer(view, auto=False):
    """
    Invoke external committer if `gfmtask_committer` is set.

    Otherwise fall back to calling `git` directly.

    If `auto` is `True`,

    - and `gfmtask_auto_commit` is set, save current file and commit;
    - and `gfmtask_auto_commit` is not set, do nothing.
    """
    file_path = get_file_path()
    if file_path:
        if auto:
            auto_commit = get_setting('gfmtask_auto_commit')
            if not auto_commit:
                return
            else:
                pass
        else:
            view.run_command('save')
            committer = get_setting('gfmtask_committer')
            if committer:
                view.window().run_command('exec', {
                    'cmd': [committer],
                    'working_dir': file_path
                })
            else:
                view.window().run_command('exec', {
                    'cmd': ['git',
                            'commit', '-a',
                            '--allow-empty-message', '-m', "''"]
                })
                pass
            # Does not pop up result window.
            view.window().run_command(
                "hide_panel", {"panel": "output.exec"}
            )
            pass
    else:
        pass
    pass


class GfmtaskToggleDone(sublime_plugin.TextCommand):

    """
    Toggle GFM task status.

    Works on all kinds of GFM tasks, ordered, unordered,
    nested, or unnested.

    - On a task marked as done (`[x]` or `[X]`),
    it will mark it as an undo task `[ ]`.

    - On a undo task `[ ]`, it will mark it as done `[x]`.

    - On a normal list item, it will convert it into a task.

    - On a normal line, it will add `- [ ]`
    before its first non blank character.

    When `gfmtask_auto_commit` is on,
    once marking a task as done, or reverting marking a task as done,
    it will also save the file, and invoke an external committer
    to commit changes.
    """

    def is_enabled(self):
        """
        Only enabled on markdown syntax.

        Enabled on markdown families, including GFM and MultiMarkdown.
        Disabled on all other syntax.
        """
        return is_markdown(self.view)

    def run(self, edit):
        """Called when the command `gfmtask_toggle_done` runs."""
        for region in self.view.sel():
            # Avoid span multiple lines.
            if region.empty():
                line = self.view.full_line(region)
                line_contents = self.view.substr(line)
                task_mark_regex = re.compile('\s*([-+*]|\d+\.) \[[ xX]\]')
                task_head = task_mark_regex.match(line_contents)
                if task_head:
                    task_mark = task_head.group(0)
                    list_mark = task_mark[0:-4]
                    # mark as done `[ ] -> [x]`
                    if task_mark.endswith('[ ]'):
                        line_contents = task_mark_regex.sub(
                            "{} [x]".format(list_mark),
                            line_contents,
                            1
                        )
                    # undo marking done `[xX] -> [ ]`
                    elif task_mark[-2] in ('x', 'X'):
                        line_contents = task_mark_regex.sub(
                            "{} [ ]".format(list_mark),
                            line_contents,
                            1
                        )
                        pass
                    self.view.replace(edit, line, line_contents)
                    invoke_committer(self.view, True)
                # line is not a task
                else:
                    # list mark (with trailing whitespace)
                    list_mark_regex = re.compile('\s*([-+*]|\d+\.) ')
                    list_mark = list_mark_regex.match(line_contents)
                    # convert a list item to a task
                    if list_mark:
                        line_contents = re.sub(
                            list_mark_regex,
                            "{}[ ] ".format(list_mark.group(0)),
                            line_contents,
                            1
                        )
                    # convert a normal line to a task
                    else:
                        line_contents = re.sub(
                            r'^(\s*)(\S)',
                            r'\1- [ ] \2',
                            line_contents,
                            1
                        )
                        pass
                    self.view.replace(edit, line, line_contents)
                    pass
            else:
                pass
            pass


class GfmtaskCommit(sublime_plugin.TextCommand):

    """
    Commit changes to task list file.

    If `gfmtask_committer` is set, invoke it,
    otherwise call `git` directly.
    """

    def is_enabled(self):
        """
        Only enabled on markdown syntax.

        Enabled on markdown families, including GFM and MultiMarkdown.
        Disabled on all other syntax.
        """
        return is_markdown(self.view)

    def run(self, edit):
        """Called when the command `gfmtask_commit` runs."""
        invoke_committer(self.view)


def find_till_end(view, regex, position):
    """
    Find all regions matching the regex from position to EOF.

    I implement this function because:

    - `find(pattern, fromPosition, <flags>)` in a while loop
    causes Sublime Text to stop responses.
    - `find_all(pattern, <flags>, <format>, <extractions>)`
    cannot specify a range to search.
    """
    todos = []
    for todo in view.find_all(regex):
        if todo.begin() < position.begin():
            pass
        else:
            todos.append(todo)
            pass
        pass
    return todos
    pass


def scan_items(view, regex, level=0, position=sublime.Region(0)):
    """Scan for list items according to _regex_ at _level_."""
    head_regex = r'^' + r'\s' * 4 * level + regex
    return find_till_end(view, head_regex, position)
    pass


class GfmtaskNext(sublime_plugin.TextCommand):

    """
    Go to the next task.

    1. Topside down;
    2. Inside out.

    Assuming outer tasks will not be marked as done
    unless all of its sub tasks are done.

    Assuming tasks is in a stack, new task is adding above old ones.

    Example:

    4. [ ] First task.
        5. [ ] Nested task.
            6. [ ] Inner task.
            7. [ ] Another inner task.
        8. [ ] Another nested task.
    1. [ ] Second task.
        2. [ ] foo
        3. [ ] bar

    Next order: 3 -> 2 -> 1 -> 8 -> 7 -> 6 -> 5 -> 4
    """

    def scan_todos(self, level=0, position=sublime.Region(0)):
        """Scan for all todos at the given level."""
        todo_mark_regex = r'([-+*]|\d+\.) \[ \] '
        return scan_items(self.view, todo_mark_regex, level, position)
        pass

    def scan_normal_items(self, level=0, position=sublime.Region(0)):
        """Scan for normal list items at the given level."""
        item_mark_regex = r'([-+*]|\d+\.) ([^[]|(\[[^ xX])|(\[[ xX][^]]))'
        return scan_items(self.view, item_mark_regex, level, position)

    def seek_next_todo(self):
        """Find next todo. Return `None` if not found."""
        level = 0
        first_level_todos = self.scan_todos()
        # No first level todos.
        if first_level_todos == []:
            return None
        else:
            todos = first_level_todos
            while True:
                if todos != []:
                    next_todo = todos[-1]
                    level += 1
                    todos = self.scan_todos(level, next_todo)
                else:
                    while True:
                        level += 1
                        items = self.scan_normal_items(level, next_todo)
                        if items == []:
                            return next_todo
                        else:
                            level += 1
                            todos = self.scan_todos(level, next_todo)
                            return
                            pass
                        pass
                    pass
                pass
            pass
        pass

    def is_enabled(self):
        """
        Only enabled on markdown syntax.

        Enabled on markdown families, including GFM and MultiMarkdown.
        Disabled on all other syntax.
        """
        return is_markdown(self.view)
        pass

    def run(self, edit):
        """Called when the command `gfmtask_next` runs."""
        next_todo = self.seek_next_todo()
        if next_todo:
            self.view.sel().clear()
            self.view.sel().add(next_todo.begin())
            self.view.show_at_center(next_todo)
        else:
            pass
        pass


class GfmtaskListener(sublime_plugin.EventListener):

    """Fold finished tasks on load and save."""

    # EventListener does not have `is_enabled` method.

    def is_enabled(self, view):
        """
        Only enabled on markdown syntax.

        Enabled on markdown families, including GFM and MultiMarkdown.
        Disabled on all other syntax.
        """
        return is_markdown(view)
        pass

    def fold_finished(self, view):
        """
        Fold finished tasks.

        Search for finished tasks, and fold them all,
        together with their sub lists.
        """
        if self.is_enabled(view):
            def scan_first_level_finished():
                first_level_finished_mark_regex = r'([-+*]|\d+\.) \[[xX]\] '
                return scan_items(view, first_level_finished_mark_regex)
                pass

            def fold_first_level_finished_task(task_region):
                start_point = task_region.begin()
                task_line = view.full_line(start_point)
                # `indented_region(point)` is an undocumented API.
                # I have found the code sample on
                # https://github.com/aziz/PlainTasks/pull/215#discussion_r25297767
                #
                # ```python
                # line = view.line(view.sel()[0].begin())
                # region = view.indented_region(line.b + 2)
                # ```
                #
                # Thus I guess `indented_region(point)` will return a region
                # starts from `point`, and succeeding lines indented
                # no less than the line of `point`.
                # `+ 2` means moving the point after new line and the start
                # of next line.
                #
                # I use `full_line` instead, which moves to the next line
                # unless it is EOF.
                task_block = view.indented_region(task_line.end())
                if task_block.empty():
                    # Fold one liner itself.
                    view.fold(task_line)
                else:
                    task_block.a = start_point
                    view.fold(task_block)
                    pass

            for region in scan_first_level_finished():
                fold_first_level_finished_task(region)
                pass
        else:
            pass
        pass

    def on_load_async(self, view):
        """Fold finished tasks on load.

        Note this does not work on calling `subl file` from the command line.
        """
        self.fold_finished(view)

    def on_pre_save_async(self, view):
        """
        Fold finished tasks on save.

        Not `on_post_save_async` because view may be closed after save.
        """
        self.fold_finished(view)
