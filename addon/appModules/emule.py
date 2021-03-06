# -*- coding: UTF-8 -*-
# eMule app module
# Copyright (C) 2012-2021 Noelia Ruiz Martínez, Alberto Buffolino, Javi Domínguez
# Released under GPL 2

import appModuleHandler
import addonHandler
import eventHandler
import api
import ui
import speech
import oleacc
import winUser
import windowUtils
import controlTypes
import NVDAObjects.IAccessible
from NVDAObjects.behaviors import RowWithFakeNavigation
from cursorManager import CursorManager
from NVDAObjects.window.edit import EditTextInfo
from scriptHandler import script
import tones

addonHandler.initTranslation()


class EmuleRowWithFakeNavigation(RowWithFakeNavigation):

	scriptCategory = addonHandler.getCodeAddon().manifest["summary"]

	def initOverlayClass(self):
		modifiers = ("control", "shift")
		for n in range(10):
			for modifier in modifiers:
				gesture = "kb:NVDA+{mod}+{num}".format(mod=modifier, num=n)
				self.bindGesture(gesture, "readColumn")
		self.bindGesture("kb:NVDA+shift+c", "copyColumn")
		self.bindGesture("kb:rightArrow", "readNextColumn")
		self.bindGesture("kb:leftArrow", "readPreviousColumn")
		self._savedColumnNumber = 0
		# Get a list of visible columns for avoid showing disabled columns
		self.enabledColumns = []
		c = 1
		try:
			while True:
				# width = 0 indicates that the column is disabled
				# and therefore, although it is accessible by NVDA, it is invisible on the screen
				if self._getColumnLocation(c).width:
					self.enabledColumns.append(c)
				c += 1
		except IndexError:  # Exceeding the last column ends the loop
			pass

	@script(
		# Translators: Message presented in input help mode.
		description=_("Reads the specified column for the current list item.")
	)
	def script_readColumn(self, gesture):
		col = int(gesture.mainKeyName[-1])
		if col == 0:
			col += 10
		if "shift" in gesture.modifierNames:
			col += 10
		if self.readColumn(col):
			self._savedColumnNumber = col

	def script_readPreviousColumn(self, gesture):
		if self.readColumn(self._savedColumnNumber - 1):
			self._savedColumnNumber -= 1

	def script_readNextColumn(self, gesture):
		if self.readColumn(self._savedColumnNumber + 1):
			self._savedColumnNumber += 1

	@script(
		# Translators: Message presented in input help mode.
		description=_("Copies the last read column of the selected list item to clipboard.")
	)
	def script_copyColumn(self, gesture):
		column = self.readColumn(self._savedColumnNumber, False)
		if api.copyToClip(column):
			# Translators: Message presented when the current column of the list item is copied to clipboard.
			ui.message(_("%s copied to clipboard") % column)

	def readColumn(self, col, verbose=True):
		if col <= 0:
			tones.beep(250, 50)
			return None
		try:
			col = self.enabledColumns[col - 1]
			header = self._getColumnHeader(col)
			subitem = self._getColumnContent(col) if self._getColumnContent(col) else ""
			column = ": ".join([header, subitem])
			if verbose:
				ui.message(column)
			return column
		except IndexError:
			tones.beep(250, 50)
			return None


class RichEditCursorManager(CursorManager):

	def makeTextInfo(self, position):
		# Fixes regression for issue 4291.
		return EditTextInfo(self, position)


