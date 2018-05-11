Project website: https://water.usgs.gov/ogw/modflow/mf2005.html

Test data: https://catalog.data.gov/dataset?q=modflow+2005

Usage with docker
$ docker run -v /home/user/dataset:/dataset -w /dataset lucasaugustomcc/modflow-2005 mf2005 [model_name]