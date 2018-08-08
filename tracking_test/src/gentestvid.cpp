#include "opencv2/core.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <cmath>

#define _USE_MATH_DEFINES //This enables M_PI macro

typedef std::map<std::string, std::vector<double>> para_type ;

//Read configuration file
void read_config(std::ifstream& ifs, para_type& para)
{ 
  std::string line, key;
  double val;
  std::istringstream iss;
  std::remove_reference<decltype(para)>::type::iterator m_it;
  
  while(std::getline(ifs, line))
    {
      iss.str(line);      
      iss >> key;

      //Insert an empty entry indexed as key
      m_it = para.insert(std::make_pair(key, para_type::mapped_type())).first;
      
      while(iss >> val)
	m_it->second.push_back(val);

      iss.clear();
    }  
}

void show_config(para_type& para)
{
  for(const auto& ele : para)
    {
      std::cout << ele.first << "\t";
      for(const auto& val : ele.second)
	std::cout << val << "\t";
      std::cout << std::endl;
    }
}

double rand_val(double min, double max, double step)
{  
  int nsteps = int((max - min) / step);
  if(nsteps == 0)
    return 0;
  
  int level = std::rand() % nsteps;
  return (min + level * step);
}

void rand_trans(cv::Mat& m, double mmin, double mmax, double step)
{
  assert(m.size() == cv::Size(3, 2));

  double mag = rand_val(mmin, mmax, step);
  double rad = rand_val(0, 360, 1) / 180 * M_PI;

  m.at<double>(0, 2) += mag * std::cos(rad);
  m.at<double>(1, 2) += mag * std::sin(rad);
}

int main(int argc, char** argv)
{
  if(argc != 4)
    {
      std::cout << "Usage: " << argv[0] << " [config] [seed image] [target video]" << std::endl;
      std::cout << "video suffix .avi recommended" << std::endl;
      return 0;
    }

  //Open file
  std::ifstream ifs(argv[1]);
  if(!ifs.is_open())
    {
      std::cout << "Cannot open file" << argv[1] << std::endl;
      return 0;
    }

  //Read paramter
  para_type para;
  read_config(ifs, para);
    
  //Read image
  cv::Mat img_seed = cv::imread(argv[2]);
  if(img_seed.empty())
    {
      std::cout << "Cannot open " << argv[2] << std::endl;
      return 0;
    }

  //Initialize video writer utilities
  cv::VideoWriter writer;
  //Open video writer stream
  if(!writer.open(std::string(argv[3]), cv::VideoWriter::fourcc('M', 'J', 'P', 'G'),
		  para["FPS"][0], img_seed.size()))
    {
      std::cout << "Cannot open video stream!" << std::endl;
      return 0;
    }
  
  //Print seed picture name
  std::cout << "Seed picture: " << argv[2] << std::endl;
  //Print Object number, To keep up with tracker data file format
  std::cout << "#Object = 1" << std::endl;
  
  //Insert seed image as the first frame
  writer << img_seed;
  
  //Affine transformation matrix
  cv::Mat m_aff(2, 3, CV_32FC1, cv::Scalar::all(0));
  cv::Point2f origin_center(para["CENTER"][0], para["CENTER"][1]);
  cv::Point2f curr_center;
  double* l_ptr = NULL;
  cv::Mat frame;
  int nframes = int(para["NFRAME"][0]);
  for(int f_idx = 1; f_idx < nframes; ++f_idx)
    {
      //Generate randon rotaiton
      m_aff = cv::getRotationMatrix2D(origin_center, rand_val(para["ROT"][0], para["ROT"][1], para["ROT"][2]), 1);
      //Generate random translation
      rand_trans(m_aff, para["TRANS"][0], para["TRANS"][1], para["TRANS"][2]);
      //Apply rotation and translation
      cv::warpAffine(img_seed, frame, m_aff, img_seed.size());
      
     writer << frame;

     //Print position of center
     l_ptr = (double*)m_aff.ptr(0);
     curr_center.x = origin_center.x * l_ptr[0] + origin_center.y * l_ptr[1] + l_ptr[2];
     l_ptr = (double*)m_aff.ptr(1);
     curr_center.y = origin_center.x * l_ptr[0] + origin_center.y * l_ptr[1] + l_ptr[2];
     std::cout << curr_center << std::endl;
    }
  
  writer.release();
  
  return 0;
}
