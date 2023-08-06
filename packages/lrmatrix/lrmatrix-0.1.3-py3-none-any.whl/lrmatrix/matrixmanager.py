from lrmatrix.rulevectormatrix import RuleVectorMatrix
from lrmatrix.explanation import Explanation
from sklearn import tree
import bisect
import numpy as np
from scipy.cluster import hierarchy
import csv
import scipy.sparse as ssp
import scipy.stats as stats
from joblib import Parallel, delayed











class MatrixManager( RuleVectorMatrix ):

	
	def __init__( self, goal, bins = 10, precision = 2, **kwargs ):

	
		super().__init__( **kwargs )


		self.goal_ = goal # 'model' or 'data'

		self.rules_ranges_diameter_ = None
		self.instances_map_ = None	
		self.histograms_matrix_ = None
		self.aggregation_metadata_ = [ '-' ] * 10
		self.bins_ = bins
		self.precision_ = precision
		

		if ( 'file_name' in kwargs ): self.load( kwargs[ 'file_name' ] )

		
		











	def rules_extration( self, tree_array, X, y, feature_importances = None, calc_support_coverage = True, calc_diameters = True, n_jobs = 1 ):

		X = self._check_input_X( X )
		y = self._check_input_y( y )


		n_trees = len( tree_array )

		self.feature_values_min_ = np.array( [ np.amin( X[:, i] ) for i in range( X.shape[1] ) ] )
		self.feature_values_max_ = np.array( [ np.amax( X[:, i] ) for i in range( X.shape[1] ) ] )

		for c in np.unique( y ):
			self.class_instances_count_[ c ] = np.count_nonzero( y == c )


		if feature_importances is not None: self.feature_importances_ = feature_importances		
		

		if self._verbose > 0: print( 'starting rules extration process ...' )

		rules_matrix = []


		if n_jobs == 1:

			for i in range( n_trees ):

				if self._verbose > 0: print( 'tree ', i )
				
				self.__path_to_rule( tree_array[ i ].tree_, tree_id = i, node = 0, rule = super()._get_empty_rule(), rules_matrix = rules_matrix )

		else:

			indexes_split = np.array_split( np.array( range( len( tree_array ) ) ), n_jobs )

			result = Parallel( n_jobs = n_jobs, backend = 'multiprocessing', verbose = self._verbose )( delayed( self._rule_extration_parallel )( indexes, tree_array ) for indexes in indexes_split )

			rules_matrix = result.pop( 0 )

			while ( len( result ) > 0 ): rules_matrix.extend( result.pop( 0 ) )
			
		
		super()._set_rules_matrix( rules_matrix )

		self.features_used_ = self._get_features_used()

		if self._verbose > 0: print( 'rules extration conclued ' + str( self.n_rules_ ) )


		if ( calc_support_coverage ): self.calc_support_coverage( X, y, n_jobs )


		if calc_diameters: self.calc_rules_ranges_diameter()











	def _rule_extration_parallel( self, indexes, tree_array ):


		rules_matrix = []
		
		for i in indexes:

				if self._verbose > 0: print( 'tree ', i )
				
				self.__path_to_rule( tree_array[ i ].tree_, tree_id = i, node = 0, rule = super()._get_empty_rule(), rules_matrix = rules_matrix )

		return rules_matrix











	def __path_to_rule( self, skl_tree, tree_id , node, rule, rules_matrix ):


		left_child = skl_tree.children_left[ node ]
		right_child = skl_tree.children_right[ node ]

		
		if ( left_child == tree._tree.TREE_LEAF ):

			
			rule[ self.ID ] = 0

			rule[ self.MODEL ] = tree_id
			rule[ self.NODE ] = node
		
			
			node_value = skl_tree.value[ node ][0]
			node_value_sum = node_value.sum()
			target =  np.argmax( node_value )
			root_node_value = skl_tree.value[0][0]
			root_node_value_sum = root_node_value.sum()
			

			rule[ self.CLASS ] = target
			rule[ self.SUPPORT ] = node_value[ target ] / root_node_value[ target ] # assuming bootstrap = False ??
			rule[ self.COVERAGE ] = node_value_sum / root_node_value_sum # assuming bootstrap = False
			rule[ self.CERTAINTY ] = node_value[ target ] / node_value_sum
			rule[ self.VALUETOTAL ] = node_value_sum
			rule[ self.ROOTVALUETOTAL ] = root_node_value_sum
			rule[ self.ROOTVALUECLASS ] = root_node_value[ target ]


			# 2009 - Using Highly Expressive Contrast Patterns for Classification - Is It Worthwhile? - Elsa Loekito and James Bailey
			# 			P True 				P False
			# Class 	a = support(P, C)	b = support(!P, C)
			# !Class 	c = support(P, !C)	d = support(!P, !C)

			# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html
			# oddsratio, pvalue = stats.fisher_exact( [ [ a, b ], [ c, d ] ] )

			# Trees created with Bootstrap instances may lead to wrong fisher_exact values, since a = support(P, C) may count the same instance mroe than once.

			#  A commonly used significance level is 0,05. If we adopt that, we can therefore conclude p < 0,05 is statistically significant, no otherwise.
			
			a = node_value[ target ]
			b = root_node_value[ target ] - node_value[ target ]
			c = node_value_sum - node_value[ target ]
			d = root_node_value_sum - node_value_sum - ( root_node_value[ target ] - node_value[ target ] )

			_, pvalue = stats.fisher_exact( [ [ a, b ], [ c, d ] ] ) # assuming bootstrap = False
			rule[ self.FISHERPVALUE ] = pvalue


			rule_copy = list( rule )
			

			n_predicates = 0
			ranges_diameter_sum = 0

			for f in range( self.n_features_ ):

				a = f * 2
				b = a + 1

				if( ( rule_copy[ a ] != 'NaN' ) and ( rule_copy[ b ] == 'NaN' ) ):

					
					rule_copy[ b ] = self.feature_values_max_[ f ]

					n_predicates += 1

					ranges_diameter_sum += abs( ( rule_copy[ b ] - rule_copy[ a ] ) / ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] ) )


				elif( ( rule_copy[ a ] == 'NaN' ) and ( rule_copy[ b ] != 'NaN' ) ):

					
					rule_copy[ a ] = self.feature_values_min_[ f ]

					n_predicates += 1

					ranges_diameter_sum += abs( ( rule_copy[ b ] - rule_copy[ a ] ) / ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] ) )


				elif( ( rule_copy[ a ] != 'NaN' ) and ( rule_copy[ b ] != 'NaN' ) ):

					
					n_predicates += 1

					ranges_diameter_sum += abs( ( rule_copy[ b ] - rule_copy[ a ] ) / ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] ) )


				else:

					rule_copy[ b ] = 0
					rule_copy[ a ] = 0


			rule_copy[ self.NPREDICATES ] = n_predicates
			rule_copy[ self.RANGESDIAMETERMEAN ] = ranges_diameter_sum / n_predicates

			
			rule_copy[ self.AUX1 ] = 0
			rule_copy[ self.AUX2 ] = 0
			rule_copy[ self.AUX3 ] = 0


			for c in range( self.n_classes_ ):

				rule_copy[ self.VALUEC0 + c ] = node_value[ c ]


			if self._verbose > 2: print( 'rule extracted ', rule_copy )	
			rules_matrix.append( rule_copy )

					
		else:


			f = skl_tree.feature[ node ]
 
			
			threshold = skl_tree.threshold[ node ]	


			a = f * 2
			b = a + 1


			aux_sup	= rule[ b ]
			if( ( rule[ b ] == 'NaN' ) or ( rule[ b ] > threshold ) ):
				aux_sup	= rule[ b ]
				rule[ b ] = threshold 

			self.__path_to_rule( skl_tree, tree_id, left_child, rule, rules_matrix )

			rule[ b ] = aux_sup



			aux_inf = rule[ a ]
			if( ( rule[ a ] == 'NaN' ) or ( rule[ a ] < threshold ) ):
				aux_inf = rule[ a ]

				eps = 0.0000001e-38 # a = np.finfo(np.float32) # a >>> finfo(resolution=1e-06, min=-3.4028235e+38, max=3.4028235e+38, dtype=float32) # a,tiny >>> 1.1754944e-38

				if threshold >= 0.0: rule[ a ] = threshold + eps
				else: rule[ a ] = threshold - eps

			self.__path_to_rule( skl_tree, tree_id, right_child, rule, rules_matrix )

			rule[ a ] = aux_inf











	def rules_to_rects( self ):

		rules = np.array( range( self.n_rules_ ) )
		features = super()._get_features_used( rules )


		bars3d = []

		for r in rules:
			
			bar3d = []
			post = []
			size = []
			for f in features:

				a = f * 2
				b = a + 1

				if( ( self.rules_matrix_[ r, a ] != 0 ) and ( self.rules_matrix_[ r, b ] != 0 ) ):

					post.append( self.rules_matrix_[ r, a ] )
					size.append( abs( self.rules_matrix_[ r, b ] - self.rules_matrix_[ r, a ] ) )

				else:

					post.append( self.feature_values_min_[ f ] )
					size.append( abs( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] ) )

			size.append( self.rules_matrix_[ r, self.CLASS ] )		
			bar3d = post
			bar3d.extend( size )

			bars3d.append( bar3d )


		return np.array( bars3d )











	def calc_rules_ranges_diameter( self, normalized = True ):

		if self._verbose > 0: print( 'starting rules ranges diameter calculation ...' )

		self.rules_ranges_diameter_ = ssp.lil_matrix( ( self.n_rules_, self.n_features_ ) )


		for rule in range( self.n_rules_ ):

			if self._verbose > 1: print( 'calculating ranges diameter of rule: ', rule )

			features_calc = []

			for f_ab in self.rules_matrix_[ rule, :( self.n_features_ * self._shift ) ].nonzero()[ 1 ]:

				f = super()._feature_map( f_ab )
				if f not in features_calc: 

					features_calc.append( f )

					a = f * 2
					b = a + 1

					diameter = self.rules_matrix_[ rule, b ] - self.rules_matrix_[ rule, a ]

					if normalized: diameter /= ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] )


					self.rules_ranges_diameter_[ rule, f ] = diameter


		if self._verbose > 0: print( 'rules ranges diameter calculated' )











	def calc_histograms( self, X, y, mode = 'used-features', norm = True, bins = None ):

		X = self._check_input_X( X )
		y = self._check_input_y( y )


		if self._verbose > 0: print( 'starting global histograms calculation ...' )


		if bins is not None: self.bins_ = bins

		if type( self.bins_ ) == str: # 'auto' 'fd' 'doane' 'scott' 'stone' 'rice' 'sturges' 'sqrt'

			bins = np.inf
			for f in range( X.shape[ 1 ] ):
				
				bin_edges = np.histogram_bin_edges( X[ :, f ], bins = self.bins_ )

				if bins > bin_edges.shape[ 0 ] - 1: bins = bin_edges.shape[ 0 ] - 1
			
			self.bins_ = bins



		histograms_matrix = []


		for c in range( self.n_classes_ ):

			if self._verbose > 1: print( 'calculating global histograms for class: ', c )


			class_indexes = np.where( y == c )[ 0 ]

			row = []
			for f in range( self.n_features_ ):

				if self._verbose > 2: print( 'calculating global histograms for class ', c, ' on feature ', f )

				min_value = self.feature_values_min_[ f ]
				max_value = self.feature_values_max_[ f ]

				hist, _ = np.histogram( X[ class_indexes, f ], bins = self.bins_, range = ( min_value,  max_value ) )


				if norm == True: hist = hist / self.class_instances_count_[ c ]
				else: hist = hist / hist.max()
				
				row.extend( hist.tolist() )


			histograms_matrix.append( row )


		if self._verbose > 0: print( 'global histograms calculated' )


		if self._verbose > 0: print( 'starting local (rules) histograms calculation ...' )


		for r in range( self.n_rules_ ):

			if self._verbose > 1: print( 'calculating ranges histogram on rule: ', r )

			
			instances = self.instances_map_[ r, : ].nonzero()[ 1 ]
			r_class = self.rules_matrix_[ r, self.CLASS ].astype(int)

			
			row = []
			for f in range( self.n_features_ ):

				min_value = self.feature_values_min_[ f ]
				max_value = self.feature_values_max_[ f ]


				if mode == 'used-features':

					a = f * 2
					b = a + 1

					alpha = self.rules_matrix_[ r, a ]
					beta = self.rules_matrix_[ r, b ]

					if ( alpha != 0.0 ) or ( beta != 0.0 ):

						hist, _ = np.histogram( X[ instances, f ], bins = self.bins_, range = ( min_value,  max_value ) )

						if norm == True: hist = hist / self.class_instances_count_[ r_class ]
						else: hist = hist / hist.max()

					else: hist = np.zeros( self.bins_ )


				elif mode == 'all-features':

					hist, _ = np.histogram( X[ instances, f ], bins = self.bins_, range = ( min_value,  max_value ) )					

					if norm == True: hist = hist / self.class_instances_count_[ r_class ]
					else: hist = hist / hist.max()


				row.extend( hist.tolist() )


			histograms_matrix.append( row )


		self.histograms_matrix_ = ssp.lil_matrix( histograms_matrix )

		
		if self._verbose > 0: print( 'local (rules) histograms calculated' )











	def _to_features_bins( self, features ):

		features_used_bins = []

		for f in features:

			start = self.bins_ * f
			end = start + self.bins_

			features_used_bins.extend( list( range( start, end ) ) )

		return features_used_bins











	def calc_feature_importances( self, mode = 'supp' ):

		
		if self._verbose > 0: print( 'starting feature importances calculation ...' )


		self.feature_importances_ = np.zeros( self.n_features_ )


		if mode == 'supp':


			# 2018 A Decision Rule Based Approach to Generational Feature Selection - Wieslaw Paja, using as measure of quality the rule coverage
			
			for f in self.features_used_:
					
				a = f * 2
				b = a + 1

				rules = self.rules_matrix_[ :, a ].nonzero()[ 0 ].tolist()
				rules.extend( self.rules_matrix_[ :, b ].nonzero()[ 0 ].tolist() )
				rules = np.unique( np.array( rules ) )

				for r in rules:
					self.feature_importances_[ f ] += self.rules_matrix_[ r, self.SUPPORT ]

			self.feature_importances_ /= self.feature_importances_.sum()


		elif mode == 'hdiff':


			for f in self.features_used_:

				if self._verbose > 1: print( 'calculating importance on feature ', f )			
				
				f_importance = 0

				for r_1 in range( 0, self.n_rules_ ):

					for r_2 in range( r_1 + 1, self.n_rules_ ):

						hist_diffs = 0
						
						
						if self.rules_matrix_[ r_1, self.CLASS ] != self.rules_matrix_[ r_2, self.CLASS ]:

							for b in range( f * self.bins_, f * self.bins_ + self.bins_ ):

								if ( self.histograms_matrix_[ r_1 + self.n_classes_, b ] == 0 ) or ( self.histograms_matrix_[ r_2 + self.n_classes_, b ] == 0 ):

									hist_diffs += ( self.histograms_matrix_[ r_1 + self.n_classes_, b ] + self.histograms_matrix_[ r_2 + self.n_classes_, b ] )

						
						# the highest value that hist_diff can have is 2.0, that is all instances from r_1 and r_2 belong to different bins
						hist_diffs /= 2
						# the highest value that min can have is 1.0, when r_1 and r_2 support all instances from their classes (support = 1.0)
						hist_diffs *= min( self.rules_matrix_[ r_1, self.SUPPORT ], self.rules_matrix_[ r_2, self.SUPPORT ] )

						if f_importance < hist_diffs: f_importance = hist_diffs


				self.feature_importances_ [ f ] = f_importance


			self.feature_importances_ /= self.feature_importances_.sum()

		
		if self._verbose > 0: print( 'feature importances calculation done' )










	
	def __order_by_link( self, matrix, method, optimal_ordering ):

		try:

			link_mat = hierarchy.linkage( matrix, method = method, optimal_ordering = optimal_ordering )
			indexes = hierarchy.leaves_list( link_mat )			
			return indexes

		except Exception as e:
			print( e )
			return np.array( range( matrix.shape[ 0 ] ) )

	









	def order_rows( self, rows, criteria, cols,

		link_method = 'complete', link_optimal_ordering = True, row_values = None ):

		
		if criteria == 'support':
			indexes = np.argsort( self.rules_matrix_[ rows, self.SUPPORT ].toarray()[ :, 0 ] )[ ::-1 ]
			return indexes

		elif criteria == 'certainty':
			indexes = np.argsort( self.rules_matrix_[ rows, self.CERTAINTY ].toarray()[ :, 0 ] )[ ::-1 ]	
			return indexes

		elif criteria == 'class & support':
			crt_1 = self.rules_matrix_[ rows, self.CLASS ].toarray()[ :, 0 ]
			crt_2 = -1 * self.rules_matrix_[ rows, self.SUPPORT ].toarray()[ :, 0 ]
			indexes = np.lexsort( ( crt_2, crt_1 ) )
			return indexes

		elif criteria == 'class & certainty':
			crt_1 = self.rules_matrix_[ rows, self.CLASS ].toarray()[ :, 0 ]
			crt_2 = -1 * self.rules_matrix_[ rows, self.CERTAINTY ].toarray()[ :, 0 ]
			indexes = np.lexsort( ( crt_2, crt_1 ) )
			return indexes
		
		elif criteria == 'range-link':
			rc_sel = np.ix_( rows, cols )
			indexes = self.__order_by_link( self.rules_ranges_diameter_[ rc_sel ].toarray(), link_method, link_optimal_ordering )
			return indexes

		elif criteria == 'delta change':
			indexes = np.argsort( row_values[ rows ] )
			return indexes

		elif criteria == 'data coverage':
			indexes = np.argsort( self.rules_matrix_[ rows, self.COVERAGE ].toarray()[ :, 0 ] )[ ::-1 ]
			return indexes

		else: return np.array( [ ] )

	









	def order_cols( self, cols, criteria, rows,

		link_method = 'complete', link_optimal_ordering = True ):

		
		if criteria == 'importance':
			indexes = np.argsort( self.feature_importances_[ cols ] )[ ::-1 ]
			return indexes
			# if self.feature_importances_ is not None:
			# 	indexes = np.argsort( self.feature_importances_[ cols ] )[ ::-1 ]
			# 	return indexes
			# else: return cols

		elif criteria == 'range-link':
			rc_sel = np.ix_( rows, cols )
			indexes = self.__order_by_link( self.rules_ranges_diameter_[ rc_sel ].toarray().T, link_method, link_optimal_ordering )
			return indexes







	



	def explanation( self, exp_type = 'global', rules = None, x_k = None, X_s = None, r_model = None, r_node = None, r_support_min = None,  r_certainty_min = None, r_pvalue_max = None, r_class = None, r_order = 'raw', f_importance_min = None, f_order = 'raw', r_label_format = 'auto', data_coverage_max = None, info_text = None, show_rule_certainty = 'auto', show_rule_fisher_pvalue = 'auto', show_rule_data_coverage = 'auto', show_feature_importance = 'auto', show_feature_range = False, show_global_histograms = 'auto', draw_distribution = 'auto', show_info_text = True ):

		
		if self.goal_ == 'model':

			if show_feature_importance == 'auto': show_feature_importance = True
			if show_rule_data_coverage == 'auto': show_rule_data_coverage = False
			if show_global_histograms == 'auto': show_global_histograms = False
			if draw_distribution == 'auto': draw_distribution = False
			if show_rule_certainty == 'auto': show_rule_certainty = True
			if show_rule_fisher_pvalue == 'auto': show_rule_fisher_pvalue = False
			if r_label_format == 'auto': r_label_format = 'r #num'

		elif self.goal_ == 'data':

			if show_feature_importance == 'auto': show_feature_importance = True
			if show_rule_data_coverage == 'auto': show_rule_data_coverage = True
			if show_global_histograms == 'auto': show_global_histograms = True
			if draw_distribution == 'auto': draw_distribution = True
			if show_rule_certainty == 'auto': show_rule_certainty = False
			if show_rule_fisher_pvalue == 'auto': show_rule_fisher_pvalue = True
			if r_label_format == 'auto': r_label_format = 'p#num'


		if info_text is None: info_text = '\n'
		else: info_text += '\n'


		cumulative_voting = None
		cumulative_data_coverage = None
		old_rules = None
		old_rule_certainties = None

		class_names = None


		if exp_type == 'global':

			if rules is None:
			
				rules = np.array( range( self.n_rules_ ) )
				features = self.features_used_

			else: # choosing rules manually

				# from version = '0.1.3' it is required to inform, for example, rules = [ 13, 9 ] to get in the visualization rules [ 14, 10 ]
				# rules -= 1 # on visualization rules start in 1 and not 0
				rules = rules.copy() # to not alter the array outside the call
				features = super()._get_features_used( rules )

			class_names = self.class_names_

			info_text += 'type ' + exp_type + '\n'


		elif exp_type == 'local': # 1 DT: 1 used rule + ( C - 1 ) closest rules, C is the number of classes

			y_pred, proba, rules, closest_rules, rules_delta_sum = super().predict_x( x_k, closest_rules = True, counterfactual_class = 'all' )
			
			rules = np.hstack( ( rules, closest_rules ) )
			features = super()._get_features_used( rules )			

			info_text += 'type ' + exp_type + '\n'


		elif exp_type == 'local-all': # 1 DT: show all DT rules

			_, proba, _, _, rules_delta_sum = super().predict_x( x_k, closest_rules = True, counterfactual_class = 'all' )

			rules = np.array( range( self.n_rules_ ) )
			features = super()._get_features_used( rules )			

			info_text += 'type ' + exp_type + '\n'


		elif exp_type == 'local-used': # RF

			y_pred, proba, rules = super().predict_x( x_k )
			features = super()._get_features_used( rules )			

			info_text += 'type ' + exp_type + '\n'


		elif exp_type == 'local-closest': # RF

			y_pred, proba, old_rules, rules, rules_delta_sum = super().predict_x( x_k, closest_rules = True )
			features = super()._get_features_used( rules )

			info_text += 'type ' + exp_type + '\n'


		elif exp_type == 'local-subset': # local explanation for one or more instances (not all of them) at VAX

			aux = []
			for x in X_s:

				_, _, rules = super().predict_x( x )

				for r in rules: 
					if r not in aux: aux.append( r )

			rules = np.array( aux )
			features = super()._get_features_used( rules )

			class_names = self.class_names_

			info_text += 'type ' + exp_type + '\n'


		
		if r_model is not None:

			indexes = np.argwhere( self.rules_matrix_[ rules, self.MODEL ].toarray()[ :, 0 ] == r_model )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'model ' + str( r_model ) + '\n'


		if r_node is not None:

			indexes = np.argwhere( self.rules_matrix_[ rules, self.NODE ].toarray()[ :, 0 ] == r_node )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'node ' + str( r_node ) + '\n'


		if r_support_min is not None:	

			indexes = np.argwhere( self.rules_matrix_[ rules, self.SUPPORT ].toarray()[ :, 0 ] >= r_support_min )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'support >= ' + str( r_support_min ) + '\n'


		if r_certainty_min is not None:	

			indexes = np.argwhere( self.rules_matrix_[ rules, self.CERTAINTY ].toarray()[ :, 0 ] >= r_certainty_min )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'certainty >= ' + str( r_certainty_min ) + '\n'


		if r_pvalue_max is not None:

			indexes = np.argwhere( self.rules_matrix_[ rules, self.FISHERPVALUE ].toarray()[ :, 0 ] <= r_pvalue_max )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ] # make sense filter old_rules here and the other places? ??
			info_text += 'pvalue <= ' + str( r_pvalue_max ) + '\n'


		if r_class is not None:	

			indexes = np.argwhere( self.rules_matrix_[ rules, self.CLASS ].toarray()[ :, 0 ] == r_class )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'class ' + self.class_names_[ r_class ] + '\n'



		if ( r_model is not None ) or ( r_node is not None ) or ( r_support_min is not None ) or ( r_certainty_min is not None ) or ( r_pvalue_max is not None ) or ( r_class is not None ): 
			features = super()._get_features_used( rules )



		if f_importance_min is not None:	

			indexes = np.argwhere( self.feature_importances_[ features ] >= f_importance_min )[ :, 0 ]
			features = features[ indexes ]

			info_text += 'importance >= ' + str( f_importance_min ) + '\n'


			

		if ( f_order != 'raw' ) and ( len( features ) != 1 ):
			indexes = self.order_cols( features, f_order, rules )
			features = features[ indexes ]


	

		if ( r_order != 'raw' ) and ( len( rules ) != 1 ):

			if ( r_order == 'delta change' ) and ( ( exp_type == 'local') or ( exp_type == 'local-all') or ( exp_type == 'local-closest') ): 

				indexes = self.order_rows( rules, r_order, features, row_values = rules_delta_sum )

			else: indexes = self.order_rows( rules, r_order, features )
			
			rules = rules[ indexes ]

			if old_rules is not None: old_rules = old_rules[ indexes ]




		if data_coverage_max is not None: # must be here because the coverage cut takes rules order in consideration

			if len( rules ) == 1: cumulative_data_coverage = np.array( [  self.rules_matrix_[ rules[ 0 ], self.COVERAGE ] ] )
			else: cumulative_data_coverage = np.copy( self.rules_matrix_[ rules, self.COVERAGE ].toarray()[ :, 0 ] )

			for i in range( 1, cumulative_data_coverage.shape[ 0 ] ):
				cumulative_data_coverage[ i ] += cumulative_data_coverage[ i - 1 ]

			indexes = np.argwhere( cumulative_data_coverage <= data_coverage_max )[ :, 0 ]
			
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			cumulative_data_coverage = cumulative_data_coverage[ indexes ]
			info_text += 'data coverage <= ' + str( data_coverage_max ) + '\n'


			features = super()._get_features_used( rules )
			if f_order != 'raw':
				indexes = self.order_cols( features, f_order, rules )
				features = features[ indexes ]


			if f_importance_min is not None:
				indexes = np.argwhere( self.feature_importances_[ features ] >= f_importance_min )[ :, 0 ]
				features = features[ indexes ]		




		features_used_ab = super()._to_features_ab( features )
		rc_sel = np.ix_( rules, features_used_ab )




		if len( rules ) == 1: rule_classes = np.array( [ self.rules_matrix_[ rules[ 0 ], self.CLASS ].astype( int ) ] )
		else: rule_classes = self.rules_matrix_[ rules, self.CLASS ].toarray()[ :, 0 ].astype( int )

		
		if len( rules ) == 1: rule_labels = [ r_label_format.replace( '#num', str( rules[ 0 ] + 1 ) ) ]
		else: rule_labels = [ r_label_format.replace( '#num', str( r + 1 ) ) for r in self.rules_matrix_[ rules, self.ID ].toarray()[ :, 0 ].astype(int) ]


		if len( rules ) == 1: rule_supports = np.array( [ self.rules_matrix_[ rules[ 0 ], self.SUPPORT ] ] )
		else: rule_supports = self.rules_matrix_[ rules, self.SUPPORT ].toarray()[ :, 0 ]


		if show_rule_data_coverage:

			if cumulative_data_coverage is None:

				if len( rules ) == 1: rule_data_coverages = np.array( [  self.rules_matrix_[ rules[ 0 ], self.COVERAGE ] ] )
				else: rule_data_coverages = np.copy( self.rules_matrix_[ rules, self.COVERAGE ].toarray()[ :, 0 ] )

				for i in range( 1, rule_data_coverages.shape[ 0 ] ):
					rule_data_coverages[ i ] += rule_data_coverages[ i - 1 ]

			else: rule_data_coverages = cumulative_data_coverage

		else: rule_data_coverages = None # data_coverage ??


		if show_rule_certainty: rule_certainties = self.rules_matrix_[ rules, self.VALUEC0: ].toarray() / self.rules_matrix_[ rules, self.VALUETOTAL ].toarray()
		else: rule_certainties = None # rules_certainty ??


		if show_rule_fisher_pvalue:
			if len( rules ) == 1: rule_pvalues = np.array( [  self.rules_matrix_[ rules[ 0 ], self.FISHERPVALUE ] ] )
			else: rule_pvalues = self.rules_matrix_[ rules, self.FISHERPVALUE ].toarray()[ :, 0 ]
		else: rule_pvalues = None # rules_pvalue ??


		features_used_bins = None
		if show_global_histograms: 

			features_used_bins = self._to_features_bins( features )
			global_histograms = self.histograms_matrix_.toarray()[ :self.n_classes_, features_used_bins ]

		else: global_histograms = None


		if draw_distribution:

			if features_used_bins is None: features_used_bins = super()._to_features_bins( features )
			rc_sel_hist = np.ix_( rules + self.n_classes_, features_used_bins )
			distribution_matrix = self.histograms_matrix_[ rc_sel_hist ].toarray()

		else: distribution_matrix = None




		support_matrix_indexes = None
		support_matrix = None
		if self.instances_map_ is not None:

			support_matrix_indexes = self.instances_map_[ rules, : ].nonzero()[ 1 ]

			sel = np.ix_( rules, support_matrix_indexes )
			support_matrix = self.instances_map_[ sel ].toarray()


		
		
		if exp_type == 'local-used': 
			cumulative_voting = super()._aggregate_voting( rules )
			proba = cumulative_voting[ -1 ]

		elif exp_type == 'local-closest': old_rule_certainties = self.rules_matrix_[ old_rules, self.VALUEC0: ].toarray() / self.rules_matrix_[ old_rules, self.VALUETOTAL ].toarray()


		if ( exp_type == 'local' ) or ( exp_type == 'local-all' ) or ( exp_type == 'local-used' ) or ( exp_type == 'local-closest' ):

			class_names = []
			for c in range( self.class_names_.shape[ 0 ] ):
				class_names.append( self.class_names_[ c ] + ' | ' + str( np.round( proba[ c ], decimals = self.precision_ ) ) )
			class_names = np.array( class_names )

		
		feature_labels = []
		for f in features:

			label = ''

			if x_k is not None: label += str( np.round( x_k[ f ], decimals = self.precision_ ) ) + ' | '				

			label += self.feature_names_[ f ]

			if show_feature_range: label += ' [' + str( np.round( self.feature_values_min_[ f ], decimals = self.precision_ ) ) + ', ' + str( np.round( self.feature_values_max_[ f ], decimals = self.precision_ ) ) + ']'

			if show_feature_importance: label += ' | ' + str( np.round( self.feature_importances_[ f ], decimals = self.precision_ ) )

			feature_labels.append( label )

		if x_k is not None: x_k = x_k[ features ]


		if show_feature_importance: feature_importances = self.feature_importances_[ features ]
		else: feature_importances = None


		info_text += '\nrules ' + str( rules.shape[ 0 ] ) + '\nby ' + r_order + '\n'
		info_text += '\nfeatures ' + str( features.shape[ 0 ] ) + '\nby ' + f_order

		if show_info_text == False: info_text = ''



		return Explanation( goal = self.goal_, exp_type = exp_type, rules = rules, features = features, 

			matrix = self.rules_matrix_[ rc_sel ].toarray(),
			
			rule_classes = rule_classes,  
			rule_labels = rule_labels, 
			rule_supports = rule_supports,

			rule_data_coverages = rule_data_coverages,
			rule_fisher_pvalues = rule_pvalues,

			rule_certainties = rule_certainties,
			cumulative_voting = cumulative_voting,
			old_rule_certainties = old_rule_certainties,
			
			feature_labels = feature_labels, 
			feature_importances = feature_importances, 
			feature_values_min = self.feature_values_min_[ features ], 
			feature_values_max = self.feature_values_max_[ features ],

			global_histograms = global_histograms,

			draw_distribution = draw_distribution,
			bins = self.bins_,
			distribution_matrix = distribution_matrix,

			support_matrix_indexes = support_matrix_indexes,
			support_matrix = support_matrix,
			
			class_names = class_names,			
			x_k = x_k,
			info_text = info_text )
		










	def save( self, file_name, rules = None, npz_format = True ):

		try:


			if rules is None: features_used_ = self.features_used_
			else: features_used_ = self._get_features_used( rules )


			if self._verbose > 0: print( 'saving rules_matrix_ ...' )

			with open( file_name + '.csv', 'w', encoding = 'utf-8' ) as csv_file:

				writer = csv.writer( csv_file, delimiter = ';' )

				writer.writerow( [ 'n_rules_', 'n_features_', 'n_classes_', 'predicate_type_', 'goal_', 'bins_', 'precision_' ] )
				writer.writerow( [ self.n_rules_, self.n_features_, self.n_classes_, self.predicate_type_, self.goal_, self.bins_, self.precision_ ] )
				writer.writerow( [ 'k_trees', 'f_subsets_sizes', 'tie_mode', 'total_rules', 'filtered', 'pivots', 'aggregated', 'discarded', 'data_coverage', 'discarded_not_checked' ] )
				writer.writerow( self.aggregation_metadata_ )
				writer.writerow( [ 'feature_names_'] )
				writer.writerow( self.feature_names_ )
				writer.writerow( [ 'feature_values_min_' ] )
				writer.writerow( self.feature_values_min_ )
				writer.writerow( [ 'feature_values_max_' ] )
				writer.writerow( self.feature_values_max_ )
				writer.writerow( [ 'features_used_' ] )
				writer.writerow( self.features_used_ )
				writer.writerow( [ 'feature_importances_' ] )
				writer.writerow( self.feature_importances_ )
				writer.writerow( [ 'class_names_' ] )
				writer.writerow( self.class_names_ )
				writer.writerow( [ 'class_instances_count_' ] )
				writer.writerow( self.class_instances_count_ )

				
				header = []
				for f in range( self.n_features_ ):
					header.append( self.feature_names_[ f ] + ' alpha ' )
					header.append( self.feature_names_[ f ] + ' beta ' )
				header.extend( self._rule_info )
				for c in range( self.n_classes_ - 1 ):
					header.append( 'value_c' + str( c + 1 ) )

				writer.writerow( header )


				if npz_format == False:

					if rules is None: writer.writerows( self.rules_matrix_.toarray() )
					else: writer.writerows( self.rules_matrix_[ rules, : ].toarray() )

				else:

					if rules is None: ssp.save_npz( file_name + '-rules_matrix_.npz', self.rules_matrix_.tocoo() )
					else: ssp.save_npz( file_name + '-rules_matrix_.npz', self.rules_matrix_[ rules, : ].tocoo() )

				
				csv_file.close()

			if self._verbose > 0: print( 'rules_matrix_ saved' )



			if npz_format == False:


				if self.rules_ranges_diameter_ is not None:

					if self._verbose > 0: print( 'saving rules_ranges_diameter_ ...' )

					with open( file_name + '-rules_ranges_diameter_.csv', 'w', encoding = 'utf-8' ) as csv_file:

						writer = csv.writer( csv_file, delimiter = ';' )
						writer.writerows( self.rules_ranges_diameter_.toarray() )
						csv_file.close()

					if self._verbose > 0: print( 'rules_ranges_diameter_ saved' )


				if self.instances_map_ is not None:

					if self._verbose > 0: print( 'saving instances_map_ ...' )

					with open( file_name + '-instances_map_.csv', 'w', encoding = 'utf-8' ) as csv_file:

						writer = csv.writer( csv_file, delimiter = ';' )
						writer.writerows( self.instances_map_.toarray() )
						csv_file.close()

					if self._verbose > 0: print( 'instances_map_ saved' )


				if self.histograms_matrix_ is not None:

					if self._verbose > 0: print( 'saving histograms_matrix_ ...' )

					with open( file_name + '-histograms_matrix_.csv', 'w', encoding = 'utf-8' ) as csv_file:

						writer = csv.writer( csv_file, delimiter = ';' )
						writer.writerows( self.histograms_matrix_.toarray() )
						csv_file.close()

					if self._verbose > 0: print( 'histograms_matrix_ saved' )


			else:


				if self.rules_ranges_diameter_ is not None:

					if self._verbose > 0: print( 'saving rules_ranges_diameter_ ...' )

					ssp.save_npz( file_name + '-rules_ranges_diameter_.npz', self.rules_ranges_diameter_.tocoo() )					

					if self._verbose > 0: print( 'rules_ranges_diameter_ saved' )

	
				if self.instances_map_ is not None:

					if self._verbose > 0: print( 'saving instances_map_ ...' )

					ssp.save_npz( file_name + '-instances_map_.npz', self.instances_map_.tocoo() )					

					if self._verbose > 0: print( 'instances_map_ saved' )


				if self.histograms_matrix_ is not None:

					if self._verbose > 0: print( 'saving histograms_matrix_ ...' )

					ssp.save_npz( file_name + '-histograms_matrix_.npz', self.histograms_matrix_.tocoo() )					

					if self._verbose > 0: print( 'histograms_matrix_ saved' )



		except Exception as e:
			print( e )









			

	def load( self, file_name, npz_format = True ):


		metadata = np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 1, max_rows = 1, dtype = str )
		self.n_rules_ = int( metadata[ 0 ] )
		self.n_features_ = int( metadata[ 1 ] )
		self.n_classes_ = int( metadata[ 2 ] )
		self.predicate_type_ = metadata[ 3 ]
		self.goal_ = metadata[ 4 ]
		self.bins_ = int( metadata[ 5 ] )
		self.precision_ = int( metadata[ 6 ] )
		if self._verbose > 0: print( 'n_features loaded', self.n_features_ )
		if self._verbose > 0: print( 'n_classes loaded', self.n_classes_ )
		if self._verbose > 0: print( 'predicate_type loaded', self.predicate_type_ )
		if self._verbose > 0: print( 'goal_ loaded', self.goal_ )
		if self._verbose > 0: print( 'bins_ loaded', self.bins_ )
		if self._verbose > 0: print( 'precision_ loaded', self.precision_ )


		self.aggregation_metadata_ = np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 3, max_rows = 1, dtype = 'str' ).tolist()
		if self._verbose > 0: print( 'aggregation_metadata loaded', self.aggregation_metadata_ )


		self.feature_names_ = np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 5, max_rows = 1, dtype = str )
		if self._verbose > 0: print( 'feature_names loaded', self.feature_names_.shape )


		self.feature_values_min_ = np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 7, max_rows = 1 )
		if self._verbose > 0: print( 'feature_values_min loaded', self.feature_values_min_.shape )

		
		self.feature_values_max_ = np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 9, max_rows = 1 )
		if self._verbose > 0: print( 'feature_values_max loaded', self.feature_values_max_.shape )

		
		self.features_used_ = np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 11, max_rows = 1, dtype = int )
		if self._verbose > 0: print( 'features_used loaded', self.features_used_.shape )


		self.feature_importances_ = np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 13, max_rows = 1 )
		if self._verbose > 0: print( 'feature_importances loaded', self.feature_importances_.shape )
		

		self.class_names_ = np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 15, max_rows = 1, dtype = str )
		if self._verbose > 0: print( 'class_names loaded', self.class_names_.shape )


		self.class_instances_count_ = np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 17, max_rows = 1, dtype = int )
		if self._verbose > 0: print( 'class_instances_count_ loaded', self.class_names_.shape )


		if self._verbose > 0: print( 'loading rules_matrix_ ...' )

		if npz_format == False:

			self.rules_matrix_ = ssp.lil_matrix( np.loadtxt( file_name + '.csv', delimiter = ';', skiprows = 19, dtype = np.float64 ) )

		else:

			self.rules_matrix_ = ssp.load_npz( file_name + '-rules_matrix_.npz' ).tolil()

		if self._verbose > 0: print( 'rules_matrix_ loaded ', self.rules_matrix_.shape )


		self.n_rules_ = self.rules_matrix_.shape[ 0 ]


		if self.predicate_type_ == 'range':
			self._shift = 2
		elif self.predicate_type_ == 'binary':
			self._shift = 1


		self._set_matrix_indexes()



		if npz_format == False:

			try:

				if self._verbose > 0: print( 'loading instances_map_ ...' )
				self.instances_map_ = ssp.lil_matrix( np.loadtxt( file_name + '-instances_map_.csv', delimiter = ';' ), dtype = int )
				if self._verbose > 0: print( 'instances_map_ loaded' )

			except Exception as e:
				print( e )


			try:

				if self._verbose > 0: print( 'loading histograms_matrix_ ...' )
				self.histograms_matrix_ = ssp.lil_matrix( np.loadtxt( file_name + '-histograms_matrix_.csv', delimiter = ';' ), dtype = int )
				if self._verbose > 0: print( 'histograms_matrix_ loaded' )

			except Exception as e:
				print( e )

		else:

			try:

				if self._verbose > 0: print( 'loading instances_map_ ...' )
				self.instances_map_ = ssp.load_npz( file_name + '-instances_map_.npz' ).tolil()
				if self._verbose > 0: print( 'instances_map_ loaded' )

			except Exception as e:
				print( e )


			try:

				if self._verbose > 0: print( 'loading histograms_matrix_ ...' )
				self.histograms_matrix_ = ssp.load_npz( file_name + '-histograms_matrix_.npz' ).tolil()
				if self._verbose > 0: print( 'histograms_matrix_ loaded' )

			except Exception as e:
				print( e )

