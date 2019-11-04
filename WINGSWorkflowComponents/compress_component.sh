DIRECTORY=$1
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "bash compress_component.sh topoflow"
    exit 1
fi
ZIP_FILE=$DIRECTORY.zip
rm $DIRECTORY/*.zip
zip -r $ZIP_FILE $DIRECTORY
mv $ZIP_FILE $DIRECTORY