class AppModule(appModuleHandler.AppModule):

	scriptCategory = addonHandler.getCodeAddon().manifest["summary"]

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_LISTITEM:
			clsList.insert(0, EmuleRowWithFakeNavigation)
		elif obj.windowClassName == "RichEdit20W":
			clsList.insert(0, RichEditCursorManager)

	def getToolBar(self):
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(
					api.getForegroundObject().windowHandle, visible=True, controlID=16127
				), winUser.OBJID_CLIENT, 0
			)
		except LookupError:
			return None
		return obj

	def getWhere(self):
		toolBar = self.getToolBar()
		if toolBar is None:
			return None
		children = toolBar.children
		for child in children:
			if child.IAccessibleStates == 16:
				return child

	def getName(self):
		where = self.getWhere()
		if where is not None:
			return where.name

	def getHeader(self):
		obj = api.getFocusObject()
		if not (
			obj and obj.windowClassName == 'SysListView32'
			and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_LISTITEM
		):
			return
		obj = obj.parent
		try:
			(left, top, width, height) = obj.location
			obj = NVDAObjects.IAccessible.getNVDAObjectFromPoint(left, top)
			return obj
		except Exception:
			return None

	def statusBarObj(self, pos):
		statusBar = api.getStatusBar()
		if statusBar:
			return statusBar.getChild(pos).name

	@script(
		# Translators: Message presented in input help mode.
		description=_("Moves the system focus and mouse to the main Tool Bar."),
		gesture="kb:control+shift+h"
	)
	def script_toolBar(self, gesture):
		obj = self.getToolBar()
		if obj is not None:
			if obj != api.getMouseObject():
				api.moveMouseToNVDAObject(obj)
				api.setMouseObject(obj)
			if controlTypes.STATE_FOCUSED not in obj.states:
				obj.setFocus()
			eventHandler.queueEvent("gainFocus", obj)

	@script(
		# Translators: Message presented in input help mode.
		# For instance: reads the search window, Statistics, IRC, etc.
		description=_("Reports the current window."),
		gesture="kb:control+shift+t"
	)
	def script_where(self, gesture):
		name = self.getName()
		if name is None:
			return
		ui.message("%s" % name)

	@script(
		# Translators: Message presented in input help mode.
		description=_("Moves the system focus to the Name field of the Search window."),
		gesture="kb:control+shift+n"
	)
	def script_name(self, gesture):
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(
					api.getForegroundObject().windowHandle, visible=True, controlID=2183
				), winUser.OBJID_CLIENT, 0
			)
		except LookupError:
			return
		if obj != api.getFocusObject():
			api.moveMouseToNVDAObject(obj)
			api.setMouseObject(obj)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0, None, None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP, 0, 0, None, None)

	@script(
		description=_(
			# Translators: Message presented in input help mode.
			"Moves the system focus and mouse to the search parameters list or Edit field for each option,"
			" in the Search window."
		),
		gesture="kb:control+shift+p"
	)
	def script_searchList(self, gesture):
		where = self.getWhere()
		if not hasattr(where, "IAccessibleChildID") or where.IAccessibleChildID != 6:
			return
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(
					api.getForegroundObject().windowHandle, controlID=2833
				), winUser.OBJID_CLIENT, 0
			)
		except LookupError:
			return
		if obj != api.getFocusObject():
			api.moveMouseToNVDAObject(obj)
			api.setMouseObject(obj)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0, None, None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP, 0, 0, None, None)

	@script(
		description=_(
			# Translators: Message presented in input help mode.
			"Moves the system focus to the first list in the current window."
			" For example the results list in the Search window, downloads in Transfer, etc."
		),
		gesture="kb:control+shift+b"
	)
	def script_list(self, gesture):
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(
					api.getForegroundObject().windowHandle, visible=True, className="SysListView32"
				), winUser.OBJID_CLIENT, 0
			)
		except LookupError:
			return
		if obj != api.getFocusObject():
			api.moveMouseToNVDAObject(obj)
			api.setMouseObject(obj)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0, None, None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP, 0, 0, None, None)

	@script(
		# Translators: Message presented in input help mode.
		description=_(
			"Moves the system focus to read-only edit boxes in the current window."
			" For example the IRC received messages."
		),
		gesture="kb:control+shift+o"
	)
	def script_readOnlyEdit(self, gesture):
		where = self.getWhere()
		if hasattr(where, "IAccessibleChildID") and where.IAccessibleChildID == 9:
			cID = -1
		else:
			cID = None
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(
					api.getForegroundObject().windowHandle, visible=True, className="RichEdit20W", controlID=cID
				), winUser.OBJID_CLIENT, 0
			)
		except LookupError:
			return
		if obj != api.getFocusObject():
			api.moveMouseToNVDAObject(obj)
			api.setMouseObject(obj)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0, None, None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP, 0, 0, None, None)

	@script(
		# Translators: Message presented in input help mode.
		description=_("Moves the navigator object and mouse to the current list headers."),
		gesture="kb:control+shift+l"
	)
	def script_header(self, gesture):
		obj = self.getHeader()
		if obj is None:
			return
		api.setNavigatorObject(obj)
		api.moveMouseToNVDAObject(obj)
		api.setMouseObject(obj)
		speech.speakObject(obj)

	@script(
		# Translators: Message presented in input help mode.
		description=_("Reports first object of the Status Bar."),
		gesture="kb:control+shift+q"
	)
	def script_statusBarFirstChild(self, gesture):
		if self.statusBarObj(0) is not None:
			ui.message(self.statusBarObj(0))

	@script(
		# Translators: Message presented in input help mode.
		description=_("Reports second object of the Status Bar."),
		gesture="kb:control+shift+w"
	)
	def script_statusBarSecondChild(self, gesture):
		if self.statusBarObj(1) is not None:
			ui.message(self.statusBarObj(1))

	@script(
		# Translators: Message presented in input help mode.
		description=_("Reports third object of the Status Bar."),
		gesture="kb:control+shift+e"
	)
	def script_statusBarThirdChild(self, gesture):
		if self.statusBarObj(2) is not None:
			ui.message(self.statusBarObj(2))

	@script(
		# Translators: Message presented in input help mode.
		description=_("Reports fourth object of the Status Bar."),
		gesture="kb:control+shift+r"
	)
	def script_statusBarForthChild(self, gesture):
		if self.statusBarObj(3) is not None:
			ui.message(self.statusBarObj(3))
