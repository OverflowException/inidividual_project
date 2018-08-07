#include <opencv2/core/utility.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;
using namespace cv;

int main(int argc, char** argv)
{
  if(argc != 3)
    {
      cout << "Usage: " << argv[0] << " <in image> <out rois>" << endl;
      return 0;
    }

  //Read image
  Mat image = imread(argv[1]);
  if(image.empty())
    {
      cout << "Cannot read image " << argv[1] << endl;
      return 0;
    }

  //Open file
  ofstream ofs(argv[2]);
  if(!ofs.is_open())
    {
      cout << "Cannot open file "  << argv[2] << endl;
      return 0;
    }

  
  vector<Rect> rois;
  selectROIs("Select ROI", image, rois, true, true);

  for(const Rect& r : rois)
    ofs << r.tl().x << "\t" << r.tl().y << "\t"
	<< r.size().width << "\t" << r.size().height
	<< endl;

  ofs.close();
  return 0;  
}
