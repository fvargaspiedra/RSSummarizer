import difflib
import os
import re

# Return a dictionary of RSS sources with a list
# of the downloaded XMLs for each source.
def find_files(target_directory):
	# Read all the RSS feed XML files
	files = os.listdir(target_directory)
	filtered_files = {}

	# Iterate over the files and return a dictionary of
	# unique RSS feed sources with a list of different
	# versions of the downloaded XMLs.
	for target_file in files:
		suffix_index = target_file.rfind("_")
		filename = target_file[:suffix_index]
		files_list = []

		if filename in filtered_files:
			files_list = filtered_files[filename]

		files_list.append(target_directory + target_file);
		filtered_files[filename] = files_list

	return filtered_files

# Compare different downloaded XMLs from the same RSS feed source
# and list only the ones that have changed.
def diff_files(files):
	files_with_diff = []
	for target_file in files:
		list_of_files = files[target_file]

		# Sort the files so the oldest is on the first index
		list_of_files.sort()

		# Compare files of the same source. If there is a change add it to the list.
		# If there is only one file, then add it to the list as well.
		if len(list_of_files) > 1:
			file1 = open(list_of_files[0], "r").read().strip().splitlines()
			file2 = open(list_of_files[1], "r").read().strip().splitlines()

			diff_lines = difflib.unified_diff(file1, file2,fromfile=list_of_files[0], tofile=list_of_files[1], n=0)
			for line in diff_lines:
				for prefix in ('---', '+++', '@@'):
					if line.startswith(prefix):
						break
					elif list_of_files[1] not in files_with_diff:
						files_with_diff.append(list_of_files[1])

			print("Deleting old file " + list_of_files[0])
			os.remove(list_of_files[0])
		else:
			files_with_diff.append(list_of_files[0])

	print("Files with new feeds: ", files_with_diff)
	return files_with_diff

# Check all RSS feed XMLs and return the list of the ones that have changed
def exec_find_files(target_directory):
	files = find_files(target_directory)
	return diff_files(files)
