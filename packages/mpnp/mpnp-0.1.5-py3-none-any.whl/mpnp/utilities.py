#coding=utf-8
from datetime import datetime
import platform
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import csv











def create_readme( author = '', msg = '', folder = './', authorization_header = True ):


	writer = open( folder + 'README.txt', 'w' )
	separator = '-----------------------------------\n\n\n'

	text = ''
	line = ''

	line = 'Author: ' + author + '\n'
	writer.write( line )
	text += line

	now = datetime.now()
	line = now.strftime( '%d/%m/%Y %H:%M:%S' ) + '\n\n'
	writer.write( line )
	text += line

	if authorization_header == True: 
		line = 'This project can not be used without its author\'s full and express authorization.\n'
		writer.write( line )
		text += line

	writer.write( separator )
	text += separator

	
	if msg != '':
		
		line = msg + '\n'
		writer.write( line )
		text += line

		writer.write( separator )
		text += separator


	line = 'System: ' + platform.system() + '\n'
	writer.write( line )
	text += line

	line = 'Processor: ' + platform.processor() + '\n'
	writer.write( line )
	text += line

	line = 'Python Version: ' + platform.python_version() + '\n'
	writer.write( line )
	text += line

	line = 'Python Implementation: ' + platform.python_implementation() + '\n'
	writer.write( line )
	text += line

	writer.write( separator )
	text += separator


	line = 'Python Packages (pip freeze):\n\n'
	writer.write( line )
	text += line

	try:
	    from pip._internal.operations import freeze
	except ImportError:  # pip < 10.0
	    from pip.operations import freeze

	for p in freeze.freeze():

		line = p  + '\n'
		writer.write( line )
		text += line


	writer.write( separator )
	text += separator


	writer.close()


	print( text )











def txtfiles_comparator( folder = './', extension = None, threshold = 0.95, hide_file_name = False ):

	# https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents


	documents = []
	header = [ ]
	count = 1
	meta_data = []


	for path, subdirs, files in os.walk(folder):
	    for name in files:

	    	add = True
	    	if ( extension is not None ):
	    		if( name.split('.')[ -1 ].lower() != extension.lower() ): add = False

	    	if add == True:

		    	file = os.path.join( path, name )

		    	header.append( 'f' + str(count) )
		    	meta_data.append( [ count, file ] )
		    	documents.append( open( file, errors = 'ignore' ).read()  )

		    	count = count + 1


	tfidf = TfidfVectorizer().fit_transform( documents )
	pairwise_similarity = tfidf * tfidf.T


	files_similarity_matrix = pairwise_similarity.toarray()
	np.fill_diagonal( files_similarity_matrix, 0 )


	meta_data = np.array( meta_data )


	with open( 'files_similarity_matrix-meta_data.csv', 'w' ) as csvfile:
		writer = csv.writer( csvfile, delimiter = ';' )
		writer.writerows( meta_data )
		csvfile.close()

	
	with open( 'files_similarity_matrix.csv', 'w' ) as csvfile:
		writer = csv.writer( csvfile, delimiter = ';' )

		
		row = [ '-' ]

		if hide_file_name == True:
			row.extend( header )
			rows_labels = np.array( [ header ] )
		else: 
			row.extend( meta_data[ :, 1 ].tolist() )
			rows_labels = np.array( [ meta_data[ :, 1 ] ] )

		writer.writerow( row )
		
		
		data = np.hstack( ( rows_labels.T, files_similarity_matrix ) )
		
		writer.writerows( data )
		csvfile.close()

	
	with open( 'files_similarity_matrix-above_threshold.csv', 'w' ) as csvfile:
		writer = csv.writer( csvfile, delimiter = ';' )

		indexes = np.argwhere( files_similarity_matrix >= threshold )

		for i in range( indexes.shape[ 0 ] ):
			
			if hide_file_name == True:
				writer.writerow( [ header[ indexes[ i, 0 ] ], header[ indexes[ i, 1 ] ], files_similarity_matrix[ indexes[ i, 0 ], indexes[ i, 1 ] ] ] )
			else:
				writer.writerow( [ meta_data[ indexes[ i, 0 ], 1 ], meta_data[ indexes[ i, 1 ], 1 ], files_similarity_matrix[ indexes[ i, 0 ], indexes[ i, 1 ] ] ] )

		csvfile.close()