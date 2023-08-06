# !/usr/bin/python
# coding=utf-8
from tentacle.slots.maya import *
from tentacle.slots.rendering import Rendering


class Rendering_maya(Rendering, Slots_maya):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		cmb = self.sb.rendering.draggable_header.ctxMenu.cmb000
		items = ['']
		cmb.addItems_(items, '')


	def cmb000(self, index=-1):
		'''Editors
		'''
		cmb = self.sb.rendering.draggable_header.ctxMenu.cmb000

		if index>0:
			text = cmb.items[index]
			if text=='':
				pass
			cmb.setCurrentIndex(0)


	def cmb001(self, index=-1):
		'''Render: camera
		'''
		cmb = self.sb.rendering.cmb001

		# self.cams = [cam for cam in rt.cameras if 'Target' not in str(cam)]
		# if self.cams:
		# 	lst = [str(cam.name) for cam in self.cams] #camera names
		# 	contents = cmb.addItems_(lst)


	def b000(self):
		'''Render Current Frame
		'''
		cmb = self.sb.rendering.cmb001
		index = cmb.currentIndex()

		try:
			rt.render (camera=self.cams[index]) #render with selected camera
		except:
			pm.mel.eval('RenderIntoNewWindow;')


	def b001(self):
		'''Open Render Settings Window
		'''
		pm.mel.eval('unifiedRenderGlobalsWindow;')


	def b002(self):
		'''Redo Previous Render
		'''
		pm.mel.eval('redoPreviousRender render;')


	def b003(self):
		'''Editor: Render Setup
		'''
		pm.mel.eval('RenderSetupWindow;')


	def b004(self):
		'''Editor: Rendering Flags
		'''
		pm.mel.eval('renderFlagsWindow;')


	def b005(self):
		'''Apply Vray Attributes To Selected Objects
		'''
		selection = pm.ls(selection=1)
		currentID=1
		for obj in selection:
			# get renderable shape nodes relative to transform, iterate through and apply subdivision
			shapes = pm.listRelatives(obj,s=1,ni=1)
			if shapes:
				for shape in shapes:
					pm.mel.eval ("vray addAttributesFromGroup "+shape+" vray_subdivision 1;")
					pm.mel.eval ("vray addAttributesFromGroup "+shape+" vray_subquality 1;")
			# apply object ID to xform. i don't like giving individual shapes IDs.
			pm.mel.eval ("vray addAttributesFromGroup "+obj+" vray_objectID 1;")
			pm.setAttr(obj+'.vrayObjectID',currentID)
			currentID+=1


	def b006(self):
		'''Load Vray Plugin
		'''
		if loadVRayPlugin(query=True):
			self.loadVRayPlugin(unload=True)
		else:
			self.loadVRayPlugin()


	def loadVRayPlugin(self, unload=False, query=False):
		'''Load/Unload the Maya Vray Plugin if it exists.

		Parameters:
			unload (bool): Unload the VRay plugin.
			query (bool): Query the state of the VRay Plugin.
		'''
		if query:
			return True if pm.pluginInfo('vrayformaya.mll', query=1, loaded=1) else False

		vray = ['vrayformaya.mll','vrayformayapatch.mll']

		if unload:
			try:
				pm.unloadPlugin(vray)
			except:
				pm.unloadPlugin(vray, force=1)
				self.sb.messageBox('{0}{1}{2}'.format("Force unloadPlugin:", str(vray), " "), messageType='Result')
		else:
			pm.loadPlugin(vray)









#module name
print (__name__)
# --------------------------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------------------------