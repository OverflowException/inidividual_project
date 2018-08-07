/*----------------------------------------------
 * Usage:
 * example_tracking_multitracker <video_name> [algorithm]
 *
 * example:
 * example_tracking_multitracker Bolt/img/%04d.jpg
 * example_tracking_multitracker faceocc2.webm KCF
 *--------------------------------------------------*/

#include <opencv2/core/utility.hpp>
#include <opencv2/tracking.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstring>
#include <ctime>
#include <utility>
#include <algorithm>
#include <unistd.h>
#include <vector>

#include "samples_utility.hpp"

using namespace std;
using namespace cv;

bool parse_arg(int argc, char** argv, string& video_name, string& roi_filename, string& algo_name)
{
  int opt = 0;
  while((opt = getopt(argc, argv, "r:a:")) != -1)
    switch(opt)
      {
      case 'r':
	roi_filename = optarg;
	break;
      case 'a':
	algo_name = optarg;
	break;
      case '?':
	return false;
      }

  //No non-optional argument. Means no video_name
  if(optind == argc)
    return false;
  
  video_name = argv[optind];
  return true;
}

template<class _T>
void genCrosshair(const Rect_<_T>& rect,
		  Point_<_T>& ch_center,
		  pair<Point_<_T>, Point_<_T>>& ch_h,
		  pair<Point_<_T>, Point_<_T>>& ch_v)
{
  ch_center = Point_<_T>((rect.tl() + rect.br()) / 2);
  
  ch_v.first = Point2d(ch_center.x, ch_center.y - 0.7 * rect.height);
  ch_v.second = Point2d(ch_center.x, ch_center.y + 0.7 * rect.height);
  ch_h.first = Point2d(ch_center.x - 0.7 * rect.width, ch_center.y);
  ch_h.second = Point2d(ch_center.x + 0.7 * rect.width, ch_center.y);
}

bool readROI(string& roi_filename, vector<Rect>& rois)
{
  ifstream ifs(roi_filename);
  if(!ifs.is_open())
    return false;
  
  string line;
  istringstream iss;
  Rect roi_buf;
  while(std::getline(ifs, line))
    {
      iss.str(line);
      
      iss >> roi_buf.x;
      iss >> roi_buf.y;
      iss >> roi_buf.width;
      iss >> roi_buf.height;
      rois.push_back(roi_buf);
      
      iss.clear();
    }

  ifs.close();
  return true;
}


int main( int argc, char** argv )
{
  string video_name, roi_filename, algo_name;
  if(!parse_arg(argc, argv, video_name, roi_filename, algo_name))
    {
      cout << "Usage: " <<  argv[0] << " <video_name> -r [ROI file] -a [algorithm]" << endl;
      cout << "Available algorithms: TLD, BOOSTING, MEDIAN_FLOW, MIL, GOTURN" << endl;
      cout << "Default = MEDIAN_FLOW" << endl;
      return 0;
    }

  //Set default tracking algorithm name to MEDIAN_FLOW
  if(algo_name.empty())
    algo_name = "MEDIAN_FLOW";


  //Capture first frame
  VideoCapture cap(video_name);
  Mat frame;
  vector<Rect> rois;
  cap >> frame;
  
  //No ROI file given, start drawing session
  if(roi_filename.empty())
    selectROIs("tracker", frame, rois, true, true);
  //ROI file given, read from ROI file
  else if(!readROI(roi_filename, rois))
    {
      cout << "Cannot read ROI file " << roi_filename << endl;
      return 0;
    }

  //If no ROI provided
  if(rois.size() == 0)
    {
      cout << "No ROI provided!" << endl;
      return 0;
    }


  vector<Rect2d> objects(rois.size());
  std::copy(rois.begin(), rois.end(), objects.begin());
  
  std::vector<Ptr<Tracker>> tracker_ptrs;
  for(size_t i = 0; i < rois.size(); i++)
    tracker_ptrs.push_back(createTrackerByName(algo_name));
  
  MultiTracker trackers;
  trackers.add(tracker_ptrs, frame, objects);
  
  pair<Point2d, Point2d> crosshair_v; //Vertical crosshair line
  pair<Point2d, Point2d> crosshair_h; //Horizontal crosshair line
  Point2d crosshair_center;  //Position of crosshair center
  vector<vector<Point>> obj_tracks(objects.size()); //Tracks of objects
  Point pt_buf;
  
  // do the tracking
  cout << "Tracking algorithm: " << algo_name << endl;  
  std::cout << "#Object = " << objects.size() << std::endl;
  
  for ( ;; )
    {
      //get frame from the video
      cap >> frame;

      //stop the program if no more images
      if(frame.empty())
  	break;

      //update the tracking result
      trackers.update(frame, objects);

      
      //draw the tracked object
      for(const Rect2d& obj : objects)
  	{
  	  rectangle(frame, obj, Scalar(0, 255, 0), 2, 1);
  	  genCrosshair(obj,  crosshair_center, crosshair_h, crosshair_v);
  	  cout << crosshair_center << endl;
  	  line(frame, crosshair_v.first, crosshair_v.second, Scalar(0, 255, 0), 2, 1);
  	  line(frame, crosshair_h.first, crosshair_h.second, Scalar(0, 255, 0), 2, 1);
  	}

      //Add points to tracks
      for(size_t obj_idx = 0; obj_idx < obj_tracks.size(); ++obj_idx)
  	{
  	  pt_buf = Point((objects[obj_idx].tl() + objects[obj_idx].br()) / 2);
  	  //New track point for display
  	  if(find(obj_tracks[obj_idx].begin(), obj_tracks[obj_idx].end(), pt_buf)
  	     == obj_tracks[obj_idx].end())
  	    obj_tracks[obj_idx].push_back(pt_buf);
  	}

      //Draw tracks
      for(const auto& track : obj_tracks)
      	for(const auto& point : track)
      	  circle(frame, point, 1, Scalar(255, 255, 255));
      
      
      //show image with the tracked object
      imshow("tracker",frame);

      //quit on ESC button
      if(waitKey(1)==27)break;
    }

}
