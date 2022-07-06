import sublime
import sublime_plugin
import sys

# Clear module cache to force reloading all modules of this package.
# See https://github.com/emmetio/sublime-text-plugin/issues/35
prefix = __package__ + "."  # don't clear the base package
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix) and module_name != __name__
]:
    del sys.modules[module_name]


# def settings(key):
#     return sublime.load_settings("HexPmInfo.sublime-settings").get(key)

def debug(*args):
    if settings("debug"):
        print("[quick-syntax]", *args)


class ChangeSyntaxCommand(sublime_plugin.WindowCommand):
    def get_selected_index(self):
        view = self.window.active_view()
        current_syntax = view.syntax().path
        all_syntaxes = list(map(lambda syntax: syntax.path, self.syntaxes))
        return all_syntaxes.index(current_syntax)

    def run(self):
        self.syntaxes = sublime.list_syntaxes()
        self.syntaxes = filter(lambda syntax: not syntax.hidden, self.syntaxes)
        self.syntaxes = list(self.syntaxes)

        # self.syntaxes = map(lambda syntax: [syntax.name, "%s" % (syntax.hidden)], self.syntaxes)
        names = list(map(lambda syntax: syntax.name, self.syntaxes))

        if self.syntaxes:
            self.get_selected_index()
            self.window.show_quick_panel(names, self.on_select, on_highlight=self.on_select,
                                         selected_index=self.get_selected_index())

    def on_select(self, index):
        if index > -1:
            syntax = self.syntaxes[index]
            view = self.window.active_view()
            view.assign_syntax(syntax.path)
