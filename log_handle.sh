#! /bin/sh

HADOOP_DIR=xxx
HADOOP_BIN=$HADOOP_DIR/bin/hadoop
HADOOP_KHAN="$HADOOP_BIN --config $HADOOP_DIR/conf_xxx"

HDFS_EVA_INPUT_PATH=xxx/$date
HDFS_EVA_OUTPUT_PATH=xxx/${date}_${local_tn}

#check data: hdfs_path, 最多等待5天 
for (( count=0; count<240; ++count )); do
    date
    datasize=$( $HADOOP_KHAN fs -du $HDFS_EVA_OUTPUT_PATH | grep ${date} | awk 'BEGIN{ i=0; } { ++i; if(i==1) print $1; }' )
    [ $datasize -gt 1000 ] && echo "data(log) of ${date} check ok~" && break
    echo "data(log) of ${date} check failed! size: $datasize"
    sleep 30m 
done
[ $count -eq 240 ] && exit 2


handle_log
