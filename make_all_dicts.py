"""
currently, only the JIS to UTF8 dictionary exists for hiragana. 
The goal of this script is to make a JIS to UTF8 dictionary for each character based on radicals.
This script takes no inputs, but yields the following output:

{"hiragana": {jis:utf16,jis:utf16},
"katakana": {jis:utf16,jis:utf16},
radical1: {jis:utf16,jis:utf16},
radical2: {jis:utf16,jis:utf16},
....,
}

where radical1 and radical2 are substituted names for 
actual UTF16strings representing radicals in the radkfile.

This will give sets of images to train nets on such that 
can have lower dimensional sets can be used to train on 
data and then output predictions for each radical
"""
import pickle
import codecs
import json
with open(file = 'radkfile', encoding = 'euc_jp') as radkstream:
	radkstring = radkstream.read()
start_parsing = False
radical_map = {}
current_rad = ''
current_rad_list = []
radklines = radkstring.splitlines()
for line in radklines:
	if(not start_parsing and line[0] == '$'):
		start_parsing = True
	if (start_parsing):
		#adds all kanji with current radical present
		if (line[0] != '$'):
			for rad in line:
				current_rad_list.append(rad)
		#update radical if necessary
		else:
			if current_rad != '':
				radical_map.update({current_rad : current_rad_list})
			current_rad_list = []
			current_rad = line[2]
			#adds a radical to a stroke_list iff it belongs in the stroke_list
			#adds a completed stroke_list to the stroke_map
#taking care of tail end of generation
radical_map.update({current_rad : current_rad_list})	
with open('radicalMap', 'w') as outfile:
	json.dump(radical_map, outfile)

#now to trim off all \u
with open('radicalMap', 'r') as trimfile:
	s = trimfile.read()
new_s = s.replace("\\u","")
with open('radicalMap', 'w') as outfile:
	outfile.write(new_s)

with open('radicalMap') as f:
	radical_map = json.load(f)
#TODO make the dictionary. kanji and hiragana will have to be done manually
utf_jis = {}
with open('All JIS codes','r', encoding ='utf-8') as charcodefile:
	lines = charcodefile.readlines()
for line in lines[1:]:
	#0,1 not useful
	#2 = jis
	#6 = UTF16
	#7 = char
	line = line.split()
	utf_jis.update({line[6]:line[2]})
save_dic= {} #this is the outputted dictionary
for rad in radical_map:
	rad_map = {}
	for k in radical_map[rad]:
		if k in utf_jis:
			rad_map.update({utf_jis[k]:k})
			print("success")
		else:
			print(k)
	save_dic.update({rad:rad_map})
print(utf_jis)