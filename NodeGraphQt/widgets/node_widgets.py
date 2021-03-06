#!/usr/bin/python
from PySide import QtGui, QtCore

from .constants import Z_VAL_NODE_WIDGET
from .stylesheet import *


class _NodeGroubBox(QtGui.QGroupBox):

    def __init__(self, label, parent=None):
        super(_NodeGroubBox, self).__init__(parent)
        margin = (0, 0, 0, 0)
        padding_top = '10px'
        if label == '':
            margin = (0, 2, 0, 0)
            padding_top = '4px'
        style = STYLE_QGROUPBOX.replace('$PADDING_TOP', padding_top)
        self.setMaximumSize(120, 50)
        self.setTitle(label)
        self.setStyleSheet(style)

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.setContentsMargins(*margin)

    def add_node_widget(self, widget):
        self._layout.addWidget(widget)


class NodeBaseWidget(QtGui.QGraphicsProxyWidget):
    """
    Base Node Widget.
    """

    value_changed = QtCore.Signal(str, str)

    def __init__(self, parent=None, name='widget', label=''):
        super(NodeBaseWidget, self).__init__(parent)
        self.setZValue(Z_VAL_NODE_WIDGET)
        self._name = name
        self._label = label

    def _value_changed(self):
        self.value_changed.emit(self.name, self.value)
        
    def setToolTip(self, tooltip):
        tooltip = tooltip.replace('\n', '<br/>')
        tooltip = '<b>{}</b><br/>{}'.format(self.name, tooltip)
        super(NodeBaseWidget, self).setToolTip(tooltip)

    @property
    def widget(self):
        return NotImplementedError

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, text):
        raise NotImplementedError

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def type(self):
        return str(self.__class__.__name__)

    @property
    def node(self):
        self.parentItem()

    @property
    def name(self):
        return self._name


class NodeComboBox(NodeBaseWidget):
    """
    ComboBox Node Widget.
    """

    def __init__(self, parent=None, name='', label='', items=None):
        super(NodeComboBox, self).__init__(parent, name, label)
        self.setZValue(Z_VAL_NODE_WIDGET + 1)
        self._combo = QtGui.QComboBox()
        self._combo.setStyleSheet(STYLE_QCOMBOBOX)
        self._combo.setMinimumHeight(24)
        self._combo.activated.connect(self._value_changed)
        list_view = QtGui.QListView(self._combo)
        list_view.setStyleSheet(STYLE_QLISTVIEW)
        self._combo.setView(list_view)
        self._combo.clearFocus()
        group = _NodeGroubBox(label)
        group.add_node_widget(self._combo)
        self.setWidget(group)
        self.add_items(items)

    @property
    def type(self):
        return 'ComboNodeWidget'

    @property
    def widget(self):
        return self._combo

    @property
    def value(self):
        return str(self._combo.currentText())

    @value.setter
    def value(self, text=''):
        index = self._combo.findText(text, QtCore.Qt.MatchExactly)
        self._combo.setCurrentIndex(index)

    def add_item(self, item):
        self._combo.addItem(item)

    def add_items(self, items=None):
        if items:
            self._combo.addItems(items)

    def all_items(self):
        return [self._combo.itemText(i) for i in range(self._combo.count)]

    def sort_items(self):
        items = sorted(self.all_items())
        self._combo.clear()
        self._combo.addItems(items)

    def clear(self):
        self._combo.clear()


class NodeLineEdit(NodeBaseWidget):
    """
    LineEdit Node Widget.
    """

    def __init__(self, parent=None, name='', label='', text=''):
        super(NodeLineEdit, self).__init__(parent, name, label)
        self._ledit = QtGui.QLineEdit()
        self._ledit.setStyleSheet(STYLE_QLINEEDIT)
        self._ledit.setAlignment(QtCore.Qt.AlignCenter)
        self._ledit.textChanged.connect(self._value_changed)
        self._ledit.clearFocus()
        group = _NodeGroubBox(label)
        group.add_node_widget(self._ledit)
        self.setWidget(group)
        self.text = text

    @property
    def type(self):
        return 'LineEditNodeWidget'

    @property
    def widget(self):
        return self._ledit

    @property
    def value(self):
        return str(self._ledit.text())

    @value.setter
    def value(self, text=''):
        self._ledit.setText(text)


class NodeCheckBox(NodeBaseWidget):
    """
    CheckBox Node Widget.
    """

    def __init__(self, parent=None, name='', label='', text='', state=False):
        super(NodeCheckBox, self).__init__(parent, name, label)
        self._cbox = QtGui.QCheckBox(text)
        self._cbox.setChecked(state)
        self._cbox.setMinimumWidth(80)
        self._cbox.setStyleSheet(STYLE_QCHECKBOX)
        self._cbox.stateChanged.connect(self._value_changed)
        group = _NodeGroubBox(label)
        group.add_node_widget(self._cbox)
        self.setWidget(group)
        self.text = text
        self.state = state

    @property
    def type(self):
        return 'CheckboxNodeWidget'

    @property
    def widget(self):
        return self._cbox

    @property
    def value(self):
        return self._cbox.isChecked()

    @value.setter
    def value(self, state=False):
        self._cbox.setChecked(state)
