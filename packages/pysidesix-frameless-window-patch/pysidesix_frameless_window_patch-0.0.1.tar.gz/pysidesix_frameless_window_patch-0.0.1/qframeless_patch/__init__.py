from PySide6.QtWidgets import *
from types import MethodType
from qframelesswindow import FramelessWindowBase,StandardTitleBar,FramelessMainWindow

def patch():
    def setupUi(self:FramelessWindowBase,Form):
        if hasattr(super(Form.__class__,self),"setupUi"):
            super(Form.__class__,self).setupUi(self._mainbody)
    def setTitleBar(self:FramelessWindowBase,titlebar):
        self._titlebar.deleteLater()
        self.layout().replaceWidget(self._titlebar,titlebar)
        self._titlebar=titlebar
    old=FramelessWindowBase._initFrameless
    def new(self:FramelessWindowBase):
        old(self)
        self._widget=QWidget()
        self._layout=QVBoxLayout()
        self._layout.setContentsMargins(0,0,0,0)
        self._titlebar=StandardTitleBar(self)
        self._mainbody=QWidget()
        self.titleBar.hide()
        self._layout.addWidget(self._titlebar)
        self._layout.addWidget(self._mainbody)
        if isinstance(self,FramelessMainWindow):
            self._widget.setLayout(self._layout)
            self.setCentralWidget(self._widget)
        else:
            self.setLayout(self._layout)
        self.setTitleBar=MethodType(setTitleBar,self)
        self.setupUi=MethodType(setupUi,self)
    FramelessWindowBase._initFrameless=new