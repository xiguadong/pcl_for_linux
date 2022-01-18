#include <iostream>
#include <sys/time.h>
//#include <filters/statistical_outlier_removal.h>
//#include <io/ply_io.h>
//#include <point_types.h>

#include <string>

#include "pcl/point_cloud.h"
#include "pcl/io/ply_io.h"
#include "pcl/io/ply/ply_parser.h"
#include "pcl/filters/statistical_outlier_removal.h"
#include "pcl/search/impl/search.hpp"



static double get_current_time(){
    struct timeval tv;
    gettimeofday(&tv, nullptr);
    return tv.tv_sec * 1000 + tv.tv_usec / 1000;
}


int main() {
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filter(new pcl::PointCloud<pcl::PointXYZ>);

  pcl::PLYReader reader;


  
  reader.read<pcl::PointXYZ>("../hand.ply", *cloud);


  pcl::StatisticalOutlierRemoval<pcl::PointXYZ> sor;

  sor.setInputCloud(cloud);

  sor.setMeanK(50);

  sor.setStddevMulThresh(1.0);

  double start = get_current_time();
//  for (int i = 0; i < 1; ++i) {
//    sor.filter(*cloud_filter);
//  }
  sor.filter(*cloud_filter);
  double end = get_current_time();

  std::cout << "cost" << end - start << "ms" << std::endl;

  std::cout << "width:" << cloud.get()->width << " height:" << cloud.get()->height << std::endl;

  std::cout << "Hello, World!" << std::endl;
  return 0;
}
