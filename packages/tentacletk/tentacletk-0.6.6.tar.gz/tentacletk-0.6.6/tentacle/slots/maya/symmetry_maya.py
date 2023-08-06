# !/usr/bin/python
# coding=utf-8
from tentacle.slots.maya import *
from tentacle.slots.symmetry import Symmetry



class Symmetry_maya(Symmetry, Slots_maya):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		cmb000 = self.sb.symmetry.draggable_header.ctxMenu.cmb000
		items = ['']
		cmb000.addItems_(items, '')

		#set initial checked state
		state = pm.symmetricModelling(query=True, symmetry=True) #application symmetry state
		axis = pm.symmetricModelling(query=True, axis=True)
		widget = 'chk000' if axis=='x' else 'chk001' if axis=='y' else 'chk002'
		getattr(self.sb.symmetry, widget).setChecked(state)
		getattr(self.sb.symmetry_submenu, widget).setChecked(state)


	def cmb000(self, index=-1):
		'''Editors
		'''
		cmb = self.sb.symmetry.draggable_header.ctxMenu.cmb000

		if index>0:
			if index==cmd.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def chk005(self, state=None):
		'''Symmetry: Topo
		'''
		self.sb.symmetry.chk004.setChecked(False) #uncheck symmetry:object space
		if any ([self.sb.symmetry.chk000.isChecked(), self.sb.symmetry.chk001.isChecked(), self.sb.symmetry.chk002.isChecked()]): #(symmetry)
			pm.symmetricModelling(edit=True, symmetry=False)
			self.sb.toggleWidgets(setUnChecked='chk000,chk001,chk002')
			self.sb.messageBox('First select a seam edge and then check the symmetry button to enable topographic symmetry', messageType='Note')


	def setSymmetry(self, state, axis):
		space = "world" #workd space
		if self.sb.symmetry.chk004.isChecked(): #object space
			space = "object"
		elif self.sb.symmetry.chk005.isChecked(): #topological symmetry
			space = "topo"

		state = state if state==0 else 1 #for case when checkbox gives a state of 2.

		tolerance = 0.25
		pm.symmetricModelling(edit=True, symmetry=state, axis=axis, about=space, tolerance=tolerance)
		# if state:
		# 	self.sb.messageBox('Symmetry: <hl>{}</hl>'.format(axis.upper(), messageType='Result'))









#module name
print (__name__)
# --------------------------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------------------------