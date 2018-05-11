Docker image for topoflow with the configuration it has in its official GitHub repository.

Pulling the image: 
`docker pull lucasaugustomcc/topoflow`

Examples are available on TopoFlow page: Download examples: https://github.com/peckhams/topoflow/tree/master/topoflow/examples
from the official Topoflow repository on GitHub: https://github.com/peckhams/topoflow

Command to run the image: 
`$ docker run -v <path_to_volume>:/out -w /out lucasaugustomcc/topoflow:latest python -m topoflow --cfg_director y=/out/Treynor_Iowa_30m`