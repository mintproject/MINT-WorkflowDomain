FROM mintproject/base-ubuntu18:latest

RUN wget "https://github.com/ARVE-Research/gwgen_f90/archive/d76772ba4ec1d1c63cc1d94d108b4893a985727f.zip" && unzip d76772ba4ec1d1c63cc1d94d108b4893a985727f.zip && cd gwgen_f90-d76772ba4ec1d1c63cc1d94d108b4893a985727f && make && mv weathergen /usr/local/bin/ && cd .. && rm -rf d76772ba4ec1d1c63cc1d94d108b4893a985727f.zip gwgen_f90-d76772ba4ec1d1c63cc1d94d108b4893a985727f
