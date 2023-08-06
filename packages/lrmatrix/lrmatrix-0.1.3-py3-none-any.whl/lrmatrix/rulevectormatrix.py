import scipy.sparse as ssp
import numpy as np
import bisect as bst
import csv
import time
from joblib import Parallel, delayed











class RuleVectorMatrix():


	def __init__( self, n_features = None, n_classes = None, feature_names = None, feature_values_min = None, feature_values_max = None, class_names = None, predicate_type = 'range', verbose = 0 ):


		self._verbose = verbose
		
		self.n_rules_ = 0

		self.features_used_ = [] # after filled convert to np.array

		self.predicate_type_ = predicate_type
		if self.predicate_type_ == 'range':
			self._shift = 2
		elif self.predicate_type_ == 'binary':
			self._shift = 1


		if ( n_features is not None ) and ( n_classes is not None ):

			self.n_features_ = n_features

			if feature_names is None: self.feature_names_ = [ 'feature ' + str( f ) for f in range( 0, self.n_features_ ) ]
			else: self.feature_names_ = feature_names

			if feature_values_min is not None: self.feature_values_min_ = feature_values_min
			if feature_values_max is not None: self.feature_values_max_ = feature_values_max

			self.feature_importances_ = np.zeros( self.n_features_ )


			self.n_classes_ = n_classes

			if class_names is None:	self.class_names_ = [ 'class ' + str( c ) for c in range( 0, self.n_classes_ ) ]
			else: self.class_names_ = class_names

			self.class_instances_count_ = np.zeros( self.n_classes_ )			


			self._set_matrix_indexes()











	def _set_matrix_indexes( self ):


		self._rule_info = [ 'id', 'model', 'node', 'class', 'support', 'coverage', 'certainty', 'n_predicates', 'ranges_diameter_mean', 'fisher_pvalue', 'aux_1', 'aux_2', 'aux_3', 'root_value_total', 'root_value_class', 'value_total', 'value_c0' ]

		
		self.ID = ( self.n_features_ * self._shift ) + self._rule_info.index( 'id' )
		self.MODEL = ( self.n_features_ * self._shift ) + self._rule_info.index( 'model' )
		self.NODE = ( self.n_features_ * self._shift ) + self._rule_info.index( 'node' )
		
		self.CLASS = ( self.n_features_ * self._shift ) + self._rule_info.index( 'class' )
		self.SUPPORT = ( self.n_features_ * self._shift ) + self._rule_info.index( 'support' )
		self.COVERAGE = ( self.n_features_ * self._shift ) + self._rule_info.index( 'coverage' )
		self.CERTAINTY = ( self.n_features_ * self._shift ) + self._rule_info.index( 'certainty' )
		
		self.NPREDICATES = ( self.n_features_ * self._shift ) + self._rule_info.index( 'n_predicates' )
		self.RANGESDIAMETERMEAN = ( self.n_features_ * self._shift ) + self._rule_info.index( 'ranges_diameter_mean' )
		self.FISHERPVALUE = ( self.n_features_ * self._shift ) + self._rule_info.index( 'fisher_pvalue' )

		self.AUX1 = ( self.n_features_ * self._shift ) + self._rule_info.index( 'aux_1' )
		self.AUX2 = ( self.n_features_ * self._shift ) + self._rule_info.index( 'aux_2' )
		self.AUX3 = ( self.n_features_ * self._shift ) + self._rule_info.index( 'aux_3' )

		self.ROOTVALUETOTAL = ( self.n_features_ * self._shift ) + self._rule_info.index( 'root_value_total' )
		self.ROOTVALUECLASS = ( self.n_features_ * self._shift ) + self._rule_info.index( 'root_value_class' )

		self.VALUETOTAL = ( self.n_features_ * self._shift ) + self._rule_info.index( 'value_total' )
		self.VALUEC0 = ( self.n_features_ * self._shift ) + self._rule_info.index( 'value_c0' )


		self.__n_rule_info = len( self._rule_info ) + self.n_classes_ - 1

		if self._verbose > 1: print( 'rule info', self._rule_info )











	def _get_empty_rule( self ):

		return [ 'NaN' ] * ( ( self.n_features_ * self._shift ) + self.__n_rule_info )










	def print_rule( self, rule ):

		print( '---' )

		print( 'rule info ::' )


		print( 'id : ' + str( self.rules_matrix_[ rule, self.ID ] ) )
		print( 'tree : ' + str( self.rules_matrix_[ rule, self.MODEL ] ) )
		print( 'node : ' + str( self.rules_matrix_[ rule, self.NODE ] ) )
		
		print( 'class : ' + self.class_names_[ int( self.rules_matrix_[ rule, self.CLASS ] ) ] )
		print( 'support : ' + str( self.rules_matrix_[ rule, self.SUPPORT ] ) )
		print( 'coverage : ' + str( self.rules_matrix_[ rule, self.COVERAGE ] ) )
		print( 'certainty : ' + str( self.rules_matrix_[ rule, self.CERTAINTY ] ) )

		print( 'predicates : ' + str( self.rules_matrix_[ rule, self.NPREDICATES ] ) )
		print( 'ranges_diameter_mean : ' + str( self.rules_matrix_[ rule, self.RANGESDIAMETERMEAN ] ) )
		print( 'fisher_pvalue : ' + str( self.rules_matrix_[ rule, self.FISHERPVALUE ] ) )

		print( 'aux_1 : ' + str( self.rules_matrix_[ rule, self.AUX1 ] ) )
		print( 'aux_2 : ' + str( self.rules_matrix_[ rule, self.AUX2 ] ) )
		print( 'aux_3 : ' + str( self.rules_matrix_[ rule, self.AUX3 ] ) )
		
		print( 'prob : ' + str( self.rules_matrix_[ rule, self.VALUEC0: ].toarray()[ 0 ] / self.rules_matrix_[ rule, self.VALUETOTAL ] ) )

		print( 'values : ' + str( self.rules_matrix_[ rule, self.VALUEC0: ].toarray()[ 0 ] ) )
		print( 'value total : ' + str( self.rules_matrix_[ rule, self.VALUETOTAL ] ) )

		print( 'root value class : ' + str( self.rules_matrix_[ rule, self.ROOTVALUECLASS ] ) )
		print( 'root value total : ' + str( self.rules_matrix_[ rule, self.ROOTVALUETOTAL ] ) )

		print( '---' )

		print( 'rule predicates ::' )

		f_printed = -1
		for f in self.rules_matrix_[ rule, :( self.n_features_ * self._shift ) ].nonzero()[ 1 ]:

			f = self._feature_map( f )

			if f != f_printed:
				f_printed = f

				a = f * 2
				b = a + 1
				print( 'f ' + str( f ) + ' : ' + self.feature_names_[ f ] + ' : [ ' + str( self.rules_matrix_[ rule, a ] ) + ', ' + str( self.rules_matrix_[ rule, b ] ) + ' ]' )

		print( '---' )











	def _insert_rule( self, rule_vector ):
		

		if self.rules_matrix_ is None:

			self.rules_matrix_ = ssp.lil_matrix( [ rule_vector ], dtype = np.float64 )

		else:

			self.rules_matrix_ = ssp.vstack( [ self.rules_matrix_, rule_vector ], format = 'lil', dtype = np.float64 ) # takes to much time to run

		self.n_rules_ += 1











	def _set_rules_matrix( self, rules_matrix ):

		self.rules_matrix_ = ssp.lil_matrix( rules_matrix, dtype = np.float64 )
		
		self.n_rules_ = self.rules_matrix_.shape[ 0 ]

		self.rules_matrix_[ :, self.ID ] = np.array( range( self.n_rules_ ) )











	def apply_rule( self, rule, x_k, y_k = None, all_predicates = True ):

		x_k = self._check_input_X( x_k )


		result = 1

		f_checked = -1

		delta_sum = 0

		for f in self.rules_matrix_[ rule, :( self.n_features_ * self._shift ) ].nonzero()[ 1 ]:

			f = self._feature_map( f )

			if f != f_checked:
				f_checked = f

				predicate, delta = self.__apply_rule_predicate( rule, f, x_k[ f ] )

				if predicate == False:

					result = 0

					if all_predicates: delta_sum += delta # check all predicates for delta_sum to turn True the rule
					else: break # dot not check all predicates if at least one is False


		if ( ( y_k is not None ) and ( result == 1 ) and ( y_k != self.rules_matrix_[ rule, self.CLASS ] ) ):
			result = -1

		if all_predicates: return result, delta_sum
		else: return result










	def _feature_map( self, f_ab ):

		if self.predicate_type_ == 'range':

			return int( f_ab / 2 )

		elif self.predicate_type_ == 'binary':

			return int( f_ab )











	def __apply_rule_predicate( self, rule, f, x_k_f ):

		result = False
		delta = 0

		if self.predicate_type_ == 'range':

			a = f * 2
			b = a + 1

			alpha = self.rules_matrix_[ rule, a ]
			beta = self.rules_matrix_[ rule, b ]

			if ( ( x_k_f >= alpha ) and ( x_k_f <= beta ) ):

				result = True

			else:

				if ( x_k_f < alpha ):

					delta = abs( x_k_f - alpha )

				else:

					delta = abs( x_k_f - beta )

				delta /= ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] )					

		elif self.predicate_type_ == 'binary':

			pass

		return result, delta











	def predict( self, X, n_jobs = 1, **kwargs ):

		X = self._check_input_X( X )


		predictions = []
		predictions_proba = []

		list_id_result = []


		if n_jobs == 1:


			for k in range( X.shape[ 0 ] ):

				if self._verbose > 0: print( 'precting instance: ', k )

				y_predicted, proba, ids = self.predict_x( X[ k, : ], **kwargs )

				predictions.append( y_predicted )
				predictions_proba.append( proba )

				list_id_result.append( ids )


		else:

			
			indexes_split = np.array_split( np.array( range( X.shape[ 0 ] ) ), n_jobs )

			result = Parallel( n_jobs = n_jobs, backend = 'multiprocessing', verbose = self._verbose )( delayed( self._predict_parallel )( indexes, X, **kwargs ) for indexes in indexes_split )

			aux = result.pop( 0 )

			predictions.extend( aux[ 0 ] )
			predictions_proba.extend( aux[ 1 ] )

			list_id_result.extend( aux[ 2 ] )

			while ( len( result ) > 0 ):

				aux = result.pop( 0 )

				predictions.extend( aux[ 0 ] )
				predictions_proba.extend( aux[ 1 ] )

				list_id_result.extend( aux[ 2 ] )



		return np.array( predictions ), np.array( predictions_proba ), np.array( list_id_result )











	def _predict_parallel( self, indexes, X, **kwargs ):


		predictions = []
		predictions_proba = []

		list_id_result = []


		for k in indexes:

			if self._verbose > 0: print( 'precting instance: ', k )

			y_predicted, proba, ids = self.predict_x( X[ k, : ], **kwargs )

			predictions.append( y_predicted )
			predictions_proba.append( proba )

			list_id_result.append( ids )

		
		return predictions, predictions_proba, list_id_result











	def predict_x( self, x_k, by_model = True, closest_rules = False, list_id = 'id', counterfactual_class = 'first'  ):

		x_k = self._check_input_X( x_k )


		if by_model:

			if not closest_rules: model = -1
			else: model = 0


			voting = ssp.lil_matrix( ( 1, self.n_classes_ ) )
			list_id_result_1 = []

			
			# used when closest_rules == True
			list_id_result_2 = []
			rules_delta_sum = []

			rules = []
			rules_class = []
			rules_delta = []


			for rule in range( self.n_rules_ ):

				if not closest_rules: 

					if( self.rules_matrix_[ rule, self.MODEL ] != model ):

						if self._verbose > 1: print( 'applying instance on rule: ', rule )

						result = self.apply_rule( rule, x_k, all_predicates = False )

						if result == 1:

							model = self.rules_matrix_[ rule, self.MODEL ]

							if list_id == 'id': list_id_result_1.append( rule ) # ??
							elif list_id == 'model': list_id_result_1.append( self.rules_matrix_[ rule, self.MODEL ].astype( int ) ) 
							elif list_id == 'node': list_id_result_1.append( self.rules_matrix_[ rule, self.NODE ].astype( int ) )

							voting += ( self.rules_matrix_[ rule, self.VALUEC0: ] / self.rules_matrix_[ rule, self.VALUETOTAL ] )

				else:

					if self._verbose > 1: print( 'applying instance on rule: ', rule )

					result, delta_sum = self.apply_rule( rule, x_k )
					rules_delta_sum.append( delta_sum )


					if( self.rules_matrix_[ rule, self.MODEL ] != model ):

						closest = self.__get_closest_rule( rule_true_class, rules, rules_class, counterfactual_class )

						if counterfactual_class == 'first': 

							if list_id == 'id': list_id_result_2.append( closest ) # ??
							elif list_id == 'model': list_id_result_2.append( self.rules_matrix_[ closest, self.MODEL ].astype( int ) )
							elif list_id == 'node': list_id_result_2.append( self.rules_matrix_[ closest, self.NODE ].astype( int ) )

						elif counterfactual_class == 'all':

							if list_id == 'id': list_id_result_2.extend( closest )
							elif list_id == 'model': list_id_result_2.extend( self.rules_matrix_[ closest, self.MODEL ].astype( int ).tolist() )
							elif list_id == 'node': list_id_result_2.extend( self.rules_matrix_[ closest, self.NODE ].astype( int ).tolist() )


						model = self.rules_matrix_[ rule, self.MODEL ]

						rules = []
						rules_class = []
						rules_delta = []


					if result == 1:

						rule_true_class = self.rules_matrix_[ rule, self.CLASS ].astype( int )

						if list_id == 'id': list_id_result_1.append( rule ) # ??
						elif list_id == 'model': list_id_result_1.append( self.rules_matrix_[ rule, self.MODEL ].astype( int ) )
						elif list_id == 'node': list_id_result_1.append( self.rules_matrix_[ rule, self.NODE ].astype( int ) )

						voting += ( self.rules_matrix_[ rule, self.VALUEC0: ] / self.rules_matrix_[ rule, self.VALUETOTAL ] )

					else:

						index = bst.bisect_left( rules_delta, delta_sum )
						rules_delta.insert( index, delta_sum )
						rules.insert( index, rule )
						rules_class.insert( index, self.rules_matrix_[ rule, self.CLASS ].astype( int ) )				

			
			if closest_rules: # last model didn't check by ' if( self.rules_matrix_[ rule, self.MODEL ] != model ): '

				closest = self.__get_closest_rule( rule_true_class, rules, rules_class, counterfactual_class )

				if counterfactual_class == 'first': 

					if list_id == 'id': list_id_result_2.append( closest ) # ??
					elif list_id == 'model': list_id_result_2.append( self.rules_matrix_[ closest, self.MODEL ].astype( int ) )
					elif list_id == 'node': list_id_result_2.append( self.rules_matrix_[ closest, self.NODE ].astype( int ) )

				elif counterfactual_class == 'all':

					if list_id == 'id': list_id_result_2.extend( closest )
					elif list_id == 'model': list_id_result_2.extend( self.rules_matrix_[ closest, self.MODEL ].astype( int ).tolist() )
					elif list_id == 'node': list_id_result_2.extend( self.rules_matrix_[ closest, self.NODE ].astype( int ).tolist() )



			voting = voting.toarray()[ 0 ]

			proba = voting / voting.sum()
			y_predicted = np.argmax( proba )


		if closest_rules: return y_predicted, proba, np.array( list_id_result_1 ), np.array( list_id_result_2 ), np.array( rules_delta_sum )
		else: return y_predicted, proba, np.array( list_id_result_1 )











	def __get_closest_rule( self, rule_true_class, rules, rules_class, counterfactual_class = 'first' ): # 'rules' and 'rules_class' sorted by rules_delta

		if counterfactual_class == 'first': 

			for i in range( len( rules ) ): 

				if rule_true_class != rules_class[ i ]: return rules[ i ]

		elif counterfactual_class == 'all':

			r_list = []
			r_list_classes = []
			r_list_classes.append( rule_true_class )

			for i in range( len( rules ) ): 

				if ( rules_class[ i ] not in r_list_classes  ): 

					r_list.append( rules[ i ] )
					r_list_classes.append( rules_class[ i ] )

			return r_list













	def _aggregate_voting( self, rules, partial = True ): # by rows above

		n_rules = rules.shape[ 0 ]

		certainty = self.rules_matrix_[ rules, self.VALUEC0: ].toarray() / self.rules_matrix_[ rules, self.VALUETOTAL ].toarray()

		if partial:

			partial_voting = []

			partial_voting.append( certainty[ 0 ] )

			for r in range( n_rules ):

				if r != 0:
					voting = np.sum( certainty[ 0:( r + 1 ) ], axis = 0 )
					partial_voting.append( voting / voting.sum() )


			return np.array( partial_voting )

		else:

			voting = np.sum( certainty, axis = 0 )
			return voting / voting.sum()



		







	def _get_features_used( self, rules = None ):


		if rules is None: rules = np.array( range( self.n_rules_ ) )

		features_ab = np.unique( self.rules_matrix_[ rules, :( self.n_features_ * self._shift ) ].nonzero()[ 1 ] )

		features_used = []

		for f_ab in features_ab:

			f = self._feature_map( f_ab )

			if f not in features_used: features_used.append( f )

		return np.array( features_used )











	def _to_features_ab( self, features ):

		features_used_ab = []

		for f in features:

			a = f * 2
			b = a + 1

			features_used_ab.append( a )
			features_used_ab.append( b )

		return features_used_ab











	def _map( self, rules, X, instances, y = None, map_type = 'binary', by_model = True ):

		
		X = self._check_input_X( X )
		if y is not None: y = self._check_input_y( y )

		
		st_time = 0

		n_instances = instances.shape[ 0 ]

		if ( map_type == 'binary' ) or ( map_type == 'binary_signed' ): instances_map = ssp.lil_matrix( ( self.n_rules_, n_instances ), dtype = np.int8 )
		elif map_type == 'real': instances_map = ssp.lil_matrix( ( self.n_rules_, n_instances ), dtype = np.float64 )

		
		if self._verbose > 0: print( 'starting instances mapping process ...' )


		for i in range( n_instances ):


			k = instances[ i ]
			model = -1 # used only when by_model == True


			
			if self._verbose > 1: 
				
				ed_time = time.time()
				rm_time = 'calculating ...'
				if st_time != 0:

					t = ( ed_time - st_time ) / 60
					rm_time = str( round( t * ( instances[ -1 ] + 1 - k ), 2 ) ) + 'min'

				else: 
					st_time = ed_time

				st_time = ed_time
				
				print( 'mapping instance ', ( k + 1 ), ' of ', instances[ -1 ] + 1, ', remaining time ' + rm_time )


			
			for r in rules:

				if by_model == True:
				
					if( self.rules_matrix_[ r, self.MODEL ] != model ):

						if ( map_type == 'binary' ) or ( map_type == 'binary_signed' ):

							if y is None: result = self.apply_rule( r, X[ k, : ], all_predicates = False )
							else: result = self.apply_rule( r, X[ k, : ], y[ k ], all_predicates = False )

						elif map_type == 'real': # ??

							if y is None: result, delta_sum = self.apply_rule( r, X[ k, : ] )
							else: result, delta_sum = self.apply_rule( r, X[ k, : ], y[ k ] )


						if result != 0:

							if map_type == 'binary': instances_map[ r, i ] = abs( result )
							elif map_type == 'binary_signed': instances_map[ r, i ] = result
							elif map_type == 'real': instances_map[ r, i ] = delta_sum

							model = self.rules_matrix_[ r, self.MODEL ]

				else:

					if ( map_type == 'binary' ) or ( map_type == 'binary_signed' ):

						if y is None: result = self.apply_rule( r, X[ k, : ], all_predicates = False )
						else: result = self.apply_rule( r, X[ k, : ], y[ k ], all_predicates = False )

					elif map_type == 'real': # ??

						if y is None: result, delta_sum = self.apply_rule( r, X[ k, : ] )
						else: result, delta_sum = self.apply_rule( r, X[ k, : ], y[ k ] )


					if result != 0:

						if map_type == 'binary': instances_map[ r, i ] = abs( result )
						elif map_type == 'binary_signed': instances_map[ r, i ] = result
						elif map_type == 'real': instances_map[ r, i ] = delta_sum			
					

		if self._verbose > 0: print( 'instances mapping process done' )


		return instances_map











	def imap( self, X, y = None, map_type = 'binary', by_model = True, n_jobs = 1 ):


		X = self._check_input_X( X )
		if y is not None: y = self._check_input_y( y )

		
		n_instances = X.shape[ 0 ]

		
		crt_1 = self.rules_matrix_[ :, self.MODEL ].toarray()[ :, 0 ]
		crt_2 = -1 * self.rules_matrix_[ :, self.SUPPORT ].toarray()[ :, 0 ]
		rules = np.lexsort( ( crt_2, crt_1 ) ) # np.lexsort( ( b, a ) ) >>> Sort by a, then by b. Having high coverage rules at first to maximize speed.


		indexes = np.array_split( np.array( range( X.shape[ 0 ] ) ), n_jobs )

		
		verbose = 0
		if self._verbose != 0: verbose = 1


		if y is not None:

			if n_jobs > 1: 

				result = Parallel( n_jobs = n_jobs, backend = 'multiprocessing', verbose = verbose )( delayed( self._map )( rules, X, instances, y, map_type = map_type, by_model = by_model ) for instances in indexes )

			elif n_jobs == 1:

				result = self._map( rules, X, indexes[ 0 ], y, map_type = map_type, by_model = by_model )

		else:

			if n_jobs > 1:

				result = Parallel( n_jobs = n_jobs, backend = 'multiprocessing', verbose = verbose )( delayed( self._map )( rules, X, instances, map_type = map_type, by_model = by_model ) for instances in indexes )

			elif n_jobs == 1:

				result = self._map( rules, X, indexes[ 0 ], map_type = map_type, by_model = by_model )				


		if n_jobs > 1:
		
			instance_map = result.pop( 0 )
			while ( len( result ) > 0 ):
				instance_map = ssp.hstack( [ instance_map, result.pop( 0 ) ], format = 'lil', dtype = np.int8 )

		elif n_jobs == 1:

			instance_map = result


		return instance_map











	def calc_support_coverage( self, X, y, n_jobs = 1 ):


		X = self._check_input_X( X )
		y = self._check_input_y( y )


		n_instances = X.shape[ 0 ]		
		instances_map = self.imap( X, y, map_type = 'binary_signed', n_jobs = n_jobs )

		if self._verbose > 1: print( 'starting support and coverage calculation process' )


		for r in range( instances_map.toarray().shape[ 0 ] ):

			if self._verbose > 1: print( 'calculating support and coverage of rule: ', r )
			
			n_supported_instances = 0
			n_covered_instances = instances_map[ r, : ].count_nonzero()

			for i in instances_map[ r, : ].nonzero()[ 1 ]:
				if ( instances_map[ r, i ] == 1 ): n_supported_instances += 1
				elif( instances_map[ r, i ] == -1 ): instances_map[ r, i ] = 1 # to use instances_map as self.instances_map_ in binary ( 0 or 1 ) ??


			self.rules_matrix_[ r, self.SUPPORT ] = n_supported_instances / self.class_instances_count_[ int( self.rules_matrix_[ r, self.CLASS ] ) ]

			self.rules_matrix_[ r, self.COVERAGE ] = n_covered_instances / n_instances		

		if self._verbose > 0: print( 'support and coverage done' )











	def _is_only_new_instances( self, r_candidate, instances_map, instances_explained, n_instances_explained ):

		instances = instances_map[ r_candidate, : ].nonzero()[ 1 ]
		n_instances = instances.shape[ 0 ]
		
		n_instances_remaining = instances_explained.shape[ 0 ] - n_instances_explained
		
		only_new_instances = False

		if n_instances <= n_instances_remaining:

			only_new_instances = True

			for i in instances:
				if instances_explained[ i ] == 1: # find rule with only new instance(s)
					only_new_instances = False
					break

		return only_new_instances











	def _get_jaccard0_rules( self, r_pivot, rules, instances_map, check_model = True, check_class = True ):


		r_pivot_instances = instances_map[ r_pivot, : ].nonzero()[ 1 ].tolist()
		r_pivot_class = self.rules_matrix_[ r_pivot, self.CLASS ]
		r_pivot_model = self.rules_matrix_[ r_pivot, self.MODEL ]
		jaccard0 = []


		index = 0
		
		while index < len( rules ):


			r = rules[ index ]


			r_class = self.rules_matrix_[ r, self.CLASS ]
			r_model = self.rules_matrix_[ r, self.MODEL ]

			model_test = True
			if check_model == True:
				model_test = r_pivot_model != r_model
			
			class_test = True
			if check_class == True:
				class_test = r_pivot_class == r_class

							
			if ( r_pivot != r ) and ( model_test ) and ( class_test ):

				r_instances = instances_map[ r, : ].nonzero()[ 1 ].tolist()

				len_r_pivot_instances = len( r_pivot_instances )
				len_r_instances = len( r_instances )

				if len_r_pivot_instances > len_r_instances: break # check rule r coverage


				add = True
				if len_r_pivot_instances == len_r_instances:

					for i in range( len_r_pivot_instances ):

						if r_pivot_instances[ i ] != r_instances[ i ]:
							add = False
							break

				else: add = False


				if add == True: 
					
					jaccard0.append( r )
					rules.remove( r )

				else: index += 1


			else: index += 1		


		return jaccard0











	def calc_predicates_metrics( self, rules = None ):


		if rules is None: rules = np.array( range( self.rules_matrix_.shape[ 0 ] ) )


		for r in rules:

			features_used = self._get_features_used( [ r ] )
			n_predicates = features_used.shape[ 0 ]

			ranges_diameter_sum = 0
			for f in features_used:

				a = f * 2
				b = a + 1

				ranges_diameter_sum += abs( ( self.rules_matrix_[ r, b ] - self.rules_matrix_[ r, a ] ) / ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] ) )

			ranges_diameter_mean = ranges_diameter_sum / n_predicates

			self.rules_matrix_[ r, self.NPREDICATES ] = n_predicates
			self.rules_matrix_[ r, self.RANGESDIAMETERMEAN ] = ranges_diameter_mean












	def aggregate_rules( self, instances_map, min_coverage = 1.0 ):


		n_instances = instances_map.shape[ 1 ]

		
		rules = np.array( range( self.rules_matrix_.shape[ 0 ] ) )
		delete = []

		total = rules.shape[ 0 ]
		filtered = 0
		pivots = 0
		aggregated = 0
		discarded = 0
		coverage = 0



		if self._verbose > 0: print( '\nstarting rules filtering process ...' )

		

		certainties = self.rules_matrix_[ rules, self.CERTAINTY ].toarray()[ :, 0 ]
		
		indexes = np.argwhere( certainties == 1.0 )[ :, 0 ]
		
		aux = rules.tolist() 
		rules = rules[ indexes ]
		aux = list( set( aux ) - set( rules.tolist() ) )

		delete.extend( aux )
		filtered += len( delete )


		
		if self._verbose > 0: print( 'rules filtering done' )
		if self._verbose > 1: print( 'partial results : filtered ',  filtered )	


		
		crt_1 = -1 * self.rules_matrix_[ rules, self.COVERAGE ].toarray()[ :, 0 ]
		crt_2 = self.rules_matrix_[ rules, self.MODEL ].toarray()[ :, 0 ]
		indexes = np.lexsort( ( crt_2, crt_1 ) ) # np.lexsort( ( b, a ) ) >>> Sort by a, then by b. Having high coverage rules at first to maximize speed.
		rules = rules[ indexes ].tolist()


		instances_explained = np.zeros( n_instances )
		n_instances_explained = 0


		
		if self._verbose > 0: print( '\nstarting rules aggregation process ...' )

		while ( len( rules ) > 0 ) and ( coverage < min_coverage ):

			
			r_candidate = rules.pop( 0 )

			if self._verbose > 3: print( '\n r_candidate ', r_candidate )
			if self._verbose > 3: print( 'rules ', rules )

			
			aggregate = True


			if n_instances_explained != 0: # do not check the first rule

				only_new_instances = self._is_only_new_instances( r_candidate, instances_map, instances_explained, n_instances_explained )
				
				if only_new_instances == False:
					aggregate = False

					if self._verbose > 1: print( 'descarting rule ', r_candidate, ' remaining rules ', len( rules ), ', coverage ', round( coverage, 5 ) )
					
					discarded += 1
					delete.append( r_candidate )


			if aggregate == True:


				r_pivot = r_candidate
				pivots += 1


				if self._verbose > 1: print( 'getting jaccard0 rules for',  r_pivot, '...' )
				rules_aggregate = self._get_jaccard0_rules( r_pivot, rules, instances_map )
				if self._verbose > 2: print( 'rules_aggregate', rules_aggregate )


				for r_aggr in rules_aggregate:

					if self._verbose > 1: print( 'aggregating rule', r_aggr )

					aggregated += 1
					
					f_checked = -1

					for f in self.rules_matrix_[ r_aggr, :( self.n_features_ * self._shift ) ].nonzero()[ 1 ]:

						f = self._feature_map( f )

						if f != f_checked:
							f_checked = f

							a = f * 2
							b = a + 1

							if ( self.rules_matrix_[ r_pivot, a ] != 0 ) or ( self.rules_matrix_[ r_pivot, b ] != 0 ):

								self.rules_matrix_[ r_pivot, a ] = max( self.rules_matrix_[ r_pivot, a ], self.rules_matrix_[ r_aggr, a ] )
								self.rules_matrix_[ r_pivot, b ] = min( self.rules_matrix_[ r_pivot, b ], self.rules_matrix_[ r_aggr, b ] )

							else:

								self.rules_matrix_[ r_pivot, a ] = self.rules_matrix_[ r_aggr, a ]
								self.rules_matrix_[ r_pivot, b ] = self.rules_matrix_[ r_aggr, b ]


					delete.append( r_aggr )


				instances = instances_map[ r_pivot, : ].nonzero()[ 1 ]
				instances_explained[ instances ] = 1
				coverage = instances_explained.sum() / n_instances				
				n_instances_explained += instances.shape[ 0 ]


				if self._verbose > 0: print( 'partial results : pivots ',  pivots, ', aggregated ', aggregated,  ', discarded ', discarded, ', coverage ', round( coverage, 5 ) )



		discarded_not_checked = 0		
		if( len( rules ) != 0 ):
			discarded += len( rules )
			discarded_not_checked = len( rules )
			delete.extend( rules )


		if self._verbose > 0: print( 'rules aggregation done' )


		self.rules_matrix_.rows = np.delete( self.rules_matrix_.rows, delete )
		self.rules_matrix_.data = np.delete( self.rules_matrix_.data, delete )

		n_rules = self.rules_matrix_._shape[ 0 ] - len( delete )		
		self.rules_matrix_._shape = ( n_rules, self.rules_matrix_._shape[ 1 ] )
		self.n_rules_ = n_rules

		
		instances_map.rows = np.delete( instances_map.rows, delete )
		instances_map.data = np.delete( instances_map.data, delete )
		instances_map._shape = ( n_rules, instances_map._shape[ 1 ] )

				
		rules = np.array( range( 0, n_rules ) )
		self.features_used_ = self._get_features_used( rules )


		self.rules_matrix_[ :, self.MODEL ] = 0
		self.rules_matrix_[ :, self.ID ] = np.array( [ rules ] ).T


		self.calc_predicates_metrics()


		if self._verbose > 0: print( 'aggregation results with tie_mode ignore: total', total, ', filtered', filtered, ', pivots', pivots, ', aggregated', aggregated, ', discarded', discarded, ', coverage', round( coverage, 5 ), ', discarded not checked', discarded_not_checked )


		return 'ignore', total, filtered, pivots, aggregated, discarded, coverage, discarded_not_checked











	def _check_input_X( self, X ):

		if X.dtype == np.float32: return X
		else:  return np.asfortranarray( X, dtype = np.float32 )











	def _check_input_y( self, y ):

		if y.dtype == np.int8: return y
		else:  return y.astype(np.int8)