#!/usr/bin/python3	
import	requests	
import	json
import	bs4
import re
import lxml
import pandas
import sys
import html
import time

def get_function(department,semester):											#this function gets the department and semester desired as arguments, and returns a list of data of all courses in said department and semester

	try :
		response = requests.get("https://registration.boun.edu.tr/scripts/sch.asp?donem="+str(semester)+"&kisaadi="+department[0]+"&bolum="+department[1], timeout = 15)			#get get the raw html from the url, url is constructed with department and semester strings given
	except:
		time.sleep(1)
		return get_function(department,semester)
	soup = bs4.BeautifulSoup(response.text,"html.parser")																															#pass the text file to construct a BeautifulSoup object
	bod=soup.body.find_all('table')																																					#find tags that has table in name
	if len(bod)<4:																																									#if there are less than 4, this means the page is empty, and has no class data in it
		return []																																									#so return empty list
	class_list_in_html = bod[3].find_all('tr')																																		#find tags that has 'tr' in it
	td_crop = lambda str : str[4:-6]																																				#anon fucntion to crop <td>****</td> tags
	course_code_crop = lambda str : str[-23:-16]																																	#anon funct to crop course codes from a string
	
	classes = []																																									#empty list of classes
	
	for i in range (1,len(class_list_in_html)):																																		#from 1 to the length of all tr tags(index 0 will be the header of the table)
		tds = class_list_in_html[i].find_all('td')																																	#find elements that has 'td' tags
		course_code = course_code_crop(str(tds[0]))																																	#crop the course code from index 0 of 'td' list, (it is always in the same position)
		if course_code == None or course_code == '':																																#if course code = None or '' continue (this is an empty table element, perhaps a lab section)
			continue
		term = semester																																								#term of that class is the semester given to the function always(no need to actually scrape)
		course_name = td_crop(html.unescape(str(tds[2])))																															#course name is between td brackets so crop from tds[2] and unescape from html format (&amp; -> &)
		instructor = td_crop((str(tds[5])))																																			#instructor name is between td brackets so crop the brackets
		classes.append([course_code,term, course_name, instructor])																													#make a list of [course_code,semester,course_name,instructor], append it to the classes list
	return classes																																									#classes now contains data for that semester and that course, ready to process

def input_format_to_url_format(semester) :										#this function gets a semester as argument and turns it into a format that is appopriate for the url (2017-Spring -> 2016/2017-Spring)
	
	
	split = semester.split('-')													#split string from '-' so ['Year','Semester']				
	semester_no	= ""
	first_year = 0
	if(split[1]=='Fall'):														#if it is fall semester no is 1 and first year of the url is the same as given semester
		semester_no = '1'
		first_year = int(split[0])
	elif(split[1]=='Spring'):													#if it is spring sem no is 2 and first year in the url is -1 of the given string
		semester_no = '2'
		first_year = int(split[0])-1
	elif(split[1]=='Summer'):													#same with spring but sem no is 3
		semester_no = '3'
		first_year = int(split[0])-1
	return str(first_year)+'/'+str(first_year+1)+'-'+semester_no				#return the string (year)/(year+1)-(semno)

def range_to_semester_list(start_semester,end_semester) :
	start_url = input_format_to_url_format(start_semester)											#turn both ranges from input format to url format
	end_url = input_format_to_url_format(end_semester)
	url_list = []																					#start with empty list
	current_url = start_url																			#start with the first indice
	while(current_url!=end_url) :
		url_list.append(current_url)																#append here because both indices inclusive
		num = int(current_url[-1])																	#check which semester it is
		if num != 3:
			num = num+1																				#if its not 3 just increment the semester number
			current_url = current_url[:-1]+str(num)
		else:
			first_year = int(current_url[:4])+1														#if it is 3 increasing it should change the academic year to the next one and semester to fall(1)
			current_url = str(first_year)+'/'+str(first_year+1)+'-1'								#get the year, increment by one to get the next academic year, construct the appopriate string
	
	url_list.append(current_url)																	#fencepost append, since both indices inclusive
	return url_list

