"""
A module containing the views for build_dashboard
"""
from asciimatics.widgets import Frame, Layout, Label, Background, Divider, ListBox, MultiColumnListBox
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from datetime import datetime
from build_dashboard import logger

class BuildListView(Frame):
    """Frame to display the list of builds for a builder

    Args:
        screen (:obj:`Screen`): The screen object
        model: The Buildbot model
    """
    def __init__(self, screen, model):
        super(BuildListView, self).__init__(screen, screen.height, screen.width)
        self.set_theme("monochrome")
        self.model = model
        self.layout = Layout([100], fill_frame=True)
        self.add_layout(self.layout)
        self.fix()

    def update(self, frame):
        self.layout.clear_widgets()
        if self.model.builder:
            builds = [ BuildListView.format_build_info(builder) 
                for builder in self.model.builder.get('builds',[]) ]
            logger.debug("Found %s builds.", len(builds))
            self.layout.add_widget(
                    Label("Builds for: " + self.model.builder['name']))
            self.layout.add_widget(Divider())
            self.layout.add_widget(MultiColumnListBox(20,
                columns=["20%", "15%", "15%", "50%"],
                options=builds,
                titles=['Number', 'Started At', 'Completed At', 'Status'],
                name='builder'))
        self.fix()
        Frame.update(self, frame)
    
    def process_event(self, event):
        if (event is not None and isinstance(event, KeyboardEvent)):
            logger.debug(event.key_code)
            if event.key_code == -1:
                raise NextScene(name="BuildbotView")
        return super(BuildListView, self).process_event(event)

    @staticmethod
    def format_build_info(build):
        number = build['number']
        if build['complete']:
            complete_time = datetime.utcfromtimestamp(
                    build['complete_at']).strftime('%Y-%m-%d %H:%M:%S')
        else:
            complete_time = ''
        start_time = datetime.utcfromtimestamp(
                    build['started_at']).strftime('%Y-%m-%d %H:%M:%S')
        state_string = build['state_string']
        buildid = build['buildid']
        formatted = ([str(number), start_time, complete_time, state_string], buildid)
        return formatted




class BuildbotView(Frame):
    """ Entrypoint view of the build-dashboard.

    Args:
        screen: The screen used for displaying the view.
        model: The BuildbotModel for retrieving data.
    """

    def __init__(self, screen, model):
        super(BuildbotView, self).__init__(screen, screen.height, screen.width)
        self.set_theme("monochrome")
        self.model = model
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._render_builders(layout) 
        self.fix()


    def _render_builders(self, layout):
        """Renders the list of builders and their build status.

        Args:
            layout (:obj:`Layout`): The layout to which to add the builders

        """
        layout.add_widget(Label("Buildbot"))
        layout.add_widget(Divider())
        builders = [ BuildbotView.format_builder_info(builder) 
            for builder in self.model.builders() ]
        logger.debug("Found %s builder.", len(builders))
        self.builder_list = MultiColumnListBox(20,
            columns=["20%", "30%", "15%", "35%"],
            options=builders,
            on_select=self._select,
            titles=['Builder', 'Description', 'Last Build', 'Status'],
            name='builder')
        layout.add_widget(self.builder_list)

    def _select(self):
        self.save()
        self.model.select_builder(self.data['builder'])
        raise NextScene(name='BuildListView')
    
    def update(self, frame):
        builders = [ BuildbotView.format_builder_info(builder) 
            for builder in self.model.builders() ]
        logger.debug("Found %s builder.", len(builders))
        self.builder_list.options = builders
        self.model.select_builder(builders[0][1])
        Frame.update(self, frame) 

    def process_event(self, event):
        return super(BuildbotView, self).process_event(event)
        
    @staticmethod
    def format_builder_info(builder):
        """ Formats the merged builder and builds message into the columns
        for a :obj:`MultiColumnListBox` in :obj:`BuildbotView`.

        Args:
            builder (:obj:`dict`): A builder :obj:`dict` with the merged
                builds :obj:`dict`.

        Returns:
            A :obj:`tuple` with four columns and id.
        """
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
        builderid = builder['builderid']
        formatted = ([name,
            description,
            last_build_time,
            state_string],
            builderid)
        return formatted
