import drawSvg as draw
import numpy as np











color_map_category = [ '#1f77b3', '#ff7e0e', '#bcbc21', '#8c564b', '#9367bc', '#e277c1', '#ffdb00', '#8a2844', '#00aa79', '#d89c00', '#a3a39e', '#46490c', '#7b6985', '#6b978c', '#ff9a75', '#835bff', '#7c6b46', '#80b654', '#bc0049', '#fd93ff', '#5d0018', '#89d1d1', '#9c8cd3', '#3f69ff', '#aa3baf' ] # https://www.color-hex.com/
color_map_binary = [ '#4daf4a','#984ea3' ]











n_rows_ = n_cols_ = None
margin_top_ = margin_right_ = margin_bottom_ = margin_left_ = None
inner_width_ = inner_height_ = None
inner_pad_row_ = inner_pad_col_ = None
col_values_max_ = col_values_min_ = None
precision_ = None











def scale( x, x_min, x_max, new_min, new_max ):
	return ( ( ( ( new_max - new_min ) * ( x - x_min ) ) / ( x_max - x_min ) ) + new_min )



def row_scale( r ):
	return scale( r, 0, n_rows_, 0, inner_height_ )



def col_scale( c ):
	return scale( c, 0, n_cols_, 0, inner_width_ )



def draw_row_label( g, r, label, font_size, rec_height, pad ):
	g.append( draw.Text( label, font_size, -pad, -( row_scale( r ) + ( rec_height / 2 ) + ( font_size / 2 )  + ( inner_pad_row_ * r ) ), text_anchor = 'end', fill = '#000000' ) )



def draw_col_label( g, c, label, font_size, degrees, pad ):

	if degrees == 0: text_anchor = 'middle'
	else: text_anchor = 'start'

	g_label = draw.Group( transform = f'translate( { col_scale( c ) + ( inner_pad_col_ * c ) }, { inner_height_ + pad } )' )
	g_label.append( draw.Text( label, font_size,  0, 0, transform = f'rotate( { degrees } )', text_anchor = text_anchor, fill = '#000000' ) )
	g.append( g_label )



def draw_title( g, title, font_size, pad ):
	g.append( draw.Text( title, font_size, ( inner_width_ / 2 ), ( pad ), text_anchor = 'middle', fill = '#000000' ) )



def draw_rows_axis_label( g, label, font_size, pad ):

	g_label = draw.Group( transform = f'translate( { -pad }, { inner_height_ / 2 } )' )					
	g_label.append( draw.Text( label, font_size,  0, 0, transform = 'rotate( -90 )', text_anchor = 'middle', fill = '#000000' ) )
	g.append( g_label  )



def draw_cols_axis_label( g, label, font_size, pad ):
	g.append( draw.Text( label, font_size, ( inner_width_ / 2 ), -( inner_height_ +  pad ), text_anchor = 'middle', fill = '#000000' ) )


import xml.sax.saxutils as xml

class Title( draw.DrawingParentElement ):
    
    TAG_NAME = 'title'
    hasContent = True

    def __init__( self, text, **kwargs ):

    	self.text = text
    	super().__init__( **kwargs )

    def writeContent(self, idGen, isDuplicate, outputFile, dryRun):
        if dryRun:
            return
        outputFile.write( xml.escape( self.text ) )











color_map_category_ = []


color_map_binary_ = []


from matplotlib.colors import LinearSegmentedColormap, to_hex

custom_colors = [ '#F5F5F5', '#303030' ]
linear_grey_scale = LinearSegmentedColormap.from_list( 'custom_linear_grey_scale', custom_colors )

def to_grey( value ):
	return to_hex( linear_grey_scale( value ) )









def col_range_scale( c, alpha, beta, rec_width ):

	c_0 = scale( c, 0, n_cols_, 0, inner_width_ )

	alpha = scale( alpha, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )
	beta = scale( beta, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )

	c_p = c_0 + alpha
	rec_width_p = beta - alpha

	return c_p, rec_width_p











def col_delta_scale( c, x_k_f, alpha, beta, rec_width ):

	c_0 = scale( c, 0, n_cols_, 0, inner_width_ )

	x_k_f = scale( x_k_f, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )

	alpha = scale( alpha, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )
	beta = scale( beta, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )

	if x_k_f < alpha:

		c_p = c_0 + x_k_f
		rec_width_p = alpha - x_k_f

	elif x_k_f > beta:

		c_p = c_0 + beta
		rec_width_p = x_k_f - beta

	return c_p, rec_width_p











