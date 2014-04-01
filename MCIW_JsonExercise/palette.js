function palette() {
	var seeds = Array('00','CC','33','66','99','FF');
	var palette = [];
	for ( i=0; i<6; i++ ) {
		for ( j=0; j<6; j++ ) {
			for( k=0; k<6; k++ ) {
				palette.push( '#' + seeds[i] + seeds[j] + seeds[k] );
			}
		}
	}
	return palette
}  