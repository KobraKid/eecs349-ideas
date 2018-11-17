import json
import kivy
import os
kivy.require('1.10.1')
from tkinter import Tk
from tkinter import filedialog
from tkinter import *
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput
from os import listdir
from pprint import pprint

kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)

keys = {
    '/table_id': 0, '/robot_id': 0, '/run_id': 0, '/data/id': 0, '/data/photo/key': 0, '/data/photo/full': 0, '/data/photo/ed': 0, '/data/photo/med': 0,
    '/data/photo/little': 0, '/data/photo/small': 0, '/data/photo/thumb': 0, '/data/photo/1024x576': 0, '/data/photo/1536x864': 0, '/data/name': 0,
    '/data/blurb': 0, '/data/goal': 0, '/data/pledged': 0, '/data/state': 0, '/data/slug': 0, '/data/disable_communication': 0, '/data/country': 0,
    '/data/currency': 0, '/data/currency_symbol': 0, '/data/currency_trailing_code': 0, '/data/deadline': 0, '/data/state_changed_at': 0, '/data/created_at': 0,
    '/data/launched_at': 0, '/data/staff_pick': 0, '/data/is_starrable': 0, '/data/backers_count': 0, '/data/static_usd_rate': 0, '/data/usd_pledged': 0,
    '/data/converted_pledged_amount': 0, '/data/fx_rate': 0, '/data/current_currency': 0, '/data/usd_type': 0, '/data/creator/id': 0, '/data/creator/name': 0,
    '/data/creator/slug': 0, '/data/creator/is_registered': 0, '/data/creator/chosen_currency': 0, '/data/creator/avatar/thumb': 0,
    '/data/creator/avatar/small': 0, '/data/creator/avatar/medium': 0, '/data/creator/urls/web/user': 0, '/data/creator/urls/api/user': 0,
    '/data/location/id': 0, '/data/location/name': 0, '/data/location/slug': 0, '/data/location/short_name': 0, '/data/location/displayable_name': 0,
    '/data/location/localized_name': 0, '/data/location/country': 0, '/data/location/state': 0, '/data/location/type': 0, '/data/location/is_root': 0,
    '/data/location/urls/web/discover': 0, '/data/location/urls/web/location': 0, '/data/location/urls/api/nearby_projects': 0, '/data/category/id': 0,
    '/data/category/name': 0, '/data/category/slug': 0, '/data/category/position': 0, '/data/category/parent_id': 0, '/data/category/color': 0,
    '/data/category/urls/web/discover': 0, '/data/profile/id': 0, '/data/profile/project_id': 0, '/data/profile/state': 0, '/data/profile/state_changed_at': 0,
    '/data/profile/name': 0, '/data/profile/blurb': 0, '/data/profile/background_color': 0, '/data/profile/text_color': 0,
    '/data/profile/link_background_color': 0, '/data/profile/link_text_color': 0, '/data/profile/link_text': 0, '/data/profile/link_url': 0,
    '/data/profile/show_feature_image': 0, '/data/profile/background_image_opacity': 0, '/data/profile/should_show_feature_image_section': 0,
    '/data/profile/feature_image_attributes/image_urls/default': 0, '/data/profile/feature_image_attributes/image_urls/baseball_card': 0, '/data/spotlight': 0,
    '/data/urls/web/project': 0, '/data/urls/web/rewards': 0, '/data/source_url': 0
}
filename = "No file chosen"
lines = 1
selected_cols = []


def get_cols(dictionary, parent, search):
    retval = ''
    for key, value in dictionary.items():
        if isinstance(value, dict):
            retval = retval + get_cols(value, parent + '/' + key, search)
            continue
        if parent + '/' + key == search or search == '':
            if value is not str:
                retval = retval + str(value)
            else:
                retval = retval + value
    return retval


def get_data_by_line(filename, lines):
    data = []
    count = 1
    with open(filename, 'rb') as f:
        for line in f:
            data.append(json.loads(line))
            if lines == 0 or int(lines) == 0:
                continue
            if count == int(lines):
                break
            else:
                count = count + 1
    return data


class FileChooseButton(Button):
    _python_access = ObjectProperty(None)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class LineCountTextInput(TextInput):
    pass


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        global selected_cols
        self.selected = is_selected
        txt = rv.data[index].get('text')
        if is_selected:
            if txt not in selected_cols:
                selected_cols.append(txt)
        else:
            selected_cols[:] = [x for x in selected_cols if x != txt]

    def reset(self):
        self.selected = False


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': key} for key in list(keys.keys())]

    def reset(self):
        # self.data = [{'text': key} for key in list(keys.keys())]
        self.layout_manager.reset()
        self.layout_manager.reset()


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    def reset(self):
        for node in self.selected_nodes:
            self.deselect_node(node)


class BeginParseButton(Button):
    pass


class DataViewer(GridLayout):
    display = ObjectProperty()

    def update_linecount(self):
        global lines
        lines = self.ids.linecounter.text

    def parse(self):
        global lines
        global filename
        if filename == "No file chosen":
            return

        # parse (lines) lines from (filename)
        # then get columns that match selected set
        data = get_data_by_line(filename, lines)
        result = ""
        sep = "=======================================================\n"
        if len(selected_cols) == 0:
            result = "Dumping data (WARNING: LARGE DATA SET)\n" + sep
            for datum in data:
                r = get_cols(datum, '', '')
                if r is None:
                    r = "<Not found>"
                result = result + r + '\n' + sep
        else:
            for datum in data:
                for col in selected_cols:
                    r = get_cols(datum, '', col)
                    if r is None:
                        r = "<Not found>"
                    result = result + col + ": " + r + '\n'
                result = result + sep
        self.display.text = result

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, file):
        global filename
        filename = os.path.join(path, file[0])
        self.dismiss_popup()

    def dismiss_popup(self):
        global filename
        newtext = filename
        if len(filename) > 29:
            newtext = filename[-29:]
        self.ids.filename.text = newtext
        self._popup.dismiss()

    def reset(self):
        global lines
        global selected_cols
        global filename
        filename = "No file chosen"
        lines = 1
        selected_cols = []
        self.ids.linecounter.text = "1"
        self.display.text = ''
        self.ids.filename.text = filename
        self.ids.rv.reset()


class MainApp(App):

    def build(self):
        self.title = "Kickstarter Data Visualizer"
        return DataViewer()


Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == "__main__":
    MainApp().run()
