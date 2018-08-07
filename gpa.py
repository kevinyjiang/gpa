"""
This script is highly specific to Columbia's grade portal, don't judge me haters
"""
import sys
import os
from bs4 import BeautifulSoup

letter_to_numeric = {
	'A+' : 4.33,
	'A' : 4.00,
	'A-' : 3.67,
	'B+' : 3.33,
	'B' : 3.00,
	'B-' : 2.67,
	'C+' : 2.33,
	'C' : 2.00,
	'C-' : 1.67,
	'D+' : 1.33,
	'D' : 1.00,
	'D-' : 0.67,
	'F' : 0.00
}

def gpa(filename):
	with open(filename, 'r') as page:
		soup = BeautifulSoup(page, 'html.parser')

		courses = soup.find_all('tr', class_ = 'clsDataGridData')

		# List of pending course names
		pending_courses = []

		# Pending points (credits) and grades
		total_pending_points = 0
		total_pending_grades = 0

		# Completed points and grades
		total_points = 0
		total_grades = 0

		# Calculate current GPA from completed courses
		for course in courses:
			if len(course.contents) == 10:
				cols = course.contents
				
				# If course is worth credits (i.e. not a discussion section)
				if cols[5].contents[0].strip() != '0.00':
					course_name = cols[4].contents[0].strip()
					points = float(cols[5].contents[0].strip())

					# If grade not yet submitted, add to pending points count
					if not cols[8].contents:
						pending_courses.append((course_name, points))
						total_pending_points += points
					# Count points if course was not taken P/F (pass fail)
					elif cols[8].contents[0].strip() != 'P':
						grade = float(cols[6].contents[0].strip())
						letter_grade = cols[8].contents[0].strip()

						total_points += points
						total_grades += points*grade
		
		print('Current GPA:')
		print(round(total_grades/total_points, 2))

		# Get user input for projected grades of pending courses
		for course in pending_courses:
			projected_letter_grade = input('Projected grade for {}: '.format(course[0]))

			# Remove pending credits for P/D/F courses, since they don't affect GPA
			if projected_letter_grade == 'P':
				total_pending_points -= course[1]
			else:
				# Validate letter grade input
				while projected_letter_grade not in letter_to_numeric:
					projected_letter_grade = input('Please enter valid letter grade: ')
				total_pending_grades += course[1]*letter_to_numeric[projected_letter_grade]

		print('Projected GPA:')
		print(round((total_pending_grades+total_grades)/(total_pending_points+total_points), 2))

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage: gpa.py <grades_html>')
		sys.exit(1)

	filename = sys.argv[1]

	if os.path.isfile(filename):
		gpa(filename)
	else:
		print('{} does not exist.'.format(filename))
		sys.exit(1)