To run the image, just do python ./delphi.py --instructions. I created an image in: https://hub.docker.com/r/dgarijo/delphi/  with further details.

docker run --volume "c:/Users/dgarijo/Desktop/sharedFolder":/out/ -it dgarijo/delphi:v1 --> interactive.


Creation of a model:
root@59c89406cc39:/src/delphils# ./delphi.py --create_model --indra_statements data/sample_indra_statements.pkl --adjective_data data/adjectiveData.tsv --output_cag_json /out/testDelphiDanielJSON --output_dressed_cag /out/testDelphiDanielCAG --output_variables_path /out/testDelphiDanielVar

Execution of a model:
root@59c89406cc39:/src/delphils# ./delphi.py --execute_model --input_dressed_cag /out/testDelphiDanielCAG --input_variables_path /out/testDelphiDanielVar --output_sequences /out/DelphiSequencesResult.csv