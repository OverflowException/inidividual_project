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


typedef std::map<std::string, std::vector<double>> para_type;

const double TWO_PI = 2 * M_PI;

//Read configuration file
bool read_config(std::ifstream& ifs, para_type& para)
{ 
  std::string line, key;
  double val;
  std::istringstream iss;
  std::remove_reference<decltype(para)>::type::iterator m_it;
  
  while(std::getline(ifs, line))
    {
      //Ignore comments
      if(line[0] == '#')
	continue;

      iss.clear();
      iss.str(line);      
      iss >> key;

      //Ignore empty lines
      if(key.empty())
	continue;
	
      //Insert an empty entry indexed as key
      m_it = para.insert(std::make_pair(key, para_type::mapped_type())).first;
      
      while(iss >> val)
	m_it->second.push_back(val);
    }

  if(para["AMP_X"].size() != para["AMP_Y"].size() ||
     para["AMP_X"].size() != para["FREQ_X"].size() ||
     para["AMP_X"].size() != para["FREQ_Y"].size())
    return false;
  else
    return true;
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

//3 decimal digits at most
double gcd(double a, double b)
{
  if(a < b)
    return gcd(b, a);

  if(b < 0.001)
    return a;
  else
    return gcd(b, a - std::floor(a / b) * b);
}

void gen_trans(cv::Mat& m,
	       const std::vector<double>& amp_x, const std::vector<double>& amp_y,
	       const std::vector<double>& freq_x, const std::vector<double>& freq_y,
	       double t)
{
  size_t comp_num = amp_x.size();
  for(size_t idx = 0; idx < comp_num; ++idx)
    {
      m.at<double>(0, 2) += amp_x[idx] * sin(TWO_PI * freq_x[idx] * t);
      m.at<double>(1, 2) += amp_y[idx] * sin(TWO_PI * freq_y[idx] * t);
    }
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
  if(!read_config(ifs, para))
    {
      std::cout << "Sine components' parameters in " << argv[1] << " incomplete!" << std::endl;
      return 0;
    }

  //Unpack paramters, avoid accessing map every time
  size_t nframe = size_t(para["NFRAME"][0]);
  size_t fps = size_t(para["FPS"][0]);
  double rot = para["ROT"][0];
  std::vector<double>& amp_x = para["AMP_X"];
  std::vector<double>& amp_y = para["AMP_Y"];
  std::vector<double>& freq_x = para["FREQ_X"];
  std::vector<double>& freq_y = para["FREQ_Y"];
  cv::Point2f origin_center(para["CENTER"][0], para["CENTER"][1]);
  //Find gcd frequency of every x, y frequency component as frequency of overall 2d movement, Hz
  double mov_freq = 0;
  for(double freq : freq_x)
    mov_freq = gcd(mov_freq, freq);
  for(double freq : freq_y)
    mov_freq = gcd(mov_freq, freq);
  std::cout << "Movement frequency = " << mov_freq << std::endl;
  //Time step for adjacent frames
  double t_step = 1 / double(fps);
  
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
  		  fps, img_seed.size()))
    {
      std::cout << "Cannot open video stream!" << std::endl;
      return 0;
    }
    
  //Affine transformation matrix
  cv::Mat m_aff(2, 3, CV_32FC1, cv::Scalar::all(0));
  cv::Point2f curr_center;
  double* l_ptr = NULL;
  cv::Mat frame;
  
  //Print seed picture name
  std::cout << "Seed picture: " << argv[2] << std::endl;
  //Print Object number, To keep up with tracker data file format
  std::cout << "#Object = 1" << std::endl;

  double t = 0;
  size_t f_idx = 0;
  for(f_idx = 0; f_idx < nframe; ++f_idx, t += t_step)
    {
      //Generate rotation
      m_aff = cv::getRotationMatrix2D(origin_center,
				      rot * sin(TWO_PI * mov_freq * t), 1);
      //Generate translation
      gen_trans(m_aff, amp_x, amp_y, freq_x, freq_y, t);
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
