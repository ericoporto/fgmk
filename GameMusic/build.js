var UglifyJS = require('uglify-js');
var fs = require('fs');

var result = UglifyJS.minify('concat.js', {
	mangle: true,
	compress: {
        sequences: true,
        properties: true,
        dead_code: true,
        drop_debugger: true,
        conditionals: true,
        comparisons: true,
        evaluate: true,
        booleans: true,
        loops: true,
        unused: true,
        hoist_funs: true,
        if_return: true,
        join_vars: true,
        cascade: true,
        warnings: true,
        negate_iife: true
	}
});

fs.writeFileSync('bgmusic.min.js', result.code)

fs.unlinkSync('concat.js')