def draw_range_matrix_legend( g, category_names, pad, binary_legend = None, info_text = None, rec_width_height = 35, stroke = '#000000', stroke_width = 1, font_size = 16, ratio = 1.0 ):

	rec_width_height *= ratio
	font_size *= ratio
	stroke_width *= ratio


	for ctg in range( category_names.shape[ 0 ] ):

		fill = color_map_category_[ ctg ]

		g.append( draw.Rectangle( 0 + pad, str( ( ctg * rec_width_height ) ), rec_width_height, rec_width_height, fill = fill, stroke = stroke, stroke_width = stroke_width ) )

		g.append( draw.Text( category_names[ ctg ], font_size, ( pad + ( rec_width_height * 1.2 ) ), -( ( ctg * rec_width_height ) + (rec_width_height / 2 ) + ( font_size / 2 ) ), text_anchor = 'start', fill = '#000000' ) )



	gradient_y_sta = ( category_names.shape[ 0 ] * rec_width_height ) + ( rec_width_height * 1 )
	gradient_y_end = ( category_names.shape[ 0 ] * rec_width_height ) + ( rec_width_height * 6 )

	gradient_x_sta = pad + ( rec_width_height * 1.2 )

	tick_width = 10

	ticks = [ 1.0, 0.75, 0.50, 0.25, 0.0 ]
	n_ticks = len( ticks )
	tick_space = ( gradient_y_end - gradient_y_sta ) / ( n_ticks - 1 )


	gradient = draw.LinearGradient( '0%', '0%', '0%', '100%', gradientUnits = None )
	gradient.addStop( offset = '0%', color = to_grey( 1.0 ) )
	gradient.addStop( offset = '25%', color = to_grey( 0.75 ) )
	gradient.addStop( offset = '50%', color = to_grey( 0.50 ) )
	gradient.addStop( offset = '75%', color = to_grey( 0.25 ) )
	gradient.addStop( offset = '100%', color = to_grey( 0.0 ) )

	
	g.append( draw.Rectangle( 0 + pad, str( gradient_y_sta ), rec_width_height, ( rec_width_height * 5 ), fill = gradient, stroke = stroke, stroke_width = stroke_width ) )

	g.append( draw.Lines( gradient_x_sta, -( gradient_y_sta ), gradient_x_sta, -( gradient_y_end ), stroke = stroke, stroke_width = stroke_width * 1.2 ) )


	for i in range( n_ticks ):

		gradient_y = gradient_y_sta + ( tick_space * i )

		g.append( draw.Lines( gradient_x_sta, -( gradient_y ), gradient_x_sta + tick_width, -( gradient_y ), stroke = stroke, stroke_width = stroke_width * 1.2 ) )

		g.append( draw.Text( str( ticks[ i ] ), font_size, ( pad + ( rec_width_height * 1.6 ) ), -( gradient_y + ( font_size / 4 ) ), text_anchor = 'start', fill = '#000000' ) )



	info_text_y = gradient_y_end + rec_width_height

	if binary_legend is not None:

		info_text_y += ( rec_width_height * 3 )

		for p in range( 2 ):

			fill = color_map_binary_[ p ]
			g.append( draw.Rectangle( 0 + pad, str( gradient_y_end + rec_width_height * ( p + 1 ) ), rec_width_height, rec_width_height, fill = fill, stroke = stroke, stroke_width = stroke_width ) )
			g.append( draw.Text( binary_legend[ p ], font_size, ( pad + ( rec_width_height * 1.2 ) ), -( ( gradient_y_end + rec_width_height * ( p + 1 ) ) + (rec_width_height / 2 ) + ( font_size / 2 ) ), text_anchor = 'start', fill = '#000000' ) )


	if info_text is not None: g.append( draw.Text( info_text, font_size, ( 0 + pad ), -( info_text_y ), text_anchor = 'start', fill = '#000000' ) )











def draw_rows_left_legend( g, legend, rec_height, title, pad, rec_width = 75, stroke = '#000000', stroke_width = 1, font_size = 16, draw_box = False, draw_frame = False, rows_left_legend_show_value = True ):

	title = title.split()
	g.append( draw.Text( title[ 0 ], font_size, -( ( rec_width / 2 ) + pad ), ( 15 + ( font_size * 1.05 ) ), text_anchor = 'middle', fill = '#000000' ) )
	g.append( draw.Text( title[ 1 ], font_size, -( ( rec_width / 2 ) + pad ), ( 15 ), text_anchor = 'middle', fill = '#000000' ) )


	for r in range( n_rows_ ):

		value = legend[ r ]

		fill = to_grey( value )
		width = rec_width * value

		g_si = draw.Group()
		value = np.round( value, decimals = precision_ )
		g_si.append( Title( text = str( value ) ) )

		if draw_box:

			g_si.append( draw.Rectangle( 0 - rec_width - pad, str( row_scale( r ) + ( inner_pad_row_ * r ) ), width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = stroke, stroke_width = stroke_width ) )
			g_si.append( draw.Rectangle( 0 - rec_width - pad, str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = 'none', fill_opacity = 0.0, stroke = stroke, stroke_width = stroke_width ) )

		else: g_si.append( draw.Rectangle( 0 - rec_width - pad, str( row_scale( r ) + ( inner_pad_row_ * r ) ), width, rec_height, shape_rendering = 'crispEdges', fill = fill ) )

		if rows_left_legend_show_value: 

			g.append( draw.Text( str( value ), font_size, -( pad - 10 ), -( row_scale( r + 0.5 ) + ( font_size * 0.5 ) + ( inner_pad_row_ * r ) ), text_anchor = 'left', fill = '#000000' ) )

		g.append( g_si )


	if draw_frame: g.append( draw.Rectangle( 0 - rec_width - pad, '0', rec_width, inner_height_ + ( inner_pad_row_ * n_rows_ ), fill = 'none', stroke = stroke, stroke_width = stroke_width ) )










