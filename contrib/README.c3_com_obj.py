I. INTRODUCTION

 The c3_com_obj package is the command line parser for C3. It was written with a
 focus on reusability for other develepors. The intent is that a
 system-administrator or programmer can add a system specific script to the c3
 tools. This document describes how to use the c3_com_obj class to achieve these
 ends.

II. GENERAL USAGE For a description of how the command line should be structured
 please see the cexec and c3-range man page. First the c3_com_obj.py file must
 be in a place that it is possible to import the package from. Either the
 package needs to be in /usr/lib/python2.1/site-packages (replace python2.1 with
 the appropriate version) or in a directory of your choosing (note: you can add
 a directory to the package search path within a python script by using
 sys.path.append( path_string) ). For two examples to follow please see both the
 cexec script and enable_cluster in the contrib directory. For most application
 modifying the cexec script is recomended as it is a general purpose script and
 is the base for most of the c3 power tools.

II. NOTES ON FOLLOWING TEXT All exceptions specific to c3 are contained in
 c3_except.py see the README for c3_except.py for inheritance hierarchy. The
 exceptions are imported into the appropriate package and are referenced from
 there. The example code from each section is continuous. If you see a variable
 name and do not know its type then look at preceding examples.

II. c3_com_obj INTERFACE

A. INITIALIZING c3_com_obj takes a string as it initial argument. this string is
 the command line to be parsed. The object that does the actual parseing is
 c3_command_line. below is an example:

	#build string from command line
	command_line_list = sys.argv[1:]
	command_line_string = ""
	for item in command_line_list: 
		command_line_string = '%s %s' % (command_line_string, item)

	#initialize c3_com_obj 
	c3_command = c3_com_obj.c3_command_line( command_line_string )

B. PHASE 1, GETTING OPTIONS There are two methods of acuiring options from the
 command line. the first is get_opt(). This methond takes no argument and
 returns a single string. It only parses the option if it begins with a "-" or
 "--". If no option is found a c3_except.end_of_option is thrown. If the option
 requires an orgument after it (for example: --file /tmp/file) then
 get_opt_string() is used. get_opt_string takes no arguments and returns a
 string from the command line. The string is delimited by spaces - that is the
 string " fa913($ --f" would return "fa913($" as it is everything between the
 spaces. A c3_except.end_of_opt_string will be thrown if there is no more of the
 command line string left and a c3_except.bad_string is thrown if for any other
 reason a string can not be resolved. Below is an example of getting two
 options.

	try: #loop untill no more options on command line
		option = c3_command.get_opt()
		while option: #option using an argument and a single and double dash 
			if (option == '-f') or (option == "--file"): 
				filename = c3_command.get_opt_string() 
			#an option without an argument and a single dash
			elif (option == '-i'):
				interactive = 1 
			else: #catch all, when an option has a correct format but no
			      #meaning print "option ", option, " is not valid"
				sys.exit()
			option = c3_command.get_opt()
	except c3_com_obj.end_of_option:
		pass

C. PHASE 2, MACHINE DEFINITIONS For a detailed description of the syntax for
 machine definitions see the c3-range(5) manpage. The method is called
 get_clusters and takes no arguments the method returns a c3_cluster_list
 object. The c3_cluster_list object contains a list of cluster names that are an
 index into a dictionary. The list of cluster names is "clusters" and the
 dictionary of nodes is "node". The get_clusters method will not throw any
 exceptions. Once a parse failure is encountered it immediatly return the
 c3_cluster_list object. This is because any text following this section is
 arbitrary. It is the arguments specific to the command being written and could
 begin with any character (there is no reason why this should fail "cexec :1-9
 3", 3 could be a command or a parse error, best to assume a command from the
 packages point of view). If no cluster name is specified then "/default" will
 be the cluster name. below is an example of usage (note: this only needs to be
 called once as it parses every cluster specified in the MACHINE DEFINITON
 section of the command line)

	#this creates a c3_cluster_list object and populates it 
	clusters = c3_com_obj.c3_cluster_list()

	clusters = c3_command.get_clusters()

D. PHASE 3, COMMAND SPECIFIC ARGUMENTS The only thing left to do at this point
 is to return the arguments specific to the command. Two functions facillitate
 doing this. If you only want a single word then the get_opt_string should be
 used. This is the same get_opt_string described in section B. If you want to
 get the rest of the string the method rest_of_string() should be used this
 returns from where the last parse failed to the end of the string. The method
 takes no arguments. below is an example of these two functions:

	source = c3_command.get_opt_string()
	target = c3_command.get_opt_string() command_to_run =
 	c3_command.rest_of_command()

E. OTHER INFORMATION While the c3_com_obj package can be used by itself its
 design was built around operating with the c3_file_obj package. The best
 example of how these two objects work together is in the cexec script. If you
 read the section where the cluster_from_file object is built you will see how
 they are meant to interact. Another good place to see the interaction is in the
 block where the command is actually run (the os.system() calls). Using the
 intersection of the two object shows which nodes need to be executed: the
 c3_file_obj tells what nodes there are physically available and the c3_com_obj
 tells which nodes the user wants to execute on.







