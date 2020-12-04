import lxml.etree as ET
from pathlib import Path
import os
import json
import sys

#####################################################
# This creates the files and folders in the current #
# working directory. Please remember to encase your #
# path to the mpackage or XML in quotation marks.   #
#####################################################

# To do:
# 		allow path to be specified?
#		account for MUDLET folders!... don't know how they look in XML, though

class Directory_Maker:
	def __init__(self, filepath):
		self.__filename = filepath[filepath.rindex("\\")+1:]
		self.__filename = self.__filename[:self.__filename.rindex(".")]
		cwd = os.path.abspath(os.getcwd())
		if filepath.endswith(".mpackage"):
			print("Now attempting to unzip the mpackage.")
			try:
				import zipfile
				with zipfile.ZipFile(filepath, 'r') as zip_ref:
					zip_ref.extractall(cwd+"\\"+self.__filename+"\\unzipped\\")
				Directory_Maker(cwd+"\\"+self.__filename+"\\unzipped\\"+self.__filename+".xml")
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
			f_tag_path = filepath[:filepath.rindex(".xml")]+"\\"+f_tag
			Path(f_tag_path).mkdir(parents=True, exist_ok=True)
			for subelement in root[toplevel_tags.index(tag)]:
				try:
					d = {}
					for subsub in subelement:
						if subsub.tag != "script":
							d[subsub.tag] = subsub.text
						else:
							# CREATE code.lua FILE HERE
							code = open(f_tag_path+"\\code.lua", "w")
							code.write(subsub.text)
							code.close()
					# Once the dictionary is made...
					json_string = json.dumps(d)
					json_file = open(f_tag_path+"\\"+f_tag+".json", "w")
					json_file.write(json_string)
					json_file.close()
				except:
					pass
				



if __name__ == "__main__":
	Directory_Maker(sys.argv[1])
