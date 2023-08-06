# !/usr/bin/python
# coding=utf-8
from tentacle.slots.maya import *
from tentacle.slots.rigging import Rigging


class Rigging_maya(Rigging, Slots_maya):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		dh = self.sb.rigging.draggable_header
		items = ['Quick Rig','HumanIK','Expression Editor','Shape Editor','Connection Editor','Channel Control Editor','Set Driven Key']
		dh.ctxMenu.cmb000.addItems_(items, 'Rigging Editors')

		cmb001 = self.sb.rigging.cmb001
		items = ['Joints','Locator','IK Handle', 'Lattice', 'Cluster']
		cmb001.addItems_(items, "Create")


	def cmb000(self, index=-1):
		'''Editors
		'''
		cmb = self.sb.rigging.draggable_header.ctxMenu.cmb000

		if index>0:
			text = cmb.items[index]
			if text=='Quick Rig':
				pm.mel.eval('QuickRigEditor;') #Quick Rig
			elif text=='HumanIK':
				pm.mel.eval('HIKCharacterControlsTool;') #HumanIK
			elif text=='Expression Editor':
				pm.mel.eval('ExpressionEditor;') #Expression Editor
			elif text=='Shape Editor':
				pm.mel.eval('ShapeEditor;') #Shape Editor
			elif text=='Connection Editor':
				pm.mel.eval('ConnectionEditor;') #Connection Editor
			elif text=='Channel Control Editor':
				pm.mel.eval('ChannelControlEditor;') #Channel Control Editor
			elif text=='Set Driven Key':
				pm.mel.eval('SetDrivenKeyOptions;') #Set Driven Key
			cmb.setCurrentIndex(0)


	def cmb001(self, index=-1):
		'''Create
		'''
		cmb = self.sb.rigging.cmb001

		if index>0:
			text = cmb.items[index]
			if text=='Joints':
				pm.setToolTo('jointContext') #create joint tool
			elif text=='Locator':
				pm.spaceLocator(p=[0,0,0]) #locator
			elif text=='IK Handle':
				pm.setToolTo('ikHandleContext') #create ik handle
			elif text=='Lattice':
				pm.lattice(divisions=[2,5,2], objectCentered=1, ldv=[2,2,2]) ##create lattice
			elif text=='Cluster':
				pm.mel.eval('CreateCluster;') #create cluster
			cmb.setCurrentIndex(0)


	def chk000(self, state=None):
		'''Scale Joint
		'''
		self.sb.toggleWidgets(setUnChecked='chk001-2')
		self.sb.rigging.tb000.ctxMenu.s000.setValue(pm.jointDisplayScale(query=1)) #init global joint display size


	def chk001(self, state=None):
		'''Scale IK
		'''
		self.sb.toggleWidgets(setUnChecked='chk000, chk002')
		self.sb.rigging.tb000.ctxMenu.setValue(pm.ikHandleDisplayScale(query=1)) #init IK handle display size
		

	def chk002(self, state=None):
		'''Scale IK/FK
		'''
		self.sb.toggleWidgets(setUnChecked='chk000-1')
		self.sb.rigging.tb000.ctxMenu.setValue(pm.jointDisplayScale(query=1, ikfk=1)) #init IKFK display size


	def s000(self, value=None):
		'''Scale Joint/IK/FK
		'''
		value = self.sb.rigging.tb000.ctxMenu.value()

		if self.sb.rigging.chk000.isChecked():
			pm.jointDisplayScale(value) #set global joint display size
		elif self.sb.rigging.chk001.isChecked():
			pm.ikHandleDisplayScale(value) #set global IK handle display size
		else: #self.sb.rigging.chk002.isChecked():
			pm.jointDisplayScale(value, ikfk=1) #set global IKFK display size


	def tb000(self, state=None):
		'''Toggle Display Local Rotation Axes
		'''
		tb = self.sb.rigging.tb000

		joints = pm.ls(type="joint") #get all scene joints

		state = pm.toggle(joints[0], query=1, localAxis=1)
		if tb.ctxMenu.isChecked():
			if not state:
				toggle=True
		else:
			if state:
				toggle=True

		if toggle:
			pm.toggle(joints, localAxis=1) #set display off

		mtk.viewportMessage("Display Local Rotation Axes:<hl>"+str(state)+"</hl>")


	def tb001(self, state=None):
		'''Orient Joints
		'''
		tb = self.sb.rigging.tb001

		orientJoint = 'xyz' #orient joints
		alignWorld = tb.ctxMenu.chk003.isChecked()
		if alignWorld:
			orientJoint = 'none' #orient joint to world

		pm.joint(edit=1, orientJoint=orientJoint, zeroScaleOrient=1, ch=1)


	def tb002(self, state=None):
		'''Constraint: Parent
		'''
		tb = self.sb.rigging.tb002

		template = tb.ctxMenu.chk004.isChecked()

		objects = pm.ls(sl=1, objectsOnly=1)

		for obj in objects[:-1]:
			pm.parentConstraint(obj, objects[:-1], maintainOffset=1, weight=1)

			if template:
				if not pm.toggle(obj, template=1, query=1):
					pm.toggle(obj, template=1, query=1)


	@mtk.undo
	def tb003(self, state=None):
		'''Create Locator at Selection
		'''
		tb = self.sb.rigging.tb003

		grpSuffix = tb.ctxMenu.t002.text()
		locSuffix = tb.ctxMenu.t000.text()
		objSuffix = tb.ctxMenu.t001.text()
		parent = tb.ctxMenu.chk006.isChecked()
		freezeTransforms = tb.ctxMenu.chk010.isChecked()
		bakeChildPivot = tb.ctxMenu.chk011.isChecked()
		scale = tb.ctxMenu.s001.value()
		stripDigits = tb.ctxMenu.chk005.isChecked()
		stripSuffix = tb.ctxMenu.chk016.isChecked()
		lockTranslate = tb.ctxMenu.chk007.isChecked()
		lockRotation = tb.ctxMenu.chk008.isChecked()
		lockScale = tb.ctxMenu.chk009.isChecked()

		selection = pm.ls(selection=True)
		if not selection:
			return Rig.createLocator(scale=scale)

		Rig.createLocatorAtObject(selection, 
			parent=parent, freezeTransforms=freezeTransforms, bakeChildPivot=bakeChildPivot, scale=scale, 
			grpSuffix=grpSuffix, locSuffix=locSuffix, objSuffix=objSuffix, stripDigits=stripDigits, stripSuffix=stripSuffix, 
			lockTranslate=lockTranslate, lockRotation=lockRotation, lockScale=lockScale
		)


	def tb004(self, state=None):
		'''Lock/Unlock Attributes
		'''
		tb = self.sb.rigging.tb004

		lockTranslate = tb.ctxMenu.chk012.isChecked()
		lockRotation = tb.ctxMenu.chk013.isChecked()
		lockScale = tb.ctxMenu.chk014.isChecked()

		sel = pm.ls(sl=True)
		Rig.setAttrLockState(sel, translate=lockTranslate, rotate=lockRotation, scale=lockScale)


	@Slots.hideMain
	def b000(self):
		'''Object Transform Limit Attributes
		'''
		node = pm.ls(sl=1, objectsOnly=1)
		if not node:
			self.sb.messageBox('Operation requires a single selected object.')
			return

		params = ['enableTranslationX','translationX','enableTranslationY','translationY','enableTranslationZ','translationZ',
			'enableRotationX','rotationX','enableRotationY','rotationY','enableRotationZ','rotationZ',
			'enableScaleX','scaleX','enableScaleY','scaleY','enableScaleZ','scaleZ']

		attrs = mtk.getParameterValuesMEL(node, 'transformLimits', params)
		self.setAttributeWindow(node, fn=Slots_maya.setParameterValuesMEL, fn_args='transformLimits', **attrs)


	def b001(self):
		'''Connect Joints
		'''
		pm.connectJoint(cm=1)


	def b002(self):
		'''Insert Joint Tool
		'''
		pm.setToolTo('insertJointContext') #insert joint tool


	def b003(self):
		'''Remove Locator
		'''
		selection = pm.ls(selection=True)
		Rig.removeLocator(selection)


	def b004(self):
		'''Reroot
		'''
		pm.reroot() #re-root joints


	def b006(self):
		'''Constraint: Point
		'''
		pm.pointConstraint(offset=[0,0,0], weight=1)


	def b007(self):
		'''Constraint: Scale
		'''
		pm.scaleConstraint(offset=[1,1,1], weight=1)


	def b008(self):
		'''Constraint: Orient
		'''
		pm.orientConstraint(offset=[0,0,0], weight=1)


	def b009(self):
		'''Constraint: Aim
		'''
		pm.aimConstraint(offset=[0,0,0], weight=1, aimVector=[1,0,0], upVector=[0,1,0], worldUpType="vector", worldUpVector=[0,1,0])


	def b010(self):
		'''Constraint: Pole Vector
		'''
		pm.orientConstraint(offset=[0,0,0], weight=1)









