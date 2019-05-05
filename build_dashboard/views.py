from asciimatics.widgets import Frame, Layout, Label, Background, Divider, ListBox, MultiColumnListBox
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from datetime import datetime

def formatBuilderInfo(builder):
    name = builder['name'] or 'None'
    description = builder['description'] or 'None'
    last_build = builder['builds'][-1]
    if last_build['complete']:
        last_build_time = datetime.utcfromtimestamp(
                    last_build['complete_at']).strftime(
                            '%Y-%m-%d %H:%M:%S')
    else:
        last_build_time = ''
    state_string = last_build['state_string']
    formatted = ([name,
        description,
        last_build_time,
        state_string],
        name)
    return formatted

class BuildbotView(Frame):
    def __init__(self, screen, model):
        super(BuildbotView, self).__init__(screen, screen.height, screen.width)
        self.set_theme("monochrome")
        self.model = model
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self.render_builders(layout)
        self.fix()

    def render_builders(self, layout):
        layout.add_widget(Label("Buildbot"))
        layout.add_widget(Divider())
        builders = [ formatBuilderInfo(builder) 
            for builder in self.model.getBuildersWithBuilds() ]
        builder_list = MultiColumnListBox(20,
            columns=[20, 40, 20, 20],
            options=builders,
            titles=['Builder', 'Description', 'Last Build', 'Status'],
            name='builder')
        layout.add_widget(builder_list)
