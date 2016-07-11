/*
 *	Loop through directory and convert PMC XML file into multiple PDFs
 *
 */


//////////// ABORT. THIS IS A TERRIBLE IDEA.

#include <stdio.h>
#include <dirent.h>

int main() {
	DIR           *d;
	struct dirent *dir;
	d = opendir("/Users/zzalsrd5/code/*");
    
	printf("Starting...\n");
	
	// Loop through directory	
	if(d) {
		while((dir = readdir(d)) != NULL) {
			printf("%s\n", dir->d_name);
		}
	
		closedir(d);
	}
	
	// Ignore if not gz

	// Unzip file

	// Read xml

	// Split into articles

	// Save each article as PDF

	return 0;
}