#module name
print (__name__)
# --------------------------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------------------------


#deprecated:

# def createLocatorAtSelection(suffix='_LOC', stripDigits=False, strip='', scale=1, parent=False, freezeChildTransforms=False, bakeChildPivot=False, lockTranslate=False, lockRotation=False, lockScale=False, _fullPath=False):
# 	'''Create locators with the same transforms as any selected object(s).
# 	If there are vertices selected it will create a locator at the center of the selected vertices bounding box.

# 	Parameters:
# 		suffix (str): A string appended to the end of the created locators name. (default: '_LOC') '_LOC#'
# 		stripDigits (bool): Strip numeric characters from the string. If the resulting name is not unique, maya will append a trailing digit. (default=False)
# 		strip (str): Strip a specific character set from the locator name. The locators name is based off of the selected objects name. (default=None)
# 		scale (float) = The scale of the locator. (default=1)
# 		parent (bool): Parent to object to the locator. (default=False)
# 		freezeChildTransforms (bool): Freeze transforms on the child object. (Valid only with parent flag) (default=False)
# 		bakeChildPivot (bool): Bake pivot positions on the child object. (Valid only with parent flag) (default=False)
# 		lockTranslate (bool): Lock the translate values of the child object. (default=False)
# 		lockRotation (bool): Lock the rotation values of the child object. (default=False)
# 		lockScale (bool): Lock the scale values of the child object. (default=False)
# 		_fullPath (bool): Internal use only (recursion). Use full path names for Dag objects. This can prevent naming conflicts when creating the locator. (default=False)

