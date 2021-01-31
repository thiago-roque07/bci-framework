# General snippets

snippets = {
    "def (snippet)": "# ----------------------------------------------------------------------\ndef [!](self):\n\t\"\"\"\"\"\"",

}

snippets_ = [
    "random.randint([!])", "random.shuffle([!])",
]


keywords = [
    'and', 'assert', 'break', 'class', 'continue',
    'del', 'elif', 'else', 'except', 'exec', 'finally',
    'for', 'from', 'global', 'if', 'import', 'in',
    'is', 'lambda', 'not', 'or', 'pass', 'print',
    'raise', 'return', 'try', 'while', 'yield',
    'None', 'True', 'False', 'as', '__name__', 'format', 'int', 'float', 'str',
    'list', 'tuple', 'dict', 'set', 'len', 'super', 'range', 'enumerate', 'hasattr', 'getattr',
]

# Stimuli delivery snippets

stimuli_snippets = {

    # Widgets
    "widgets.label (snippet)": "widgets.label('[!]', typo='body1')",
    "widgets.button (snippet)": "widgets.button('[!]', on_click=None)",
    "widgets.switch (snippet)": "widgets.switch('[!]', checked=True, on_change=None, id='')",
    "widgets.checkbox (snippet)": "widgets.checkbox('[!]', [[str, bool], ...], on_change=None, id='')",
    "widgets.radios (snippet)": "widgets.radios('[!]', [[str, [str], ...]], on_change=None, id='')",
    "widgets.select (snippet)": "widgets.select('[!]', [[str, [str], ...]], on_change=None, id='')",
    "widgets.slider (snippet)": "widgets.slider('[!]', min=1, max=10, step=0.1, value=5, on_change=None, id='')",
    "widgets.range_slider (snippet)": "widgets.range_slider('[!]', min=0, max=20, value_lower=5, value_upper=15, step=1, on_change=None, id='')",
    "self.widgets.get_value()": "self.widgets.get_value('[!]')",


}

stimuli_snippets_ = [

    # API
    'self.add_run_progressbar([!])', 'self.set_progress([!])' 'self.send_marker(\'[!]\')',

    # Brython
    'timer.set_timeout([!])',
    'timer.clear_timeout([!])'
]


stimuly_keywords = [
    '@DeliveryInstance.local', '@DeliveryInstance.remote', '@DeliveryInstance.both',
    'self.dashboard', 'self.stimuli_area',
    'self.build_areas()', 'self.add_cross()',
]


# Data analisys snippets

analisys_snippets = {

}

analisys_snippets_ = [

]

analisys_keywords = [

]


[stimuli_snippets.update({key.replace('[!]', ''): key}) for key in stimuli_snippets_]
[analisys_snippets.update({key.replace('[!]', ''): key})for key in analisys_snippets_]
[snippets.update({key.replace('[!]', ''): key}) for key in snippets_]


STIMULI_KEYWORDS = stimuly_keywords + list(stimuli_snippets.keys()) + list(snippets.keys())
ANALISYS_KEYWORDS = analisys_keywords + list(analisys_snippets.keys()) + list(snippets.keys())
