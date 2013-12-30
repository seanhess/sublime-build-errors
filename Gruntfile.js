module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            options: {},
            test: {
                src: ['test/*.txt'],
                dest: 'test/output/out.txt',
            },
        },

        watch: {
            test: {
                files: ['test/*.txt'],
                tasks: ["concat"],
            },

            compile: {
                files: ['test/*.ts'],
                tasks: ["exec:compile"],
            },
        },

        exec: {
            compile: { cmd: 'tsc test/test.ts -m commonjs'},
        }
    });

    // Load the plugin that provides the "uglify" task.
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-exec');

    // Default task(s).
    grunt.registerTask('default', ['watch']);

};