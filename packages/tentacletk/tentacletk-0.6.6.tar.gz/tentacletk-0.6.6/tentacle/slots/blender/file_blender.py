# !/usr/bin/python
# coding=utf-8
from tentacle.slots.blender import *
from tentacle.slots.file import File



class File_blender(File, Slots_blender):
	def __init__(self, *args, **kwargs):
		Slots_blender.__init__(self, *args, **kwargs)
		File.__init__(self, *args, **kwargs)


		cmb000 = self.sb.file.draggable_header.ctxMenu.cmb000
		items = []
		cmb000.addItems_(items, 'File Editors')

		cmb002 = self.sb.file.cmb002
		# autoSaveState = pm.autoSave(q=True, enable=True) #set the initial autosave state.
		# autoSaveInterval = pm.autoSave(q=True, int=True)
		# autoSaveAmount = pm.autoSave(q=True, maxBackups=True)
		# cmb002.ctxMenu.add('QPushButton', setObjectName='b000', setText='Open Directory', setToolTip='Open the autosave directory.') #open directory
		# cmb002.ctxMenu.add('QPushButton', setObjectName='b002', setText='Delete All', setToolTip='Delete all autosave files.') #delete all
		# cmb002.ctxMenu.add('QCheckBox', setText='Autosave', setObjectName='chk006', setChecked=autoSaveState, setToolTip='Set the autosave state as active or disabled.') #toggle autosave
		# cmb002.ctxMenu.add('QSpinBox', setPrefix='Amount: ', setObjectName='s000', setMinMax_='1-100 step1', setValue=autoSaveAmount, setHeight_=20, setToolTip='The number of autosave files to retain.') #autosave amount
		# cmb002.ctxMenu.add('QSpinBox', setPrefix='Interval: ', setObjectName='s001', setMinMax_='1-60 step1', setValue=autoSaveInterval/60, setHeight_=20, setToolTip='The autosave interval in minutes.') #autosave interval
		# cmb002.ctxMenu.chk006.toggled.connect(lambda s: pm.autoSave(enable=s, limitBackups=True))
		# cmb002.ctxMenu.s000.valueChanged.connect(lambda v: pm.autoSave(maxBackups=v, limitBackups=True))
		# cmb002.ctxMenu.s001.valueChanged.connect(lambda v: pm.autoSave(int=v*60, limitBackups=True))
		# cmb002.addItems_(self.getRecentAutosave(appendDatetime=True), 'Recent Autosave', clear=True)

		cmb003 = self.sb.file.cmb003
		cmb003.addItems_([], "Import")

		cmb004 = self.sb.file.cmb004
		items = []
		cmb004.addItems_(items, 'Export')


	def cmb000(self, index=-1):
		'''Editors
		'''
		cmb = self.sb.file.draggable_header.ctxMenu.cmb000

		if index>0:
			text = cmb.items[index]
			if text=='':
				mel.eval('') #
			if text=='':
				mel.eval('') #
			if text=='':
				mel.eval('') #
			cmb.setCurrentIndex(0)


	def cmb001(self, index=-1):
		'''Recent Projects
		'''
		cmb = self.sb.file.cmb006.ctxMenu.cmb001

		if index>0:
			pm.mel.setProject(cmb.items[index]) #mel.eval('setProject "'+items[index]+'"')
			cmb.setCurrentIndex(0)


	def cmb002(self, index=-1):
		'''Recent Autosave
		'''
		cmb = self.sb.file.cmb002

		if index>0:
			file = Slots.fileTimeStamp(cmb.items[index], detach=True)
			pm.openFile(file, open=1, force=True)
			cmb.setCurrentIndex(0)


	def cmb003(self, index=-1):
		'''Import
		'''
		cmb = self.sb.file.cmb003

		if index>0: #hide then perform operation
			self.sb.parent().hide(force=1)
			if index==1: #Import
				mel.eval('Import;')
			elif index==2: #Import options
				mel.eval('ImportOptions;')
			elif index==3: #FBX Import Presets
				mel.eval('FBXUICallBack -1 editImportPresetInNewWindow fbx;') #Fbx Presets
			elif index==4: #Obj Import Presets
				mel.eval('FBXUICallBack -1 editImportPresetInNewWindow obj;') #Obj Presets
			cmb.setCurrentIndex(0)


	def cmb004(self, index=-1):
		'''Export
		'''
		cmb = self.sb.file.cmb004

		if index>0: #hide then perform operation
			self.sb.parent().hide(force=1)
			if index==1: #Export selection
				mel.eval('ExportSelection;')
			elif index==2: #Unreal
				mel.eval('SendToUnrealSelection;')
			elif index==3: #Unity 
				mel.eval('SendToUnitySelection;')
			elif index==4: #GoZ
				mel.eval('print("GoZ"); source"C:/Users/Public/Pixologic/GoZApps/Maya/GoZBrushFromMaya.mel"; source "C:/Users/Public/Pixologic/GoZApps/Maya/GoZScript.mel";')
			elif index==5: #Send to 3dsMax: As New Scene
				mel.eval('SendAsNewScene3dsMax;') #OneClickMenuExecute ("3ds Max", "SendAsNewScene"); doMaxFlow { "sendNew","perspShape","1" };
			elif index==6: #Send to 3dsMax: Update Current
				mel.eval('UpdateCurrentScene3dsMax;') #OneClickMenuExecute ("3ds Max", "UpdateCurrentScene"); doMaxFlow { "update","perspShape","1" };
			elif index==7: #Send to 3dsMax: Add to Current
				mel.eval('AddToCurrentScene3dsMax;') #OneClickMenuExecute ("3ds Max", "AddToScene"); doMaxFlow { "add","perspShape","1" };
			elif index==8: #Export to Offline File
				mel.eval('ExportOfflineFileOptions;') #ExportOfflineFile
			elif index==9: #Export options
				mel.eval('ExportSelectionOptions;')
			elif index==10: #FBX Export Presets
				mel.eval('FBXUICallBack -1 editExportPresetInNewWindow fbx;') #Fbx Presets
			elif index==11: #Obj Export Presets
				mel.eval('FBXUICallBack -1 editExportPresetInNewWindow obj;') #Obj Presets
			cmb.setCurrentIndex(0)


	def cmb005(self, index=-1):
		'''Recent Files
		'''
		cmb = self.sb.file.cmb005

		if index>0:
			force=True; force if str(pm.mel.file(query=1, sceneName=1, shortName=1)) else not force #if sceneName prompt user to save; else force open
			pm.openFile(cmb.items[index], open=1, force=force)
			cmb.setCurrentIndex(0)


	def cmb006(self, index=-1):
		'''Project Folder
		'''
		cmb = self.sb.file.cmb006

		path = self.formatPath(pm.workspace(query=1, rd=1)) #current project path.
		items = [f for f in os.listdir(path)]

		project = self.formatPath(path, 'dir') #add current project path string to label. strip path and trailing '/'

		cmb.addItems_(items, project, clear=True)

		if index>0:
			os.startfile(path+items[index-1])
			cmb.setCurrentIndex(0)


	def tb000(self, state=None):
		'''Save
		'''
		tb = self.sb.file.draggable_header.ctxMenu.tb000

		wireframe = tb.ctxMenu.chk000.isChecked()
		increment = tb.ctxMenu.chk001.isChecked()
		quit = tb.ctxMenu.chk002.isChecked()

		if wireframe:
			pm.mel.DisplayWireframe()

		if increment:
			pm.mel.IncrementAndSave()
		else:
			filetype = 'mayaAscii' #type: mayaAscii, mayaBinary, mel, OBJ, directory, plug-in, audio, move, EPS, Adobe(R) Illustrator(R)
			pm.saveFile(force=1, preSaveScript='', postSaveScript='', type=filetype)

		if quit: #quit maya
			import time
			for timer in range(5):
				self.mtk.viewportMessage('Shutting Down:<hl>'+str(timer)+'</hl>')
				time.sleep(timer)
			pm.mel.quit() # pm.Quit()


	def lbl000(self):
		'''Set Project
		'''
		newProject = mel.eval("SetProject;")

		self.cmb006() #refresh cmb006 items to reflect new project folder


	def lbl001(self):
		'''Minimize Main Application
		'''
		mel.eval("minimizeApp;")
		self.sb.parent().hide(force=1)


	def lbl002(self):
		'''Restore Main Application
		'''
		pass


	def lbl003(self):
		'''Close Main Application
		'''
		# force=false #pymel has no attribute quit error.
		# exitcode=""
		sceneName = str(mel.eval("file -query -sceneName -shortName;")) #if sceneName prompt user to save; else force close
		mel.eval("quit;") if sceneName else mel.eval("quit -f;")
		# pm.quit (force=force, exitcode=exitcode)


	def lbl004(self):
		'''Open current project root
		'''
		dir_ = pm.workspace(query=1, rd=1) #current project path.
		os.startfile(self.formatPath(dir_))


	def b000(self):
		'''Autosave: Open Directory
		'''
		# dir1 = str(pm.workspace(query=1, rd=1))+'autosave' #current project path.
		dir2 = os.environ.get('MAYA_AUTOSAVE_FOLDER').split(';')[0] #get autosave dir path from env variable.

		try:
			# os.startfile(self.formatPath(dir1))
			os.startfile(self.formatPath(dir2))
		except FileNotFoundError as error:
			return 'Error: The system cannot find the file specified.'


	def b002(self):
		'''Autosave: Delete All
		'''
		files = self.getRecentAutosave()
		for file in files:
			try:
				os.remove(file)
			except Exception as error:
				print (error)


	def b015(self):
		'''Remove String From Object Names.
		'''
		from_ = str(self.sb.file.t000.text()) #asterisk denotes startswith*, *endswith, *contains* 
		to = str(self.sb.file.t001.text())
		replace = self.sb.file.chk004.isChecked()
		selected = self.sb.file.chk005.isChecked()

		objects = pm.ls (from_) #Stores a list of all objects starting with 'from_'
		if selected:
			objects = pm.ls (selection=1) #if use selection option; get user selected objects instead
		from_ = from_.strip('*') #strip modifier asterisk from user input

		for obj in objects:
			relatives = pm.listRelatives(obj, parent=1) #Get a list of it's direct parent
			if 'group*' in relatives: #If that parent starts with group, it came in root level and is pasted in a group, so ungroup it
				relatives[0].ungroup()

			newName = to
			if replace:
				newName = obj.replace(from_, to)
			pm.rename(obj, newName) #Rename the object with the new name


	def getRecentFiles(self, index=None):
		'''Get a list of recent files.

		Parameters:
			index (int): Return the recent file directory path at the given index. Index 0 would be the most recent file.

		Return:
			(list)(str)
		'''
		files = pm.optionVar(query='RecentFilesList')
		result = [self.formatPath(f) for f in list(reversed(files)) 
					if "Autosave" not in f] if files else []

		try:
			return result[index]
		except (IndexError, TypeError) as error:
			return result


	def getRecentProjects(self):
		'''Get a list of recently set projects.

		Return:
			(list)
		'''
		files = pm.optionVar(query='RecentProjectsList')
		result = [self.formatPath(f) for f in list(reversed(files))]

		return result


	def getRecentAutosave(self, appendDatetime=False):
		'''Get a list of autosave files.

		Parameters:
			appendDatetime (bool): Attach a modified timestamp and date to given file path(s).

		Return:
			(list)
		'''
		dir1 = str(pm.workspace(query=1, rd=1))+'autosave' #current project path.
		dir2 = os.environ.get('MAYA_AUTOSAVE_FOLDER').split(';')[0] #get autosave dir path from env variable.

		files = self.getDirContents(dir1, 'filepaths', includeFiles=('*.mb', '*.ma')) + self.getDirContents(dir2, 'filepaths', includeFiles=('*.mb', '*.ma'))
		result = [self.formatPath(f) for f in list(reversed(files))] #format and reverse the list.

		if appendDatetime:  #attach modified timestamp
			result = Slots.fileTimeStamp(result)

		return result