# 	Example:
# 		createLocatorAtSelection(strip='_GEO', suffix='', stripDigits=True, scale=10, parent=True, lockTranslate=True, lockRotation=True)
# 	'''
# 	import pymel.core as pm
# 	sel = pm.ls(selection=True, long=_fullPath, objectsOnly=True)
# 	sel_verts = pm.filterExpand(sm=31)

# 	if not sel:
# 		error = '# Error: Nothing Selected. #'
# 		print (error)
# 		return error

# 	def _formatName(name, stripDigits=stripDigits, strip=strip, suffix=suffix):
# 		if stripDigits:
# 			name_ = ''.join([i for i in name if not i.isdigit()])	
# 		return name_.replace(strip, '')+suffix

# 	def _parent(obj, loc, parent=parent, freezeChildTransforms=freezeChildTransforms, bakeChildPivot=bakeChildPivot):
# 		if parent: #parent
# 			if freezeChildTransforms:
# 				pm.makeIdentity(obj, apply=True, t=1, r=1, s=1, normal=2) #normal parameter: 1=the normals on polygonal objects will be frozen. 2=the normals on polygonal objects will be frozen only if its a non-rigid transformation matrix.
# 			if bakeChildPivot:
# 				pm.select(obj); pm.mel.BakeCustomPivot() #bake pivot on child object.
# 			objParent = pm.listRelatives(obj, parent=1)
# 			pm.parent(obj, loc)
# 			pm.parent(loc, objParent)

# 	def _lockChildAttributes(obj, lockTranslate=lockTranslate, lockRotation=lockRotation, lockScale=lockScale):
# 		try: #split in case of long name to get the obj attribute.  ex. 'f15e_door_61_bellcrank|Bolt_GEO.tx' to: Bolt_GEO.tx
# 			setAttrs = lambda attrs: [pm.setAttr('{}.{}'.format(obj.split('|')[-1], attr), lock=True) for attr in attrs]
# 		except: #if obj is type object:
# 			setAttrs = lambda attrs: [pm.setAttr('{}.{}'.format(obj, attr), lock=True) for attr in attrs]

# 		if lockTranslate: #lock translation values
# 			setAttrs(('tx','ty','tz'))

# 		if lockRotation: #lock rotation values
# 			setAttrs(('rx','ry','rz'))
				
# 		if lockScale: #lock scale values
# 			setAttrs(('sx','sy','sz'))

# 	_fullPath = lambda: self.createLocatorAtSelection(suffix=suffix, stripDigits=stripDigits, 
# 				strip=strip, parent=parent, scale=scale, _fullPath=True, 
# 				lockTranslate=lockTranslate, lockRotation=lockRotation, lockScale=lockScale)

# 	if sel_verts: #vertex selection

# 		objName = sel_verts[0].split('.')[0]
# 		locName = _formatName(objName, stripDigits, strip, suffix)

# 		loc = pm.spaceLocator(name=locName)
# 		if not any([loc, _fullPath]): #if locator creation fails; try again using the objects full path name.
# 			_fullPath()

# 		pm.scale(scale, scale, scale)

# 		bb = pm.exactWorldBoundingBox(sel_verts)
# 		pos = ((bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2, (bb[2] + bb[5]) / 2)
# 		pm.move(pos[0], pos[1], pos[2], loc)

# 		_parent(objName, loc)
# 		_lockChildAttributes(objName)

# 	else: #object selection
# 		for obj in sel:

# 			objName = obj.name()
# 			locName = _formatName(objName, stripDigits, strip, suffix)

# 			loc = pm.spaceLocator(name=locName)
# 			if not any([loc, _fullPath]): #if locator creation fails; try again using the objects fullpath name.
# 				_fullPath()

# 			pm.scale(scale, scale, scale)

# 			tempConst = pm.parentConstraint(obj, loc, mo=False)
# 			pm.delete(tempConst)
# 			pm.select(clear=True)

# 			_parent(obj, loc)
# 			_lockChildAttributes(objName)


