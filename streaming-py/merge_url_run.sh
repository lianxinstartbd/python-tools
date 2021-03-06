#!/bin/bash 
HADOOP_ROOT="/home/work/hadoop-client/hadoop/"
HADOOP_BIN="$HADOOP_ROOT/bin/hadoop"
HADOOP_HENG="$HADOOP_BIN --config $HADOOP_ROOT/conf_heng"

#输入为：两组url数据A和B，存储在不同的hdfs_path中，取在B中但不在A中的url，并存储到hdfs_path中
#map规则：格式为int key\tvalue
#-partitioner com.baidu.sos.mapred.lib.IntHashPartitioner \
function get_mergeurl()
{
    #input: 输入文件的hdfs_path
    local input1="test1"
    local input2="test2"
    
    #out_data: 输出文件的hdfs_path
    local out_data="hdfs_url"
    local map_file="./merge_url_map.py"
    local red_file="./merge_Url_red.py"
    local job_name="test_mergefurl"
    $HADOOP_HENG fs -rmr $out_data
    $HADOOP_HENG streaming \
        -D mapred.job.queue.name="test" \
        -D mapred.job.priority="HIGH" \
        -D mapred.job.name=${job_name} \
        -D mapred.job.map.capacity=1000 \
        -D mapred.job.reduce.capacity=1000 \
        -D mapred.reduce.tasks=5000 \
        #集群上python包:分发HDFS压缩文件、压缩文件内部具有目录结构
        -cacheArchive "//python2.7.tar.gz#python" \
        -input "$input1" \
        -input "$input2" \
        -output "$out_data" \
        -mapper "python/bin/python $map_file" \
        -reducer "python/bin/python $red_file" \
        -file $map_file \
        -file $red_file \
    if [ $? -ne 0 ]
    then
        exit 1
    fi
    #$HADOOP_HENG fs -touchz "${joined_data}/@manifest"
}
#-reducer "python/bin/python $red_file" \
get_mergeurl