def draw_rows_right_legend( g, legend, rec_height, title, pad, rec_width = 75, stroke = '#000000', stroke_width = 1, font_size = 16, draw_box = False, draw_frame = False, draw_change_line = False ):

	title = title.split()

	g.append( draw.Text( title[ 0 ], font_size, ( ( rec_width / 2 ) + pad ), ( 15 + ( font_size * 1.05 ) ), text_anchor = 'middle', fill = '#000000' ) )
	g.append( draw.Text( title[ 1 ], font_size, ( ( rec_width / 2 ) + pad ), ( 15 ), text_anchor = 'middle', fill = '#000000' ) )

	
	if draw_change_line: old_argmax = np.argmax( legend[ 0 ] )

	
	for r in range( n_rows_ ):

		if legend.ndim >= 2:

				width_sum = 0
				for c in range( legend.shape[ 1 ] ):

					value = legend[ r, c ]
					
					fill = color_map_category_[ c ]
					width = rec_width * value

					g_si = draw.Group()
					g_si.append( Title( text = str( np.round( value, decimals = precision_ ) ) ) )

					if draw_box: g_si.append( draw.Rectangle( 0 + pad + width_sum, str( row_scale( r ) + ( inner_pad_row_ * r ) ), width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = stroke, stroke_width = stroke_width ) )
					else: g_si.append( draw.Rectangle( 0 + pad + width_sum, str( row_scale( r ) + ( inner_pad_row_ * r ) ), width, rec_height, shape_rendering = 'crispEdges', fill = fill ) )

					g.append( g_si )

					width_sum += width

		else: 

			value = legend[ r ]

			g_si = draw.Group()
			g_si.append( Title( text = str( np.round( value, decimals = precision_ ) ) ) )

			if value >= 0.05: fill = color_map_binary_[ 1 ] # 0.05 ??
			else: fill = color_map_binary_[ 0 ]

			if draw_box: g_si.append( draw.Rectangle( 0 + pad, str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = stroke, stroke_width = stroke_width ) )
			else: g_si.append( draw.Rectangle( 0 + pad, str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = fill ) )

			g.append( g_si )


		if draw_change_line: 
			argmax = np.argmax( legend[ r ] )
			if old_argmax != argmax:
				old_argmax = argmax
				
				g.append( draw.Lines( ( pad ), -( row_scale( r + 0.5 ) ), rec_width + ( pad ), -( row_scale( r + 0.5 ) ), stroke = stroke, stroke_width = stroke_width * 2 ) )


	if draw_frame: g.append( draw.Rectangle( 0 + pad, '0', rec_width, inner_height_ + ( inner_pad_row_ * ( n_rows_ - 1 ) ), fill = 'none', stroke = stroke, stroke_width = stroke_width ) ) 











def draw_cols_top_legend( g, legend, rec_width, title, pad, rec_height = 20, stroke = '#000000', stroke_width = 1, font_size = 16, draw_box = True, draw_frame = False ):

	g.append( draw.Text( title, font_size, ( ( inner_width_ + ( inner_pad_col_ * ( n_cols_ - 1 ) ) ) / 2 ), ( rec_height + pad + 15 ), text_anchor = 'middle', fill = '#000000' ) )
	
	for c in range( n_cols_ ):

		value = legend[ c ]

		fill = to_grey( value )
		width = rec_width * value

		g_si = draw.Group( transform = f'translate( { col_scale( c ) + ( inner_pad_col_ * c ) }, { -( rec_height + pad ) } )' )

		if draw_box: 

			g_si.append( draw.Rectangle( 0, '0', width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = stroke, stroke_width = stroke_width ) )
			g_si.append( draw.Rectangle( 0, '0', rec_width, rec_height, shape_rendering = 'crispEdges', fill = 'none', stroke = stroke, stroke_width = stroke_width ) )
		
		else: g_si.append( draw.Rectangle( 0, '0', width, rec_height, shape_rendering = 'crispEdges', fill = fill ) )

		g_si.append( Title( text = str( np.round( value, decimals = precision_ ) ) ) )
		g.append( g_si )


	if draw_frame: g.append( draw.Rectangle( 0, str( -( rec_height + pad ) ), inner_width_, rec_height, fill = 'none', stroke = stroke, stroke_width = stroke_width ) )











