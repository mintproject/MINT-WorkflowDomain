Docker image for PIHM with the basic configuration it has in its official page.

Pulling the image: 
`docker pull lucasaugustomcc/pihm`

Version: v2.2
Solver: Sundials v2.2.0

Test data set: http://www.pihm.psu.edu/PIHM_v2.2.tar

Command to run the image: 
`$ docker run -v /home/user/dataset_PIHM_v2.2:/dataset -w /dataset lucasaugustomcc/pihm pihm [project_name]`

Usage on a local machine
$ ./pihm, and have a file in the current directory named projectName.txt with the project name in it
OR
$ ./pihm project_name, and have a file in the current directory named project_name.txt with the project name in it