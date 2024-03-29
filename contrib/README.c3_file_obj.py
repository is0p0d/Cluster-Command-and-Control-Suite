I. INTRODUCTION

 The c3_file_obj package is the configuration file parser for C3. It was written
 with a focus on reusability for other develepors. The intent is that a
 system-administrator or programmer that wishes to add a system specific script
 to the c3 tools should have as easy a time as they could. This document
 describes how to use the c3_file_obj class to achieve these ends.

II. GENERAL USAGE For a description of how the configuration file should be
 structured please see the c3.conf man page. The c3_file_obj.py file must be in
 a place that it is possible to import the package from. Either the package
 needs to be in /usr/lib/python2.1/site-packages (replace python2.1 with the
 appropriate version) or in a directory of your choosing (note: you can add a
 directory to the package search path within a python script by using
 sys.path.append( path_string) ). For the two examples that follow please see
 both the cexec script and enable_cluster in the contrib directory. For most
 applications, modifying the cexec script is recomended, as it is a general
 purpose script and is the base for most of the c3 power tools.

II. NOTES ON FOLLOWING TEXT All exceptions specific to c3 are contained in
 c3_except.py see the README for c3_except.py for inheritance hierarchy. The
 exceptions are imported into the appropriate package and are referenced from
 there. The example code from each section is continuous (that is the example
 code could be extracted into one large script). If you are unsure of what a
 variable is look at preceding examples to find its declaration.

III. c3_file_obj INTERFACE

A. INITIALIZING When initializing a cluster_def object from the c3_file_obj
 package you need to pass a string containing the path to the file to parse. The
 only exceptions than can be thrown are from the standard python file class
 (namely IOError) below is an example.

	#initialize a cluster_def object
	path = "/etc/c3.conf"
	try: 
		file = c3_file_obj.cluster_def( path )
	except IOError:
		print "error opening file", path
		sys.exit()

B. STEP 1, READ BASIC CLUSTER INFORMATION In order to begin parsing a cluster
 the get_next_cluster method must be called. The first time get_next_cluster is
 called it will read the first cluster from the file. get_next_cluster takes no
 arguments and does not return any information. get_next_cluster sets internal
 variable of the cluster_def object. get_next_cluster can throw the following
 exceptions. invalid_head_node will be raised when a head node declaration
 fails. invalid_cluster_block will be raised if a { is not present to begin a
 cluster block. no_more_clusters signals the end of file. Below is an example of
 its usage. NOTE: these methods may be called anytime after get_next_cluster as
 they are parsed during that method.

	try: 
		#read first cluster typically you would loop until no_more_clusters
		#is thrown
		file.get_next_cluster() 
		#read cluster information - see below for functions
	except c3_file_obj.no_more_clusters:
		pass #done parsing the file
	except c3_file_obj.parse_error, error:
		#error in file, exiting
		print error.description
		print "Somewhere around ", error.last
		sys.exit()

C. GETTING GENERAL CLUSTER INFORMATION Some information is static for each
 cluster and read during get_next_cluster. There are several accessor functions
 for retrieving this information. get_external_head_node takes no arguments and
 returns a string containing the external interface name of the current cluster
 being read, similarly get_internal_head_node returns the internal interface
 name. if a cluster is an indirect cluster the external name is set to None, if
 only interface name is specified on a cluster both the internal and external
 names are set to the same value (if a cluster only has an internal interface
 then only a single interface name should be supplied setting both name equal).
 get_cluster_name returns the name of the current cluster being read. Two
 exceptions may get thrown if get_next_cluster has not been called before.
 no_head_node will be raised during one of the get_*_head_node calls and
 no_cluster_name can be thrown from get_cluster_name. below is an example of
 usage.

	#this should be between the two file.get_next_cluster() calls in section B.
	cluster_name = file.get_cluster_name()
	cluster_define[cluster_name] = {} 
	cluster_define[cluster_name]['external'] = file.get_external_head_node() 
	cluster_define[cluster_name]['internal'] = file.get_internal_head_node()

D. READING WHAT NODES ARE AVAILABLE get_next_node is the method used to retrieve
 node information from the file. get_next_node takes no arguments and returns a
 c3_file_obj.node_obj. node_obj consists of a string called name and a integer
 dead. Name contains the interface name listed in the configuration file and
 dead is the status of the node. A dead value of 0 means the node is online,
 non-zero entries mark the node as offline. several exceptions may be thrown
 from this method. indirect_cluster may be thrown as indirect clusters do not
 contain any node information in them. invalid_node will be raise when an
 invalid name for a node has been specified. not_in_range will be raised when an
 exclude range is outside of the noderange it is being applied to. And finally
 end_of_cluster is thrown when a } is encounterd signaling the end of the
 cluster definition block. Below is an example of useage.

	cluster_define[cluster_name['nodes'] = [] 
	#since the cluster has an external name is must be a direct cluster. 
	if cluster_define[cluster_name]['external']:
		try:
			while(1):
				node_obj = file.get_next_node() 
				cluster_define[cluster_name]['nodes'].append\
					( c3_file_obj.node_obj() ) 
				cluster_define[cluster_name]['nodes'][-1] = node_obj
	except c3_file_obj.end_of_cluster:
		pass #done reading cluster 
	except c3_file_obj.parse_error, error:
		print error.description print "Somewhere around ", error.last 
		sys.exit()

E. OTHER METHODS One other method is available. reread_file causes the
 cluster_def object to reinitialize all its internal variables and start parsing
 from the beginning of the supplied file again. The method takes no arguments
 and returns nothing.
