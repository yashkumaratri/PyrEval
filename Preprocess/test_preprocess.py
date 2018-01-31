#Preprocessing xml files from stanford corenlp 
#Copyright (C) 2017  Yanjun Gao

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import glob
import sys
from time import time
from lib_preprocessing import getRealName, CleanSegmentations, VectorizeSummary, DecomposeSummary, getRoot
from sif_embedding import SIF_master
mode = sys.argv[1]
model = sys.argv[2]
file_dir = sys.argv[3]
#mode = 2

"""
=============== MAIN ===================
"""


#summaries = [sys.argv[1]]
peer_summaries = []
wise_crowd = []
test_summaries = []
timer = time()

error_file = '../Preprocess/errors-file.txt'
errors = [] 
if int(mode) == 1:
	#dir1 = "../Preprocess/peer_summaries"
	dir1 = file_dir + "/Preprocess/peer_summaries"
	#dir1 = file_dir + "/Preprocess/peer_summaries"
	print "currently preprocessing ", dir1 
elif int(mode) == 2:
	#dir1 = "../Preprocess/wise_crowd_summaries"
	dir1 = file_dir + "/wise_crowd_summaries"
	#dir1 = file_dir + "/Preprocess/wise_crowd_summaries"
	print "currently preprocessing ", dir1 
#elif int(mode) == 3:
	#dir1 = "../Preprocess/test_summaries"
else:
	dir1 = None
	print "Option doesn't exist!!!"

if (dir1):
	summaries = sorted(list(glob.iglob(dir1+ '/*.xml')))
	for n, summary in enumerate(summaries):
		try:
			DecomposeSummary(summary, n + 1,dir1)
			summary, seg_ids = CleanSegmentations(summary, dir1,n+1)
			if int(model) == 1:
				VectorizeSummary(summary, seg_ids, dir1,n+1)
			else:
				print "SIF Modeling"
				print summary 
				clfile = summary + ".cl"
				#segf = summary[:summary.rfind(".")]
				#realname = getRealName(segf)
				SIF_master(summary,clfile,dir1,n+1)
				#VectorizeSummary(summary, seg_ids, dir1,n+1)
		except:
			print "current file failed: ", n, " ", summary
			errors.append(summary)
	
	#with open(error_file,'w') as f:
	#	for each in errors:
	#		f.write(each)
done = time()
print('Time: {}'.format(str(done - timer)))
#if int(mode) ==2:
#	command = 'mv ../Preprocess/wise_crowd_summaries ../Pyramid/wise_crowd'
#	os.system(command)

print "Finish Preprocess!!!"
