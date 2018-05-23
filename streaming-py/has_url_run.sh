#!/bin/bash 
HADOOP_ROOT="/home/work/hadoop-client/hadoop/"
HADOOP_BIN="$HADOOP_ROOT/bin/hadoop"
HADOOP_HENG="$HADOOP_BIN --config $HADOOP_ROOT/conf_heng"

#输入为：两批url数据，一批存储在一个固定的文件中，另一批存储在hdfs_path中，获取到两批数据的交集，并存储到hdfs_path中
#map规则：格式为int key\tvalue
#-partitioner com.baidu.sos.mapred.lib.IntHashPartitioner \
function get_hasurl()
{
    #input: 输入文件的hdfs_path
    local input1="input_path"
    local local_file="local_file"
 
    #out_data: 输出文件的hdfs_path
    local out_data="hdfs_url"
    local map_file="./only_url_map.py"
    local job_name="test_onlyfurl"

    $HADOOP_HENG fs -rmr $out_data
    $HADOOP_HENG streaming \
        -D mapred.job.queue.name="test" \
        -D mapred.job.priority="HIGH" \
        -D mapred.job.name=${job_name} \
        -D mapred.job.map.capacity=1000 \
        -D mapred.job.reduce.capacity=1000 \
        -D mapred.reduce.tasks=1 \
        #集群上python包:分发HDFS压缩文件、压缩文件内部具有目录结构
        -cacheArchive "//python2.7.tar.gz#python" \
        -input "$input1" \
        -output "$out_data" \
        -mapper "python/bin/python $map_file" \
        -reducer "cat" \
        -file $map_file \
        -file $local_file \
    if [ $? -ne 0 ]
    then
        exit 1
    fi
    #$HADOOP_HENG fs -touchz "${joined_data}/@manifest"
}
#-reducer "python/bin/python $red_file" \
get_hasurl

