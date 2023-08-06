from sklearn import tree
import numpy as np
import graphviz
import pydotplus











def nodelink( skl_tree, color_map_category = [ '#1f77b3', '#ff7e0e', '#bcbc21', '#8c564b', '#9367bc', '#e277c1', '#ffdb00', '#8a2844', '#00aa79', '#aa3baf', '#d89c00', '#a3a39e', '#3f69ff', '#46490c', '#7b6985', '#6b978c', '#ff9a75', '#835bff', '#7c6b46', '#80b654', '#bc0049', '#fd93ff', '#5d0018', '#89d1d1', '#9c8cd3' ], **kwargs ):

	dot_data = tree.export_graphviz( skl_tree, **kwargs )

	graph = pydotplus.graph_from_dot_data( dot_data )
	nodes = graph.get_node_list()

	for node in nodes:

	    if node.get_label():

	    	n = int( node.get_name() )

	    	if n == 0: node.set_fillcolor( '#ffffffff' ) # root node, white

	    	else:

	    		left_child = skl_tree.tree_.children_left[ n ]

	    		if ( left_child == tree._tree.TREE_LEAF ): # leaf node

			    	c = np.argmax( skl_tree.tree_.value[ n ][ 0 ] ) 
		    		node.set_fillcolor( color_map_category[ c ] )

		    	else: node.set_fillcolor( '#e6e6e3ff' ) # internal node, gray

	return graph