import lxml.etree as ET
from pathlib import Path
import os
import json
import sys
import platform

#####################################################
# This creates the files and folders in the current #
# working directory. Please remember to encase your #
# path to the mpackage or XML in quotation marks.   #
#####################################################

# To do:
# 		allow path to be specified?
#		account for MUDLET folders!... don't know how they look in XML, though

class Directory_Maker:
	# *filepath* should point directly to the file you're attempting to
	# unpackage - whether it's an mpackage or an XML.
	# *use_cwd* will say whether to use the the current working directory
	# of PyMuddler or to use the working directory of the file itself.
	def __init__(self, filepath, use_cwd=True):
		self.platform = platform.system()
		# This attempts to account for Linux
		if "/" in filepath:
			self.__filename = filepath[filepath.rindex("/")+1:]
		elif "\\" in filepath:
			self.__filename = filepath[filepath.rindex("\\")+1:]
		else:
			self.__filename = filepath
		self.__filename = self.__filename[:self.__filename.rindex(".")]
		if use_cwd:
			cwd = os.path.abspath(os.getcwd())
		else:
			# This also attempts to account for Linux.
			if "/" in filepath:
				cwd = filepath[:filepath.rindex("/")]
			elif "\\" in filepath:
				cwd = filepath[:filepath.rindex("\\")]
			else:
				cwd = os.path.abspath(os.getcwd())
		if filepath.endswith(".mpackage"):
			print("Now attempting to unzip the mpackage.")
			try:
				import zipfile
				if self.platform == "Windows":
					with zipfile.ZipFile(filepath, 'r') as zip_ref:
						zip_ref.extractall(cwd+"\\"+self.__filename+"\\unzipped\\")
					Directory_Maker(cwd+"\\"+self.__filename+"\\unzipped\\"+self.__filename+".xml")
				else:
					with zipfile.ZipFile(filepath, 'r') as zip_ref:
						zip_ref.extractall(cwd+"/"+self.__filename+"/unzipped/")
					Directory_Maker(cwd+"/"+self.__filename+"/unzipped/"+self.__filename+".xml")
			except Exception as e:
				print("An unexpected error occured trying to unpackage the file.")
				print(e)
		elif filepath.endswith(".xml"):
			print("Making a new directory for the files")
			Path(filepath[:filepath.rindex(".xml")]).mkdir(parents=True, exist_ok=True)
			print("OK!")
			XML_Parser(filepath)
		else:
			print("Wrong filetype.")

class XML_Parser:
	def __init__(self, filepath):
		tree = ET.parse(filepath)
		root = tree.getroot()
		toplevel_tags = [toplevel.tag for toplevel in root]
		for tag in toplevel_tags:
			f_tag = tag[:tag.index("Package")].lower()
			if platform.system() == "Windows":
				f_tag_path = filepath[:filepath.rindex(".xml")]+"\\"+f_tag
			else:
				f_tag_path = filepath[:filepath.rindex(".xml")]+"/"+f_tag
			Path(f_tag_path).mkdir(parents=True, exist_ok=True)
			for subelement in root[toplevel_tags.index(tag)]:
				try:
					d = {}
					for subsub in subelement:
						if subsub.tag != "script":
							d[subsub.tag] = subsub.text
						else:
							# CREATE code.lua FILE HERE
							if platform.system() == "Windows":
								code = open(f_tag_path+"\\code.lua", "w")
							else:
								code = open(f_tag_path+"/code.lua", "w")
							code.write(subsub.text)
							code.close()
					# Once the dictionary is made...
					json_string = json.dumps(d)
					if platform.system() == "Windows":
						json_file = open(f_tag_path+"\\"+f_tag+".json", "w")
					else:
						json_file = open(f_tag_path+"/"+f_tag+".json", "w")
					json_file.write(json_string)
					json_file.close()
				except:
					pass
				



if __name__ == "__main__":
	if len(sys.argv) == 3:
		Directory_Maker(sys.argv[1], sys.argv[2])
	else:
		Directory_Maker(sys.argv[1])