def url_format_to_output_format(semester):
	semester_no = (semester[-1:])																	#pull the semester number and the year from string
	first_year = int(semester[:4])
	if semester_no == '1':																			#if its semester 1, it is Fall and year is the same
		return str(first_year)+'-Fall'									
	elif semester_no == '2':
		return str(first_year+1)+'-Spring'															#if it is semester 2, it is Spring and year is  +1
	elif semester_no == '3':
		return str(first_year+1)+'-Summer'															#if semester 3, Summer and year is +1
		
def url_semester_to_output_semester(semester_list):													
	out_semester_str = ''																			#iterate over list to find output format of each year
	for sem in semester_list:																		#then append to to the list and return the string so you have ['...2018-Fall, 2019-Spring..']
		out = url_format_to_output_format(sem)
		out_semester_str = out_semester_str+out+'; '
	return out_semester_str
		
	
def parse_list(data,semesters,department) :
	U_set = set()																					#distinct U courses offered for department
	G_set = set()																					#distinct G courses offered for department
	course_dict = {}																				# 'course_code' : ['course_name',semesters_offered_set(),distinct_instructor_set()]
	instructor_set = set()																			#distinct instructors for departments
	semesters_dict = {}																				#'semester' : [number of U for semester, number of G for semester, distinct_instructor_set for semester,distinc_grad_courses,distinct_undergrad_courses]
	for semester in semesters:
		semesters_dict.update({semester:[0,0,set(),set(),set()]})
	for data_item in data :
			if len(data_item)>0:
				course_code = data_item[0]																	#divide data to elements to work easily
				term = data_item[1]
				course_name = data_item[2]
				instructor = data_item[3]
				if not(course_code[-3]=='5'or course_code[-3]=='6' or course_code[-3]=='7'):				#if its a U class
					sem_list = semesters_dict.get(term)														#get list of the semester
					sem_list[0] = sem_list[0]+1																#increment number of U classes ofered that semester
					sem_list[2].add(instructor)																#add instructor to the list of distinc instructors that semester
					sem_list[3].add(course_code)
					semesters_dict.update({term:sem_list})													#update the dictionary
					U_set.add(course_code)																	#add course to the U courses for the department
				else :
					sem_list = semesters_dict.get(term)														# else its the same but G values are incremented instead
					sem_list[1] = sem_list[1]+1																
					sem_list[2].add(instructor)	
					sem_list[4].add(course_code)
					semesters_dict.update({term:sem_list})
					G_set.add(course_code)
				instructor_set.add(instructor)														#add instructor to the listof distinct instructors for dept
				if course_code in course_dict.keys() :
					course_values = course_dict.get(course_code)
					course_values[1].add(term)														#if course is already in the dictionary, add the semester and insturctor to the respective sets
					course_values[2].add(instructor)
					course_dict.update({course_code : course_values})
				else :
					list = [course_name, set(), set()]												#else add it to the dictionary
					list[1].add(term)
					list[2].add(instructor)
					course_dict.update({course_code : list})					
					
								#start consturcting the csv
					
	instructor_set.discard('STAFF STAFF')
	grad_undergrad = 'U'+str(len(U_set))+' G'+str(len(G_set))+'; ; '+ ug_values(semesters_dict)			# append to U# G# under the course code column
	
	top_row = department[0]+'('+department[2]+'); ' +grad_undergrad+str(len(instructor_set))			#construct the top row of the department's table (ex: 'CMPE(Computer Engineering), U5 G2,..... U22, G13, I8)
	lines = []																							#lines for the table
	for course in course_dict.keys():																	#for each course in the dictionary,
		course_list = course_dict.get(course)															#get the data
		course_list[2].discard('STAFF STAFF')															#remove 'STAFF STAFF' if it exist from the instructor set
		course_row = ' ; '+course+'; '+course_list[0]+'; '+x_string(course_list[1],url_format_to_output_format(semesters[0]),url_format_to_output_format(semesters[-1]))+str(len(course_list[1]))+'/'+str(len(course_list[2]))	#consturct string for the course (ex: ',CMPE150, Inro to Computer Engineering, x, x, x... , 3/7'
		lines.append(course_row)																		#append the string to the lines list
	code = lambda elem : elem[2:9]																		#anon function to return course codes from the line string
	lines.sort(key=code)																				#sort the lines list by the course codes
	lines.insert(0,top_row)																				#insert the top row to the start of list
	
	return lines																						#return lines to print