#module name
print (__name__)
# --------------------------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------------------------



# deprecated:


	# def tb000(self, state=None):
	# 	'''
	# 	Save
	# 	'''
	# 	tb = self.sb.file.tb000
	# 	if state=='setMenu':
	# 		tb.ctxMenu.add('QCheckBox', setText='ASCII', setObjectName='chk003', setChecked=True, setToolTip='Toggle ASCII or binary file type.')
	# 		tb.ctxMenu.add('QCheckBox', setText='Wireframe', setObjectName='chk000', setChecked=True, setToolTip='Set view to wireframe before save.')
	# 		tb.ctxMenu.add('QCheckBox', setText='Increment', setObjectName='chk001', setChecked=True, setToolTip='Append and increment a unique integer value.')
	# 		tb.ctxMenu.add('QCheckBox', setText='Quit', setObjectName='chk002', setToolTip='Quit after save.')
	# 		return

	# 	increment = tb.ctxMenu.chk001.isChecked()
	# 	ASCII = tb.ctxMenu.chk003.isChecked()
	# 	wireframe = tb.ctxMenu.chk000.isChecked()
	# 	quit = tb.ctxMenu.chk002.isChecked()

	# 	preSaveScript = ''
	# 	postSaveScript = ''

	# 	type_ = 'mayaBinary'
	# 	if ASCII: #toggle ascii/ binary
	# 		type_ = 'mayaAscii' #type: mayaAscii, mayaBinary, mel, OBJ, directory, plug-in, audio, move, EPS, Adobe(R) Illustrator(R)

	# 	if wireframe:
	# 		mel.eval('DisplayWireframe;')

	# 	#get scene name and file path
	# 	fullPath = str(mel.eval('file -query -sceneName;')) #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.blender/elise_mid.009.mb
	# 	index = fullPath.rfind('/')+1
	# 	curFullName = fullPath[index:] #ie. elise_mid.009.mb
	# 	path = fullPath[:index] #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.blender/

	# 	if increment: #increment filename
	# 		newName = self.incrementFileName(curFullName)
	# 		self.deletePreviousFiles(curFullName, path)
	# 		pm.saveAs (path+newName, force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
	# 		print('{0} {1}'.format('Result:', path+newName))
	# 	else:	#save without renaming
	# 		pm.saveFile (force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
	# 		print('{0} {1}'.format('Result:', path+currentName,))

	# 	if quit: #quit maya
	# 		import time
	# 		for timer in range(5):
	# 			self.mtk.viewportMessage('Shutting Down:<hl>'+str(timer)+'</hl>')
	# 			time.sleep(timer)
	# 		mel.eval("quit;")
	# 		# pm.Quit()


	# @staticmethod
	# def incrementFileName(fileName):
	# 	'''
	# 	Increment the given file name.

	# 	Parameters:
	# 		fileName (str): file name with extension. ie. elise_mid.ma

	# 	Return:
	# 		(str) incremented name. ie. elise_mid.000.ma
	# 	'''
	# 	import re

	# 	#remove filetype extention
	# 	currentName = fileName[:fileName.rfind('.')] #name without extension ie. elise_mid.009 from elise_mid.009.mb
	# 	#get file number
	# 	numExt = re.search(r'\d+$', currentName) #check if the last chars are numberic
	# 	if numExt is not None:
	# 		name = currentName[:currentName.rfind('.')] #strip off the number ie. elise_mid from elise_mid.009
	# 		num = int(numExt.group())+1 #get file number and add 1 ie. 9 becomes 10
	# 		prefix = '000'[:-len(str(num))]+str(num) #prefix '000' removing zeros according to num length ie. 009 becomes 010
	# 		newName = name+'.'+prefix #ie. elise_mid.010
			
	# 	else:
	# 		newName = currentName+'.001'

	# 	return newName


	# @staticmethod
	# def deletePreviousFiles(fileName, path, numberOfPreviousFiles=5):
	# 	'''
	# 	Delete older files.

	# 	Parameters:
	# 		fileName (str): file name with extension. ie. elise_mid.ma
	# 		numberOfPreviousFiles (int): Number of previous copies to keep.
	# 	'''
	# 	import re, os

	# 	#remove filetype extention
	# 	currentName = fileName[:fileName.rfind('.')] #name without extension ie. elise_mid.009 from elise_mid.009.mb
	# 	#get file number
	# 	numExt = re.search(r'\d+$', currentName) #check if the last chars are numberic
	# 	if numExt is not None:
	# 		name = currentName[:currentName.rfind('.')] #strip off the number ie. elise_mid from elise_mid.009
	# 		num = int(numExt.group())+1 #get file number and add 1 ie. 9 becomes 10

	# 		oldNum = num-numberOfPreviousFiles
	# 		oldPrefix = '000'[:-len(str(oldNum))]+str(oldNum) #prefix the appropriate amount of zeros in front of the old number
	# 		oldName = name+'.'+oldPrefix #ie. elise_mid.007
	# 		try: #search recursively through the project folder and delete any old folders with the old filename
	# 			dir_ =  os.path.abspath(os.path.join(path, "../.."))
	# 			for root, directories, files in os.walk(dir_):
	# 				for filename in files:
	# 					if all([filename==oldName+ext for ext in ('.ma','.ma.swatches','.mb','.mb.swatches')]):
	# 						try:
	# 							import os
	# 							os.remove(filename)
	# 						except:
	# 							pass
	# 		except OSError:
	# 			print('{0} {1}'.format('Error: Could not delete', path+oldName))
	# 			pass