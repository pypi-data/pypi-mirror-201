from lrmatrix.matrixmanager import MatrixManager
from lrmatrix.matrixdraw import color_map_category
import numpy as np
from sklearn import tree
from sklearn import preprocessing
from scipy.spatial.distance import pdist, squareform
import math











class VAX( MatrixManager ):

	
	def __init__( self, **kwargs ):

		super().__init__( goal = 'data', **kwargs )











	def fit( self, X, y, f_subsets_sizes = [ 'log2' ], k_trees = 3, class_weight = None, aggregate = True, calc_histograms = True, save_stages = False, file_name = None, npz_format = True, n_jobs = 1, calc_diameters = False, random_seed = None ):

		X = self._check_input_X( X )
		y = self._check_input_y( y )


		if isinstance( f_subsets_sizes, str ) and ( f_subsets_sizes == 'auto' ):

			f_subsets_sizes = [ None ]

			size_values = [] # to not include the same feature size

			n = int( math.sqrt( X.shape[ 1 ] ) )
			if ( n != 0 ) and ( n not in size_values ): 
				f_subsets_sizes.append( 'sqrt' )
				size_values.append( n )

			n = int( math.log2( X.shape[ 1 ] ) )
			if ( n != 0 ) and ( n not in size_values ): 
				f_subsets_sizes.append( 'log2' )
				size_values.append( n )

			n = int( X.shape[ 1 ] * 0.2 ) # arbitrary
			if ( n != 0 ) and ( n not in size_values ): 
				f_subsets_sizes.append( 0.2 )
				size_values.append( n )

			n = int( X.shape[ 1 ] * 0.5 ) # arbitrary
			if ( n != 0 ) and ( n not in size_values ): 
				f_subsets_sizes.append( 0.5 )
				size_values.append( n )


		self.aggregation_metadata_[ 0 ] = k_trees
		self.aggregation_metadata_[ 1 ] = str( f_subsets_sizes )


		tree_array = []
		n_subsets = len( f_subsets_sizes )
		total_trees = k_trees * n_subsets

		
		

		# RFm - Random Forest Miner 
		np.random.seed( seed = random_seed ) # Issue #1 ??

		for t in range( k_trees ):
			for s in range( n_subsets ):

				subsets_size = f_subsets_sizes[ s ]

				if self._verbose > 0: print( 'creating decision tree for data explanation ', ( t * n_subsets ) + ( s + 1 ), ' of ',  total_trees )

				clf = tree.DecisionTreeClassifier( criterion = 'gini', splitter = 'best', max_depth =  None, min_samples_split =  2, min_samples_leaf = 1, max_features = subsets_size, class_weight = class_weight )
				clf.fit( X, y )

				tree_array.append( clf )
			
		np.random.seed( seed = None ) #  Issue #1 ??
		# print( np.random.randint( 100, size = 10 ) ) # to check if random is not fixed after DTs creation ??



		
		self.rules_extration( tree_array, X, y, feature_importances = None, calc_support_coverage = False, calc_diameters = False, n_jobs = n_jobs ) # calc_diameters False, since it not userful at this point 
		if save_stages: self.save( file_name + '-bfagg', npz_format = npz_format )


		self.instances_map_ = self.imap( X, y, map_type = 'binary', by_model = True, n_jobs = n_jobs )
		if save_stages: self.save( file_name + '-bfagg', npz_format = npz_format )


		if aggregate:

			tie_mode, total, filtered, pivots, aggregated, discarded, coverage, discarded_not_checked = self.aggregate_rules( self.instances_map_, min_coverage = 1.0 )
			self.aggregation_metadata_[ 2 ] = tie_mode
			self.aggregation_metadata_[ 3 ] = total
			self.aggregation_metadata_[ 4 ] = filtered
			self.aggregation_metadata_[ 5 ] = pivots
			self.aggregation_metadata_[ 6 ] = aggregated
			self.aggregation_metadata_[ 7 ] = discarded
			self.aggregation_metadata_[ 8 ] = coverage
			self.aggregation_metadata_[ 9 ] = discarded_not_checked

			if save_stages: self.save( file_name, npz_format = npz_format )


		if calc_histograms:
			self.calc_histograms( X, y )
			self.calc_feature_importances()
			if save_stages: self.save( file_name, npz_format = npz_format )


		if calc_diameters: # ??
			self.calc_rules_ranges_diameter()
			if save_stages: self.save( file_name, npz_format = npz_format )


		return tree_array












	def __mat_W( self, shape, lam ):

		d = shape[ 1 ]
		matrix = np.identity( d )

		for i in range( d ):

			if i < d / 2: matrix[ i, i ] *= ( 1 - lam )
			else: matrix[ i, i ] *= lam

		return matrix











	def extend_X( self, X, standard_scaler = True, lam = None ):

		
		X_ext = np.zeros( X.shape, dtype = X.dtype ) 
		

		y_pclass = np.full( X.shape[ 0 ], -1 ).astype(int)
		

		for p in range( self.instances_map_.shape[ 0 ] ):

			instances = self.instances_map_[ p, : ].nonzero()[ 1 ]
			y_pclass[ instances ] = p


			for f in range( X_ext.shape[ 1 ] ):
				X_ext[ instances, f ] = X[ instances, f ].mean()


		X_ext = np.hstack( ( X, X_ext ) )


		if standard_scaler == True: X_ext = preprocessing.StandardScaler().fit_transform( X_ext )


		if lam is not None:

			W = self.__mat_W( X_ext.shape, lam )
			X_ext = np.dot( X_ext, W )


		return X_ext, y_pclass











	# based 1964 Multidimensional Scaling By Optimizing Goodness Of Fit To A Nonmetric Hypothesis, with 0.5 since i > j (only half matrix is used)

	def kruskal_stress( self, X_2, X_1, metric ):

		dist_2 = squareform( pdist( X_2, metric = metric ) ) # ??
		dist_1 = squareform( pdist( X_1, metric = metric ) )
		
		raw_stress = 0.5 * np.sum( ( dist_2 - dist_1 ) ** 2 )
		stress = np.sqrt( raw_stress / ( 0.5 * np.sum( dist_1 ** 2 ) ) )
		
		return raw_stress, stress











	def plot_map( self, X, y, patterns, plt, fig = None, ax = None, mode = 'vertical', width = None, height = None, font_legend_size = 12, size = 75, linewidth = 0.75, alpha = 1.0, color_map1 = 'auto', ncol_map1 = 'auto', color_map2 = 'auto', ncol_map2 = 'auto', bbox_to_anchor = ( 0.5, 1.115 ) ):


		plt.rc( 'legend', fontsize = font_legend_size )

		
		if mode == 'vertical': 

			if width is None: width = 8
			if height is None: height = 9

			if( fig is None ) and ( ax is None ): fig, ax = plt.subplots( nrows = 2, ncols = 1, figsize = ( width, height ) )

		elif mode == 'horizontal':

			if width is None: width = 16
			if height is None: height = 4.5

			if( fig is None ) and ( ax is None ): fig, ax = plt.subplots( nrows = 1, ncols = 2, figsize = ( width, height ) )


		if isinstance( color_map1, str ) and ( color_map1 == 'auto' ): 
			color_map1 = [ '#f2f2f2ff' ]
			color_map1.extend( color_map_category[ :self.class_names_.shape[ 0 ] ] )
			color_map1 = np.array( color_map1 )

		if isinstance( color_map2, str ) and ( color_map2 == 'auto' ): 
			color_map2 = [ '#f2f2f2ff' ]
			color_map2.extend( color_map_category[ self.class_names_.shape[ 0 ]: ] )
			color_map2 = np.array( color_map2 )






		ax[ 0 ].tick_params( top = False, bottom = False, left = False, right = False, labelleft = False, labelbottom = False ) # no ticks
		plot1 = ax[ 0 ].scatter( X[ :, 0 ], X[ :, 1 ], s = size, color = color_map1[ y + 1 ], linewidth = linewidth, edgecolor = 'black', alpha = alpha, picker = True ) # ploting

		# legend
		legend = self.class_names_
		if ncol_map1 == 'auto': ncol_map1 = self.class_names_.shape[0]

		handles = []
		for c in range( legend.shape[0] ):
			handles.append( plt.Rectangle( (0, 0), 1, 1, linewidth = linewidth, edgecolor = 'black', facecolor = color_map1[ c + 1 ], alpha = alpha ) )
		ax[ 0 ].legend( handles, legend, ncol = ncol_map1, bbox_to_anchor = bbox_to_anchor, loc = 'upper center' )




		

		y_pclass = np.zeros( y.shape[ 0 ], dtype = int )
		y_pclass[ : ] = -1

		for p in range( patterns.shape[ 0 ] ):	
			instances = self.instances_map_[ patterns[ p ], : ].nonzero()[ 1 ]
			y_pclass[ instances ] = p

		legend = np.array( [ 'p' + str( p + 1 ) for p in  patterns ] )
		if ncol_map2 == 'auto': ncol_map2 = patterns.shape[ 0 ]


		ax[ 1 ].tick_params( top = False, bottom = False, left = False, right = False, labelleft = False, labelbottom = False ) # no ticks
		plot2 = ax[ 1 ].scatter( X[ :, 0 ], X[ :, 1 ], s = size, color = color_map2[ y_pclass + 1 ], linewidth = linewidth, edgecolor = 'black', alpha = alpha, picker = True ) # ploting

		# legend
		handles = []
		for c in range( legend.shape[0] ):
			handles.append( plt.Rectangle( (0, 0), 1, 1, linewidth = linewidth, edgecolor = 'black', facecolor = color_map2[ c + 1 ], alpha = alpha ) )
		ax[ 1 ].legend( handles, legend, ncol = ncol_map2, bbox_to_anchor = bbox_to_anchor, loc = 'upper center' )




		

		return fig, ax