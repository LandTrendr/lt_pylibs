'''LandTrendr Map Definitions.
Used for TimeSync validation.'''

class Struct:
	def __init__(self, **entries): 
		self.__dict__.update(entries)

class ltbands:
	greatest_fast_disturbance = {1: 'YOD', 2: 'MAG', 3: 'DUR'}
	vertyrs = {1: "YR1", 2: "YR2", 3: "YR3", 4: "YR4", 5: "YR5", 6: "YR6", 7: "YR7"}
	vertvals = {1: "VAL1", 2: "VAL2", 3: "VAL3", 4: "VAL4", 5: "VAL5", 6: "VAL6", 7: "VAL7"}

class ltbands_robust:
	greatest_fast_disturbance = {1: 'YEAR OF DISTURBANCE', 2: 'SCALED MAGNITUDE OF DISTURBANCE', 3: 'DURATION OF DISTURBANCE'}
	vertyrs = {1: "VERTEX YEAR 1", 2: "VERTEX YEAR 2", 3: "VERTEX YEAR 3", 4: "VERTEX YEAR 4", 5: "VERTEX YEAR 5", 
			   6: "VERTEX YEAR 6", 7: "VERTEX YEAR 7"}
	vertvals = {1: "VERTEX VALUE 1", 2: "VERTEX VALUE 2", 3: "VERTEX VALUE 3", 4: "VERTEX VALUE 4", 5: "VERTEX VALUE 5", 
				6: "VERTEX VALUE 6", 7: "VERTEX VALUE 7"}


ltlabelmap = {'greatest_fast_disturbance_mmu11_tight': Struct(**{'searchstrings': ['outputs/nbr/nbr_lt_labels/*[0-9]_greatest_fast_disturbance_mmu11_tight.bsq',
															   			'outputs/nbr/nbr_lt_labels_mr227/*[0-9]_greatest_fast_disturbance_mmu11_tight.bsq'],
											 		  			 'bands': ltbands.greatest_fast_disturbance,
											 		  			 'bands_robust': ltbands_robust.greatest_fast_disturbance,
											 		  			 'numpy_dtype': 'i2',
											 		  			 'nickname': 'GFD_MMU11_TIGHT'}),
			  'second_greatest_fast_disturbance_mmu11_tight': Struct(**{'searchstrings': ['outputs/nbr/nbr_lt_labels/*[0-9]_second_greatest_fast_disturbance_mmu11_tight.bsq',
															 		  		   'outputs/nbr/nbr_lt_labels_mr227/*[0-9]_second_greatest_fast_disturbance_mmu11_tight.bsq'],
											 				 			'bands': ltbands.greatest_fast_disturbance,
											 				 			'bands_robust': ltbands_robust.greatest_fast_disturbance,
											 				 			'numpy_dtype': 'i2',
											 				 			'nickname': '2ND_GFD_MMU11_TIGHT'}),
			  'greatest_fast_disturbance': Struct(**{'searchstrings': ['outputs/nbr/nbr_lt_labels/*[0-9]_greatest_fast_disturbance.bsq',
																	   'outputs/nbr/nbr_lt_labels_mr227/*[0-9]_greatest_fast_disturbance.bsq'],
										  			 'bands': ltbands.greatest_fast_disturbance,
										  			 'bands_robust': ltbands_robust.greatest_fast_disturbance,
										  			 'numpy_dtype': 'i2',
										  			 'nickname': 'GFD'}),
			  'second_greatest_fast_disturbance': Struct(**{'searchstrings': ['outputs/nbr/nbr_lt_labels/*[0-9]_second_greatest_fast_disturbance.bsq',
																   			  'outputs/nbr/nbr_lt_labels_mr227/*[0-9]_second_greatest_fast_disturbance.bsq'],
										  					'bands': ltbands.greatest_fast_disturbance,
										  					'bands_robust': ltbands_robust.greatest_fast_disturbance,
										  					'numpy_dtype': 'i2',
										  					'nickname': '2ND_GFD'}),
			  'greatest_disturbance_mmu11_tight': Struct(**{'searchstrings': ['outputs/nbr/nbr_lt_labels/*[0-9]_greatest_disturbance_mmu11_tight.bsq',
																	   		  'outputs/nbr/nbr_lt_labels_mr227/*[0-9]_greatest_disturbance_mmu11_tight.bsq'],
										  			 		'bands': ltbands.greatest_fast_disturbance,
										  			 		'bands_robust': ltbands_robust.greatest_fast_disturbance,
										  			 		'numpy_dtype': 'i2',
										  			 		'nickname': 'GD_MMU11_TIGHT'}),
			  'second_greatest_disturbance_mmu11_tight': Struct(**{'searchstrings': ['outputs/nbr/nbr_lt_labels/*[0-9]_second_greatest_disturbance_mmu11_tight.bsq',
																   			  		 'outputs/nbr/nbr_lt_labels_mr227/*[0-9]_second_greatest_disturbance_mmu11_tight.bsq'],
										  						   'bands': ltbands.greatest_fast_disturbance,
										  						   'bands_robust': ltbands_robust.greatest_fast_disturbance,
										  						   'numpy_dtype': 'i2',
										  						   'nickname': '2ND_GD_MMU11_TIGHT'}),
			  'greatest_disturbance': Struct(**{'searchstrings': ['outputs/nbr/nbr_lt_labels/*[0-9]_greatest_disturbance.bsq',
																  'outputs/nbr/nbr_lt_labels_mr227/*[0-9]_greatest_disturbance.bsq'],
										  		'bands': ltbands.greatest_fast_disturbance,
										  		'bands_robust': ltbands_robust.greatest_fast_disturbance,
										  		'numpy_dtype': 'i2',
										  		'nickname': 'GD'}),
			  'second_greatest_disturbance': Struct(**{'searchstrings': ['outputs/nbr/nbr_lt_labels/*[0-9]_second_greatest_disturbance.bsq',
																   		 'outputs/nbr/nbr_lt_labels_mr227/*[0-9]_second_greatest_disturbance.bsq'],
										  			   'bands': ltbands.greatest_fast_disturbance,
										  			   'bands_robust': ltbands_robust.greatest_fast_disturbance,
										  			   'numpy_dtype': 'i2',
										  			   'nickname': '2ND_GD'}),
			  'nbr_vertvals': Struct(**{'searchstrings': ['outputs/nbr/*[0-9]_vertvals.bsq'],
										  			   'bands': ltbands.vertvals,
										  			   'bands_robust': ltbands_robust.vertvals,
										  			   'numpy_dtype': 'i2',
										  			   'nickname': 'NBR_VERTVALS'}),
			  'nbr_vertyrs': Struct(**{'searchstrings': ['outputs/nbr/*[0-9]_vertyrs.bsq'],
										  			   'bands': ltbands.vertyrs,
										  			   'bands_robust': ltbands_robust.vertyrs,
										  			   'numpy_dtype': 'i2',
										  			   'nickname': 'NBR_VERTYRS'})}