def ug_values(semesters_dict) :																		#function to consturct ug string for each semester																			
	strLarge = ''																					#empty string
	U_final = 0																						#U value for all the semesters
	G_final = 0																						#G value for all
	for semester in semesters_dict.keys():															#for all semesters in the dict
		sem_list = semesters_dict.get(semester)														# get the list
		sem_list[2].discard('STAFF STAFF')															#remove 'STAFF STAFF' from the instructors for that semester
		u = len(sem_list[3])																		#u is the index 0
		g = len(sem_list[4])																		#g is index 1
		U_final = U_final+ u																		#increase the final value by the values of this semester
		G_final = G_final+ g
		i = len(sem_list[2])																		#I for the semester is length of the instructor list
		strC = 'U'+str(u)+' G'+str(g)+' I'+str(i)+'; '												#append U(value_of_u) G(value_of_g) I(value_of_i), to the string
		strLarge = strLarge+(strC)
	return strLarge+'U'+str(U_final)+' G'+str(G_final)+' I'											#return the string after the run of the loop + U(final) G(final) I(value of that is appended out of the function)

def x_string(semester_set,start_semester,end_semester):												# construct 'x,x,' portion of the string for the semester given, for the range of semesters given
	string = ''
	for current_semester in range_to_semester_list(start_semester,end_semester):					#for each semster in the list
		if current_semester in semester_set:														#if it exist in the set of given semesters
			atom = 'x; '																			#add an 'X,'
		else: atom = '; '																			#or an empty string otherwise ' ,'
		string = string+atom	
	return string																					#return the string consturcted

