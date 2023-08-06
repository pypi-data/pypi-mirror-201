from lrmatrix.matrixmanager import MatrixManager











class ExplainableMatrix( MatrixManager ):

	
	def __init__( self, **kwargs ):


		super().__init__( goal = 'model', **kwargs )