def draw_cols_top_legend_2( g, legend, rec_width, title, pad, bins, rec_height = 20, rec_height_fix = 1.5, stroke = '#000000', stroke_width = 1, font_size = 16, draw_cols_line = False ):

	g.append( draw.Text( title, font_size, ( ( inner_width_ + ( inner_pad_col_ * ( n_cols_ - 1 ) ) ) / 2 ), ( rec_height + pad + 15 ), text_anchor = 'middle', fill = '#000000' ) )

	rec_width_bin = rec_width / bins

	for r in range( legend.shape[ 0 ] ):

		fill = color_map_category_[ r ]
		
		for c in range( n_cols_ ):

			g_si = draw.Group( transform = f'translate( { col_scale( c ) }, { -( rec_height + pad ) } )' )

			g_si.append( Title( text = np.array2string( np.array( [ col_values_min_[ c ], col_values_max_[ c ] ] ), precision = precision_, separator = ',', suppress_small = True ) ) )

			b_str = ( c * bins )
			b_end = ( c * bins ) + bins			
			

			g_si.append( draw.Rectangle( 0 + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = fill, fill_opacity = 0.25 ) )


			for p in range( bins ): 
				
				value = legend[ r, ( ( c * bins ) + p ) ]
				r_p = r + ( 1 - value )
				rec_height_p = rec_height * value


				if ( value != 0 ) and ( rec_height_fix > rec_height_p ):

					rec_height_p += rec_height_fix # histogram bar too small, not even showing

					value = rec_height_p / rec_height
					r_p = r + ( 1 - value )


				g_aux = draw.Group()
				# g_aux.append( Title( text = np.array2string( legend[ r, b_str:b_end ], precision = precision_, separator = ',', suppress_small = True ) ) ) # todos os bins ??
				g_aux.append( Title( text = np.array2string( value, precision = precision_, separator = ',', suppress_small = True ) ) ) # somente o valor do bin ??

				g_aux.append( draw.Rectangle( 0 + ( rec_width_bin * p ) + ( inner_pad_col_ * c ), str( row_scale( r_p ) + ( inner_pad_row_ * r ) ), rec_width_bin, rec_height_p, shape_rendering = 'crispEdges', fill = fill ) )

				g_si.append( g_aux )


			if draw_cols_line: g_si.append( draw.Rectangle( 0 + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = None, fill_opacity = 0.0, stroke = stroke, stroke_width = stroke_width ) )


			g.append( g_si )











def draw_x_lines( g, x_k, rec_width, pad, stroke = '#000000', stroke_width = 2 ):

	for c in range( x_k.shape[ 0 ] ):

		x_k_f = x_k[ c ]

		c_p = col_scale( c + ( scale( x_k_f, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width ) / rec_width ) ) + ( inner_pad_col_ * c )

		g_si = draw.Group()
		g_si.append( Title( text = str( np.round( x_k_f, decimals = precision_ ) ) ) )
		g_si.append( draw.Lines( c_p, 0, c_p, -inner_height_ - pad, stroke = stroke, stroke_width = stroke_width, stroke_dasharray = '7,14' ) )

		g.append( g_si )











def draw_row_line( g, r, stroke, stroke_width ):
	g.append( draw.Lines( 0, -( row_scale( r ) + ( ( inner_pad_row_ * r ) - inner_pad_row_ / 2 ) ), inner_width_ + ( inner_pad_col_ * ( n_cols_ - 1 ) ), -( row_scale( r ) + ( ( inner_pad_row_ * r ) - inner_pad_row_ / 2 ) ), stroke = stroke, stroke_width = stroke_width ) )


def draw_col_line( g, c, stroke, stroke_width ):
	g.append( draw.Lines( col_scale( c ) + ( ( inner_pad_col_ * c ) - inner_pad_col_ / 2 ), 0, col_scale( c ) + ( ( inner_pad_col_ * c ) - inner_pad_col_ / 2 ), -inner_height_ - ( inner_pad_row_ * ( n_rows_ - 1 ) ), stroke = stroke, stroke_width = stroke_width ) )