def main(argv):
	
	semesters = range_to_semester_list(argv[1],argv[2])												#find list of semesters in the format of url
	 
	departments = [	['AD','MANAGEMENT','Management'],['ASIA','ASIAN+STUDIES','Asian Studies'],['ASIA','ASIAN+STUDIES+WITH+THESIS','Asian Studies With Thesis'],
 					['ATA','ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY','Ataturk Institute For Modern Turkish History'],['AUTO','AUTOMOTIVE+ENGINEERING','Automotive Engineering'],
			    	['BIO','MOLECULAR+BIOLOGY+%26+GENETICS','Molecular Biology&Genetics'],
					['BIS','BUSINESS+INFORMATION+SYSTEMS','Business Information Systems'],
					['BM','BIOMEDICAL+ENGINEERING','Biomedical Engineering'],
					['CCS','CRITICAL+AND+CULTURAL+STUDIES','Critical and Cultural Studies'],
					['CE','CIVIL+ENGINEERING','Civil Enginerring'],
					['CEM','CONSTRUCTION+ENGINEERING+AND+MANAGEMENT','Constrction Engineering and Management'],
					['CET','COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY','Computer Education&Educational Technology'],
					['CET','EDUCATIONAL+TECHNOLOGY','Educational Technology'],
					['CHE','CHEMICAL+ENGINEERING','Chemical Engineering'],
					['CHEM','CHEMISTRY','Chemistry'],
					['CMPE','COMPUTER+ENGINEERING','Computer Engineering'],
					['COGS','COGNITIVE+SCIENCE','Cognitive Science'],
					['CSE','COMPUTATIONAL+SCIENCE+%26+ENGINEERING','Computational Science&Engineering'],
					['EC','ECONOMICS','Economics'],
					['ED','EDUCATIONAL+SCIENCES','Educational Sciences'],
					['EE','ELECTRICAL+%26+ELECTRONICS+ENGINEERING','Electrical&Electronics Engineering'],
					['EF','ECONOMICS+AND+FINANCE','Economics and Finance'],
					['ENV','ENVIRONMENTAL+SCIENCES','Enviromental Sciences'],
					['ENVT','ENVIRONMENTAL+TECHNOLOGY','Enviromental Technology'],
					['EQE','EARTHQUAKE+ENGINEERING','Earthquake Engineering'],
					['ETM','ENGINEERING+AND+TECHNOLOGY+MANAGEMENT','Engineering and Technology Management'],
					['FE','FINANCIAL+ENGINEERING','Financial Engineering'],
					['FLED','FOREIGN+LANGUAGE+EDUCATION','Foreign Language Education'],
					['GED','GEODESY','Geodesy'],
					['GPH','GEOPHYSICS','Geophysics'],
					['GUID','GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING','Guidance&Psychological Counseling'],
					['HIST','HISTORY','History'],
					['HUM','HUMANITIES+COURSES+COORDINATOR','Humanities Courses Coordinator'],
					['IE','INDUSTRIAL+ENGINEERING','Industrial Engineering'],
					['INCT','INTERNATIONAL+COMPETITION+AND+TRADE','International Competition and Trade'],
					['INT','CONFERENCE+INTERPRETING','Conference Interpreting'],
					['INTT','INTERNATIONAL+TRADE','International Trade'],
					['INTT','INTERNATIONAL+TRADE+MANAGEMENT','International Trade Management'],
					['LING','LINGUISTICS','Linguistics'],
					['LL','WESTERN+LANGUAGES+%26+LITERATURES','Western Languages&Literatures'],
					['LS','LEARNING+SCIENCES','Learning Sciences'],
					['MATH','MATHEMATICS','Mathematics'],
					['ME','MECHANICAL+ENGINEERING','Mechanical Engineering'],
					['MECA','MECHATRONICS+ENGINEERING','Mechatronics Engineering'],
					['MIR','INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST','International Relations/Turkey/Europe and the Middle East'],
					['MIR','INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS','International Relations/Turkey/Europe and the Middle East with Thesis'],
					['MIS','MANAGEMENT+INFORMATION+SYSTEMS','Management Information Systems'],
					['PA','FINE+ARTS','Fine Arts'],
					['PE','PHYSICAL+EDUCATION','Physical Education'],
					['PHIL','PHILOSOPHY','Philosophy'],
					['PHYS','PHYSICS','Physics'],
					['POLS','POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS','Political Science&International Relations'],
					['PRED','PRIMARY+EDUCATION','Primary Education'],
					['PSY','PSYCHOLOGY','Psychology'],
					['SCED','MATHEMATICS+AND+SCIENCE+EDUCATION','Mathematics and Science Education'],
					['SCED','SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION','Secondary School Science And Mathematics Education'],
					['SCO','SYSTEMS+%26+CONTROL+ENGINEERING','Systems&Control Engineering'],
					['SOC','SOCIOLOGY','Sociology'],
					['SPL','SOCIAL+POLICY+WITH+THESIS','Social Policy With Thesis'],
					['SWE','SOFTWARE+ENGINEERING','Software Engineering'],
					['SWE','SOFTWARE+ENGINEERING+WITH+THESIS','Software Engineering Thesis'],
					['TK','TURKISH+COURSES+COORDINATOR','Turkish Courses Coordinator'],
					['TKL','TURKISH+LANGUAGE+%26+LITERATURE','Turkish Language&Litearature'],
					['TR','TRANSLATION+AND+INTERPRETING+STUDIES','Translation and Interpreting Studies'],
					['TRM','SUSTAINABLE+TOURISM+MANAGEMENT','Sustainable Tourism Management'],
					['TRM','TOURISM+ADMINISTRATION','Tourism Administration'],
					['WTR','TRANSLATION','Translation'],
					['XMBA','EXECUTIVE+MBA','Executive MBA'],
					['YADYOK','SCHOOL+OF+FOREIGN+LANGUAGES','School of Foreign Languages']
				  ]
					 
	department_data = []																			#list of courses in each department
	for department in departments :																	#for each department
		data = []
		for semester in semesters :																	#for each semester
			this_data = get_function(department,semester)											#get the list of classes
			data = data+this_data																	#merge with the other semestersfor department
		department_data.append(data)																#append whole departments list to the big list
	
	
	
	
	semesters_str = url_semester_to_output_semester(semesters)										#get the string of semester from the list given (eg: ' 2018-Fall, 2019-Spring,...'
	
	top_of_table =  'Dept./Prog. (name); Course Code; Course Name; '+semesters_str+'Total Offerings'	#construct the top portion of the table, as a string
	print(top_of_table)																				#print the top
	
	i = 0
	for department in department_data :																#for each department in the data
		lines =	parse_list(department_data[i], semesters,departments[i])							#get the lines to be printed from that departments data, data list is ordered as well
		for line in lines:																			#print each line of the list returned by the method
			print(line)
		i = i+1																						#increment the loop index
	
if __name__ == "__main__":
	main(sys.argv)
	
	
	
						  

		
	