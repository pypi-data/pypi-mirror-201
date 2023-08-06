from lrmatrix.matrixdraw import draw_range_matrix, draw_category_matrix
import numpy as np











class Explanation( ):


	def __init__( self, goal, exp_type, rules, features, 

		matrix, 

		rule_classes, rule_labels, rule_supports, rule_data_coverages, rule_fisher_pvalues, rule_certainties, cumulative_voting, old_rule_certainties,

		feature_labels, feature_importances, feature_values_min, feature_values_max, global_histograms,

		draw_distribution, bins, distribution_matrix,

		support_matrix_indexes, support_matrix,

		class_names, x_k = None, info_text = None ):


		self.svg_draw_ = None
		self.svg_draw_smatrix_ = None

		self.y = None
		self.instance_names = None


		self.goal = goal
		self.exp_type = exp_type

		self.rules_ = rules
		self.n_rules_ = rules.shape[ 0 ]
		self.features_ = features

		self.matrix = matrix

		self.rule_classes = rule_classes
		self.rule_labels = rule_labels
		self.rule_supports = rule_supports

		self.rule_data_coverages = rule_data_coverages
		self.rule_fisher_pvalues = rule_fisher_pvalues			

		self.rule_certainties = rule_certainties
		self.cumulative_voting = cumulative_voting
		self.old_rule_certainties = old_rule_certainties

		self.feature_labels = feature_labels
		self.feature_importances = feature_importances
		self.feature_values_min = feature_values_min
		self.feature_values_max = feature_values_max
		self.global_histograms = global_histograms

		self.draw_distribution = draw_distribution
		self.bins = bins
		self.distribution_matrix = distribution_matrix

		self.support_matrix_indexes = support_matrix_indexes
		self.support_matrix = support_matrix
		
		self.class_names = class_names
		self.x_k = x_k
		self.info_text = info_text











	def create_svg( self, draw_row_labels = False, draw_col_labels = False, **kwargs ):

		self.row_labels = None
		if draw_row_labels: self.row_labels = self.rule_labels

		self.col_labels = None
		if draw_col_labels: self.col_labels = self.feature_labels


		self.cols_top_legend_1_title = ''


		self.rows_right_legend_2_title = None
		self.rows_right_legend_2 = None
		

		if self.goal == 'data':

			self.cols_top_legend_1_title = 'Variable Importance'

			rows_left_legend_1_title = 'Pattern Support'

			self.rows_right_legend_2_title = 'FET p'
			self.rows_right_legend_2 = self.rule_fisher_pvalues

		elif self.goal == 'model':

			self.cols_top_legend_1_title = 'Feature Importance'

			rows_left_legend_1_title = 'Rule Support'

			if self.exp_type == 'local-used':

				self.rows_right_legend_2_title = 'Cumulative Voting'
				self.rows_right_legend_2 = self.cumulative_voting

			elif self.exp_type == 'local-closest':

				self.rows_right_legend_2_title = 'Old-Rule Certainty'
				self.rows_right_legend_2 = self.old_rule_certainties


		

		self.svg_draw_ = draw_range_matrix( 

			matrix = self.matrix, 
			col_values_min = self.feature_values_min, 
			col_values_max = self.feature_values_max,

			matrix_row_categories = self.rule_classes, 
			category_names = self.class_names, 

			draw_distribution = self.draw_distribution,
			bins = self.bins,
			distribution_matrix = self.distribution_matrix,
			 
			row_labels = self.row_labels,
			col_labels = self.col_labels,

			rows_left_legend_1_title = rows_left_legend_1_title,
			rows_left_legend_1 = self.rule_supports,

			rows_left_legend_2_title = 'Cumulative Coverage',
			rows_left_legend_2 = self.rule_data_coverages,

			cols_top_legend_1_title = self.cols_top_legend_1_title,
			cols_top_legend_1 = self.feature_importances,

			cols_top_legend_2_title = 'Global Histograms',
			cols_top_legend_2 = self.global_histograms,

			rows_right_legend_1_title = 'Rule Certainty',
			rows_right_legend_1 = self.rule_certainties,

			rows_right_legend_2_title = self.rows_right_legend_2_title,
			rows_right_legend_2 = self.rows_right_legend_2,

			x_k = self.x_k,
			info_text = self.info_text,

			**kwargs )











	def save( self, file_name, pixel_scale = 'default' ):

		if '.png' in file_name:

			if pixel_scale != 'default': self.svg_draw_.setPixelScale( pixel_scale )
			else: self.svg_draw_.setPixelScale( 2 )

			self.svg_draw_.savePng( file_name )

			self.svg_draw_.setPixelScale( 1 )

		elif '.svg' in file_name:

			if pixel_scale != 'default': self.svg_draw_.setPixelScale( pixel_scale )
			else: self.svg_draw_.setPixelScale( 1 ) 

			self.svg_draw_.saveSvg( file_name )

			self.svg_draw_.setPixelScale( 1 )
			











	def display_jn( self, display_type = 'svg', pixel_scale = 'default' ):

		if display_type == 'svg':

			if pixel_scale != 'default': self.svg_draw_.setPixelScale( pixel_scale )
			else: self.svg_draw_.setPixelScale( 0.45 )

			return self.svg_draw_

		elif display_type == 'png':

			if pixel_scale != 'default': self.svg_draw_.setPixelScale( pixel_scale )
			else: self.svg_draw_.setPixelScale( 2 ) 

			return self.svg_draw_.rasterize()











	def to_dict( self ):

		result_dict = {}

		result_dict['matrix'] = self.matrix.tolist()

		result_dict['col_values_min'] = self.feature_values_min.tolist()
		result_dict['col_values_max'] = self.feature_values_max.tolist()

		result_dict['row_categories'] = self.rule_classes.tolist()
		result_dict['category_names'] = self.class_names.tolist()
		result_dict['row_labels'] = self.row_labels
		result_dict['rows_left_legend'] = self.rule_supports.tolist() 
		result_dict['rows_right_legend_1'] = self.rule_certainties.tolist()
		result_dict['rows_right_legend_2'] = self.rows_right_legend_2.tolist()
		result_dict['rows_right_legend_2_title'] = self.rows_right_legend_2_title

		result_dict['col_labels'] = self.col_labels
		result_dict['cols_top_legend'] = self.feature_importances.tolist()


		if self.x_k is not None: result_dict['x_k'] = self.x_k.tolist()
		else: result_dict['x_k'] = None
		result_dict['info_text'] = self.info_text


		return result_dict











	def smatrix( self, y = None, instance_names = None ):

		self.y = y
		self.instance_names = instance_names









		

	def create_svg_smatrix( self, draw_row_labels = False, draw_col_labels = False, **kwargs ):


		self.row_labels = None
		if draw_row_labels: self.row_labels = self.rule_labels

		
		aux_labels = None
		if draw_col_labels:

			if self.instance_names is None: aux_labels = self.support_matrix_indexes.astype( 'str' )

			else:

				aux_labels = []

				for i in self.support_matrix_indexes:
					aux_labels.append( self.instance_names[ i ] )

				aux_labels = np.array( aux_labels )


		matrix_col_categories = None
		category_names = None

		if self.y is not None: 

			matrix_col_categories = self.y[ self.support_matrix_indexes ]
			category_names = self.class_names 


		self.svg_draw_smatrix_ = draw_category_matrix( 

			matrix = self.support_matrix,

			title = 'Support Matrix',

			row_labels = self.row_labels,
			col_labels = aux_labels,

			matrix_col_categories = matrix_col_categories,
			category_names = category_names,

			**kwargs )











	def save_smatrix( self, file_name, pixel_scale = 'default' ):
		
		if '.png' in file_name:

			if pixel_scale != 'default': self.svg_draw_smatrix_.setPixelScale( pixel_scale )
			else: self.svg_draw_smatrix_.setPixelScale( 2 )

			self.svg_draw_smatrix_.savePng( file_name )

			self.svg_draw_smatrix_.setPixelScale( 1 )

		elif '.svg' in file_name:

			if pixel_scale != 'default': self.svg_draw_smatrix_.setPixelScale( pixel_scale )
			else: self.svg_draw_smatrix_.setPixelScale( 1 ) 

			self.svg_draw_smatrix_.saveSvg( file_name )

			self.svg_draw_smatrix_.setPixelScale( 1 )











	def display_smatrix_jn( self, display_type = 'svg', pixel_scale = 'default' ):

		if display_type == 'svg':

			if pixel_scale != 'default': self.svg_draw_smatrix_.setPixelScale( pixel_scale )
			else: self.svg_draw_smatrix_.setPixelScale( 0.45 )

			return self.svg_draw_smatrix_

		elif display_type == 'png':

			if pixel_scale != 'default': self.svg_draw_smatrix_.setPixelScale( pixel_scale )
			else: self.svg_draw_smatrix_.setPixelScale( 2 ) 

			return self.svg_draw_smatrix_.rasterize()