def draw_range_matrix( matrix, col_values_min, col_values_max, matrix_row_categories, category_names,

	draw_distribution = False, distribution_matrix = None, bins = 5,

	cols_top_legend_1 = None, cols_top_legend_1_title = None, cols_top_legend_2 = None, cols_top_legend_2_title = None, draw_box_col_top_legend = True, draw_frame_top_legend = True,

	rows_left_legend_1 = None, rows_left_legend_1_title = None, rows_left_legend_2 = None, rows_left_legend_2_title = None, draw_box_row_left_legend = True, draw_frame_left_legend = True, rows_left_legend_show_value = False,

	rows_right_legend_1 = None, rows_right_legend_1_title = None, rows_right_legend_2 = None, rows_right_legend_2_title = None, rows_right_legend_width = 75, draw_box_row_right_legend = True, draw_frame_right_legend = True,

	x_k = None, draw_x_k = False, draw_deltas = False, info_text = None, draw_change_line = False,

	width = 2160, height = 1080, margin_top = 125, margin_right = 550, margin_bottom = 100, margin_left = 300, font_size = 25,

	title = None, title_font_size = 25, title_pad = 30,

	rows_axis_label = None, rows_axis_label_font_size = None, pad_row_axis_label = 175, row_labels = None, row_label_font_size = None, pad_row_label = 15, draw_rows_line = False, inner_pad_row = 0,

	cols_axis_label = None, cols_axis_label_font_size = None, pad_col_axis_label = 115, col_labels = None, col_label_degrees = 0, col_label_font_size = None, pad_col_label = 50, draw_cols_line = False, inner_pad_col = 0,

	rec_width_fix = 5.0, rec_height_fix = 1.5, background_color = '#ffffff', cell_background = 'none', cell_background_color = 'auto', draw_range_box = False, draw_box_frame = True, draw_legend = True, stroke = '#000000', stroke_width = 2,

	color_map_category = color_map_category, color_map_binary = color_map_binary, 

	binary_legend = None, precision = 2, matrix_legend_ratio = 1.0 ):


	global n_rows_ , n_cols_, margin_top_, margin_right_, margin_bottom_, margin_left_, inner_width_, inner_height_, inner_pad_row_, inner_pad_col_, col_values_max_, col_values_min_, color_map_category_, color_map_binary_, precision_


	if rows_axis_label_font_size is None: rows_axis_label_font_size = font_size
	if row_label_font_size is None: row_label_font_size = font_size
	if cols_axis_label_font_size is None: cols_axis_label_font_size = font_size
	if col_label_font_size is None: col_label_font_size = font_size

	
	color_map_category_ = color_map_category
	color_map_binary_ = color_map_binary


	n_rows_ = matrix.shape[ 0 ]
	n_cols_ = int( matrix.shape[ 1 ] / 2 )


	col_values_max_ = col_values_max
	col_values_min_ = col_values_min


	margin_top_ = margin_top
	margin_right_= margin_right
	margin_bottom_ = margin_bottom
	margin_left_ = margin_left


	inner_width_ = width - margin_right_ - margin_left_
	inner_height_ = height - margin_top_ - margin_bottom_

	rec_width = inner_width_ / n_cols_
	rec_height = inner_height_ / n_rows_


	inner_pad_row_ = inner_pad_row
	inner_pad_col_ = inner_pad_col

	pad_col_label += ( inner_pad_row_ * n_rows_ )


	precision_ = precision



	d = draw.Drawing( width, height, origin = ( 0, -height ) ) # bug - use arg y as string, except for text ??
	if background_color is not None: d.append( draw.Rectangle( 0, '0', width, height, fill = background_color ) ) # background_color

	g_matrix = draw.Group( transform = f'translate( { margin_left_ }, { margin_top_ } )' )



	for r in range( n_rows_ ):		

		for c in range( n_cols_ ):

			a = c * 2
			b = a + 1

			alpha = matrix[ r, a ]
			beta = matrix[ r, b ]

			fill = color_map_category_[ matrix_row_categories[ r ] ]



			if ( alpha != 0.0 ) or ( beta != 0.0 ):


				
				if not draw_deltas:



					g_si = draw.Group()
					g_si.append( Title( text = np.array2string( np.array( [ col_values_min_[ c ], col_values_max_[ c ] ] ), precision = precision_, separator = ',', suppress_small = True ) ) )

					if ( cell_background == 'all' ) or ( cell_background == 'used' ): g_si.append( draw.Rectangle( col_scale( c ) + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = 'none', fill_opacity = 0.25 ) )
					else: g_si.append( draw.Rectangle( col_scale( c ) + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = '#ffffff', stroke = 'none' ) )
					
					g_matrix.append( g_si )



					if draw_distribution == True:

						rec_width_bin = rec_width / bins

						# g_si = draw.Group()
						# b_str = ( c * bins )
						# b_end = ( c * bins ) + bins
						# g_si.append( Title( text = np.array2string( distribution_matrix[ r, b_str:b_end ], precision = precision_, separator = ',', suppress_small = True ) ) ) # todos os bins ??

						for p in range( bins ):

							g_si = draw.Group() 
				
							value = distribution_matrix[ r, ( ( c * bins ) + p ) ]
							r_p = r + ( 1 - value )
							rec_height_p = rec_height * value


							if ( value != 0 ) and ( rec_height_fix > rec_height_p ):

								rec_height_p += rec_height_fix # histogram bar too small, not even showing

								value = rec_height_p / rec_height
								r_p = r + ( 1 - value )


							g_si.append( Title( text = np.array2string( value, precision = precision_, separator = ',', suppress_small = True ) ) ) # somente o valor do bin ??

							g_si.append( draw.Rectangle( col_scale( c ) + ( rec_width_bin * p ) + ( inner_pad_col_ * c ), str( row_scale( r_p ) + ( inner_pad_row_ * r ) ), rec_width_bin, rec_height_p, shape_rendering = 'crispEdges', fill = fill ) )

							g_matrix.append( g_si )



					if ( draw_distribution == False ) or ( draw_range_box == True ):


						if draw_distribution == True: fill_aux = 'None'
						else: fill_aux = fill


						c_p, rec_width_p = col_range_scale( c, matrix[ r, a ], matrix[ r, b ], rec_width )


						if rec_width_fix > rec_width_p: # range too small, not even showing

							rec_width_p = rec_width_fix # so the range is size fixed

							if ( ( c + 1 ) * rec_width ) - c_p < rec_width_fix: c_p -= rec_width_fix # when fixing the width results the rectangle shape occupying the right cell

						if ( rec_width - rec_width_p ) < rec_width_fix: # range too big, leading to the conclusion of being the complete range, occupying all cell width

							rec_width_p = rec_width - rec_width_fix

							if ( matrix[ r, b ] == col_values_max_[ c ] ): c_p = ( c * rec_width ) + rec_width_fix


						g_si = draw.Group()
						g_si.append( Title( text = np.array2string( np.array( [ alpha, beta ] ), precision = precision_, separator = ',', suppress_small = True ) ) )

						if draw_range_box == False: g_si.append( draw.Rectangle( c_p + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width_p, rec_height, shape_rendering = 'crispEdges', fill = fill_aux ) )
						else: g_si.append( draw.Rectangle( c_p + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width_p, rec_height, shape_rendering = 'crispEdges', fill = fill_aux, stroke = stroke, stroke_width = stroke_width ) )
						
						g_matrix.append( g_si )	


				elif ( x_k[ c ] < alpha ) or ( x_k[ c ] > beta ):


					x_k_f = x_k[ c ]
					c_p, rec_width_p = col_delta_scale( c, x_k_f, alpha, beta, rec_width )

					if x_k_f < alpha:

						fill = color_map_binary_[ 0 ]
						rect_info = str( np.round( alpha - x_k_f, decimals = precision_ ) )						

					elif x_k_f > beta:

						fill = color_map_binary_[ 1 ]
						rect_info = str( np.round( beta - x_k_f, decimals = precision_ ) )


					if cell_background == 'used': g_matrix.append( draw.Rectangle( col_scale( c ), str( row_scale( r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = 'none', opacity = 0.25 ) ) # cell background

					g_si = draw.Group()
					g_si.append( Title( text = rect_info ) )
					g_si.append( draw.Rectangle( c_p, str( row_scale( r ) ), rec_width_p, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = 'none' ) )
					g_matrix.append( g_si )



			else: # if there is no range, it may be a histrogram and cell can be colored by class or 'cell_background_color'



				used_cell = False
				if draw_distribution == True:

					indexes = list( range( ( c * bins ), ( ( c * bins ) + bins ) ) )
					is_hist = distribution_matrix[ r, indexes ].sum() != 0


					if is_hist == True:

						used_cell = True


						if ( cell_background == 'all' ) or ( cell_background == 'used' ):

							g_si = draw.Group()
							g_si.append( draw.Rectangle( col_scale( c ) + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = 'none', fill_opacity = 0.25 ) )					
							g_matrix.append( g_si )


						rec_width_bin = rec_width / bins

						# g_si = draw.Group()
						# b_str = ( c * bins )
						# b_end = ( c * bins ) + bins
						# g_si.append( Title( text = np.array2string( distribution_matrix[ r, b_str:b_end ], precision = precision_, separator = ',', suppress_small = True ) ) ) # todos os bins ??

						for p in range( bins ):

							g_si = draw.Group() 
				
							value = distribution_matrix[ r, ( ( c * bins ) + p ) ]
							r_p = r + ( 1 - value )
							rec_height_p = rec_height * value


							if ( value != 0 ) and ( rec_height_fix > rec_height_p ):

								rec_height_p += rec_height_fix # histogram bar too small, not even showing

								value = rec_height_p / rec_height
								r_p = r + ( 1 - value )


							g_si.append( Title( text = np.array2string( value, precision = precision_, separator = ',', suppress_small = True ) ) ) # somente o valor do bin ??

							g_si.append( draw.Rectangle( col_scale( c ) + ( rec_width_bin * p ) + ( inner_pad_col_ * c ), str( row_scale( r_p ) + ( inner_pad_row_ * r ) ), rec_width_bin, rec_height_p, shape_rendering = 'crispEdges', fill = fill ) )

							g_matrix.append( g_si )


				if ( used_cell == False ) and ( cell_background == 'all' ):

					if cell_background_color == 'auto': 

						fill_aux = fill
						fill_opacity_aux = 0.25

					else: 

						fill_aux = cell_background_color 
						fill_opacity_aux = 1.0

					g_si = draw.Group()
					g_si.append( draw.Rectangle( col_scale( c ) + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = fill_aux, stroke = 'none', fill_opacity = fill_opacity_aux ) )					
					g_matrix.append( g_si )







	pad = 30
	pad_row_label += 75 + pad





	if title is not None: draw_title( g_matrix, title, title_font_size, title_pad )
	if rows_axis_label is not None: draw_rows_axis_label( g_matrix, rows_axis_label, font_size = rows_axis_label_font_size, pad = pad_row_axis_label )
	if cols_axis_label is not None: draw_cols_axis_label( g_matrix, cols_axis_label, font_size = cols_axis_label_font_size, pad = pad_col_axis_label )





	if draw_box_frame: g_matrix.append( draw.Rectangle( 0, str( 0 ), inner_width_ + ( inner_pad_col_ * ( n_cols_ - 1 ) ), inner_height_ + ( inner_pad_row_ * ( n_rows_ - 1 ) ), fill = 'none', stroke = stroke, stroke_width = stroke_width ) ) # matrix box frame




	if ( col_labels is not None ) or draw_cols_line: 
		for c in range( n_cols_ ):

			if col_labels is not None: 

				if ( x_k is not None ) and draw_x_k:
					
					c_p = c + ( scale( x_k[ c ], col_values_min_[ c ], col_values_max_[ c ], 0, rec_width ) / rec_width )
					draw_col_label( g_matrix, c_p, col_labels[ c ], col_label_font_size, col_label_degrees, pad = pad_col_label )

				else: draw_col_label( g_matrix, ( c + 0.5 ), col_labels[ c ], col_label_font_size, col_label_degrees, pad = pad_col_label )

			if draw_cols_line and ( c <= n_cols_ - 2 ): draw_col_line( g_matrix, c + 1, stroke, stroke_width )





	if ( x_k is not None ) and draw_x_k: draw_x_lines( g_matrix, x_k, rec_width, pad_col_label - pad, stroke_width = stroke_width * 1.7 )
	




	g_left_legend = draw.Group( transform = f'translate( { margin_left_ }, { margin_top_ } )' )

	
	if rows_left_legend_2 is not None:

		if rows_left_legend_show_value == True: pad += 60
		draw_rows_left_legend( g_left_legend, rows_left_legend_2, rec_height, rows_left_legend_2_title, pad = pad, font_size = font_size, stroke = stroke, stroke_width = stroke_width, draw_box = draw_box_row_left_legend, draw_frame = draw_frame_left_legend, rows_left_legend_show_value = rows_left_legend_show_value )
		pad += 75
		if rows_left_legend_show_value == True: 
			pad += 45
			pad_row_label += 135
		pad_row_label += 45




	if rows_left_legend_show_value == True: 
		pad += 45
		pad_row_label += 45
	draw_rows_left_legend( g_left_legend, rows_left_legend_1, rec_height, rows_left_legend_1_title, pad = pad, font_size = font_size, stroke = stroke, stroke_width = stroke_width, draw_box = draw_box_row_left_legend, draw_frame = draw_frame_left_legend, rows_left_legend_show_value = rows_left_legend_show_value )




	if ( row_labels is not None ) or draw_rows_line: 
		for r in range( n_rows_ ): 
			
			if row_labels is not None: draw_row_label( g_matrix, r, row_labels[ r ], font_size = row_label_font_size, rec_height = rec_height, pad = pad_row_label )

			if draw_rows_line and ( r <= n_rows_ - 2 ): draw_row_line( g_matrix, r + 1, stroke, stroke_width )




	g_top_legend = draw.Group( transform = f'translate( { margin_left_ }, { margin_top_ } )' )
	pad = 15
	if cols_top_legend_1 is not None:
		if cols_top_legend_2 is not None: pad += 15 + 100 + ( rec_height * category_names.shape[ 0 ] )
		draw_cols_top_legend( g_top_legend, cols_top_legend_1, rec_width, title = cols_top_legend_1_title, pad = pad, font_size = font_size, stroke_width = stroke_width, draw_box = draw_box_col_top_legend, draw_frame = draw_frame_top_legend )




	if cols_top_legend_2 is not None:
		pad = 15 + ( rec_height * category_names.shape[ 0 ] )
		draw_cols_top_legend_2( g_top_legend, cols_top_legend_2, rec_width, rec_height = rec_height, rec_height_fix = rec_height_fix, title = cols_top_legend_2_title, pad = pad, bins = bins, draw_cols_line = draw_cols_line, font_size = font_size, stroke = stroke, stroke_width = stroke_width )




	g_right_legend = draw.Group( transform = f'translate( { margin_left_ + inner_width_ }, { margin_top_ } )' )
	pad = 30 + ( inner_pad_col_ * ( n_cols_ - 1 ) )

	if rows_right_legend_1 is not None:

		draw_rows_right_legend( g_right_legend, rows_right_legend_1, rec_height, rows_right_legend_1_title, pad = pad, rec_width = rows_right_legend_width, font_size = font_size, stroke_width = stroke_width, draw_box = draw_box_row_right_legend, draw_frame = draw_frame_right_legend )
		pad += 95




	if rows_right_legend_2 is not None: 

		pad += 25
		draw_rows_right_legend( g_right_legend, rows_right_legend_2, rec_height, rows_right_legend_2_title, pad = pad, rec_width = rows_right_legend_width, draw_change_line = draw_change_line, font_size = font_size, stroke_width = stroke_width, draw_box = draw_box_row_right_legend, draw_frame = draw_frame_right_legend )
		pad += 95



	pad += 45
	if draw_legend: draw_range_matrix_legend( g_right_legend, category_names, binary_legend = binary_legend, info_text = info_text, pad = pad, font_size = font_size, stroke = stroke, stroke_width = stroke_width, ratio = matrix_legend_ratio )	
	
	

	d.append( g_matrix )
	d.append( g_left_legend )
	d.append( g_right_legend )
	d.append( g_top_legend )

	return d











def draw_category_matrix_legend( g, category_names, pad, info_text = None, rec_width_height = 35, stroke = '#000000', stroke_width = 1, font_size = 16, ratio = 1.0 ):

	rec_width_height *= ratio
	font_size *= ratio
	stroke_width *= ratio


	for ctg in range( category_names.shape[ 0 ] ):

		fill = color_map_category_[ ctg ]

		g.append( draw.Rectangle( 0 + pad, str( ( ctg * rec_width_height ) ), rec_width_height, rec_width_height, fill = fill, stroke = stroke, stroke_width = stroke_width ) )

		g.append( draw.Text( category_names[ ctg ], font_size, ( pad + ( rec_width_height * 1.2 ) ), -( ( ctg * rec_width_height ) + (rec_width_height / 2 ) + ( font_size / 2 ) ), text_anchor = 'start', fill = '#000000' ) )


	info_text_y = ( ( category_names.shape[ 0 ] + 2 ) * rec_width_height )

	if info_text is not None: g.append( draw.Text( info_text, font_size, ( 0 + pad ), -( info_text_y ), text_anchor = 'start', fill = '#000000' ) )











def draw_category_matrix( matrix, matrix_col_categories = None, category_names = None,

	width = 2160, height = 1080, margin_top = 75, margin_right = 75, margin_bottom = 75, margin_left = 75, font_size = 25,

	title = None, title_font_size = None, title_pad = 30,

	rows_axis_label = None, rows_axis_label_font_size = None, pad_row_axis_label = 50, row_labels = None, row_label_font_size = None, pad_row_label = 25, inner_pad_row = 0,

	cols_axis_label = None, cols_axis_label_font_size = None, pad_col_axis_label = 50, col_labels = None, col_label_degrees = 0, col_label_font_size = None, pad_col_label = 25, inner_pad_col = 0,

	background_color = '#ffffff', cell_background_color = '#ffffff', color_map_category = color_map_category, 

	draw_box_frame = True, draw_cell_frame = True, stroke = '#000000', stroke_width = 2,  info_text = None, matrix_legend_ratio = 1.0 ):


	global n_rows_, n_cols_, margin_top_, margin_right_, margin_bottom_, margin_left_, inner_width_, inner_height_, inner_pad_row_,	inner_pad_col_


	if title_font_size is None: title_font_size = font_size
	if rows_axis_label_font_size is None: rows_axis_label_font_size = font_size
	if row_label_font_size is None: row_label_font_size = font_size
	if cols_axis_label_font_size is None: cols_axis_label_font_size = font_size
	if col_label_font_size is None: col_label_font_size = font_size


	n_rows_ = matrix.shape[ 0 ]
	n_cols_ = matrix.shape[ 1 ]


	margin_top_ = margin_top
	margin_right_= margin_right
	margin_bottom_ = margin_bottom
	margin_left_ = margin_left


	inner_width_ = width - margin_right_ - margin_left_
	inner_height_ = height - margin_top_ - margin_bottom_

	
	rec_width = inner_width_ / n_cols_
	rec_height = inner_height_ / n_rows_


	inner_pad_row_ = inner_pad_row
	inner_pad_col_ = inner_pad_col

	pad_col_label += ( inner_pad_row_ * n_rows_ )



	d = draw.Drawing( width, height, origin = ( 0, -height ) ) # *** bug - use arg y as string, except for text ?? ***
	if background_color is not None: d.append( draw.Rectangle( 0, '0', width, height, fill = background_color ) ) # background_color

	g_matrix = draw.Group( transform = f'translate( { margin_left_ }, { margin_top_ } )' )

	

	draw_column_labels = True

	for r in range( n_rows_ ):

		
		if row_labels is not None: draw_row_label( g_matrix, r, row_labels[ r ], font_size = row_label_font_size, rec_height = rec_height, pad = pad_row_label )


		for c in range( n_cols_ ):

			
			if ( col_labels is not None ) and draw_column_labels: draw_col_label( g_matrix, ( c + 0.5 ), col_labels[ c ], col_label_font_size, col_label_degrees, pad = pad_col_label )


			fill = cell_background_color
			
			if matrix[ r, c ] != 0:

				if matrix_col_categories is None: fill = '#000000'
				else: fill = color_map_category_[ matrix_col_categories[ c ] ]

			
			if draw_cell_frame == True: g_matrix.append( draw.Rectangle( col_scale( c ) + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, fill = fill, shape_rendering = 'crispEdges', stroke = stroke, stroke_width = stroke_width ) )
			else: g_matrix.append( draw.Rectangle( col_scale( c ) + ( inner_pad_col_ * c ), str( row_scale( r ) + ( inner_pad_row_ * r ) ), rec_width, rec_height, fill = fill, shape_rendering = 'crispEdges' ) )


		draw_column_labels = False




	if draw_box_frame: g_matrix.append( draw.Rectangle( 0, str( 0 ), inner_width_ + ( inner_pad_col_ * ( n_cols_ - 1 ) ), inner_height_ + ( inner_pad_row_ * ( n_rows_ - 1 ) ), fill = 'none', stroke = stroke, stroke_width = stroke_width ) )



	
	if title is not None: draw_title( g_matrix, title, title_font_size, title_pad )
	

	
	if rows_axis_label is not None: draw_rows_axis_label( g_matrix, rows_axis_label, font_size = rows_axis_label_font_size, pad = pad_row_axis_label )


	
	if cols_axis_label is not None: draw_cols_axis_label( g_matrix, cols_axis_label, font_size = cols_axis_label_font_size, pad = pad_col_axis_label )



	g_right_legend = draw.Group( transform = f'translate( { margin_left_ + inner_width_ }, { margin_top_ } )' )
	pad = 50 + ( inner_pad_col_ * ( n_cols_ - 1 ) )

	if ( matrix_col_categories is not None ) and ( category_names is not None ): draw_category_matrix_legend( g_right_legend, category_names, info_text = info_text, pad = pad, font_size = font_size, stroke = stroke, stroke_width = stroke_width, ratio = matrix_legend_ratio )



	d.append( g_matrix )
	d.append( g_right_legend )

	return d